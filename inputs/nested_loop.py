def f(i, j):
    print(i, j)


for i in range(3):
    f(i, 0)
    for j in range(3):
        f(i, j)
