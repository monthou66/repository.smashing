#!/usr/bin/python
# -*- coding: utf-8 -*-

# use to restart service if stopped / stop if running
#############################################################################################################################################
#############################################################################################################################################
## 
## This is a generic default.py that can be inserted into any service script.
## To work properly the service needs to use the following settings:
## log.level
## addon.log
## notify.action
## if these are not present the script falls back to default values
##
## This script will stop / start a service and log its actions
##
#############################################################################################################################################
#############################################################################################################################################
import xbmc
import xbmcgui
import xbmcaddon
import os
import xbmcvfs
from time import gmtime, strftime

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_DIR = xbmc.translatePath(ADDON.getAddonInfo('path'))
AddonName = ADDON.getAddonInfo('name')
FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
if  not os.path.isdir(FOLDER):
    os.mkdir(FOLDER)
addonlogfile = os.path.join(FOLDER, "addon.log")
WIN = xbmcgui.Window(10000)
# set defaults
loglevel = 'debug'
addonlog = 'false'
notify = 'true'
service = 'stopped'
running = 'false'
disabled = 'false'
restarted = 'false'
logfile = []
fallback = 'script.me.stopstart'

def getsettings():
    global loglevel, addonlog, notify, message
    try:
        if ADDON.getSetting('addon.log') == 'true':
            addonlog = 'true'
        else:
            addonlog = 'false'
    except:
        message = 'No addonlog setting found.  Default will be used'
        addtolog()  
    message = ""            # leaves a blank line in addonlog if enabled
    addtolog()    
    message = ('%s: running default.py'% ADDON_ID)
    addtolog()
    try:
        if ADDON.getSetting('log.level') == "0":
            loglevel = 'debug'
        elif ADDON.getSetting('log.level') == "1":
            loglevel = 'normal'
        elif ADDON.getSetting('log.level') == "2":
            loglevel = 'off'
    except:
        message = 'No loglevel setting found.  Default will be used'
        addtolog()
    message = ('loglevel is %s'% loglevel)
    addtolog()
    message = ('addonlog setting is %s'% addonlog)
    addtolog()
    try:
        if ADDON.getSetting('notify.action') == 'false': 
            notify = 'false'
        else:
            notify = 'true'
    except:
        message = 'No notification level setting found.  Default will be used'
        addtolog()
    message = ('notify is set to %s'% notify)
    addtolog()
        
def checkrunning():
    global message, running
    activeaddons = xbmcvfs.listdir('addons://running/')[1]
    message = ('Active addons are: %s'% activeaddons)
    addtolog()
    if ADDON_ID in activeaddons:
        message = ('%s is running'% ADDON_ID)
        running = 'true'
    else:
        message = ('%s is not running'% ADDON_ID)
        running = 'false'
    addtolog()


def restartaddon():
    global message
    message = 'restarting addon'
    addtolog()
    if notify == 'true':
        xbmc.executebuiltin('Notification(%s, restarting)'% ADDON_ID)
        xbmc.sleep(300)
    #stop addon
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% ADDON_ID) 
    xbmc.sleep(300)
    # check addon is stopped:
    if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
        message = ('%s was not successfully disabled.  Trying again'% ADDON_ID)
        addtolog()
        xbmc.executebuiltin('Notification(%s, trying to disable)'% ADDON_ID)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% ADDON_ID)
        xbmc.sleep(3000)
        if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
            message = ('%s could not be disabled.  Script stopping'% ADDON_ID)
            addtolog()
            xbmc.executebuiltin('Notification(%s, Failed to stop)'% ADDON_ID)
        else:
            disabled = 'true'
    else:
        disabled = 'true'
    if disabled == 'true':
        restarted = 'false'
        message = ('%s disabled via json'% ADDON_ID)
        addtolog()
        #start addon
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% ADDON_ID)
        xbmc.sleep(300)
        if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
            restarted = 'true'
        else:
            xbmc.sleep(1000)
            if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
                restarted = 'true'
        if restarted == 'true':
            message = ('%s successfully started'% ADDON_ID)
            addtolog()
            xbmc.executebuiltin('Notification(%s, started)'% ADDON_ID)
        else:
            message = ('%s could not be started'% ADDON_ID) 
            addtolog()
            xbmc.executebuiltin('Notification(%s disabled, check log)'% ADDON_ID)
            
def stopaddon():
    global message
    message = 'stopping addon'
    addtolog()
    if notify == 'true':
        xbmc.executebuiltin('Notification(%s, stopping)'% ADDON_ID)
        xbmc.sleep(300)  
    #stop addon
    xbmc.executebuiltin("StopScript(%s)"% ADDON_ID)
    xbmc.sleep(1000)
    checkrunning()
    if running == 'false':
        message = ('%s was stopped.'% ADDON_ID)
        addtolog()
        xbmc.executebuiltin('Notification(%s, stopped)'% ADDON_ID)
        WIN.setProperty('%s.running'% ADDON_ID, 'stopped')
    else:
        message = ('%s was not successfully stopped.  Trying again.'% ADDON_ID)
        addtolog()
        xbmc.executebuiltin("StopScript(%s)"% ADDON_ID)
        xbmc.executebuiltin('Notification(%s, trying to stop)'% ADDON_ID)
        xbmc.sleep(3000)
        checkrunning()
        if running == 'false':
            message = ('%s was stopped.'% ADDON_ID)
            addtolog()
            # Notification needs to be sent twice or it's truncated - no idea why????????????
            xbmc.executebuiltin('Notification(%s, stopped)'% ADDON_ID)
            xbmc.sleep(1000)
            xbmc.executebuiltin('Notification(%s, stopped)'% ADDON_ID)
            WIN.setProperty('%s.running'% ADDON_ID, 'stopped')
        else:
            message = ('Unable to stop %s'% ADDON_ID)
            addtolog()
            xbmc.executebuiltin('Notification(%s, Failed to stop)'% ADDON_ID)
            
def forgetaboutit():
    global message
    message = 'Action cancelled by user'
    addtolog()
    if notify == 'true':
        xbmc.executebuiltin('Notification(No action taken, closing)')
        
def printstar():
    xbmc.log("%s ***********************************************************************************"% ADDON_ID, 2)
    xbmc.log("%s ************************************************************************************"% ADDON_ID, 2)
    
def addtolog():
    global message, logfile
    logfile.append(message)
    if addonlog == 'true':
        printaddonlog()
    message = ""

def printlog():
    if loglevel == 'debug':
        printstar()
    if not loglevel == 'off':
        length = len(logfile)
        c = 0
        while c < length:
            line = logfile[c]
            xbmc.log("%s: default.py:   %s"% (ADDON_ID, line), 2)
            c = c + 1        
    if loglevel == 'debug':
        printstar()
    
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
        nextline = ('\n%s    %sdefault.py:    %s'%(dateandtime, ADDON_ID, message))
    else:
        nextline = ('\n')
    with open(addonlogfile, "a") as myfile:
        myfile.write(nextline)    
    
getsettings()
checkrunning()
    
if running == 'true':
    statone = ('%s is running'% AddonName)
    stattwo = 'Would you like to stop it?'
    yesnowindow = xbmcgui.Dialog().yesno(statone, stattwo)
    if yesnowindow:
        stopaddon()
    else:
        forgetaboutit()
else:
    statone = ('%s is stopped'% AddonName)
    stattwo = 'Would you like to restart it?'
    yesnowindow = xbmcgui.Dialog().yesno(statone, stattwo)
    if yesnowindow:
        restartaddon()
    else:
        forgetaboutit()
printlog()

exit()   

