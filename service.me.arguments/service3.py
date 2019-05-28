#!/usr/bin/python
# -*- coding: utf-8 -*-
# triggered when text file is created
import os
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
from time import gmtime, strftime

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
AddonName = ADDON.getAddonInfo('name')
FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
if  not os.path.isdir(FOLDER):
    os.mkdir(FOLDER)
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
    
defaultscriptfolder = xbmc.translatePath('special://masterprofile/scripts')
scriptfolder = 'not set'
monitorfile = os.path.join(FOLDER, "passarguments.txt")
message = ""
scriptfolderset = 'false'

notifythis = ""
pause = 'false'
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
    global message
    xbmc.log("%s:    %s"% (ADDON_ID, message), 2)
    if addonlog == 'true':
        printaddonlog()
    message = ""

def printaddonlog():
    try:
        dateandtime = strftime("%Y-%m-%d     %H:%M:%S", gmtime())
    except:
        dateandtime = 'Date and time not known'
    if not os.path.exists(addonlogfile):
        with open(addonlogfile, "a") as myfile:
            header = ('%s    LOGFILE\n'% ADDON_ID)
            myfile.write(header)
    if not message == "":
        nextline = ('\n%s    %s'%(dateandtime, message))
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
    global scriptfolder, message
    if not xbmcvfs.exists(scriptfolder):
        message = ("Invalid scriptfolder specified: %s"% checkfolder)
        printlog()
        # dialog to say folder invalid / go back to settings
        yesnowindow = xbmcgui.Dialog().yesno('Arguments script: Invalid script folder', 'Click yes to set again', 'Click no to disable for this session')
        if yesnowindow:
		    # xbmcaddon.Addon().openSettings()
		    ADDON.openSettings()
        else:
            message = 'Service stopped for this session by user after invalid script folder selection'
            printlog()
            stopaddon()        
            
def clearlogs():
    global message, notifythis
    if os.path.exists(addonlogfile):
        os.remove(addonlogfile)
        xbmc.sleep(300)
        if os.path.exists(addonlogfile):
            message = 'Failed to delete logfile'
            notifythis = ("Problem, addon logs not cleared")
        else:
            message = 'Addon logs cleared'
            notifythis = ("Addon logs, cleared")
        printlog()
    else:
        message = 'No addon logs found'
        notifythis = ("Addon log, not found")
    notifystuff()
    ADDON.setSetting('clear.addonlogs', 'false')
        
        
            
def getsettings():
    global checkfolder, monitorfolder, monitorfile, idletime, freq, loglevel, addonlog, notify, scriptfolderset, scriptfolder
    # set defaults
    monitorfolder = FOLDER
    notify = 'true'
    scriptfolderset = 'false'
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
		    redofoldersettings()
    monitorfile = os.path.join(monitorfolder, "passarguments.txt")
    idletime = ADDON.getSetting('check.frequency')      # check for file every n seconds - default = 10, max = 60
    idletime = int(idletime)
    xbmc.log("idletime is %d seconds"% idletime, 2)
    if idletime > 60:
        idletime = 60
    if idletime < 25:
        freq = int(60/idletime)
    else:
        freq = 1
    #testing
    printstar()
    xbmc.log("idletime is now %d seconds"% idletime, 2)
    xbmc.log("freq is %d"% freq, 2)
    idletime = idletime * 1000
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
        printstar()
    elif loglevel == 'normal':
        message = 'settings run - enable addon debug for more info'
        printlog()    

def checkfile():
    global message, notifythis, pause, first, second, third, fourth, fifth, sixth
    # set defaults
    first = 'not set'
    second = 'not set'
    third = 'not set'
    fourth = 'not set'
    fifth = 'not set'
    sixth = 'not set'
    if os.path.exists(monitorfile):
        if loglevel == 'debug':
            message = ("%s: File found - %s"% (ADDON_ID, monitorfile))
            printlog()
        with open (monitorfile,"r") as myfile:
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
        cleanup()
        if not first == 'not set':
            process()
    else:
        xbmc.sleep(idletime)
      
def cleanup():
    xbmcvfs.delete(monitorfile)

def process():
    global message, checkfolder, myscriptpath, myscript, myargs, notifythis
    if first == 'command':
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
xbmc.executebuiltin('Notification(%s, started)'% AddonName)
monsettings = SettingMonitor()
getsettings()

while(not xbmc.abortRequested):
    xbmc.sleep(100)
    checkfile()