import functools, warnings
from operator import mul, add, truediv, sub
import math

class ButtonFunction:
    def __init__(self, func_generator):
        self.func_generator = func_generator

    def __call__(self, *args):
        func = self.func_generator(*args)
        def wrapped(x):
            x = int(x) if isinstance(x, float) and x.is_integer() else x
            try:
                # we don't allow float to be generated
                res = func(x)
                assert isinstance(res, int) or (isinstance(res, float) and res.is_integer()), 'float result is not allowed'
                assert x < 100000000, 'result is too large'
                return int(res)
            except Exception as e:
                warnings.warn(str(e))
                warnings.warn('Function: {} cannot be applied on value: {}'.format(args[-1], x))
                return x # use identical function if the function raise exception
        return wrapped

    def __get__(self, instance, instancetype):
        """Implement the descriptor protocol to make decorating instance method possible."""
        # Return a partial function with the first argument is the instance of the class decorated.
        return functools.partial(self.__call__, instance)

class Button:
    ops = {'+': add, '-': sub, '/': truediv, '*': mul}
    d = {
        '<<': lambda x: int(str(x)[:-1]),
        'x^2': lambda x: x**2,
        'x^3': lambda x: x**3,
        '+/-': lambda x: -x,
        'reverse': lambda x: math.copysign(1, x) * int(str(abs(x))[::-1]),
        'sum': lambda x: math.copysign(1, x) * sum(map(int, str(abs(x)))),
        'shift<': lambda x: int(str(x)[1:] + str(x)[0]),
        'shift>': lambda x: int(str(x)[-1] + str(x)[:-1]),
        'mirror': lambda x: int(str(x) + str(x)[::-1]),
        'inv10': lambda x: int(''.join(map(lambda x:str(10-int(x))[-1], str(x)))), # inv10(105) = 905
    }
    def __init__(self, name):
        '''type: 'static' | 'digit' | 'operator' | 'transform' | 'button_modifier' | 'store' '''
        # only digit and operator buttons are specific
        # all other type of buttons are singleton
        self.name = name
        self.type = self._get_type(name)

    @property
    def func(self):
        return self._get_func()

    def add(self, button):
        v = int(self.name[3:])
        if button.type == 'digit':
            return Button(str(int(button.name) + v))
        elif button.type == 'operator':
            return Button(button.name[0] + str(int(button.name[1:]) + v))
        return button

    def store(self, value):
        assert self.type == 'store'
        self.name += str(value)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name

    def _get_type(self, name):
        if name in self.d:             return 'static'
        elif name[0] in self.ops:      return 'operator'
        elif '=>' in name:             return 'transform'
        elif name.startswith('[+]'):   return 'button_modifier'
        elif name.startswith('store'): return 'store'
        else:                          return 'digit'

    @ButtonFunction
    def _get_func(self):
        if self.type == 'static':    return self.d[self.name]
        if self.type == 'digit':     return lambda x: int(str(x) + self.name)
        if self.type == 'transform':  return lambda x: int(str(x).replace(*self.name.split('=>')))
        if self.type == 'operator':  return lambda x: self.ops[self.name[0]](x, int(self.name[1:]))
        if self.type == 'store':     return lambda x: int(str(x) + self.name[5:])





