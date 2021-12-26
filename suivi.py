
from drivers import DockerDriver, InvalidDriverError

if __name__ == '__main__':
    try:
        eas = DockerDriver()
        eas.create()
        eas.logs()
        print(eas.stats())
        del eas
    except InvalidDriverError as err:
        print(err)
