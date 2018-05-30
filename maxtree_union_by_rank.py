import numpy as np
import time
import matplotlib.pyplot as plt

# def find_root(x):
#     if zpar[x] == x:
#         return x
#     else:
#         zpar[x] = find_root(zpar[x])
#         return zpar[x]


def find_root(x):
    z = x
    while not z == zpar[z]:
        z = zpar[z]

    while not x == z:
        y = zpar[x]
        zpar[x] = z
        x = y

    return z


def find_node(x, k):
    while (parent[x] != k) and (x != parent[x]):
        x = parent[x]
    if parent[x] == k:
        return True


def neighbors(p):
    n = []
    if p > width:
        n.append(p - width)    # top
    if p % width > 0:
        n.append(p - 1)             # left
    if (p + 1) % width != 0:
        n.append(p + 1)             # right
    if p < width * (height - 1):
        n.append(p + width)    # bottom
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
        rank[p] = 0
        rep[p] = p
        zp = p
        for n in neighbors(p):
            if zpar[n] != undef:
                zn = find_root(n)
                if zn != zp:
                    parent[rep[zn]] = p
                    if rank[zp] < rank[zn]:
                        zp, zn = zn, zp
                    zpar[zn] = zp
                    rep[zp] = p
                    if rank[zp] == rank[zn]:
                        rank[zp] = rank[zp] + 1

    canonize_tree(f, R, parent)
    # compute_area(f, R, parent)
    return R, parent


def canonize_tree(f, R, parent):
    for p in R[::-1]:
        q = parent[p]
        if f[parent[q]] == f[q]:
            parent[p] = parent[q]


def compute_area(f, R, parent):
    for p in R:
        if parent[p] != p:
            area[parent[p]] = area[parent[p]] + area[p]
        # print p, parent[p], area


import cv2
f = cv2.imread('lena.bmp', 0)

undef = -1
height, width = f.shape
parent = [undef] * f.size
zpar = [undef] * f.size
rank = [undef] * f.size
rep = [undef] * f.size
area = [1] * f.size

t = time.time()
R, parent = compute_tree(f.ravel())
t0 = time.time() - t
print t0

print 'R:', np.array(R)
print 'parent:', np.array(parent)
