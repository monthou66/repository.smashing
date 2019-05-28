#!/usr/bin/python
# -*- coding: utf-8 -*-
# triggered when text file is created
import os
import shutil
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import socket
import time
from time import gmtime, strftime

host = socket.gethostname()
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
AddonName = ADDON.getAddonInfo('name')
FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
if  not os.path.isdir(FOLDER):
    os.mkdir(FOLDER)
workingfolder = os.path.join(FOLDER, "working")
if  not os.path.isdir(workingfolder):
    os.mkdir(workingfolder)
archive = os.path.join(FOLDER, "archive")
filestocheck = os.path.join(workingfolder, "aaafilestocheck.txt")
if  not os.path.isdir(archive):
    os.mkdir(archive)
    
nodelaytemp = os.path.join(workingfolder, "nodelay")
if  not os.path.isdir(nodelaytemp):
    os.mkdir(nodelaytemp)
addonlogfile = os.path.join(FOLDER, "addon.log")
ADDON_DIR = xbmc.translatePath(ADDON.getAddonInfo('path'))
WIN = xbmcgui.Window(10000)
# set defaults
WIN.setProperty('%s.running'% ADDON_ID, 'started') 

if ADDON.getSetting('restart.addon') == 'true':
    ADDON.setSetting('restart.addon', 'false')
if ADDON.getSetting('stop.addon') == 'true':
    ADDON.setSetting('stop.addon', 'false')
if ADDON.getSetting('clear.addonlogs') == 'true':
    ADDON.setSetting('clear.addonlogs', 'false')
if ADDON.getSetting('clear.archives') == 'true':
    ADDON.setSetting('clear.archives', 'false')
    
defaultscriptfolder = xbmc.translatePath('special://masterprofile/scripts')
scriptfolder = 'not set'
monitorfile = os.path.join(FOLDER, "passarguments.txt")
message = ""
message2 = ""
message3 = ""
message4 = ""
message5 = ""
message6 = ""
message7 = ""
message8 = ""
message9 = ""
message10 = ""
scriptfolderset = 'false'
defaultcentralfolder = "smb://192.168.1.25/Stuff/XBMC Stuff/central/"       # folder needs to end in a "/" for xbmcvfs.exists
notifythis = ""
pause = 'false'
defaultarchivenumber = 10
countcentral = 3600
# idletime = 10000

#tempfortesting
scriptfolder = xbmc.translatePath('special://masterprofile/smashing/smashingfavourites/scripts')
recursivecheck = 'true'
#write in another folder
checkwrite = xbmc.translatePath('special://masterprofile/addon_data/service.me.pvrcontrol/test.txt')
with open(checkwrite, "a") as myfile:
    myfile.write('Oh yes I can')
       
def printstar():
    xbmc.log("%s ***********************************************************************************"% ADDON_ID, 2)
    xbmc.log("%s ************************************************************************************"% ADDON_ID, 2)
    
def printlog():
    global message, message2, message3, message4, message5, message6, message7, message8, message9, message10, nextmess
    messages = []
    messages.append(message)
    messages.append(message2)    
    messages.append(message3)    
    messages.append(message4)    
    messages.append(message5)
    messages.append(message6)
    messages.append(message7)    
    messages.append(message8)    
    messages.append(message9)    
    messages.append(message10)
    if not loglevel == 'off':
        c = 0
        while c < 10:
            nextmess = messages[c]
            if not nextmess == "":
                xbmc.log("%s:    %s"% (ADDON_ID, nextmess), 2)
                if addonlog == 'true':
                    printaddonlog()
            c = c + 1
    message = ""
    message2 = ""
    message3 = ""
    message4 = ""
    message5 = ""
    message6 = ""
    message7 = ""
    message8 = ""
    message9 = ""
    message10 = ""
    
def printaddonlog():
    try:
        dateandtime = strftime("%Y-%m-%d     %H:%M:%S", gmtime())
    except:
        dateandtime = 'Date and time not known'
    if not os.path.exists(addonlogfile):
        with open(addonlogfile, "a") as myfile:
            header = ('%s    LOGFILE\n'% ADDON_ID)
            myfile.write(header)
    if not nextmess == "":
        nextline = ('\n%s    %s'%(dateandtime, nextmess))
    else:
        nextline = ('\n')
    with open(addonlogfile, "a") as myfile:
        myfile.write(nextline)
        
