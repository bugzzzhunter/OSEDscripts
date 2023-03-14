#!/usr/bin/python

import time,os
import pattern
import pykd

#fd=open("fuzz_out.txt","a")

def main():
    
    
    pykd.go()

    fsFile = os.path.abspath('.')+'\\exploitStatus.txt'

    while not os.path.exists(fsFile):
        continue

    fs=open(fsFile,'r')

    es=fs.readlines()
    fs.close()
    os.remove(fsFile)

    if es[0].strip():

        eip=str(hex(pykd.getIP()))
        try:
            index=pattern.pattern_search(eip)
            print("Pattern "+eip+" found at: "+str(index))
            #fd.write("Pattern found at: "+str(index))
            f=open('status.txt','w')
            f.write(str(index))
            f.close()
        except:
            print("Pattern not found! Attempting SEH check!")
            exchainIP=pykd.dbgCommand('!exchain').split(" ")[-1].strip()
            print(exchainIP)
            try:
                index=pattern.pattern_search(str("0x"+exchainIP))
                print("Pattern "+str("0x"+exchainIP)+" found at: "+str(index))
                #fd.write("Pattern found at: "+str(index))
                f=open('status.txt','w')
                f.write(str(index))
                f.close()
            except:
                print("Pattern not found!")


if __name__ == '__main__':
    main()
