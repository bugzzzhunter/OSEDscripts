import os, argparse

import ApplicationHandler, exploitHandler

winDBGcmd = "g"

def runExploitMode(mode,eFile, eDelay):
    global winDBGcmd

    print("[*]Exploiting "+appName)
    if not eFile:
        eFile = os.path.abspath('.')+"\exploit.py"
        while not os.path.exists(eFile):
            eFile = input("[!]Exploit.py file not found! Please provide valid path: ")
    else:
        while not os.path.exists(eFile):
            eFile = input("[!]Exploit.py file not found! Please provide valid path: ")

    eh = exploitHandler.exploitHandler
    #eh.parseeFile(eFile)

    #eh.exploit(ah,appName,mode,eFile,eDelay)
    eh.exploit(appName,mode,eFile,eDelay)
    
def main():
    #global ah
    global appName
    global winDBGcmd

    exp = False

    exploitModes = ['runApp', 'crash', 'findIndex', 'findBadChar', 'quickRun']

    parser = argparse.ArgumentParser()
    #group = parser.add_mutually_exclusive_group()
    #subparsers = parser.add_subparsers(help='sub-command help')
    parser.add_argument(
        'app', 
        help='Application/Service you want to hack'
    )
    parser.add_argument(
        '-c', 
        '--cmd', 
        help='WinDBG command to run (works only with runApp mode)', 
    )
    parser.add_argument(
        '-e', 
        '--exploit', 
        help='python exploit file to be passed on to winDBG as "!py exploit.py"', 
    )
    parser.add_argument(
        '-ed', 
        '--exploitDelay', 
        help='Delay in running exploit file in seconds. Default = 2',
        type=int,
        default=2 
    )
    parser.add_argument(
        '-m', 
        '--mode', 
        choices=exploitModes,
        help='exploit mode - '+', '.join(exploitModes),
        metavar='',
        required=True
    ) 

    args = parser.parse_args()

    appName=args.app
    #ah = ApplicationHandler.runApplication()

    if args.cmd:
        winDBGcmd=args.cmd
    if args.mode == 'runApp':
        ah = ApplicationHandler.runApplication()
        pid=ah.startService(appName)
        winDBGcmd+=';Workspace=Default'
        windbgProc=ah.launchWindbg(pid,winDBGcmd)
        print('[*]Application '+appName+' is up and runnning with pid '+str(pid))
    elif args.mode == 'quickRun':
        ah = ApplicationHandler.runApplication()
        pid=ah.startService(appName)
        windbgProc=ah.launchWindbg(pid,winDBGcmd)
        print('[*]Application '+appName+' is up and runnning with pid '+str(pid))
    elif args.mode == 'crash' or args.mode == 'findIndex' or args.mode == 'findBadChar':
        winDBGcmd=""
        exp = True
        runExploitMode(args.mode, args.exploit, args.exploitDelay)


        
if __name__ == '__main__':
    main()