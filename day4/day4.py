import sys

def parseInputRound1():
    pairs_containing_whole = 0
    for line in sys.stdin:
        (pair1, pair2) = line.split(',')
        (par1L, par1H) = pair1.split('-')
        (par2L, par2H) = pair2.split('-')
        if int(par1L) <= int(par2L) and int(par1H) >= int(par2H) or int(par1L) >= int(par2L) and int(par2H) >= int(par1H):
            pairs_containing_whole += 1
    return pairs_containing_whole

def parseInputRound2():
    pairs_containing_whole = 0
    for line in sys.stdin:
        (pair1, pair2) = line.split(',')
        (par1L, par1H) = pair1.split('-')
        (par2L, par2H) = pair2.split('-')
        if int(par1L) <= int(par2H) and int(par1L) >= int(par2L) or int(par1H) >= int(par2L) and int(par2H) >= int(par1H):
            pairs_containing_whole += 1
        elif int(par1L) <= int(par2L) and int(par1H) >= int(par2H) or int(par1L) >= int(par2L) and int(par2H) >= int(par1H):
            pairs_containing_whole += 1
    return pairs_containing_whole

if __name__=='__main__':
    # print(parseInputRound1())
    print(parseInputRound2())
