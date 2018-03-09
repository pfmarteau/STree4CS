# STree4CS
# Suffix Trees for Sequence Covering Similarity Evaluation
Python implementation of Suffix Trees and Generalized Suffix Trees for sequence (list) of integers and for the evaluation of the covering similarity. 
This code has been derived from Peter Us (petrus) implementation of generalized suffix trees available at https://github.com/ptrus/suffix-trees, under The MIT License (MIT).


### Installation
In the install directory:

$ python3 setup.py

or

$ pip3 install git+https://github.com/pfmarteau/STree4CS

### Usage

```python3
import STrees4CS as STree

# Suffix-Tree example.
st = STree([[1, 10, 5, 3 200, 8, 10, 2]])
print(st.find([1, 10])) # 0
print(st.find_all([10])) # [1, 6]

# Building a generalized Suffix-Tree.
A = [[1, 2, 3], [4, 5, 6, 2, 3, 7], [1, 2, 3, 4]]
st = STree(A)

# print the longest common subsequence for the set A
print(st.lcs()) # [2, 3]

# Sequence Covering similarity example
S=[[1,1,2,2,3,4,1,1,5,6], [1,2,4,3,4,5,7,5,1], [6,5,1,7,4,5,6]]
s=[1,1,5,7,5,1,7,4]

# Build the generalized Suffix-Tree for S
st = STree(S)

# get the S-optimal covering similarity for s
score, lbreak, lss = st.evaluateDichotomic(s)
print(score) # 0.75
print(lss) # the optimal covering [[1, 1, 5], [7, 5, 1], [7, 4]], 

```


# Usage note
This library is mostly an academic exercise. If you need an efficient library I would recommend a python-wrapped c implementation,
such as (http://www.daimi.au.dk/~mailund/suffix_tree.html).


# More information about the sequence covering similarity
* https://arxiv.org/abs/1712.02084
* https://arxiv.org/abs/1801.07013
