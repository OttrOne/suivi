import time
from drivers import DockerDriver, InvalidDriver, DriverNotFound, ImageNotFound
from drivers.driver import Driver
from monitoring import Monitoring
from threading import Thread
import argparse

def get_driver(name: str) -> Driver:

    drivers = {
        "docker": DockerDriver,
    }
    driver = drivers.get(name)

    if driver is None:
        raise DriverNotFound()

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

    parser.add_argument('-s',
                       '--silent',
                       action='store_true',
                       help='suppress status i/o and only print results')

    args = parser.parse_args()

    try:
        eas = get_driver(args.driver)()
        eas.create(args.image, args.command)

        print(eas.stats())
        eee = Monitoring(eas)
        eee.start()
        for i in range(10):
            #print(eas.stats().cpupercent)
            time.sleep(1.4)
        eee.stop()
        print(eee.export().export())
    except (DriverNotFound, InvalidDriver, ImageNotFound) as err:
        print(err)
