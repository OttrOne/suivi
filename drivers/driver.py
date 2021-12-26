class DriverMeta(type):

    def __instancecheck__(cls, __instance) -> bool:
        return cls.__subclasscheck__(type(__instance))

    def __subclasscheck__(cls, __subclass: type) -> bool:
        return (hasattr(__subclass, 'create') and
                callable(__subclass.create))

class Driver(metaclass=DriverMeta):
    pass
