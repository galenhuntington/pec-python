#  Voting/PEC.hs


from math import floor
from fractions import Fraction
from itertools import zip_longest


class PECInput:
    def __init__(self, e, v):
        self.electors = e
        self.votes = v

    def __str__(self):
        return f"{self.electors} -> {':'.join(map(str, self.votes))}"


def apportion(el, vs):
    def loop(lt, sv):
        es = [x / sv for x in vs]
        f_es = [floor(x) for x in es]
        sfe = sum(f_es)
        if sfe == el:
            return f_es
        elif sfe < el:
            upf = max(e / (Fraction(f) + 1) for e, f in zip(es, f_es))
            return loop(f_es, sv * upf)
        else:
            return lt
    return loop([0] * len(vs), Fraction(sum(vs), el))


def addAtLarge(atl, vs, els):
    mv = max(vs)
    maxes = [i for i, x in enumerate(vs) if x == mv]
    es = atl // len(maxes)
    els1 = els[:]
    for i in maxes:
        els1[i] += es
    return els1


def vpeRange(vs, reps):
    l = list(zip(vs, reps))
    # not sure if 2nd value needs to be lazy, but might as well
    return (max(Fraction(n, d + 1) for n, d in l),
            lambda: min(Fraction(n, d) for n, d in l if d > 0))


def changes(votes, evs):
    ct = len(evs)
    for fr in range(ct):
        frv = votes[fr]
        fre = evs[fr]
        if fre > 0:
            for to in range(ct):
                if fr != to:
                    tov = votes[to]
                    toe = evs[to]
                    ratio = Fraction(fre, toe + 1)
                    yield ((frv - ratio * tov) / (ratio + 1), (fr, to))


def leastChange(*args):
    return min(changes(*args))


#  Parsers.

# unused since Python has split
def splitOn(c, s):
    (x, y) = s.split(c, 1)
    if y == "":
        return
    else:
        yield x
        splitOn(c, y[1:])


def readVoteLine(row):
    [st, *cols] = row.split(",")
    [h, *t] = map(lambda s: int(s) if s and s[0].isdigit() else 0, cols)
    return (st[:2], PECInput(h, t))


def readVoteSet(s):
    return list(map(readVoteLine, filter(
        lambda x: x != "" and x[0] != "#", s.split("\n"))))


def readVoteFile(fn):
    with open(fn, 'r') as f:
        return readVoteSet(f.read())


def addVec(v1, v2):
    return map(lambda u: u[0] + u[1], zip_longest(v1, v2, fillvalue=0))