def notifystuff():
    global notifythis, pause, message
    if notify == 'true':
        if not notifythis == "":
            xbmc.executebuiltin('Notification(%s)'% notifythis)
            # send notifiucation to log?
            message = ('Notification sent: %s'% notifythis)
            printlog()
        if pause == 'true':
            message = 'pausing for 1 second'
            printlog()
            xbmc.sleep(1000)
    notifythis = ""
    pause = 'false'

def stopaddon():
    global message, notifythis, pause
    if loglevel == 'debug':
        printstar()
    if not loglevel == 'none':
        message = 'stopping addon'
        printlog()
    if loglevel == 'debug':
        printstar()
    notifythis = ("%s, stopping"% ADDON_ID)
    pause = 'true'
    notifystuff()
    target = os.path.join(ADDON_DIR, "scripts", "stop.py")
    if loglevel == 'debug':
        message = ("target script is %s"% target)
        printlog()
        printstar()
    xbmc.executebuiltin('RunScript(%s, %s)'% (target, ADDON_ID))   
    # service is disabled via json in target script

def restartaddon():
    global message, notifythis, pause
    if loglevel == 'debug':
        printstar()
    if not loglevel == 'none':
        message = 'restarting addon'
        printlog()
    notifythis = ("%s, restarting"% ADDON_ID)
    pause = 'true'
    notifystuff()        
    target = os.path.join(ADDON_DIR, "scripts", "restart.py")
    if loglevel == 'debug':
        message = ("target script is %s"% target)
        printlog()
        printstar()
    xbmc.executebuiltin('RunScript(%s, %s)'% (target, ADDON_ID))   
    # service is disabled and enabled via json in target script
    
# get settings
class SettingMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onSettingsChanged(self):
        xbmc.log("%s: Settings have changed**************************************************************"% ADDON_ID, 2)
        # xbmc.executebuiltin('Notification(%s, settings changed)'% ADDON_ID)
        getsettings()

def checkfolderpath():
    global monitorfolder, monitorfile, message
    if xbmcvfs.exists(checkfolder):
        monitorfolder = checkfolder
    else:
        message = ("Invalid monitor folder specified: %s"% checkfolder)
        printlog()
	    # dialog to say folder invalid / go back to settings
        yesnowindow = xbmcgui.Dialog().yesno('Arguments script: Invalid monitor folder', 'Click yes to set again', 'Click no to disable for this session')
        if yesnowindow:
		    # xbmcaddon.Addon().openSettings()
		    ADDON.openSettings()
        else:
            message = 'Service stopped for this session by user after invalid monitor folder selection'
            printlog()
            stopaddon()

def checkscriptfolderpath():
    global scriptfolder, scriptfolderset, message
    if not xbmcvfs.exists(scriptfolder):
        message = ("Invalid scriptfolder specified: %s"% scriptfolder)
        printlog()
        # dialog to say folder invalid / go back to settings or disable scriptfolder
        yesnowindow = xbmcgui.Dialog().yesno('Arguments script: Invalid script folder', 'Click yes to set again', 'Click no to disable script folder setting')
        if yesnowindow:
		    # xbmcaddon.Addon().openSettings()
		    ADDON.openSettings()
        else:
            message = 'Script folder selection was invalid so setting has been disabled'
            printlog()
            scriptfolderset = 'false'
            notifythis = ("Script folder, is disabled")
            notifystuff()
            ADDON.setSetting('script.folder', 'false')

def checkslash():
    global message, checkstring, newstring
    newstring = checkstring
    message = 'running checkslash()'
    printlog()
    message = ("string to check is %s"% checkstring)
    printlog()
    # check for "/" at end - for xbmcvfs, needed for directories
    last = checkstring[-1:]
    if not last == "/":
        newstring = checkstring + "/"
        message = ("string changed to %s"% newstring)
        printlog()
    else:
        message = 'No change made to string'
        printlog()
    
