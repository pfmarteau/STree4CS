import STree4CS as STree
import random
import numpy as np


def randomList(rg, minl, maxl):
    l = int(random.uniform(minl, maxl))
    out = []
    for i in range(l):
        out.append(random.randint(0, rg))
    return out


def str2intarray(s):
    out = []
    for e in s:
        out.append(ord(e))
    return out


def coveringDistance_str(s1, s2):
    '''
    :param s1: string
    :param s2: string
    :return: covering distance between s1 and s2
    '''
    s11 = str2intarray(s1)
    s22 = str2intarray(s2)
    st1 = STree.STree4CS([s11])
    st2 = STree.STree4CS([s22])
    d1 = st1.evaluateSimple(s22)
    d2 = st2.evaluateSimple(s11)
    d = 1.0 / 2.0 * (2 - d1[0] - d2[0])
    return d


def coveringDistance(s1, s2):
    '''
    :param s1: list of integers
    :param s2: list of integers
    :return: covering distance between s1 and s2
    '''
    st1 = STree.STree4CS([s1])
    st2 = STree.STree4CS([s2])
    d1 = st1.evaluateSimple(s2)
    d2 = st2.evaluateSimple(s1)
    d = 1.0 / 2.0 * (2 - d1[0] - d2[0])
    return d


def coveringSimilariy(s1, s2):
    '''
    :param s1: list of integers
    :param s2: list of integers
    :return: covering similarity between s1 and s2
    '''
    st1 = STree.STree4CS([s1])
    st2 = STree.STree4CS([s2])
    d1 = st1.evaluateSimple(s2)
    d2 = st2.evaluateSimple(s1)
    d = (d1[0] + d2[0]) / 2.0
    return d


def test0():
    a = [[1, 2, 3], [4, 5, 6, 2, 3, 7], [1, 2, 3, 4]]
    st = STree.STree4CS(a)
    print('the LCSS in S=', a, ' is:')
    print(st.lcs())


def test1():
    '''
    test the triangle indequality of the covering distance
    :return:
    '''
    rg = 3
    minl = 10
    maxl = 20
    for n in range(100):
        s1 = randomList(rg, minl, maxl)
        s2 = randomList(rg, minl, maxl)
        s3 = randomList(rg, minl, maxl)
        d12 = coveringDistance(s1, s2)
        d13 = coveringDistance(s1, s3)
        d23 = coveringDistance(s2, s3)
        print('.', end='', flush=True)
        if (d12 > d13 + d23):
            print(coveringDistance(s1, s2))
            print(coveringDistance(s1, s3) + coveringDistance(s3, s2))
            print(coveringDistance(s2, s2))
            break
    print('no violation of the triangle inequality detected')

def test2():
    print('covering distance between [10,2, 3, 5,10, 2, 7, 8] and [10,2, 3, 5,11, 2, 7, 8] is ', coveringDistance([10,2, 3, 5,10, 2, 7, 8], [10,2, 3, 5,11, 2, 7, 8]))

def test3():
    print('covering distance between \'amrican\' and \'american\' is ', coveringDistance_str('amrican', 'american'))
    print('covering distance  between \'european\' and \'american\' is ', coveringDistance_str('european', 'american'))
    print('covering distance  between \'european\' and \'indoeuropean\' is ', coveringDistance_str('european', 'indoeuropean'))
    print('covering distance  between \'indian\' and \'indoeuropean\' is ', coveringDistance_str('indian', 'indoeuropean'))
    print('covering distance  between \'indian\' and \'american\' is ', coveringDistance_str('indian', 'american'))
    print('covering distance  between \'narcotics\' and \'narcoleptics\' is ',
          coveringDistance_str('narcotics', 'narcoleptics'))
    print('covering distance  between \'burns out\' and \'outburns\' is ', coveringDistance_str('burns out', 'outburns'))
