from drivers import DockerDriver, KubernetesDriver, InvalidDriver, DriverNotFound, ImageNotFound
from drivers.driver import Driver
from monitoring import Monitoring
from threading import Thread
from strictyaml import load
from path import Path
from utils import handle_variables
import argparse

from penetration import Penetration

def get_driver(name: str) -> Driver:

    drivers = {
        "docker": DockerDriver,
        "kubernetes": KubernetesDriver,
    }
    driver = drivers.get(name)

    if driver is None:
        raise DriverNotFound()

    # check driver integrity
    if not issubclass(driver, Driver):
        raise InvalidDriver(f"{driver.__name__} is not a valid suivi driver.")

    return driver

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.',
                                    epilog='MIT 2022 Dustin Kroeger')
    parser.add_argument('image', type=str, help='the image to run')

    parser.add_argument('--driver', action='store',
                        dest='driver', default="docker",
                        help='selected driver (default: docker)')

    parser.add_argument('-c',
                       dest='command',
                       action='store',
                       metavar='COMMAND',
                       type=str,
                       default='',
                       help='the command to run in the container')

    parser.add_argument('-n',
                       dest='pcycles',
                       action='store',
                       metavar='CYCLES',
                       type=int,
                       default=1,
                       help='the amount of pen cycles')

    parser.add_argument('-s',
                       '--silent',
                       action='store_true',
                       help='suppress status i/o and only print results')

    parser.add_argument('-f',
                       dest='config',
                       action='store',
                       metavar='FILE',
                       help='configuration file')

    parser.add_argument('-o',
                       dest='output',
                       action='store',
                       metavar='FILE',
                       help='monitoring output file')

    args = parser.parse_args()
    config = None

    try:
        if args.config:
            config = load(handle_variables(Path(args.config).text())).data
            print(config)

        client = get_driver(args.driver)()
        client.create(args.image, args.command)
        print(args.config)
        print(client.stats())
        mon = Monitoring(client)

        pen = Penetration(client, config['penetration'] if config and 'penetration' in config else None)

        mon.start()
        for i in range(args.pcycles):
            pen.penetrate()
        mon.stop()

        if args.output:
            Path(args.output).write_text(mon.export().json(), encoding='UTF-8')

        print(client.stats())
        print(mon.export())
        print(client.forecast(mon.export()))
        del client
    except (DriverNotFound, InvalidDriver, ImageNotFound) as err:
        print(err)
    except FileNotFoundError:
        print(f"The configuration file '{args.config}' could not be found.")
