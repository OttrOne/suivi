class DriverMeta(type):

    def __instancecheck__(cls, __instance) -> bool:
        return cls.__subclasscheck__(type(__instance))

    def __subclasscheck__(cls, __subclass: type) -> bool:
        return (
                hasattr(__subclass, 'create') and callable(__subclass.create)
            ) and (
                hasattr(__subclass, 'logs') and callable(__subclass.logs)
            ) and (
                hasattr(__subclass, 'stats') and callable(__subclass.stats)
            ) and (
                hasattr(__subclass, 'stop') and callable(__subclass.stop)
            ) and (
                hasattr(__subclass, 'cleanup') and callable(__subclass.cleanup)
            ) and (
                hasattr(__subclass, 'wait') and callable(__subclass.wait)
            )

class Driver(metaclass=DriverMeta):
    pass
