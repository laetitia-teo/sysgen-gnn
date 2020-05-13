"""
Defines the grammar as well as functions operating on them.
"""
import re
import numpy as np

from functools import reduce

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
# TODO: maybe more efficient computation of empirical distribs

RULESETIDX = 0
RULESETDICT = {} # indexed by RuleSet name, contains RuleSet objects

def link(s):
    # links rule symbols with their actual adress
    if re.search(r"^<\w+>$", s):
        return RULESETDICT[s]
    return s

class RuleSet():
    """
    A class reprenting a set of production rules, originating from the same
    symbol.
    """
    def __init__(self, prod_string):
        research = re.search(
            r"^(<\w+>) *->(.+)$",
            prod_string)
        if not research:
            raise ValueError('Ill-formed rule expression')
        self.name = research[1]
        self.rulelist = re.findall(r"[<?\w+>? +]*<?\w+>?", research[2])
        self.N = len(self.rulelist)

        # to get unique ids for rule applications,
        # only if rule not already registered
        if self.name not in RULESETDICT:
            self.rulesetidx = RULESETIDX
            globals()['RULESETIDX'] = self.rulesetidx + self.N
            globals()['RULESETDICT'][self.name] = self
        else:
            raise Warning("Rule already registered")
            self.rulesetidx = RULESETDICT[self.name].rulesetidx

    def __repr__(self):
        return "RuleSet " + self.name

def prod(r):
    """
    Generate sentence starting from rule r.
    Also returns list of rule application indices, in a left-first traversal 
    of rule application DAG.
    """
    if isinstance(r, str):
        return r, []
    if isinstance(r, RuleSet):
        idx = np.random.choice(r.N)
        rule = r.rulelist[idx]
        words = rule.split()
        words = [link(word) for word in words]
        rl, ll = zip(*[prod(word) for word in words])
        l2 = []
        for e in ll:
            l2 += e
        return " ".join(rl), [idx + r.rulesetidx] + l2

def prodl(r, l):
    """
    Generate a sentence from the list of rule applications.
    Consumes l, be sure to pass a copy to keep l.
    """
    if isinstance(r, str):
        return r, l
    if isinstance(r, RuleSet) and l:
        idx = l[0]
        l = l[1:]
        if idx not in range(r.rulesetidx, r.rulesetidx + r.N):
            raise KeyError("Rule index {} not valid for RuleSet {}".format(
                idx, r.name))
        rule = r.rulelist[idx - r.rulesetidx]
        words = rule.split()
        words = [link(word) for word in words]
        rlist = []
        for word in words:
            r2, l = prodl(word, l)
            rlist.append(r2)
        return " ".join(rlist), l
    if isinstance(r, RuleSet) and not l:
        raise ValueError(
            f"Empty list was given for non-terminal rule {r.name}")

### Atom divergence of datasets

# datasets are lists of lists
def AD(V, W):
    """
    Compute the Atom Divergence of datasets V and W.
    Commutative.
    """
    # concatenate V and W into a flat lists.
    cat = lambda a, b: a + b
    V = reduce(cat, V)
    W = reduce(cat, W)

    # empirical distributions
    Dv = {}
    Dw = {}
    for v in V:
        try:
            Dv[v] += 1
        except KeyError:
            Dv[v] = 1
    for w in W:
        try:
            Dw[w] += 1
        except KeyError:
            Dw[w] = 1
    Pv = []
    Pw = []
    for i in range(RULESETIDX):
        try:
            Pv.append(Dv[i])
        except KeyError:
            Pv.append(0)
        try:
            Pw.append(Dw[i])
        except KeyError:
            Pw.append(0)
    Pv = np.array(Pv) / sum(Pv)
    Pw = np.array(Pw) / sum(Pw)

    return 1 - np.sum(Pv**0.5 * Pw**0.5)

### Testing

# register rules
rules = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12]
rules = list([RuleSet(r) for r in rules])
S = rules[-1]

# create 2 datasets of size n and m
n = 2
m = 3
V = [prod(S)[1] for _ in range(n)]
W = [prod(S)[1] for _ in range(m)]

ad = AD(V, W)