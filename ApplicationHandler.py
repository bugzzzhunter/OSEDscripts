import subprocess, psutil 
import sys, os
import time

class runApplication:

    def getServiceDetails(self, appName, getInfo):
        p = subprocess.Popen(["powershell.exe", "(Get-WmiObject -Class Win32_Service -Filter \"Name LIKE '"+appName+"'\")."+getInfo], stdout=subprocess.PIPE, shell=True)
        ret = p.communicate()
        return ret[0].decode('ascii').strip()

    def restartService(self, appName):
        p = subprocess.Popen(["powershell.exe", "Restart-Service -Name "+appName.replace(' ','` ')], stdout=subprocess.PIPE, shell=True)
        ret = p.communicate()
        return ret[0].decode('ascii').strip()


    def launchWindbg(self, pid,winDBGcmd):
        cmd = '"C:\\Program Files\\Windows Kits\\10\\Debuggers\\x86\windbg.exe" -W "Default" -c ".load pykd;'+winDBGcmd+'" -p '+str(pid)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
        return p
        #os.system('"'+cmd+'"')

    def startService(self,appName):
            
        #global appName

        if appName[-4:] == '.exe':
            if os.path.exists(appName):
                #print("File exists")
                #time.sleep(3)
                procName = appName.split('\\')[-1]
                #print(procName)
                if procName.lower() in (p.name().lower() for p in psutil.process_iter()):
                    pid=[p.pid for p in psutil.process_iter() if p.name().lower()==procName.lower()][0]
                    if pid:
                        print("existing PID: "+str(pid))
                        return pid
                else:
                    p=subprocess.Popen(appName,stdout=subprocess.PIPE, shell=False)
                    #print("new PID: "+str(p.pid))
                    return p.pid
            else:
                print("Application exe does not exist!")
                sys.exit()
        else:
            #print('Ch3cking service: '+appName)
            serviceState=self.getServiceDetails(appName,"state")
            if serviceState and serviceState == 'Running':
                #print("Service "+appName+" is "+serviceState)
                pid=self.getServiceDetails(appName,"ProcessId")
                return pid
            elif serviceState:
                #Start/Restart service
                self.restartService(appName)
                #print("Service exist but not running! \r\nStarting service!")
                pid=self.getServiceDetails(appName,"ProcessId")
                return pid
            else:
                print("Application/Service does not exist!")
                sys.exit()