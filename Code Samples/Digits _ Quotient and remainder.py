def quot_rem(n1,n2):
    a=n1/n2
    q=float("%.2f" % a)
    while n1>n2:
        r=n1//n2
    else:
        r=n1
    X=(q,r)
    return X
