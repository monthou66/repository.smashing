# -*- coding: utf-8 -*-

# run script from folder and browse up a level or to subfolder

import xbmc
import xbmcaddon
import xbmcgui
import os

# defaults
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
# set scripts folder
USERDATA = xbmc.translatePath('special://masterprofile')
DEFAULTFOLDER = os.path.join(USERDATA, "scripts")
SCRIPTFOLDER = USERDATA
checkupalevel = ""
loglevel = 'on'
argsenabled = 'on'

def printstar():
    xbmc.log("%s ***********************************************************************************"% ADDON_ID, 2)
    xbmc.log("%s ************************************************************************************"% ADDON_ID, 2)

def printlog():
    global message
    if loglevel == 'on':
        xbmc.log("%s:    %s"% (ADDON_ID, message), 2)
    message = ""    
    
    
def getsettings():
    global loglevel, argsenabled, SCRIPTFOLDER
    if ADDON.getSetting('debug.enabled') == 'false':
        loglevel = 'off'
    else:
        loglevel = 'on'
    if ADDON.getSetting('args.enabled') == 'false':
        argsenabled = 'off'
    else:
        loglevel = 'on'        
    # possible to start with argument for alternative script folders
    try:
        checkfolder = sys.argv[1]
        if os.path.isdir(checkfolder):
            SCRIPTFOLDER = checkfolder
    except:  
        if ADDON.getSetting('scriptfolder.default') == 'true':
            SCRIPTFOLDER = DEFAULTFOLDER
        else:
            if ADDON.getSetting('scriptfolder.custom') == 0:
                checkfolder = ADDON.getSetting('scriptfolder.browse')
                SCRIPTFOLDER = checkfolder
            elif ADDON.getSetting('scriptfolder.custom') == 1:
                checkfolder = ADDON.getSetting('scriptfolder.enter')
                SCRIPTFOLDER = checkfolder
            else:
		        SCRIPTFOLDER = DEFAULTFOLDER
        if not os.path.isdir(SCRIPTFOLDER):
            SCRIPTFOLDER = USERDATA
    printsettings()    
        
def printsettings():
    global message
    message = ""
    printlog()
    message = 'Settings:'
    printlog()
    message = ('Scripts folder is %s'% SCRIPTFOLDER)
    printlog()
    message = ('Script debugging is %s'% loglevel)
    printlog()
    message = ('Arguments feature is %s'% argsenabled)
    printlog()
    
def scanfailed():
    global folders,files, SCRIPTFOLDER, message
    message = ("Problem listing contents of scripts folder: %s"% SCRIPTFOLDER)
    printlog()
    message = ("Switching to userdata: %s"% USERDATA)
    printlog()
    xbmc.executebuiltin('Notification(Script folder unavailable, Switching to userdata)')
    SCRIPTFOLDER = USERDATA
    try:
        contents = sorted(os.listdir(USERDATA))                 # use sorted() to get list in alphabetical order
        folders, files = xbmcvfs.listdir(USERDATA)
    except:
        message = ("Problem listing contents of scripts folder: %s"% SCRIPTFOLDER)
        printlog()
        xbmc.executebuiltin('Notification(%s, Problem - check log)'% ADDON_ID)
        exit()

def noscripts():
    global message
    message = ("No scripts found in scripts folder: %s"% SCRIPTFOLDER)
    printlog()
    xbmc.executebuiltin('Notification(%s, Problem - check log)'% ADDON_ID)
    exit()

def nochoice():
    global message
    message = "No script selected.  Action cancelled by user"
    printlog()
    xbmc.executebuiltin('Notification(%s, script cancelled)'% ADDON_ID)
    exit()

def pathproblem():
    global message
    message = ("Script path is not valid: %s"% target)
    printlog()
    xbmc.executebuiltin('Notification(%s, Problem - check log)'% ADDON_ID)
    exit()

