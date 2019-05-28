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
message = ""
if ADDON.getSetting('restart.addon') == 'true':
    ADDON.setSetting('restart.addon', 'false')
if ADDON.getSetting('stop.addon') == 'true':
    ADDON.setSetting('stop.addon', 'false')
if ADDON.getSetting('clear.addonlogs') == 'true':
    ADDON.setSetting('clear.addonlogs', 'false')
monitorfile = os.path.join(FOLDER, "passarguments.txt")
notifythis = ""
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
    global notifythis, message
    if notify == 'true':
        if not notifythis == "":
            xbmc.executebuiltin('Notification(%s)'% notifythis)
            # send notifiucation to log?
            message = ('Notification sent: %s'% notifythis)
            printlog()
    notifythis = ""

def stopaddon():
    global message
    if loglevel == 'debug':
        printstar()
    if not loglevel == 'none':
        message = 'stopping addon'
        printlog()
    if loglevel == 'debug':
        printstar()
    if notify == 'true':
        xbmc.executebuiltin('Notification(%s, stopping)'% ADDON_ID)
        xbmc.sleep(1000)
    target = os.path.join(ADDON_DIR, "scripts", "stop.py")
    if loglevel == 'debug':
        message = ("target script is %s"% target)
        printlog()
        printstar()
    xbmc.executebuiltin('RunScript(%s, %s)'% (target, ADDON_ID))   
    # service is disabled via json in target script

def restartaddon():
    global message
    if loglevel == 'debug':
        printstar()
    if not loglevel == 'none':
        message = 'restarting addon'
        printlog()
    if notify == 'true':
        xbmc.executebuiltin('Notification(%s, restarting)'% ADDON_ID)
        xbmc.sleep(1000)
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
        monitorfile = os.path.join(nonitorfolder, "passarguments.txt")
    else:
	    redofoldersettings()
		
def redofoldersettings():
    # dialog to say folder invalid / go back to settings
    yesnowindow = xbmcgui.Dialog().yesno('Arguments script: Invalid monitor folder', 'Click yes to set again', 'Click no to disable for this session')
    if yesnowindow:
		# xbmcaddon.Addon().openSettings()
		ADDON.openSettings()
    else:
        if loglevel == 'debug':
            printstar()
        if not loglevel == 'none':
            message = ("Invalid folder specified: %s"% checkfolder)
            printlog()
            stopaddon()

def clearlogs():
    global message
    if os.path.exists(addonlogfile):
        os.remove(addonlogfile)
        xbmc.sleep(300)
        if os.path.exists(addonlogfile):
            message = 'Failed to delete logfile'
            xbmc.executebuiltin('Notification(Problem, addon logs not cleared)')
        else:
            message = 'Addon logs cleared'
            xbmc.executebuiltin('Notification(Addon logs, cleared)')
        printlog()
    else:
        message = 'No addon logs found'
        xbmc.executebuiltin('Notification(Addon log, not found)')
    ADDON.setSetting('clear.addonlogs', 'false')
        
        
            
def getsettings():
    global checkfolder, monitorfolder, monitorfile, idletime, freq, loglevel, addonlog, notify
    # set defaults
    monitorfolder = FOLDER
    notify = 'true'
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
    if not ADDON.getSetting('monitor.default') == 'true':
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
        printstar()
    elif loglevel == 'normal':
        message = 'settings run - enable addon debug for more info'
        printlog()    

def checkfile():
    global message, first, second, third
    # set defaults
    first = 'not set'
    second = 'not set'
    third = 'not set'
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
                    except:
                        pass
                except:
                    pass
            except:
                pass
            if loglevel == 'debug':
                xbmc.log("first line is %s"% first, 2)
                printlog()
                xbmc.log("second line is %s"% second, 2)
                printlog()
                xbmc.log("third line is %s"% third, 2)
                printlog()
            if notify == 'true':
                xbmc.executebuiltin('Notification(%s, processing file)'% AddonName)
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