def checkcentralpath():
    global centralfolder, centralfolderset, checkstring, message
    if not xbmcvfs.exists(centralfolder):
        # check for "/"
        checkstring = centralfolder
        checkslash()
        if not newstring == checkstring:
            centralfolder = newstring
            message = ("central folder path changed to %s"% centralfolder)
            printlog()
            checkcentralpath()
        else:
            message = ("Unavailable central folder specified: %s"% centralfolder)
            printlog()
            if nocentral == 'prompt':
                # dialog to say folder unavailable / go back to settings or ignore
                yesnowindow = xbmcgui.Dialog().yesno('Arguments script: Central folder is unavailable', 'Click yes to set again', 'Click no to disable central folder setting')
                if yesnowindow:
		            ADDON.openSettings()
                else:
                    message = 'Central folder selection was unavailable so setting has been disabled'
                    printlog()
                    centralfolderset = 'false'
                    notifythis = ("Central folder, is disabled")
                    notifystuff()     
                    ADDON.setSetting('central.folder', 'false')
            
def clearlogs():
    global message, notifythis
    if os.path.exists(addonlogfile):
        try:
            os.remove(addonlogfile)
            xbmc.sleep(300)
            message = 'Addon logs cleared'
            printlog()
            notifythis = ("Addon logs, cleared")
        except:
            message = 'Failed to delete logfile'
            printlog()
            notifythis = ("Problem, addon logs not cleared")
    else:
        message = 'No addon logs found'
        printlog()
        notifythis = ("Addon log, not found")
    notifystuff()
    ADDON.setSetting('clear.addonlogs', 'false')
        
def cleararchives():
    global message, notifythis
    if os.path.exists(archive):
        message = ('Trying to delete archive: %s'% archive)
        printlog()
        try:
            shutil.rmtree(archive)
            xbmc.sleep(300)
            message = 'Archive folder cleared'
            printlog()
            notifythis = ("Archive folder, cleared")
        except:
            message = 'Failed to delete archive folder'
            printlog()
            notifythis = ("Problem, archive folder not cleared")
    else:
        message = 'No archive folder found'
        printlog()
        notifythis = ("Archive folder, not found")
        notifystuff()
        xbmc.sleep(1000)
    if not os.path.exists(archive):
        try:
            os.mkdir(archive)
        except:
            message = ('Failed to create archive folder: %s'% archive)
            printlog()
            notifythis = ("Problem, check log")
            notifystuff()
            xbmc.sleep(1000)
    notifystuff()
    ADDON.setSetting('clear.archives', 'false')

    
