import argparse, warnings
from button import Button
try:
    from gooey import Gooey
except:
    Gooey = lambda x:x # dummy Gooey wrapper

class CalculatorGameState:
    def __init__(self, register, moves, target, button_names, solution=None, portals=None):
        assert all(isinstance(b, str) for b in button_names), 'You should create game state with button name'
        self.register = register
        self.moves = moves
        self.target = target
        self.buttons = [Button(b) for b in button_names]
        self.solution = solution or []
        self.portals = portals

    def __hash__(self):
        matters = map(str, (self.register, self.target, self.buttons))
        return hash(' '.join(matters))

    def send_through_portal(self, num):
        if not self.portals: return num
        inp, outp = self.portals
        s = str(num)
        if not num or len(s) < inp:
            return num
        extracted = s[-inp]
        be_extracted = s[:len(s)-inp] + s[len(s)-inp+1:]
        to_be_added, remain = be_extracted[:len(be_extracted)-outp+1], be_extracted[len(be_extracted)-outp+1:]
        to_be_added = str(int(to_be_added) + int(extracted))
        num = int(to_be_added + remain)
        return self.send_through_portal(num)

    def get_successors(self):
        if self.moves <= 0: return
        for b in self.buttons:
            if b.type == 'store': # additional operation provided by 'store'
                button_names = [str(b) if b.type != 'store' else 'store{}'.format(self.register) for b in self.buttons]
                yield CalculatorGameState(self.register, self.moves-1,
                        self.target, button_names, self.solution + ['store'], self.portals)

            if b.type == 'button_modifier':
                button_names = [str(b.add(bu)) for bu in self.buttons]
            else:
                button_names = [*map(str, self.buttons)]
            reg = b.func(self.register)
            if self.portals:
                reg = self.send_through_portal(reg)
            yield CalculatorGameState(reg, self.moves-1,
                    self.target, button_names, self.solution + [str(b)], self.portals)

    def is_goal(self):
        return self.register == self.target

    def __str__(self):
        return 'Register: {}, Moves: {}, Target: {}, Buttons: {}'.format(
                self.register, self.moves, self.target, ' '.join(map(str, self.buttons)))

    def __repr__(self):
        return str(self)

class Calculator_Solver:
    def __init__(self, *args, **kw):
        self.start = CalculatorGameState(*args, **kw)

    def solve(self): # DFS
        # state: (current register, actions left)
        dp = [self.start]
        steps = {hash(self.start):self.start.moves}
        while dp:
            state = dp.pop()
            for s in state.get_successors():
                if s.is_goal():
                    return s.solution
                if hash(s) in steps and steps[hash(s)] >= s.moves: continue
                steps[hash(s)] = s.moves
                dp.append(s)
        return ['Fail']

@Gooey
def get_args():
    parser = argparse.ArgumentParser(description='Crash Calculator: the Game')
    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('-m', '--moves', type=int, required=True,
            help='The moves allowed to use')
    requiredNamed.add_argument('-t', '--target', nargs="*", type=int, required=True,
            help='The target number(s)')
    requiredNamed.add_argument('-r', '--register', type=int, required=True,
            help='The original number in the register')
    requiredNamed.add_argument('-b', '--buttons', nargs="*", type=str, required=True,
            help="Buttons available, E.g. *2 | 1 | \"<<\" | \"6=>9\" | store | mirror | inv10 | [+]2")

    optional = parser.add_argument_group('Optional Arguments')
    optional.add_argument('-p', '--portals', nargs=2, type=int, default=None,
            help='The locations of portals counting from the right.')
    optional.add_argument('-d', '--debug', action='store_true',
            help='Show warnings from buttons')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    not args.debug and warnings.filterwarnings("ignore")
    for t in args.target:
        cs = Calculator_Solver(
                register=args.register,
                moves=args.moves,
                target=t,
                button_names=args.buttons,
                portals=args.portals)
        print('Solution for target {}: {}.'.format(t, ', '.join(cs.solve())))
