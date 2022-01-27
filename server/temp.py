
def ntoa(n):
    c4 = n % 93 + 33
    c3 = n // 93 % 93 + 33
    c2 = n // 93**2 % 93 + 33
    c1 = n // 93**3 % 93 + 33

    return ''.join(map(chr, (c1, c2, c3, c4)))


for i in range(1):
    print(ntoa(74805197))
