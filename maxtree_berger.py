import numpy as np
import time

## Recursive find_root
# def find_root(x):
#     if zpar[x] == x:
#         return x
#     else:
#         zpar[x] = find_root(zpar[x])
#         return zpar[x]


def find_root(x):
    """Non-recursive version find_root procedure"""

    r = x
    while not r == zpar[r]:
        r = zpar[r]

    t1 = x
    while not t1 == r:
        t2 = zpar[t1]
        zpar[t1] = r
        t1 = t2

    return r


def neighbors(p):
    n = []
    if p > height:
        n.append(p - height)    # top
    if p % height > 0:
        n.append(p - 1)             # left
    if (p + 1) % height != 0:
        n.append(p + 1)             # right
    if p < height * (width - 1):
        n.append(p + height)    # bottom
    return n


def reverse_sort(f):
    r = list([])
    for i in range(f.max(), f.min() - 1, -1):
        a = np.array(np.where(f == i)).ravel()
        r.extend(a)
    return r


def compute_tree(f):
    R = reverse_sort(f)
    for p in R:
        parent[p] = p
        zpar[p] = p
        for n in neighbors(p):
            if zpar[n] != undef:
                r = find_root(n)
                if r != p:
                    parent[r] = p
                    zpar[r] = p

    canonize_tree(f, R, parent)
    return R, parent


def canonize_tree(f, R, parent):
    for p in R[::-1]:
        q = parent[p]
        if f[parent[q]] == f[q]:
            parent[p] = parent[q]


import cv2
f = cv2.imread('lena.bmp', 0)
# f = np.array([[3, 3, 1, 4, 2], [4, 1, 2, 3, 1]])
# f = np.array([[15,13,16],[12,12,10],[16,12,14]])
undef = -1
width, height = f.shape
parent = [undef] * f.size
zpar = [undef] * f.size

t = time.time()
R, parent = compute_tree(f.ravel())
t = time.time() - t
print t

print 'R:', np.array(R)
print 'parent:', np.array(parent)
