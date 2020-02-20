import functools
from operator import mul, add, truediv, sub

class ButtonFunction:
    def __init__(self, func_generator):
        self.func_generator = func_generator

    def __call__(self, *args):
        func = self.func_generator(*args)
        def wrapped(x):
            try:
                x = int(x) if isinstance(x, float) and x.is_integer() else x
                return func(x)
            except:
                pass # E.g. if we perform "<<" on 1.2, it won't work
        return wrapped

    def __get__(self, instance, instancetype):
        """Implement the descriptor protocol to make decorating instance method possible."""
        # Return a partial function with the first argument is the instance of the class decorated.
        return functools.partial(self.__call__, instance)

class Button:
    d = {'<<': lambda x: x // 10 }
    ops = {'+': add, '-': sub, '/': truediv, '*': mul}
    def __init__(self, name):
        self.name = name
        self.func = self._parse(name)

    @ButtonFunction
    def _parse(self, name):
        if name in self.d:
            return self.d[name]
        elif name[0] in self.ops:
            return lambda x: self.ops[name[0]](x, int(name[1:]))
        elif '=>' in name:
            return lambda x: int(str(x).replace(*name.split('=>')))
        else:
            return lambda x: int(str(x) + name)

