import typing
from collections.abc import Callable

def overload_by_arg_count():
    registry = {}

    def decorator(func: Callable):
        hints = typing.get_type_hints(func)
        print(hints)
        
        def wrapper(*args, **kwargs):
            key = len(args) - 1  # -1, потому что args включает self
            if key in registry:
                return registry[key](*args, **kwargs)
            raise TypeError(f"No method with {key} arguments")

        def register(count):
            def inner(f):
                registry[count] = f
                return wrapper
            return inner

        wrapper.register = register
        return wrapper
    return decorator

if __name__ == "__main__":
    
    @overload_by_arg_count()
    def test(x:int):
        pass
    
    @test.register(1)
    def test(x:int,y:int):
        pass
    
    @test.register(2)
    def test(x:int,y:int,z:int):
        pass
    
    test()
    test(1)
    test(1,3)