def getsettings():
    global message, checkfolder, monitorfolder, monitorfile, idletime, freq, loglevel, addonlog, notify, scriptfolderset, scriptfolder, centralfolder, centralfolderset, nocentral, centralidletime, centraldelay, centralfreq, archivenumber, archiveall
    # set defaults
    monitorfolder = FOLDER
    notify = 'true'
    scriptfolderset = 'false'
    centralfolderset = 'false'
    if ADDON.getSetting('clear.addonlogs') == 'true':
        clearlogs()
    if ADDON.getSetting('log.level') == "0":
        loglevel = 'debug'
    elif ADDON.getSetting('log.level') == "1":
        loglevel = 'normal'
    elif ADDON.getSetting('log.level') == "2":
        loglevel = 'off'
    if ADDON.getSetting('addon.log') == 'true':
        addonlog = 'true'
    if ADDON.getSetting('notify.action') == 'false': 
        notify = 'false'
    if ADDON.getSetting('stop.addon') == 'true':
        stopaddon()
    if ADDON.getSetting('restart.addon') == 'true':
        restartaddon()
    if ADDON.getSetting('monitor.default') == 'true':
        monitorfolder = FOLDER
    else:
        if ADDON.getSetting('monitor.custom') == 0:
            checkfolder = ADDON.getSetting('monitor.browselocal')
            checkfolderpath()
        elif ADDON.getSetting('monitor.custom') == 1:
            checkfolder = ADDON.getSetting('monitor.browse')
            checkfolderpath()
        elif ADDON.getSetting('monitor.custom') == 2:
            checkfolder = ADDON.getSetting('monitor.enter')
            checkfolderpath()
        else:
		    monitorfolder = FOLDER
    monitorfile = os.path.join(monitorfolder, "passarguments.txt")
    checkfrequency = ADDON.getSetting('check.frequency')      # check for file every n seconds - default = 10, max = 60
    checkfrequency = int(checkfrequency)
    message = ("checkfrequency is %d seconds"% checkfrequency)
    printlog()
    if checkfrequency > 60:
        checkfrequency = 60
    if checkfrequency < 25:
        freq = int(60/checkfrequency)
    else:
        freq = 1
    #testing
    printstar()
    message = ("idletime is now %d seconds"% checkfrequency)
    printlog()
    message = ("freq is %d"% freq)
    printlog()
    idletime = checkfrequency * 1000
    printstar()  
    if ADDON.getSetting('script.folder') == 'true': 
        scriptfolderset = 'true'
        if ADDON.getSetting('scriptfolder.default') == 'true': 
            scriptfolder = defaultscriptfolder
        else:
            if ADDON.getSetting('scriptfolder.method') == "0":
                scriptfolder = ADDON.getSetting('scriptfolder.browse')
            elif ADDON.getSetting('scriptfolder.method') == "1":
                scriptfolder = ADDON.getSetting('scriptfolder.enter')
        checkscriptfolderpath()
        
    if ADDON.getSetting('central.folder') == 'true': 
        centralfolderset = 'true'
        if ADDON.getSetting('central.default') == 'true': 
            centralfolder = defaultcentralfolder
        else:
            if ADDON.getSetting('central.method') == "0":
                centralfolder = ADDON.getSetting('central.browse')
            elif ADDON.getSetting('central.method') == "1":
                centralfolder = ADDON.getSetting('central.enter')
        centraldelay = ADDON.getSetting('central.delay')
        centralidletime = ADDON.getSetting('central.frequency')        # check for file every n seconds - min = idletime, default = 120, max = 3600 - express as multiple of idletime
        centralidletime = int(centralidletime)
        message = ("centralidletime is %d seconds"% centralidletime)
        printlog()        
        if centralidletime > 3600:
            centralidletime = 3600
        if centralidletime < checkfrequency:
            centralidletime = checkfrequency
        x = centralidletime/checkfrequency
        # round to nearest integer
        y = int(x)
        z = x - y
        if z > 0.5:
            centralfreq = y + 1
        else:
            centralfreq = y
        message = ("centralfreq is %d"% centralfreq)
        printlog()       
        if ADDON.getSetting('central.unavailable') == "0":
            nocentral = 'ignore'
        elif ADDON.getSetting('central.unavailable') == "1":
            nocentral = 'prompt'            
        checkcentralpath()    
    if ADDON.getSetting('clear.archives') == 'true':
        cleararchives()


    if ADDON.getSetting('archive.number') == 0:
        archivenumber = 0
    else:
        archivenumber = ADDON.getSetting('archive.enter')
    if ADDON.getSetting('archive.number') == 2:
        archiveall = 'true'
    else: archiveall = 'false'

    archivenumber = int(archivenumber)
  


  
    printsettings()    
        
def printsettings():
    global message
    if loglevel == 'debug':
        printstar()
        message = ""
        printlog()
        message = 'Settings:'
        printlog()
        message = ('loglevel = %s'% loglevel)
        printlog()
        message = ('addonlog = %s'% addonlog)
        printlog()
        message = ('notify = %s'% notify)
        printlog()
        message = ('monitorfolder = %s'% monitorfolder)
        printlog()
        message = ('monitorfile = %s'% monitorfile)
        printlog()
        message = ('idletime = %s'% idletime)
        printlog()
        if scriptfolderset == 'true':
            message = ('scriptfolder = %s'% scriptfolder)
        else:
            message = 'scriptfolder is not enabled'
        printlog()
        if centralfolderset == 'true':
            message = ('central folder = %s'% centralfolder)
            printlog()
            message = ('central idletime = %s'% centralidletime)
            printlog()
            message = ('central delay = %s'% centraldelay)
            printlog()
            message = ('nocentral = %s'% nocentral)
            printlog()
        else:
            message = 'central folder is not enabled'
            printlog()
        message = ('archivenumber is %d'% archivenumber)
        printlog()
        message = ('archiveall is %s'% archiveall)
        printlog()
        printstar()
    elif loglevel == 'normal':
        message = 'settings run - enable addon debug for more info'
        printlog()    

