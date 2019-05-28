#!/usr/bin/python
# -*- coding: utf-8 -*-
# need to add to startup of specified addon:
                                            # if ADDON.getSetting('stop.addon') == 'true':
                                                # ADDON.setSetting('stop.addon', 'false')
    
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import sys

xbmc.sleep(300)
thisscript = sys.argv[0]
WIN = xbmcgui.Window(10000)

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
    xbmc.log("%s: asked to stop non-running or non-existent addon (%s)."% (thisscript, ADDON_ID), 2)
    xbmc.executebuiltin('Notification(Problem script %s, check log for details)'% thisscript)
    exit()

def checkrunning():
    global message, running
    activeaddons = xbmcvfs.listdir('addons://running/')[1]
    xbmc.log('Active addons are: %s'% activeaddons, 2)
    if ADDON_ID in activeaddons:
        xbmc.log('%s is running'% ADDON_ID, 2)
        running = 'true'
    else:
        xbmc.log('%s is not running'% ADDON_ID, 2)
        running = 'false'

    
#stop addon
xbmc.executebuiltin("StopScript(%s)"% ADDON_ID)
xbmc.sleep(1000)
checkrunning()
if running == 'false':
        xbmc.log('%s was stopped.'% ADDON_ID, 2)
        xbmc.executebuiltin('Notification(%s, stopped)'% ADDON_ID)
        WIN.setProperty('%s.running'% ADDON_ID, 'stopped')
else:
    xbmc.log('%s was not successfully stopped.  Trying again.'% ADDON_ID, 2)
    xbmc.executebuiltin("StopScript(%s)"% ADDON_ID)
    xbmc.executebuiltin('Notification(%s, trying to stop)'% ADDON_ID)
    xbmc.sleep(3000)
    checkrunning()
    if running == 'false':
        WIN.setProperty('%s.running'% ADDON_ID, 'stopped')
        xbmc.log("%s: addon (%s)successfully stopped"% (thisscript, ADDON_ID), 2)
        # Notification needs to be sent twice or it's truncated - no idea why????????????
        xbmc.executebuiltin('Notification(%s, stopped)'% ADDON_ID)
        xbmc.sleep(1000)
        xbmc.executebuiltin('Notification(%s, stopped)'% ADDON_ID)
    else:
        xbmc.log('%s: Unable to stop %s'% (thisscript, ADDON_ID), 2)
        xbmc.executebuiltin('Notification(%s, Failed to stop)'% ADDON_ID)

exit()
