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