def gettimestamp():
    global message, notifythis, pause, seconds, secondstring
    try:
        seconds = time.time()       # seconds past epoch for timestamp
        seconds = int(seconds)      # > whole number
        secondstring = str(seconds)
    except:
        secondstring = '0000000000'    # if can't get time run all actions with no delays   
        message = 'Cannot get timestamp - setting to 000'
        printlog()
        
def runchecksanddostuff():
    global message, notifythis, pause, countcentral
    # deal with central check count
    if countcentral >= centralfreq:
        countcentral = 0
        checkcentralfolder()
    else:
        countcentral = countcentral + 1
        message = ('central count is now %d'% countcentral)
    if monitorfolder == workingfolder:
        checkworking()
    else:
        # list contents, move anything needed into working
        # looking for text documents not starting with 'aaa'
        dirs = []
        files = []
        interesting = []
        dirs, files = xbmcvfs.listdir(monitorfolder)
        num = len(files)
        message = ('Checking local folder: %s'% monitorfolder)
        printlog()
        c = 0
        while c < num:
            next = files[c]
            first = next[:3]
            if not first == 'aaa':
                ext = next[-3:]
                if ext == 'txt':
                    interesting.append(next)
            c = c + 1
        size = len(interesting)
        if size == 0:
            message = 'No files found in local folder'
        elif size == 1:
            message = ('There is one file in the local folder to move: %s'% interesting)    
        else:
            message = ('There are %d files in the local folder to move: %s'% (size, interesting))
        printlog()
        if size == 0:
            checkworking()
        else:
            # process files - add timestamp, add local to filename, move interesting files to working folder
            # timestamp
            gettimestamp()
            c = 0
            while c < size:
                name = interesting[c]
                source = os.path.join(monitorfolder, name)             # existing central file
                newname = secondstring + ".local." + name
                target = os.path.join(workingfolder, newname)
                message = ('Copying %s to %s'%(source, target))
                printlog()
                xbmcvfs.rename(source, target)
                xbmc.sleep(300)
                c = c + 1
            checkworking()

def checkworking():
    global message, notifythis, pause, activefile, activefilename
    # check if there are any files to process
    # look for text files not starting with 'aaa'
    dirs = []
    files = []
    todolist = []
    dirs, files = xbmcvfs.listdir(workingfolder)
    num = len(files)
    message = ('Checking working folder: %s'% workingfolder)
    printlog()
    c = 0
    while c < num:
        next = files[c]
        first = next[:3]
        if not first == 'aaa':
            ext = next[-3:]
            if ext == 'txt':
                todolist.append(next)
        c = c + 1
    size = len(todolist)
    if size == 0:
        message = 'No files to process in working folder'
        printlog()
        # make sure marker file is deleted
        if os.path.exists(filestocheck):
            os.remove(filestocheck)
        xbmc.sleep(idletime)
    else:
        message = ('%d files found in working folder: %s'% (size, todolist))
        printlog()
        # check how many files are to run now
        gettimestamp()
        c = 0
        while c < size:
            file = todolist[c]
            activefile = os.path.join(workingfolder, file)
            try:
                filetimestring = file[:10]
                filetime = int(filetimestring)
            except:                
                newname = secondstring + ".working." + file
                target = os.path.join(workingfolder, newname)
                message = ('Found unexpected file in working folder: %s'% activefile)
                printlog()
                message = ('Renaming %s to %s'%(activefile, target))
                printlog()
                xbmcvfs.rename(activefile, target)
                xbmc.sleep(300)            
                filetimestring = secondstring
                filetime = int(secondstring)
                file = newname
                activefile = target            
            if not filetime > seconds:          # ie no wait necessary
                # delete marker if it was a delayed file
                deletemarker = 'false'
                if 'local' in file:
                    deletemarker = 'true'
                elif 'nodelay' in file:
                    deletemarker = 'true'
                if deletemarker == 'true':
                    # make sure marker file is deleted
                    if os.path.exists(filestocheck):
                        os.remove(filestocheck)
                activefilename = file
                readfile()
            else:
                # stop, because all remaining files are to be delayed
                timeleft = filetime - seconds
                timeleftstring = str(timeleft)
                message = ('Next file to run is %s'% file)
                printlog()
                message = ('%s will run in approx %s seconds'% (file, timeleftstring))
                printlog()
                # if marker present read contents. Check timeleft is less than contents
                if os.path.exists(filestocheck):
                    with open(filestocheck, "r") as myfile:
                        output = myfile.read()
                        output = output.strip()
                        oldtimeleft = int(output)
                    if timeleft < oldtimeleft:           # ie countdown to process file is not working
                        message = ('Problem processing %s'% activefile)
                        printlog()
                        message = ('countdown problem.  Old timeleft is %s, new timeleft is %s'% (oldtimeleft, timeleft))
                        notifythis = ("%s, countdown problem - check log"% AddonName)
                        notifystuff()
                # make new marker file.  Write time left to it.
                with open(filestocheck, "w") as myfile:
                    myfile.write(timeleftstring)
            c = c + 1

    
    
