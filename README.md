# OSEDscripts
 My OSED scripts.
 
 You can reset the debugging environment using this script, test the default POC and find the EIP index. Few more things like adding windbg commands can also be done.

 The script needs modification in POC file.
  1. Replace your buffer variable name as 'inputBuffer'.
  2. Declare size of buffer using variable name as 'size'.
  3. Hard code IP addres of your target.
  
 (Refer to POC's in inputFiles folder)
 
 Script runs on all the OSED applications.
 
 To reset debugging environment. A simple way to do it is as below.
 
 ![Reset environment](StartAppForDebug.gif)
 
 
 Use below commands to check if app crashes with POC and to find EIP index.
 
![CrashAndFindIndex](CrashAppAndFindIndex.gif)
