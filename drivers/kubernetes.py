from os import stat

from .driver import Driver
from .exceptions import InvalidDriver, NotRunning, ImageNotFound
from kubernetes import client, config
from utils import id_generator
from models import Sample, SampleSet
from typing import Union
from time import sleep
from re import search
from kubernetes.client.exceptions import ApiException
from math import pow
from strictyaml import as_document

# NOTES
# Ephermal Containers need a feature gate because alpha

def kubernetes_desuffix(value: str):
    suffixes = {
        "Ki": pow(2, 10),
        "Mi": pow(2, 20),
        "Gi": pow(2, 30),
        "Ti": pow(2, 40),
        "Pi": pow(2, 50),
        "Ei": pow(2, 60),

        "n": pow(10, -9),
        "u": pow(10, -6),
        "m": pow(10, -3),
        "k": pow(10, 3),
        "M": pow(10, 6),
        "G": pow(10, 9),
        "T": pow(10, 12),
        "P": pow(10, 15),
        "E": pow(10, 18),
    }
    match = search(r'(\d+)(\D+)', value)

    if match:
        pre = int(match.group(1))
        factor = suffixes.get(match.group(2))

    else: # value has no suffix
        pre = int(value)
        factor = 1

    return pre * factor

class KubernetesDriver:

    def __init__(self, raise_errors=True):

        self.raise_errors = raise_errors
        self._container = None
        config.load_kube_config()
        self._client = client.CoreV1Api()
        self.namespace = 'default'
        self.hostname = None

    def create(self, image: str, command: Union[None, str]):
        id = id_generator()

        # create subject pod
        self.meta = client.V1ObjectMeta(name=f"suivi-{id}", namespace=self.namespace, labels={"suivi" : "target"})
        container = client.V1Container(name=f"suivi-{id}", image=image)
        pod_spec = client.V1PodSpec(containers=[container])
        pod_body = client.V1Pod(metadata=self.meta, spec=pod_spec, kind='Pod', api_version='v1')

        self._pod = self._client.create_namespaced_pod(namespace=self.namespace, body=pod_body)

        # create service
        service_meta = client.V1ObjectMeta(name=f"suivi-{id}-gateway", namespace=self.namespace)
        service_port = client.V1ServicePort(protocol='TCP', target_port=80, port=80)
        service_spec = client.V1ServiceSpec(ports=[service_port], selector={"suivi" : "target"})
        service_body = client.V1Service(metadata=service_meta, spec=service_spec)

        self._service = self._client.create_namespaced_service(namespace=self.namespace, body=service_body)

        self.hostname = f"suivi-{id}-gateway"
        # wait for readyness
        tries = 30
        for i in range(tries):
            res = self._client.read_namespaced_pod_status(self.meta.name, self.meta.namespace)
            if res.status.phase == 'Running':
                return True
            sleep(1)

    def wait(self, name):

        while True:
            res = self._client.read_namespaced_pod_status(name, self.meta.namespace)
            if res.status.phase == 'Succeeded' or res.status.phase == 'Failed':

                self._client.delete_namespaced_pod(name, self.meta.namespace)
                return True
            sleep(1)

    def logs(self):

        logs = self._client.read_namespaced_pod_log(self.meta.name, self.meta.namespace)
        print(logs)

    def stats(self) -> Union[Sample, None]:
        api = client.CustomObjectsApi()
        try:
            resource = api.get_namespaced_custom_object(group='metrics.k8s.io', version='v1beta1', namespace=self.meta.namespace, plural='pods', name=self.meta.name)

        except ApiException as err:
            if err.status != 404:
                print(err)
            return None

        for con in resource['containers']:
            if con['name'] == self.meta.name:
                cpu = con['usage']['cpu']
                mem = con['usage']['memory']
                return Sample(kubernetes_desuffix(cpu), kubernetes_desuffix(mem))

        return None

    def join(self, image: str, command: Union[None, str]):

        name = f"{self.meta.name}-companion-{id_generator()}"
        # create subject pod
        meta = client.V1ObjectMeta(name=name, namespace=self.namespace, labels={"suivi" : "companion"})
        container = client.V1Container(name=name, image=image, args=command.split(' '))
        pod_spec = client.V1PodSpec(containers=[container], restart_policy='Never')
        pod_body = client.V1Pod(metadata=meta, spec=pod_spec, kind='Pod', api_version='v1')

        self._companion = self._client.create_namespaced_pod(namespace=self.namespace, body=pod_body)
        self.companion = name
        return name

    def forecast(self, samples: SampleSet) -> str:

        samples = samples.export()
        cpu = samples['cpu']['80%'] if samples['cpu']['80%'] > 0.005 else 0.005
        mem = samples['memory']['80%']

        fc = {
            'resources' : {
                'requests' : {
                    'cpu' : f"{cpu}",
                    'memory' : f"{mem}",
                },
                'limits' : {
                    'cpu' : f"{cpu}",
                    'memory' : f"{mem}",
                }
            }
        }

        return as_document(fc).as_yaml()

    def stop(self):
        self._client.delete_namespaced_pod(self.meta.name, self.meta.namespace)
        self._client.delete_namespaced_service(f"{self.meta.name}-gateway", self.meta.namespace)
        pass

    def cleanup(self):
        pass