def listthings():
    global OPTIONS, header, folders, upalevel, message
    # list all scripts and subfolders in folder
    contents = []
    SCRIPTS = []
    folders = []
    try:
        contents = sorted(os.listdir(SCRIPTFOLDER))                 # use sorted() to get list in alphabetical order
    except:
        scanfailed()
    # list scripts
    num = len(contents)
    c = 0
    while c < num:
        next = contents[c]
        nextpath = os.path.join(SCRIPTFOLDER, next)
        if os.path.isfile(nextpath):
            if next[-3:] == '.py':
                SCRIPTS.append(next)
        else:
            folders.append(next)
        c = c + 1
        
        # sort scripts and folders alphabetically
        # works for python2 only
        # https://stackoverflow.com/questions/10269701/case-insensitive-list-sorting-without-lowercasing-the-result
        SCRIPTS = sorted(SCRIPTS, key=lambda s: s.lower())
        folders = sorted(folders, key=lambda s: s.lower())
        
    size = len(SCRIPTS)
    if size == 0:
        header = 'No scripts here.  Select a folder'
    else:
        header = 'Select a script to run or a folder to browse' 

    # check up a level - add to option to subfolders list if valid
    if '/' in SCRIPTFOLDER:
        sep = '/'
    elif '\\' in SCRIPTFOLDER:
        sep = '\\'
    else:
        sep = 'false'
    if not sep == 'false':
        # upalevel = SCRIPTFOLDER.split(sep, 1)[0]
        upalevel = sep.join(SCRIPTFOLDER.split(sep)[:-1])
        # if in root of drive on windows:
        if upalevel[-1:] == ':':
            upalevel = upalevel + '\\'
        
        #testing
        message = ("Scriptfolder is: %s"% SCRIPTFOLDER)
        printlog()
        message = ("upalevel is: %s"% upalevel)
        printlog()
        
        
        if os.path.isdir(upalevel):
            # add 'up a level' to start of folders list
            folders.insert(0, 'Up a level')
    # make new list of all options
    OPTIONS = []
    OPTIONS = folders + SCRIPTS    
    message = ('Options are: %s'% OPTIONS)
    printlog()
    choosestuff()

def choosestuff():
    global SCRIPTFOLDER, target, CHOICE, message
    target = ""
    # Display list of scripts and get choice
    CHOOSE = xbmcgui.Dialog().select(header, OPTIONS)
    if CHOOSE == -1:
        nochoice()
    CHOICE = OPTIONS[CHOOSE]
    message = ('Option chosen is: %s'% CHOICE)
    printlog()
    if CHOICE == 'Up a level':
        SCRIPTFOLDER = upalevel
        listthings()
    else:
        if CHOICE in folders:
            SCRIPTFOLDER = os.path.join(SCRIPTFOLDER, CHOICE)
            listthings()
        else:
            target = os.path.join(SCRIPTFOLDER, CHOICE)
            if os.path.isfile(target):
                if argsenabled == 'on':
                    runscriptwithargs()
                else:
                    simplerunscript()
            else:
                pathproblem()

def getarguments():
    global arg
    # get sys.argv[1]
    keyboard = xbmc.Keyboard("", "Enter argument", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        arg = keyboard.getText()
               
def runscriptwithargs():
    global target, message
    # check if script uses arguments - if yes prompt, if no run
    message = ("Script to run is: %s"% target)
    printlog()
    # check for argument function
    if 'sys.argv[1]' in open(target).read():
        yesnoargument = xbmcgui.Dialog().yesno("%s","Do you want to run with an argument?","Click yes to add an argument")
        if yesnoargument:
            getarguments()
            args = arg
            if 'sys.argv[2]' in open(target).read():
                yesnoargument = xbmcgui.Dialog().yesno("%s","Do you want to run with a second argument?","Click yes to add another argument")
                if yesnoargument:
                    getarguments()
                    args = args + ', ' + arg
            target = target + ', ' + args
            xbmcgui.Dialog().ok(CHOICE, 'Press ok to run script with arguments')
    xbmc.executebuiltin('Notification(executing, %s)'% CHOICE)
    xbmc.sleep(2000)
    xbmc.executebuiltin('RunScript(%s)'% target)
    exit()



def simplerunscript():
    global message
    # run script and exit
    message = ("Script to run is: %s"% target)
    printlog()
    xbmc.executebuiltin('Notification(executing, %s)'% CHOICE)
    xbmc.sleep(2000)
    xbmc.executebuiltin('RunScript(%s)'% target)
    exit()
        
# start

# xbmc.executebuiltin('Notification(%s, started)'% ADDON_ID)
getsettings()
if loglevel == 'on':
    printstar()
    message = "starting script"
    printlog()
    printsettings()
listthings()


    
   









