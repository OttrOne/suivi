import time
from drivers import DockerDriver, InvalidDriverError
from monitoring import Monitoring
from threading import Thread

if __name__ == '__main__':
    try:
        eas = DockerDriver()
        eas.create()
        eas.logs()
        #print(eas.stats())
        eee = Monitoring(eas)
        uuu = Monitoring(eas)
        eee.start()
        uuu.start()
        for i in range(10):
            #print(eas.stats().cpupercent)
            time.sleep(1.4)
        eee.stop()
        uuu.stop()
        print(eee.export().export())
        print(uuu.export().export())
        del eas
    except InvalidDriverError as err:
        print(err)
