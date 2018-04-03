'''
Derived rom Peter Us (petrus) implementation of generalized suffix trees available at https://github.com/ptrus/suffix-trees
The MIT License (MIT),
Modified by P-F. Marteau, 9 november 2017 to cope with list of integers and covering similarity computation
Bug in the 'evaluateDichotomic()' function, corrected by François Brochard (Master 2 student at Université Bretagne Sud), 7th of March 2018
'''
import sys
import numpy as np
import math


class STree4CS():
    """Class representing the suffix tree."""

    def __init__(self, input=''):
        self.root = _SNode()
        self.root.depth = 0
        self.root.idx = 0
        self.root.parent = self.root
        self.root._add_suffix_link(self.root)
        self.begs = []
        self.ends = []
        if not input == '':
            self.build(input)

    def _check_input(self, input):
        """Checks the validity of the input.

        In case of an invalid input throws ValueError.
        """
        if isinstance(input, str):
            return 'st'
        elif isinstance(input, list):
            if all(isinstance(item, list) for item in input):
                return 'gst'

        raise ValueError("Sequence argument should be of type list or"
                         " a list of sequences")

    def build(self, x):
        """Builds the Suffix tree on the given input.
        If the input is of type List of Sequences:
        Generalized Suffix Tree is built.

        :param x: Sequence or List of Sequences
        """
        type = self._check_input(x)

        if type == 'st':
            x += next(self._terminalSymbolsGenerator())
            self._build(x)
        if type == 'gst':
            self._build_generalized(x)

    def _build(self, x):
        """Builds a Suffix tree."""
        self.word = x
        self._build_McCreight(x)

    def _build_McCreight(self, x):
        """Builds a Suffix tree using McCreight O(n) algorithm.

        Algorithm based on:
        McCreight, Edward M. "A space-economical suffix tree construction algorithm." - ACM, 1976.
        Implementation based on:
        UH CS - 58093 String Processing Algorithms Lecture Notes
        """
        u = self.root
        d = 0
        for i in range(len(x)):
            while u.depth == d and u._has_transition(x[d + i]):
                u = u._get_transition_link(x[d + i])
                d = d + 1
                while d < u.depth and x[u.idx + d] == x[i + d]:
                    d = d + 1
            if d < u.depth:
                u = self._create_node(x, u, d)
            self._create_leaf(x, i, u, d)
            if not u._get_suffix_link():
                self._compute_slink(x, u)
            u = u._get_suffix_link()
            d = d - 1
            if d < 0:
                d = 0

    def _create_node(self, x, u, d):
        i = u.idx
        p = u.parent
        v = _SNode(idx=i, depth=d)
        v._add_transition_link(u, x[i + d])
        u.parent = v
        p._add_transition_link(v, x[i + p.depth])
        v.parent = p
        return v

    def _create_leaf(self, x, i, u, d):
        w = _SNode()
        w.idx = i
        w.depth = len(x) - i
        u._add_transition_link(w, x[i + d])
        w.parent = u
        return w

    def _compute_slink(self, x, u):
        d = u.depth
        v = u.parent._get_suffix_link()
        while v.depth < d - 1:
            v = v._get_transition_link(x[u.idx + v.depth + 1])
        if v.depth > d - 1:
            v = self._create_node(x, v, d - 1)
        u._add_suffix_link(v)

    def _build_Ukkonen(self, x):
        """Builds a Suffix tree using Ukkonen's online O(n) algorithm.
        Algorithm based on:
        Ukkonen, Esko. "On-line construction of suffix trees." - Algorithmica, 1995.
        """
        # TODO.
        raise NotImplementedError()

    def _build_generalized(self, xs):
        """Builds a Generalized Suffix Tree (GST) from the array of sequences provided.
        """
        terminal_gen = self._terminalSymbolsGenerator()

        # _xs = [x + next(terminal_gen) for x in xs]
        _xs = []
        n = 0
        beg = 0
        for x in xs:
            end = beg + len(x)
            self.begs.append(beg)
            self.ends.append(end)
            _xs += x + next(terminal_gen)
            n += 1
            beg = end + 1
        self.word = _xs
        self._generalized_word_starts(xs)
        self._build(_xs)
        self.root._traverse(self._label_generalized)

    def _label_generalized(self, node):
        """Helper method that labels the nodes of GST with indexes of sequences
        found in their descendants.
        """
        if node.is_leaf():
            x = {self._get_word_start_index(node.idx)}
        else:
            x = {n for ns in node.transition_links for n in ns[0].generalized_idxs}
        node.generalized_idxs = x

    def _get_word_start_index(self, idx):
        """Helper method that returns the index of the sequence based on node's
        starting index"""
        i = 0
        for _idx in self.word_starts[1:]:
            if idx < _idx:
                return i
            else:
                i += 1
        return i

    def lcs(self, seqIdxs=-1):
        """Returns the Largest Common Subsequence of sequences provided in seqIdxs.
        If seqIdxs is not provided, the LCS of all sequences is returned.

        ::param seqIdxs: Optional: List of indexes of sequences.
        """
        if seqIdxs == -1 or not isinstance(seqIdxs, list):
            seqIdxs = set(range(len(self.word_starts)))
        else:
            seqIdxs = set(seqIdxs)

        deepestNode = self._find_lcs(self.root, seqIdxs)
        start = deepestNode.idx
        end = deepestNode.idx + deepestNode.depth
        return self.word[start:end]

    def _find_lcs(self, node, seqIdxs):
        """Helper method that finds LCS by traversing the labeled GSD."""
        nodes = [self._find_lcs(n, seqIdxs)
                 for (n, _) in node.transition_links
                 if n.generalized_idxs.issuperset(seqIdxs)]

        if nodes == []:
            return node

        deepestNode = max(nodes, key=lambda n: n.depth)
        return deepestNode

    def _generalized_word_starts(self, xs):
        """Helper method returns the starting indexes of sequences in GST"""
        self.word_starts = []
        i = 0
        for n in range(len(xs)):
            self.word_starts.append(i)
            i += len(xs[n]) + 1

    def find(self, y):
        """Returns starting position of the subsequence y in the sequence used for
        building the Suffix tree.

        :param y: Seq
        :return: Index of the starting position of sequence y in the sequence used for building the Suffix tree
                 -1 if y is not a subsequence.
        """
        node = self.root
        while True:
            edge = self._edgeLabel(node, node.parent)
            if edge[:len(y)] == y:  # edge.startswith(y):
                return node.idx

            i = 0
            while (i < len(edge) and edge[i] == y[0]):
                y = y[1:]
                i += 1

            if i != 0:
                if i == len(edge) and y != []:
                    pass
                else:
                    return -1

            node = node._get_transition_link(y[0])
            if not node:
                return -1

    def find_all(self, y):
        node = self.root
        while True:
            edge = self._edgeLabel(node, node.parent)
            if edge[:len(y)] == y:  # edge.startswith(y):
                break

            i = 0
            while (i < len(edge) and edge[i] == y[0]):
                y = y[1:]
                i += 1

            if i != 0:
                if i == len(edge) and y != []:
                    pass
                else:
                    return []

            node = node._get_transition_link(y[0])
            if not node:
                return []

        leaves = node._get_leaves()
        return [n.idx for n in leaves]

    def _edgeLabel(self, node, parent):
        """Helper method, returns the edge label between a node and it's parent"""
        return self.word[node.idx + parent.depth: node.idx + node.depth]

    def _terminalSymbolsGenerator(self):
        """Generator of unique terminal symbols used for building the Generalized Suffix Tree.
        negative integer is used to ensure that terminal symbols
        are not part of the input sequence.
        """
        UPPAs = [i for i in range(1, 1000000)]
        for i in UPPAs:
            yield ([-i])
        raise ValueError("To many input sequences.")

    def getNextBreakDichotomic(self, s):
        '''
        :param s: a subsequence
        :return: returns the index t corresponding to the next break, i.e. the location where the current subsequence of the covering will end
        '''
        beg = 0
        end = len(s)
        t = int((beg + end) / 2)
        t0 = beg
        while True:
            # print(t,beg,end)
            srch = self.find(s[beg:t])
            while srch >= 0 and np.abs(t - end) > 1:
                # print('.',end='',flush=True)
                t0 = t
                t = int((t + end) / 2)
                srch = self.find(s[beg:t])
            if np.abs(t0 - end) <= 1:
                break
            srch = self.find(s[beg:t])
            while srch < 0 and np.abs(t - t0) > 1:
                # print('*', end='', flush=True)
                t = int((t0 + t) / 2)
                srch = self.find(s[beg:t])
            if np.abs(t - t0) <= 1:
                break

        while self.find(s[beg:t]) < 0 and t > 0:
            # print(t, end=' ', flush=True)
            t -= 1
        while self.find(s[beg:t]) >= 0 and t <= end:
            # print('+', end='', flush=True)
            t += 1
        '''if(t<len(s)):
            print('!!',self.find(s[beg:t]))'''
        return t

    def evaluateDichotomic(self, s):
        '''
        :param s: the sequence for which the covering similarirty will be evaluated
        :return: the covering simlarity for s evaluated using the dichotomic way
        '''
        '''evaluate the covering of the suffix tree with regard to input sequence s
        returns score, the sum of the length of all the subsequences of s found in the Stree
        returnslbreak, the list of the symbols that have break the search of a subsequence and the length of the
        previously found subsequence'''
        lbreak = []
        lss = []
        beg = 0
        L = len(s)
        if L==0:
            return [1,[],[]]
        while beg<L :
            end = self.getNextBreakDichotomic(s[beg:]) + beg -1
            if end == beg : #if s[beg] isn't in the tree
               end+=1
            if end<L :
               lbreak.append([s[end] , end-beg])
            lss.append(s[beg:end])
            beg = end
        score = (L-len(lss)+1)/L
        return [score,lbreak,lss]

    def evaluateSimple(self, s):
        '''
        :param s: the sequence for which the covering similarirty will be evaluated
        :return: the covering simlarity for s
        '''
        '''evaluate the covering of the suffix tree with regard to input sequence s
        returns score, the sum of the length of all the subsequences of s found in the Stree
        returnslbreak, the list of the symbols that have break the search of a subsequence and the length of the
        previously found subsequence'''
        lbreak = []
        lss = []
        beg = 0
        L = len(s)
        while beg < L:
            end = beg + 1
            while end <= L and self.find(s[beg:end]) >= 0:
                end += 1
            # print(beg,end,end='||')
            beg0 = end
            if end <= L:
                lbreak.append([end - 1 - beg, s[end - 1]])
                if end - 1 - beg > 0:
                    beg0 = end - 1
            if(beg+1==end):
               end+=1
            lss.append(s[beg:end - 1])
            beg = beg0
        score = (L - len(lbreak)) / L
        return [score, lbreak, lss]

    def getSeqId(self, n):
        '''
        :param n: a sequence index (time-stamp): in the generalized suffix tree, the sequences of the input set S are
        (virtually) concatenated and n is a symbol index in this concatenated sequence
        :return: the sequence ID that contains the index n, i.e. the location of the sequence in the concatenation.
        '''
        lb = self.begs
        le = self.ends
        L = len(lb)
        te = L - 1
        tb = 0
        while True:
            t = int((te + tb) / 2)
            if te == tb or np.abs(tb - te) == 1:
                break
            elif n < lb[t]:
                te = t - 1
            elif n > lb[t]:
                tb = t + 1
            elif n == lb[t]:
                return t, 0
            # print(t,tb,te)
        while lb[tb] > n:
            tb = tb - 1
        while le[tb] < n:
            tb = tb + 1
        return tb, n - lb[tb]


