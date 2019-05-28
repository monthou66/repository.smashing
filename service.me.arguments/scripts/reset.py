#!/usr/bin/python
# -*- coding: utf-8 -*-

# check addon is valid
# disable addon
# delete addon data folder
# re-enable addon

# argument1 = addon id
    
import xbmc
import xbmcaddon
import xbmcgui
import sys
import os
import shutil

def stopscript():
    xbmc.log("%s:   Action cancelled by user"% thisscript, 2)
    xbmc.log("%s:   Stopping script"% thisscript, 2)
    xbmc.executebuiltin('Notification(Action, cancelled)')
    exit()
    
def checkdata():
    if os.path.isdir(DATA):
        xbmc.log("%s:   Data folder set to %s"% (thisscript, DATA), 2)
    else:
        xbmc.log("%s:   Addon data folder not found at %s"% (thisscript, TEST), 2)
        xbmc.log("%s:   Stopping script"% thisscript, 2)
        xbmc.executebuiltin('Notification(Problem script %s, check log for details)'% thisscript)
        exit()

def confirmdelete():
    header = ('Delete all data: %s'% ADDON_ID)
	# confirm delete
    yesnowindow = xbmcgui.Dialog().yesno(header, 'Click yes to delete', 'Click no to cancel action')
    if not yesnowindow:
        stopscript()
    xbmcgui.Dialog().ok(header, 'Press ok to delete now')           # last chance to cancel
    xbmc.log("%s:   Delete confirmed"% thisscript, 2)        
        
def delete():
    xbmc.log("%s:   running delete function"% thisscript, 2)
    try:
        shutil.rmtree(DATA)
        xbmc.log("%s: removed data folder - %s"% (thisscript, DATA), 2)
        xbmc.sleep(300)
    except:
        xbmc.log("%s: Failed to remove data folder - %s"% (thisscript, DATA), 2)
        xbmc.executebuiltin('Notification(problem, check log)')

def disable():    
    xbmc.log("%s:   running disable function"% thisscript, 2)
    #disable addon
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% ADDON_ID) 
    xbmc.sleep(300)
    # check addon is stopped:
    if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
        xbmc.log("%s: failed to stop addon (%s).  Trying again."% (thisscript, ADDON_ID), 2)
        xbmc.sleep(1000)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% ADDON_ID)
        if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
            xbmc.log("%s: failed to stop addon (%s)."% (thisscript, ADDON_ID), 2)
            xbmc.executebuiltin('Notification(Problem stopping %s, check log for details)'% ADDON_ID)
            exit()
        else:
            xbmc.log("%s: addon (%s)successfully stopped"% (thisscript, ADDON_ID), 2)

def enable():    
    xbmc.log("%s:   running enable function"% thisscript, 2)
    # restart addon
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% ADDON_ID)
    xbmc.sleep(2000)
    # check addon is started
    if not xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% ADDON_ID)
        xbmc.sleep(2000)
        if not xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
            xbmc.log("%s: addon could not be re-enabled (%s)."% (thisscript, ADDON_ID), 2)
            xbmc.executebuiltin('Notification(Problem re-enabling %s, check log for details)'% ADDON_ID)
            exit()
    xbmc.log("%s: addon has been restarted (%s)."% (thisscript, ADDON_ID), 2)
    # Notification needs to be sent twice or it's truncated - no idea why????????????
    xbmc.executebuiltin('Notification(%s, restarted)'% ADDON_ID)
    xbmc.sleep(1000)
    xbmc.executebuiltin('Notification(%s, restarted)'% ADDON_ID)
    xbmc.sleep(3000)
    exit()

    

xbmc.sleep(300)
thisscript = sys.argv[0]
xbmc.log("Running %s"% thisscript, 2) 
# makes sure specified addon is valid and running:
try:
    ADDON_ID = sys.argv[1]
except:
    ADDON_ID = 'not found'
    xbmc.log("Running %s"% thisscript, 2)
    xbmc.log("ADDON_ID is %s"% ADDON_ID, 2)
    xbmc.executebuiltin('Notification(problem, check log)')
    exit()
if not xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
    xbmc.log("%s: asked to restart non-running or non-existent addon (%s)."% (thisscript, ADDON_ID), 2)
    xbmc.executebuiltin('Notification(Problem script %s, check log for details)'% thisscript)
    exit()

# check for addon data folder
USERDATA = xbmc.translatePath('special://masterprofile')
DATA = os.path.join(USERDATA, "addon_data", ADDON_ID)
checkdata()
confirmdelete()
disable()
delete()
enable()
