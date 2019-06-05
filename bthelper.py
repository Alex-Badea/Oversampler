def genseq(initstr, stopcond, incrementer, resetter):
    seq = []
    seq.append(initstr.copy())
    str = initstr
    halt = False
    head = len(initstr) - 1

    def STOP(): return stopcond(str[head])
    def INCREMENT(): str[head] = incrementer(str[head])
    def RESET_LWR():
        for i in range(head + 1, len(str)):
            str[i] = resetter(str[i-1])
    def REWIND(): nonlocal head; head = len(str)-1
    def PRINT(): seq.append(str.copy())
    def REACH_MSB(): return head == 0
    def UNWIND(): nonlocal head; head -= 1
    def HALT(): nonlocal halt; halt -= 1

    while not halt:
        if not STOP():
            INCREMENT()
            RESET_LWR()
            REWIND()
            PRINT()
        else:
            if not REACH_MSB():
                UNWIND()
            else:
                HALT()
    return seq