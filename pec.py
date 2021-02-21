#! /usr/bin/python3

#  apportion.hs

from voting.pec import \
    apportion, addAtLarge, leastChange, readVoteFile, addVec, vpeRange
from fractions import Fraction
from math import floor
import sys

atLarges = 2


def roundish(lo, hi):
    if hi < lo:
        return hi
    else:
        rto = lambda m: (hi // m) * m
        pfind = lambda p: p // 10 if rto(p) < lo else pfind(p * 10)
        pow_ = pfind(1)
        return rto(
            5 * pow_ if rto(5 * pow_) >= lo else
            2 * pow_ if rto(2 * pow_) >= lo else
            pow_)


def chfor(w):
    return chr(ord('A') + w)


def pr(*s):
    print(*s, end="")


def printrow(l):
    pr("".join(map(lambda x: f" {x:>4d}", l)))


[_, file_] = sys.argv
list_ = readVoteFile(file_)
tot = []

pr(f"   {'t':>5s}   ")
for c in range(len(list_[0][1].votes)):
    pr(f" {chfor(c):>4s}")

print(f"   {'v/e':>11s}   {'Δ':>14s}")

for (st, peci) in list_:
    ev = peci.electors
    vs = peci.votes
    apports = apportion(ev - atLarges, vs)
    evs = addAtLarge(atLarges, vs, apports)
    tot = addVec(tot, evs)
    pr(f"{st} {ev:5,d}   ")
    printrow(evs)
    tie = sum(evs) != ev
    (a, b) = vpeRange(vs, apports)
    a_ = floor(a)
    vpe = a_ if tie else roundish(a_ + 1, floor(b()))
    pr(f" {vpe:>13,d}")
    if tie:
        print(f" {'1':>12s} *→*", end="")
    else:
        (chg, (fr, to)) = leastChange(vs, apports)
        pr(f" {floor(chg + 1):>12,d} {chfor(fr)}→{chfor(to)}")
        mx = max(vs)
        if len(list(filter(lambda x: 2 * chg - Fraction(mx - x) > 0, vs))) > 1:
            pr(" *")
    print()

tot = list(tot)
pr(f"t: {sum(tot):>5,d}   ")
printrow(tot)
print()


# print(format_string("%n", 1234556))

# print(PECInput(100, [2,3,4]))
# print(apportion(11, [199, 207]))
# print(addAtLarge(atLarges, [199,207], apportion(11, [199, 207])))
# print(leastChange([199, 207], [5, 6]))


# print(roundish(139, 233))