def readfile():
    global message, notifythis, pause, first, second, third, fourth, fifth, sixth
    # set defaults
    first = 'not set'
    second = 'not set'
    third = 'not set'
    fourth = 'not set'
    fifth = 'not set'
    sixth = 'not set'            
    if os.path.exists(activefile):
        if loglevel == 'debug':
            message = ("%s: File found - %s"% (ADDON_ID, activefile))
            printlog()
        with open (activefile,"r") as myfile:
            data=myfile.readlines()
            try:
                first = data[0].strip()
                try:
                    second = data[1].strip()
                    try:            
                        third = data[2].strip()
                        try:            
                            fourth = data[3].strip()
                            try:            
                                fifth = data[4].strip()
                                try:            
                                    sixth = data[5].strip()
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
            if loglevel == 'debug':
                printstar()
                xbmc.log("first line is %s"% first, 2)
                printlog()
                xbmc.log("second line is %s"% second, 2)
                printlog()
                xbmc.log("third line is %s"% third, 2)
                printlog()
                if not third == 'not set':
                    xbmc.log("fourth line is %s"% fourth, 2)
                    printlog()
                    if not fourth == 'not set':
                        xbmc.log("fifth line is %s"% fifth, 2)
                        printlog()
                        if not fifth == 'not set':
                            xbmc.log("sixth line is %s"% sixth, 2)
                            printlog()                          
            notifythis = ("%s, processing file"% AddonName)
            pause = 'true'
            notifystuff()
        if archivenumber > 0:
            archiveactive()
        else:
            cleanactive()
        if not first == 'not set':
            process()
    else:
        xbmc.sleep(idletime)

def cleanactive():
    global message, notifythis
    try:
        xbmcvfs.delete(activefile)
        message = ('Deleted active file: %s'% activefilename)
        printlog()
    except:
        message = ('Problem deleting %s'% activefilename)
        printlog()
        message = ('Failed to delete %s'% activefilename)
        printlog()
        notifythis = ("%s, problem - check log"% AddonName)
        notifystuff()
    checkarchivesize()
    
def archiveactive():
    global message, notifythis
    source = activefile
    target = os.path.join(archive, activefilename)
    try:
        xbmcvfs.rename(source, target)
        message = ('Archived active file: %s'% activefilename)
        printlog()
    except:
        message = ('Problem archiving %s'% activefilename)
        printlog()
        message = ('Failed to move - source: %s, target: %s'% (source, target))
        printlog()
        notifythis = ("%s, archive problem - check log"% AddonName)
        notifystuff()
    checkarchivesize()
    
def checkarchivesize():
    global message, notifythis
    # check archive size
    if archiveall == 'false':
        arch = []
        arch = os.listdir(archive)
        size = len(arch)
        if size > archivenumber:
            num = size - archivenumber
            c = 0
            message = ('Cleaning archive to leave %d files'% archivenumber)
            printlog()
            while c < num:
                oldfile = arch[c]
                oldfilepath = os.path.join(archive, oldfile)
                try:
                    xbmcvfs.delete(oldfilepath)
                    message = ('Deleted file from archive: %s'% oldfile)
                    printlog()
                except:
                    message = ('Problem deleting %s'% oldfile)
                    printlog()
                    notifythis = ("%s, problem - check log"% AddonName)
                    notifystuff()
                c = c + 1
                

