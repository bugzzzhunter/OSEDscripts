import subprocess
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

    def getProcessDetails(self, appName):
        #print(appName)
        p = subprocess.Popen(["powershell.exe", "(Get-Process -ProcessName "+appName+").Id"], stdout=subprocess.PIPE, shell=True)
        ret = p.communicate()
        return ret[0].decode('ascii').strip()


    def launchWindbg(self, pid,winDBGcmd):
        if ';Workspace=Default' in winDBGcmd:
            cmd = '"C:\\Program Files\\Windows Kits\\10\\Debuggers\\x86\windbg.exe" -c ".load pykd;'+winDBGcmd.replace(';Workspace=Default','')+'" -p '+str(pid)   # Low performance
        else:
            cmd = '"C:\\Program Files\\Windows Kits\\10\\Debuggers\\x86\windbg.exe" -c ".load pykd;'+winDBGcmd+'" -p '+str(pid) 
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
                pid=self.getProcessDetails(procName[:-4])
                #print("PID is:"+str(pid))
                if 'Cannot find' not in pid:
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