# -*- coding: utf-8 -*-
# exit kodi
import xbmc
import xbmcaddon
import xbmcgui
import os
import shutil

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_DIR = xbmc.translatePath(ADDON.getAddonInfo('path'))
defaultoptionsfolder = os.path.join(ADDON_DIR, "resources", "default_options")
localoptionsfolder = xbmc.translatePath(ADDON.getAddonInfo('profile'))
USERDATA = xbmc.translatePath('special://masterprofile')
# advsetts = os.path.join(USERDATA, "advancedsettings")
output = os.path.join(USERDATA, "advancedsettings.xml")
# previous = os.path.join(advsetts, "previousadvancedsettings.xml")
previous = os.path.join(localoptionsfolder, "previousadvancedsettings.xml")

def nofilesfound():
    xbmc.log("%s: no .xml files found in %s or %s"% (ADDON_ID, defaultoptionsfolder, localoptionsfolder), 2)
    xbmc.executebuiltin('Notification(No files found, check log)')
    exit()

def cancel():
    xbmc.log("%s: script cancelled"% ADDON_ID, 2)
    xbmc.executebuiltin('Notification(Action, cancelled)')
    exit()

def checkprevious():
    if os.path.exists(previous):
        try:
            os.remove(previous)
            xbmc.log("%s: File deleted - %s"% (ADDON_ID, previous), 2)
            xbmc.sleep(300)
        except:
            xbmc.log("%s: problem deleting file - %s"% (ADDON_ID, previous), 2)
            xbmc.executebuiltin('Notification(Problem, check log)')
            exit()

def archive():
    # move advancedsettings.xml out
    try:
        os.rename(output, previous)
        xbmc.log("%s: Moved %s to %s"% (ADDON_ID, output, previous), 2)
        xbmc.sleep(300)
    except:
        xbmc.log("%s: Problem.  Failed to move %s to %s"% (ADDON_ID, output, previous), 2)
        xbmc.executebuiltin('Notification(Problem, check log)')
        exit()
                
xbmc.log("%s: starting"% ADDON_ID, 2)

xbmc.log("%s: localoptionsfolder is: %s"% (ADDON_ID, localoptionsfolder), 2)

if not os.path.isdir(localoptionsfolder):
    os.mkdir(localoptionsfolder)
# check for files 
allfiles = []
xmlfiles = []
defaultfiles = []
localfiles = []
defaultfiles = os.listdir(defaultoptionsfolder)
localfiles = os.listdir(localoptionsfolder)
allfiles = defaultfiles + localfiles
num = len(allfiles)
c = 0
while c < num:
    file = allfiles[c]
    if file[-3:] == 'xml':
        xmlfiles.append(file)
    c = c + 1
size = len(xmlfiles)
if size < 1:
    nofilesfound()
# select new advancedsettings file    
CHOOSE = xbmcgui.Dialog().select("Advanced Settings - Options", xmlfiles)
xbmc.log("%s: CHOOSE is %s"% (ADDON_ID, CHOOSE), 2)
if CHOOSE == -1:
    cancel()  
CHOICE = xmlfiles[CHOOSE]
source = os.path.join(defaultoptionsfolder, CHOICE)
if not os.path.isfile(source):
    source = os.path.join(localoptionsfolder, CHOICE)
xbmc.log("%s: CHOICE is %s"% (ADDON_ID, CHOICE), 2)
xbmc.log("%s: source is %s"% (ADDON_ID, source), 2)
# tidy up
if os.path.exists(output):
    checkprevious()
    archive()
# copy new file into place    
try:
    shutil.copyfile(source, output)
    xbmc.log("%s: copied %s to %s"% (ADDON_ID, source, output), 2)
    xbmcgui.Dialog().ok('New advanced settings are in place', 'Restart kodi to apply them')
except:
    xbmc.log("%s: Problem copying %s to %s"% (ADDON_ID, source, output), 2)
    xbmc.executebuiltin('Notification(Problem, check log)')
exit()