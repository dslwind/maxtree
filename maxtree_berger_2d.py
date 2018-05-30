import numpy as np
import time


def find_root(x):
    if np.array_equal(zpar[x[0], x[1]], x):
        return x
    else:
        zpar[x[0], x[1]] = find_root(zpar[x[0], x[1]])
        return zpar[x[0], x[1]]


def neighbors(p):
    n = []
    if p[0] > 0:
        n.append([p[0] - 1, p[1]])
    if p[0] < width - 1:
        n.append([p[0] + 1, p[1]])
    if p[1] > 0:
        n.append([p[0], p[1] - 1])
    if p[1] < height - 1:
        n.append([p[0], p[1] + 1])
    return n


def reverse_sort(f):
    c = list([])
    for i in range(f.max(), f.min() - 1, -1):
        a = np.array(np.where(f == i)).T
        b = [a[j] for j in range(len(a))]
        c.extend(b)
    return np.array(c)


def compute_tree(f):
    R = reverse_sort(f)
    for p in R:
        parent[p[0], p[1]] = p
        zpar[p[0], p[1]] = p
        for n in neighbors(p):
            if not np.array_equal(zpar[n[0], n[1]], np.array([undef, undef])):
                r = np.array(find_root(n))
                if not np.array_equal(r, p):
                    parent[r[0], r[1]] = p
                    zpar[r[0], r[1]] = p

    canonize_tree(parent, f, R)
    return R, parent


def canonize_tree(parent, f, R):
    for p in R[::-1]:
        q = parent[p[0], p[1]]
        t = parent[q[0], q[1]]
        if f[t[0], t[1]] == f[q[0], q[1]]:
            parent[p[0], p[1]] = parent[q[0], q[1]]


import cv2
# f = cv2.imread('lena.bmp', 0)
f = np.array([[3, 3, 1, 4, 2], [4, 1, 2, 3, 1]])
# f = np.array([[15,13,16],[12,12,10],[16,12,14]])
undef = -1
width, height = f.shape
parent = np.ones((width, height, 2), dtype=int) * undef
zpar = np.ones((width, height, 2), dtype=int) * undef
# print compute_tree(f)
t = time.time()
R, parent = compute_tree(f)
t = time.time() - t
print t
print R
print parent 
