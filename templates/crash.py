#!/usr/bin/python

import time, os
import pykd


fd=open("fuzz_out.txt","a")

def main():
    
    pykd.go()

    fsFile = os.path.abspath('.')+'\\exploitStatus.txt'
    print(fsFile)

    while not os.path.exists(fsFile):
        continue
    print("Exploit status found!")
    fs=open(fsFile,'r')

    es=fs.readlines()
    print(es)
    fs.close()
    os.remove(fsFile)

    print(pykd.dbgCommand('r'))
    
    if es[0].strip():
        if hex(pykd.getIP()) == '0x41414141':
            print('*'*10+'Application crashed!'+'*'*10)
            #Restart app with pattern
            print("EIP is:"+str(hex(pykd.getIP())))
            f=open('status.txt','w')
            f.write('True')
            f.close()
        elif '41414141' in pykd.dbgCommand('!exchain'):
            print('*'*10+'Application crashed!'+'*'*10)
            print(pykd.dbgCommand('!exchain'))
            #Restart app with pattern
            print(str(hex(pykd.getIP())))
            print("!exchain is:"+str(pykd.dbgCommand('!exchain')))
            f=open('status.txt','w')
            f.write('True')
            f.write('\nSEH')
            f.close()
        elif '41414141' in pykd.dbgCommand('r'):
            print('*'*10+'Application crashed but no EIP control!'+'*'*10)
            print(pykd.dbgCommand('r'))
            fd.write(pykd.dbgCommand('r'))
            #Restart app with pattern
            print(str(hex(pykd.getIP())))
            f=open('status.txt','w')
            f.write('True')
            f.close()
    else:
        print('*'*10+'Application not crashed!'+'*'*10)



if __name__ == '__main__':
    main()
