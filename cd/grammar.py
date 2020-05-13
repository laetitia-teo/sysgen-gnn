"""
Defines the grammar as well as functions operating on them.
"""
import re
import numpy as np


r1 = "<Art> -> the | a"
r2 = "<Col> -> E | red | green | blue | purple | yellow | grey"
r3 = "<Loc> -> E | on your left | on your right | in front of you | behind you"
r4 = "<DDoor> -> <Art> <Col> door <Loc>"
r5 = "<DBall> -> <Art> <Col> ball <Loc>"
r6 = "<DBox> -> <Art> <Col> box <Loc>"
r7 = "<DKey> -> <Art> <Col> key <Loc>"
r8 = "<D> -> <DDoor> | <DBall> | <DBox> | <DKey>"
r9 = "<DNDoor> -> <DBall> | <DBox> | <DKey>"
r10 = "<Cl> -> go to <D> | pick up <DNDoor> | open <DDoor> |"\
           + " put <DNDoor> next to <D>"
r11 = "<S1> -> <Cl> | <Cl> and <Cl>"
r12 = "<S> -> <S1> | <S1> then <S1> | <S1> after you <S1>"
# TODO: handle punctuation

# for testing purposes
rules = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12]

def setn(n, N):
    if n == -1:
        n = np.random.randint(N)
    return n

def art(n=-1, plist=[]):
    n = setn(n, 2)
    if n == 0:
        return "the"
    if n ==1:
        return "a"

def col(n=-1, plist=[]):
    n = setn(n, 7)
    if n == 0:
        return "E"
    if n == 1:
        return "red"
    if n == 2:
        return "green"
    if n == 3:
        return "blue"
    if n == 4:
        return "purple"
    if n == 5:
        return "yellow"
    if n == 6:
        return "gray"

def loc(n=-1, plist=[]):
    n = setn(n, 5)
    if n == 0:
        return "E"
    if n == 1:
        return "on your left"
    if n == 2:
        return "on your right"
    if n == 3:
        return "in front of you"
    if n == 4:
        return "behind you"

def ddoor(n=-1, plist=[]):
    n = setn(n, 1)
    if n == 0:
        return art() + " " + col() + " door " + loc()

def dball(n=-1, plist=[]):
    n = setn(n, 1)
    if n == 0:
        return art() + " " + col() + " ball " + loc()

def dbox(n=-1, plist=[]):
    n = setn(n, 1)
    if n == 0:
        return art() + " " + col() + " box " + loc()

def dkey(n=-1, plist=[]):
    n = setn(n, 1)
    if n == 0:
        return art() + " " + col() + " key " + loc()

def dndoor(n=-1, plist=[]):
    n = setn(n, 3)
    if n == 0:
        return dball()
    if n == 1:
        return dbox()
    if n == 2:
        return dkey()

def d(n=-1, plist=[]):
    n = setn(n, 4)
    if n == 0:
        return ddoor()
    if n == 1:
        return dball()
    if n == 2:
        return dbox()
    if n == 3:
        return dkey()

def cl(n=-1, plist=[]):
    n = setn(n, 4)
    if n == 0:
        return "go to " + d()
    if n == 1:
        return "pick up " + d()
    if n == 2:
        return "open " + ddoor()
    if n == 3:
        return "put " + dndoor() + " next to " + d()

def s1(n=-1, plist=[]):
    n = setn(n, 2)
    if n == 0:
        return cl()
    if n == 1:
        return cl() + " and " + cl()

def s(n=-1, plist=[]):
    n = setn(n, 3)
    if n == 0:
        return s1()
    if n == 1:
        return s1() + ", then " + s1()
    if n == 2:
        return s1() + " after you " + s1() 

class Rule():
    def __init__(self, prod_string):
        research = re.search(
            r"^(<\w+>) *->(.+)$",
            prod_string)
        if not research:
            raise ValueError('Ill-formed rule expression')
        self.name = research[1]
        self.prodlist = re.findall(r"[<?\w+>? +]*<?\w+>?", research[2])
        self.N = len(self.prodlist)

        self.register_name()

    def register_name(self):
        globals()[self.name] = self.prod

    def get_prod(self):
        # converts the rules in executable form
        def f(s):
            if re.search(r"^<\w+>$", s):
                return "globals()['" + s + "']()"
            return "'" + s + "'"
        rule = np.random.choice(self.prodlist)
        words = rule.split()
        words = list(map(f, words))
        return "+ ' ' + ".join(words)

    def prod(self):
        return eval(self.get_prod())

    def __repr__(self):
        return "Rule " + self.name

### Testing 

rules = list(map(lambda x: Rule(x), rules))
