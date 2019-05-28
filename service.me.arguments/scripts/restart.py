#!/usr/bin/python
# -*- coding: utf-8 -*-
# need to add to startup of specified addon:
                                            # if ADDON.getSetting('restart.addon') == 'true':
                                                # ADDON.setSetting('restart.addon', 'false')
    
import xbmc
import xbmcaddon
import sys

xbmc.sleep(300)
thisscript = sys.argv[0]

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
        
# restart addon
xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% ADDON_ID)
xbmc.sleep(1000)

# check addon is started
if not xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% ADDON_ID)
    xbmc.sleep(1000)
    if not xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON_ID):
        xbmc.log("%s: addon could not be re-enabled (%s)."% (thisscript, ADDON_ID), 2)
        xbmc.executebuiltin('Notification(Problem re-enabling %s, check log for details)'% ADDON_ID)
        exit()
xbmc.log("%s: addon has been restarted (%s)."% (thisscript, ADDON_ID), 2)
# Notification needs to be sent twice or it's truncated - no idea why????????????
xbmc.executebuiltin('Notification(%s, restarted)'% ADDON_ID)
xbmc.sleep(3000)
xbmc.executebuiltin('Notification(%s, restarted)'% ADDON_ID)
exit()