def process():
    global message, checkfolder, myscriptpath, myscript, myargs, notifythis
    if first == 'central':
        checkcentralfolder()
    elif first == 'command':
        mycommand = second
        xbmc.executebuiltin("%s"% mycommand)
    # run script by just giving name - if it's an installed script or in the scripts folder
    elif first == 'script':
        myscript = second
        if not third == 'not set':
            myargs = third
        else:
            myargs = ""
        if xbmc.getCondVisibility('System.HasAddon(%s)'% myscript):
            xbmc.executebuiltin("RunScript(%s,%s)"% (myscript, myargs))
        else:
            # look for a script in the scripts folder
            checkfolder = scriptfolder
            findscript()
            # if script not found and recursive check enabled look deeper in scripts folder
            if myscriptpath == 'not set':
                if recursivecheck == 'true':
                    findfolders()
            # run script if found
            if not myscriptpath == 'not set':
                xbmc.executebuiltin("RunScript(%s,%s)"% (myscriptpath, myargs))
            # or log error
            else:
                if loglevel == 'debug':
                    printstar()
                message = ("script not found: %s"% myscript)
                printlog()
                if loglevel == 'debug':
                    printstar()
                notifythis = ("script not found, %s"% myscript)
                notifystuff()
    elif 'json' in first:
        setdialog = 'false'
        if 'dialog' in first:
            setdialog = 'true'
        start = ""
        finish = ""
        json_command = ""
        try:
            json_command = second
        except:
            pass
        if 'start' in third:
            try:
                start = fourth
            except:
                pass
            if 'finish' or 'stop' in fifth:
                try:
                    finish = sixth
                except:
                    pass
        if json_command == "":
            message = 'No json_command read'
            printlog()
        else:
            json_query = 'no response'
            try:
                json_query = xbmc.executeJSONRPC(json_command)
                try:
                    json_query = unicode(json_query, 'utf-8', errors='ignore')
                except:
                    pass
                message = "json_query is:"
                printlog()
                message = json_query
                printlog()
                # typical response is eg >> json_query is {"id":1,"jsonrpc":"2.0","result":{"name":"Kodi","version":{"major":17,"minor":4,"revision":"20170717-b22184d","tag":"releasecandidate","tagversion":"1"}}}
                # so apply eg start = 'major":'
                # and finish = ',"minor'
                # to get easily readable result
                if not start == "":
                    result = ""
                    try:
                        result = (json_query.split(start))[1].split(finish)[0]
                        result = str(result)
                        message = ('Result of json command is %s'% result)
                        printlog()
                        if setdialog == 'true':
                            xbmcgui.Dialog().ok("json result:", result)
                    except:
                        message = 'Could not process json result'
                        printlog()                        
            except:
                message = 'Script was not able to process the json command'
            printlog()

def renamefile():
    global message, notifythis, newfile
    newfile = 'not set'
    # rename text file - check if number at end, if so add 1 and check again
    filename = usedname[:-3]  # dropped 'txt'
    
    message = 'running renamefile()'
    printlog()
    message = ('old name is %s'% usedname)
    printlog()
    message = ('cleaned name - less txt - is %s'% filename)
    printlog()
    message = ('new file is %s'% newfile)
    printlog
    message = 'Trying new file names:'
    # add a 1 to the end of the string, check if exists, if it does add 2 etc
    c = 1
    while c < 10:
        d = str(c)
        message = ('c = %s'% d)
        printlog()
        checkname = filename + d + ".txt"
        message = ('checkname is %s'% checkname)
        printlog()
        if not xbmcvfs.exists(checkname):
            newfile = checkname
            message = ('%s does not exist already'% checkname)
            printlog()
            message = ('newfile is now %s'% checkname)
            printlog()
            c = 10
        else:
            message = ('%s exists already so try next'% checkname)
            c = c + 1
    message = 'Finished renamefile()'
    printlog()
    message = ('New file name is %s'% newfile)
    printlog()
    if newfile == 'not set':
        message = ('Could not find new name for %s'% checkname)
        printlog()
        xbmc.sleep(1000)
        notifythis = ('Problem with central folder, check log')
        notifystuff()    
    message = 'returning to checkcentralfolder()'
    printlog()
    