class _SNode():
    """Class representing a Node in the Suffix tree."""

    def __init__(self, idx=-1, parentNode=None, depth=-1):
        # Links
        self._suffix_link = None
        self.transition_links = []
        # Properties
        self.idx = idx
        self.depth = depth
        self.parent = parentNode
        self.generalized_idxs = {}

    def __str__(self):
        return ("SNode: idx:" + str(self.idx) + " depth:" + str(self.depth) +
                " transitons:" + str(self.transition_links))

    def _add_suffix_link(self, snode):
        self._suffix_link = snode

    def _get_suffix_link(self):
        if self._suffix_link != None:
            return self._suffix_link
        else:
            return False

    def _get_transition_link(self, suffix):
        for node, _suffix in self.transition_links:
            if _suffix == '__@__' or suffix == _suffix:
                return node
        return False

    def _add_transition_link(self, snode, suffix=''):
        tl = self._get_transition_link(suffix)
        if tl:  # TODO: imporve this.
            self.transition_links.remove((tl, suffix))
        self.transition_links.append((snode, suffix))

    def _has_transition(self, suffix):
        for node, _suffix in self.transition_links:
            if _suffix == '__@__' or suffix == _suffix:
                return True
        return False

    def is_leaf(self):
        return self.transition_links == []

    def _traverse(self, f):
        for (node, _) in self.transition_links:
            node._traverse(f)
        f(self)

    def _get_leaves(self):
        if self.is_leaf():
            return [self]
        else:
            return [x for (n, _) in self.transition_links for x in n._get_leaves()]