def checkcentralfolder():
    global message, centralfile, usedname
    # check folder for text files
    # ignore anything starting with 'aaa'
    # list all relevant text files, check if they have already been processed
    # list files to process
    # extract any files with bbbbb in filename to run first
    # process them in alphabetical order  
    dirs = []
    files = []
    textfiles = []
    dirs, files = xbmcvfs.listdir(centralfolder)
    num = len(files)
    message = ('There are %d files in the central folder: %s'% (num, files))
    printlog()
    c = 0
    checkhost = "." + host + "."
    while c < num:
        next = files[c]
        first = next[:3]
        if not first == 'aaa':
            ext = next[-3:]
            if ext == 'txt':
                if checkhost not in next:            
                    if 'nodelay' in next:
                        if next not in textfiles:
                            textfiles.append(next)
        c = c + 1
    c = 0
    while c < num:
        next = files[c]
        first = next[:3]
        if not first == 'aaa':
            ext = next[-3:]
            if ext == 'txt':
                if checkhost not in next:
                    if next not in textfiles:
                        textfiles.append(next)
        c = c + 1
    
    textnum = len(textfiles)
    message = ('There are %d files in the central folder to process: %s'% (textnum, textfiles))
    printlog()

    # process files - copy to local working folder, add host to filename, add timestamp
    # timestamp
    gettimestamp()
    c = 0
    while c < textnum:
        name = textfiles[c]
        centralfile = os.path.join(centralfolder, name)             # existing central file
        if 'nodelay' in name:
            newlocalname = secondstring + ".central." + name            # rename in local folder with timestamp
        else:
            secondsplusdelay = seconds + centraldelay
            secondsplusdelaystring = str(secondsplusdelay)              
            newlocalname = secondsplusdelaystring + ".central." + name  # rename in local folder with delayed runtime        
        localfile = os.path.join(workingfolder, newlocalname)
        namelesstxt = name[:-3]
        newcentralname = namelesstxt + host + '.txt'                # rename in central folder
        newcentralfile = os.path.join(centralfolder, newcentralname)
        # check newcentralfile doesn't already exist.
        if xbmcvfs.exists(newcentralfile):
            usedname = newcentralfile
            renamefile()
            newcentralfile = newfile
        message = ('File to process is %s'% name)
        printlog()
        if not newcentralfile == 'not set':
            message = ('Copying %s to %s'%(centralfile, localfile))
            printlog()
            xbmcvfs.copy(centralfile, localfile)
            xbmc.sleep(300)
            message = ('Renaming %s to %s'%(centralfile, newcentralfile))
            printlog()
            xbmcvfs.rename(centralfile, newcentralfile)
            xbmc.sleep(300)
        c = c + 1


def findscript():
    global myscriptpath
    myscriptpath = 'not set'
    checklist = []
    checklist = os.listdir(checkfolder)
    k = len(checklist)
    c = 0
    while c < k:
        test = checklist[c]
        if myscript == test:
            testpath = os.path.join(checkfolder, test)
            if os.path.isfile(testpath):
                myscriptpath = testpath
                c = k
        c = c + 1

def findfolders():
    global checkfolder, myscriptpath
    check = []
    check = os.listdir(scriptfolder)
    p = len(check)
    c = 0
    while c < p:
        next = check[c]
        nextpath = os.path.join(scriptfolder, next)
        if not os.path.isfile(nextpath):
            checkfolder = nextpath
            findscript()
        if not myscriptpath == 'not set':
            c = p
        c = c + 1
                                   
# test delay start by  10 seconds
xbmc.sleep(10000)
if ADDON.getSetting('notify.action') == 'true': 
    xbmc.executebuiltin('Notification(%s, started)'% AddonName)
monsettings = SettingMonitor()
getsettings()

while(not xbmc.abortRequested):
    xbmc.sleep(100)
    runchecksanddostuff()