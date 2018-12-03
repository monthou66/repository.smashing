#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import os
import shutil
import xbmcvfs
import time

########################################################################################################################
########################################################################################################################
##                                      script.me.smashingsync
##
##
##
##  SMASHINGTARGET - download stuff to here from master copy
##
##  if start with 'force': runs without dialogs, uses first available source (advancedsettings.xml if valid)
##                         overwrites folders in userdata/smashing
##
##
##
##
########################################################################################################################
########################################################################################################################

USERDATA = xbmc.translatePath('special://masterprofile')
ADVANCEDSETTINGS = os.path.join(USERDATA, "advancedsettings.xml")
SMASHINGFOLDER = os.path.join(USERDATA, "smashing")
SMASHINGFAVOURITES = os.path.join(SMASHINGFOLDER, "smashingfavourites")
defaultsmashingfile = os.path.join(SMASHINGFAVOURITES, "miscfiles", "sync", "defaultsmashingsource.txt")
SMASHINGTARGET = os.path.join(SMASHINGFOLDER, "smashingtarget")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
updatefile = os.path.join(SMASHINGTEMP, "miscfiles", "update.txt")
updatescript = os.path.join(SMASHINGFAVOURITES, "scripts", "utilityscripts", "updateaddon.py")

# defaults:
thisaddon = 'script.me.smashingsync'
ADVANCEDSMASHING = 'false'
DEFAULTSAVEDSMASHING = 'false'
SAVEDSMASHING = 'false'
update = 'not set'
problem = 'false'
force = 'false'
listproblemfolders = []
advancedoption = 'The smashing folder specified in advancedsettings.xml is:'
defaultoption = 'The default smashing folder specified is:'
aa = 'Load from location in advancedsettings'
bb = 'load from default location'
cc = 'input a folder location'
dd = 'cancel operation'
ee = 'Remove a folder from userdata/smashing'
ff = 'Check for updated addon'

print 'running script.me.smashingsync'

def selectoption():
    print 'running selectoption()'
    # ask the question - update addon or sync settings?
    chooseoption = 'What do you want to do?'
    options = []
    one = 'Check for updates to the sync addon'
    two = 'Sync folders'
    three = 'Exit'
    options.append(one)
    options.append(two)
    options.append(three)
    CHOOSE = xbmcgui.Dialog().select(chooseoption, options)
    CHOICE = options[CHOOSE]
    if CHOOSE == -1:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Script, cancelled)')
        cleanup()
    elif CHOICE == three:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Script, cancelled)')
        cleanup()
#    elif CHOICE == one:

def getversion():
    global textfile, version
    print 'running getversion()'
    print ('textfile to check is %s'% textfile)
    if os.path.isfile(textfile):
        versionfile = open(textfile, 'r')
        version = versionfile.read()
        versionfile.close()
        version = version.strip()
        print ('textfile has version %s'% version)
    else:
        version = 'not found'
        print 'no version found'
    
    
def checkforupdatedaddon():
    global textfile, version, ADVANCEDSMASHINGCHECKED, DEFAULTPATHS, smashingsource, update
    print 'running checkforupdatedaddon()'
    # set defaults
    highest = 0
    selectedversion = 0
    advancedversion = 0
    
    ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))
    currentfolder = os.path.join(ADDONSFOLDER, thisaddon)
    currenttextfile = os.path.join(currentfolder, "version.txt")
    textfile = currenttextfile
    getversion()
    currentversion = version
    print ('currentversion is %s'% currentversion)
    # check addon in smashingfavourites
    smashingfolder = os.path.join(SMASHINGFAVOURITES, 'miscfiles', 'addons', 'myaddons', thisaddon)
    smashingtextfile = os.path.join(smashingfolder, 'version.txt')
    textfile = smashingtextfile
    getversion()
    smashingversion = version
    print ('smashingversion is %s'% smashingversion)
    # check addon in advancedsettings
    if not ADVANCEDSMASHINGCHECKED == 'false':
        advancedfolder = os.path.join(ADVANCEDSMASHINGCHECKED, 'smashingfavourites', 'miscfiles', 'addons', 'myaddons', thisaddon)
        advancedtextfile = os.path.join(advancedfolder, 'version.txt')
        textfile = advancedtextfile
        getversion()
        advancedversion = version
    # check addon in default location
    size = len(DEFAULTPATHS)
    defaults = []
    defaultfolders = []
    if not size == 0:
        c = 0
        while c < size:
            folder = DEFAULTPATHS[c]
            addonfolder = os.path.join(folder, 'smashingfavourites', 'miscfiles', 'addons', 'myaddons', thisaddon)
            textfile = os.path.join(addonfolder, 'version.txt')
            getversion()
            defaults.append(version)
            defaultfolders.append(addonfolder)
            c = c + 1
    # check user-selected addon if not one of the above
    if not smashingsource == ADVANCEDSMASHINGCHECKED:
        if not smashingsource in DEFAULTPATHS:
            selectedfolder = os.path.join(smashingsource, 'smashingfavourites', 'miscfiles', 'addons', 'myaddons', thisaddon)
            selectedtextfile = os.path.join(selectedfolder, 'version.txt')
            textfile = selectedtextfile
            getversion()
            selectedversion = version
    # find highest version available:
    smashingversion = str(smashingversion)
    print ('smashingversion is %s'% smashingversion)
    if smashingversion.isdigit():
        print 'check140'
        smashingversion = int(smashingversion)
        highest = smashingversion
        source = smashingfolder
    selectedversion = str(selectedversion)
    if selectedversion.isdigit():
        selectedversion = int(selectedversion)
        if selectedversion > highest:
            highest = selectedversion
            source = selectedfolder
    advancedversion = str(advancedversion)
    if advancedversion.isdigit():
        advancedversion = int(advancedversion)
        if advancedversion > highest:
            highest = advancedversion
            source = advancedfolder
    num = len(defaults)
    if num > 0:
        c = 0
        while c < num:
            check = defaults[c]
            check = str(check)
            if check.isdigit():
                check = int(check)
                if check > highest:
                    highest = check
                    sourcefolder = defaultfolders[c]
                    source = sourcefolder
            c = c + 1
    # check vs current version:
    if currentversion.isdigit():
        currentversion = int(currentversion)
    else:
        currentversion = 0
    print ('current version is %d'% currentversion)
    print ('highest available version is %d'% highest)
    print ('version %d is found at: %s'% (highest, source))
    if highest > currentversion:
        header = ('Current addon version is %d; version %d is available'% (currentversion, highest))
        yesnowindow = xbmcgui.Dialog().yesno(header, 'Click yes to update, no to continue')
        if yesnowindow:
            print 'Update selected.'
            print ('Closing %s'% thisaddon)
            xbmc.executebuiltin('Notification(Starting, update process)')
            # write source and destination to file
            sourceline = ('source = %s'% source)
            newversion = ('newversion = Available version is version %d'% highest)
            destline = ('dest = %s'% currentfolder)
            oldversion = ('oldversion = Current version is %d'% currentversion)
            updateaddonid = ('updateaddonid = %s'% thisaddon)            
            f = open(updatefile, 'w')
            f.write("%s\n" % sourceline)
            f.write("%s\n" % destline)
            f.write("%s\n" % newversion)
            f.write("%s\n" % oldversion)
            f.write("%s\n" % updateaddonid)
            f.close()

            # start update script
            print 'trying update script'
            if os.path.isfile(updatescript):
                xbmc.executebuiltin('RunScript(%s)'% updatescript)
            else:
                print ('update script not found at %s'% updatescript)
                xbmc.executebuiltin('Notification(No update script found at, %s)'% updatescript)
            cleanup()
        else:
            print 'Update not selected'
    else:
        print 'no update available'
        xbmc.executebuiltin('Notification(No update, available)')
    if update == 'true':
        xbmc.executebuiltin('Notification(All, done)')
        cleanup()
        
    
def maketarget():            
    # make folders if necessary
    print 'running maketarget()'
    if not os.path.isdir(SMASHINGFOLDER):
        os.mkdir(SMASHINGFOLDER)
        xbmc.sleep(300)
    if not os.path.isdir(SMASHINGTARGET):
        os.mkdir(SMASHINGTARGET)

def checktarget():
    global DELETEFOLDER, smashingsubs
    print 'running checktarget():'
    # check SMASHINGTARGET - if not empty give option to move into place; empty if necessary
    checktarget = os.listdir(SMASHINGTARGET)
    sizetarget = len(checktarget)
    if sizetarget > 0:
        smashingsubs = []
        c = 0
        d = 0
        while c < sizetarget:
            check = checktarget[c]
            print ('check is %s'% check)
            if check[:8] == 'smashing':
                smashingsubs.append(check)
                d = d + 1
            else:
                DELETEFOLDER = os.path.join(SMASHINGTARGET, check)
                removefolder()
            c = c + 1
        if d >0:
            choosestuff() 
        
def inputpath():
    global input
    print 'running inputpath()'
    # input smashing folder location manually
    keyboard = xbmc.Keyboard("", "Enter path to smashing folder", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        input = keyboard.getText()
        checkinput()
    else:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Script, cancelled)')
        cleanup()
        
def checkinput():
    global input, smashingsource
    print 'running checkinput()'
    if not input[-1:] == '/':                   # folder needs to end in a /
        input = input + '/'
    if xbmcvfs.exists(input):
        print 'check1'
        check = os.path.join(input, "smashingfavourites/")

        if xbmcvfs.exists(check):
            print 'check2'
            smashingsource = input
        else:
            yesnowindow = xbmcgui.Dialog().yesno('Input path is not valid', 'Click yes to try again')
            if yesnowindow:
                print 'check3'
                inputpath()
            else:
                print 'Script cancelled by user'
                xbmc.executebuiltin('Notification(Script, cancelled)')
                cleanup()
    else:
        yesnowindow = xbmcgui.Dialog().yesno('Input path is not valid', 'Click yes to try again')
        if yesnowindow:
            print 'check4'
            inputpath()
        else:
            print 'Script cancelled by user'
            xbmc.executebuiltin('Notification(Script, cancelled)')
            cleanup()    
        
def checkpath():            
    global checkpathvalid
    print 'running checkpath()'
#    print ('checkpathvalid is %s'% checkpathvalid)
    check = os.path.join(checkpathvalid, "smashingfavourites/")
    if xbmcvfs.exists(check):
#    if os.path.isdir(check):
        checkpathvalid = 'true'
#        print 'checkpathvalid is true'
#    else:
#        print 'checkpathvalid is false'

def getsmashinglocation():
    global smashingsource, checkpathvalid, aa, bb, cc, dd, ee, ff, update, defaultoption, ADVANCEDSMASHINGCHECKED, DEFAULTPATHS
    print 'running getsmashinglocation()'
    options = []
    ADVANCEDSMASHINGCHECKED = 'false'
    DEFAULTSAVEDSMASHINGCHECKED = 'false'
    DEFAULTPATHS = []
    # get SMASHING location from advancedsettings.xml
    if os.path.isfile(ADVANCEDSETTINGS):    
        lines = file(ADVANCEDSETTINGS, 'r').readlines()
        num = len(lines)
        c = 0
        while c < num:
            test = lines[c].strip()
            if test == '<from>smb://Source smashing</from>':
                d = c + 1
                checkline = lines[d].strip()
                c = 1000
            else:
                c = c + 1
        # lines.close()
        if c == 1000:
            start = '<to>'
            finish = '</to>'
            ADVANCEDSMASHING = (checkline.split(start))[1].split(finish)[0]
            ADVANCEDSMASHING = ADVANCEDSMASHING.strip()
            checkpathvalid = ADVANCEDSMASHING
            checkpath()
            if checkpathvalid == 'true':
                xbmcgui.Dialog().ok(advancedoption, ADVANCEDSMASHING)
                options.append(aa)
                ADVANCEDSMASHINGCHECKED = ADVANCEDSMASHING
            else:
                ADVANCEDSMASHING = 'false'
        
    # get SMASHING location from defaultsmashingfile
    if os.path.exists(defaultsmashingfile):
        with open(defaultsmashingfile) as f:
            lines = f.readlines()
            num = len(lines)
            c = 0
            while c < num:
                DEFAULTSAVEDSMASHING = lines[c]
                DEFAULTSAVEDSMASHING = DEFAULTSAVEDSMASHING.strip()
                if not DEFAULTSAVEDSMASHING == ADVANCEDSMASHING:
                    checkpathvalid = DEFAULTSAVEDSMASHING
                    checkpath()
                    if checkpathvalid == 'true':
                        DEFAULTPATHS.append(DEFAULTSAVEDSMASHING)
                c = c + 1
            size = len(DEFAULTPATHS)
            if size == 0:
                DEFAULTSAVEDSMASHING = 'false'
            elif size == 1:
                DEFAULTSAVEDSMASHING = DEFAULTPATHS[0]
                options.append(bb)
                xbmcgui.Dialog().ok(defaultoption, DEFAULTSAVEDSMASHING)
            elif size > 1:
                DEFAULTSAVEDSMASHING = 'multi'
                bb = 'choose from default locations'
                options.append(bb)
                if size < 4:
                    defaultoption = 'Default smashing folder options specified are:'
                    xbmcgui.Dialog().ok(defaultoption, *DEFAULTPATHS)
                else:
                    defaultoption = 'Too many default options to list.  The first 3 are:'
                    x = DEFAULTPATHS[0]
                    y = DEFAULTPATHS[1]
                    z = DEFAULTPATHS[2]
                    xbmcgui.Dialog().ok(defaultoption, x, y, z)
        
    # ask the question - which folder to use

    choosefolder = 'Choose which folder to use'
    if len(options) == 0:
        choosefolder = 'There are no valid folders to choose from'
    options.append(cc)
    options.append(ee)
    options.append(ff)
    options.append(dd)
    CHOOSE = xbmcgui.Dialog().select(choosefolder, options)
    CHOICE = options[CHOOSE]
    if CHOOSE == -1:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Script, cancelled)')
        cleanup()
    elif CHOICE == dd:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Script, cancelled)')
        cleanup()
    elif CHOICE == ff:
        smashingsource = SMASHINGFOLDER
        update = 'true'
    elif CHOICE == cc:
        # input a path
        inputpath()
    elif CHOICE == aa:
        smashingsource = ADVANCEDSMASHING
    elif CHOICE == ee:
        removesmashingfolder()
    elif CHOICE == bb:
        if not DEFAULTSAVEDSMASHING == 'multi':
            smashingsource = DEFAULTSAVEDSMASHING
        else:
            choosedefault = 'Choose from the following folders:'
            CHOOSE = xbmcgui.Dialog().select(choosedefault, DEFAULTPATHS)
            CHOICE = DEFAULTPATHS[CHOOSE]
            if CHOOSE == -1:
                print 'Script cancelled by user'
                xbmc.executebuiltin('Notification(Script, cancelled)')
                cleanup()
            else:
                smashingsource = CHOICE
    else:
        print 'Something went wrong'
        xbmc.executebuiltin('Notification(Script, cancelled)')
        cleanup()
    print ('smashingsource is %s'% smashingsource)
    
def choosestufftocopy():
    global smashingsource, SUBFOLDERNAME
    print 'running choosestufftocopy()'
    folders = []
    files = []
    options = []
    choices = []
    invalid = 'false'
    folders, files = xbmcvfs.listdir(smashingsource)
    options = folders + files
    options
    question = 'Choose options to copy to local folder:'
    a = 'Cancel operation'
    if a not in options:
        options.append(a)
    choicenumbers = xbmcgui.Dialog().multiselect(question, options)
    if choicenumbers == None:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Action, cancelled)')
        cleanup()
    elif choicenumbers == []:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Action, cancelled)')
        cleanup()
    else:
        num = len(choicenumbers)
        if num > 0:
            c = 0
            while c < num:
                nextnumber = choicenumbers[c]
                nextnumber = int(nextnumber)
                next = options[nextnumber]
                choices.append(next)
                c = c + 1
            print ('choices = %s'% choices)       
        if num > 1:
            if a in choices:
                invalid = 'true'
    if invalid == 'true':
        yesnowindow = xbmcgui.Dialog().yesno('Invalid options selected', 'Click yes to try again', 'Click no to cancel script')
        if yesnowindow:
            xbmc.sleep(300)
            choosestufftocopy() 
        else:
            print 'Script cancelled by user'
            xbmc.executebuiltin('Notification(Script, cancelled)')
            cleanup()
    # deal with negative choice first:
    if choices[0] == a:
        xbmc.executebuiltin('Notification(Operation, cancelled)')
        print 'Script cancelled by user'
    else:
        # if we're still here there are folders to copy in
        c = 0
        num = len(choices)
        while c < num:
            SUBFOLDERNAME = choices[c]
            copytokodi()
            c = c + 1
        xbmc.executebuiltin('Notification(Copy, complete)')
        print 'All subfolders copied.'

def copytokodi():
    global SUBFOLDERNAME, source, target, next
    print 'running copytokodi()'    
    source = os.path.join(smashingsource, SUBFOLDERNAME)
    target = os.path.join(SMASHINGTARGET, SUBFOLDERNAME)

    if not os.path.isdir(target):
        os.mkdir(target)
    dirs = []
    files = []
    dirs, files = xbmcvfs.listdir(source)
#    print ('source is: %s'% source)
    # contents = list(contents)
    num = len(dirs)
#    print ('num = %d'% num)
    if num == 0:
#        print 'No subfolders - end of the line'
        pass
    else:
        c = 0
#        print 'Subfolders in source are:'
        while c < num:
            next = dirs[c]
#            print next
            targetdir = os.path.join(target, next)
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel2()
#        xbmcvfs.mkdir(targetdir)
            c = c + 1
    num = len(files)
#    print ('num = %d'% num)
    if num == 0:
#        print 'No files in source'
        pass
    else:
        c = 0
#        print 'Files in source are:'
        while c < num:
            next = files[c]
#            print next
            sourcefile = os.path.join(source, next)
            targetfile = os.path.join(target, next)
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1

def copyproblem():
    global listproblemfolders
    print 'running copyproblem()'
    print 'Not all folders were processed:'
    num = len(listproblemfolders)
    c = 0
    while c < num:
        folder = listproblemfolders[c]
        print folder
        c = c + 1
    xbmcgui.Dialog().ok('Problem - check log', 'All levels were not copied')
    cleanup()
    
def replacefolders():
    global SUBFOLDERNAME
    print 'running replacefolders()'
    contents = os.listdir(SMASHINGTARGET)
    num = len(contents)
    c = 0
    while c < num:
        SUBFOLDERNAME = contents[c]
        replacefolder()
        c = c + 1
    # check it's worked
    contents = os.listdir(SMASHINGTARGET)
    num = len(contents)
    if num == 0:
        print 'Folders updated successfully'
        xbmcgui.Dialog().ok('All done', 'Folders have been updated')
    else:
        print 'Oops.  Something went wrong.  Folders were not updated'
        xbmcgui.Dialog().ok('Oops', 'Something went wrong')
    cleanup()
    
    
    
def copylevel2():
    global next, next2, sourcelevel2, targetlevel2
    print 'running copylevel2()'
    level2files = []
    level2dirs = []
    sourcelevel2 = os.path.join(source, next)
    targetlevel2 = os.path.join(target, next)
    level2dirs, level2files = xbmcvfs.listdir(sourcelevel2)
    print ('sourcelevel2 is: %s'% sourcelevel2)
    numlevel2 = len(level2dirs)
    print ('numlevel2 = %d'% numlevel2)
    if numlevel2 == 0:
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel2 are:'
        while c < numlevel2:
            next2 = level2dirs[c]
            print next2
            targetdir = os.path.join(targetlevel2, next2)
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel3()
#            xbmcvfs.mkdir(targetdir)
            c = c + 1
    numlevel2 = len(level2files)
    print ('numlevel2 = %d'% numlevel2)
    if numlevel2 == 0:
        print 'No files in sourcelevel2'
    else:
        c = 0
        print 'Files in sourcelevel2 are:'
        while c < numlevel2:
            next2 = level2files[c]
            print next2
            sourcefile = os.path.join(sourcelevel2, next2)
            targetfile = os.path.join(targetlevel2, next2)
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1

            
def copylevel3():
    global next2, next3, sourcelevel3, targetlevel3
    print 'running copylevel3()'
    level3files = []
    level3dirs = []
    sourcelevel3 = os.path.join(sourcelevel2, next2)
    targetlevel3 = os.path.join(targetlevel2, next2)
    level3dirs, level3files = xbmcvfs.listdir(sourcelevel3)
    print ('sourcelevel3 is: %s'% sourcelevel3)
    numlevel3 = len(level3dirs)
    print ('numlevel3 = %d'% numlevel3)
    if numlevel3 == 0:
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel3 are:'
        while c < numlevel3:
            next3 = level3dirs[c]
            print ('next3 is %s'% next3)
            targetdir = os.path.join(targetlevel3, next3)
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel4()
            c = c + 1
    numlevel3 = len(level3files)
    print ('numlevel3 = %d'% numlevel3)
    if numlevel3 == 0:
        print 'No files in sourcelevel3'
    else:
        c = 0
        print 'Files in sourcelevel3 are:'
        while c < numlevel3:
            next3 = level3files[c]
            print ('next3 is %s'% next3)
            sourcefile = os.path.join(sourcelevel3, next3)
            print ('copylevel3sourcefile is %s'% sourcefile)
            targetfile = os.path.join(targetlevel3, next3)
            print ('copylevel3targetfile is %s'% targetfile)
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1            

def copylevel4():																	# change name
    global next3, next4, sourcelevel4, targetlevel4									# change 4 numbers
    print 'running copylevel4()'													# change 1 number
    level4files = []																# change 1 number
    level4dirs = []																	# change 1 number
    sourcelevel4 = os.path.join(sourcelevel3, next3)								# change 3 numbers
    targetlevel4 = os.path.join(targetlevel3, next3)								# change 3 numbers
    level4dirs, level4files = xbmcvfs.listdir(sourcelevel4)							# change 3 numbers
    print ('sourcelevel4 is: %s'% sourcelevel4)										# change 2 numbers
    numlevel4 = len(level4dirs)														# change 2 numbers
    print ('numlevel4 = %d'% numlevel4)												# change 2 numbers
    if numlevel4 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel4 are:'										# change 1 number
        while c < numlevel4:														# change 1 number
            next4 = level4dirs[c]													# change 2 numbers
            print ('next4 is %s'% next4)											# change 2 numbers
            targetdir = os.path.join(targetlevel4, next4)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel5()															# change 1 number
            c = c + 1
    numlevel4 = len(level4files)													# change 2 numbers
    print ('numlevel4 = %d'% numlevel4)												# change 2 numbers
    if numlevel4 == 0:
        print 'No files in sourcelevel4'											# change 1 number
    else:
        c = 0
        print 'Files in sourcelevel4 are:'											# change 1 number
        while c < numlevel4:														# change 1 number
            next4 = level4files[c]													# change 2 numbers
            print ('next4 is %s'% next4)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel4, next4)							# change 2 numbers
            print ('copylevel4sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel4, next4)							# change 2 numbers
            print ('copylevel4targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel5():																	# change name
    global next4, next5, sourcelevel5, targetlevel5									# change 4 numbers
    print 'running copylevel5()'													# change 1 number
    level5files = []																# change 1 number
    level5dirs = []																	# change 1 number
    sourcelevel5 = os.path.join(sourcelevel4, next4)								# change 3 numbers
    targetlevel5 = os.path.join(targetlevel4, next4)								# change 3 numbers
    level5dirs, level5files = xbmcvfs.listdir(sourcelevel5)							# change 3 numbers
    print ('sourcelevel5 is: %s'% sourcelevel5)										# change 2 numbers
    numlevel5 = len(level5dirs)														# change 2 numbers
    print ('numlevel5 = %d'% numlevel5)												# change 2 numbers
    if numlevel5 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel5 are:'										# change 1 number
        while c < numlevel5:														# change 1 number
            next5 = level5dirs[c]													# change 2 numbers
            print ('next5 is %s'% next5)											# change 2 numbers
            targetdir = os.path.join(targetlevel5, next5)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel6()															# change 1 number
            c = c + 1
    numlevel5 = len(level5files)													# change 2 numbers
    print ('numlevel5 = %d'% numlevel5)												# change 2 numbers
    if numlevel5 == 0:
        print 'No files in sourcelevel5'											# change 1 number
    else:
        c = 0
        print 'Files in sourcelevel5 are:'											# change 1 number
        while c < numlevel5:														# change 1 number
            next5 = level5files[c]													# change 2 numbers
            print ('next5 is %s'% next5)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel5, next5)							# change 2 numbers
            print ('copylevel5sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel5, next5)							# change 2 numbers
            print ('copylevel5targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel6():																	# change name
    global next5, next6, sourcelevel6, targetlevel6									# change 4 numbers
    print 'running copylevel6()'													# change 1 number
    level6files = []																# change 1 number
    level6dirs = []																	# change 1 number
    sourcelevel6 = os.path.join(sourcelevel5, next5)								# change 3 numbers
    targetlevel6 = os.path.join(targetlevel5, next5)								# change 3 numbers
    level6dirs, level6files = xbmcvfs.listdir(sourcelevel6)							# change 3 numbers
    print ('sourcelevel6 is: %s'% sourcelevel6)										# change 2 numbers
    numlevel6 = len(level6dirs)														# change 2 numbers
    print ('numlevel6 = %d'% numlevel6)												# change 2 numbers
    if numlevel6 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel6 are:'										# change 1 number
        while c < numlevel6:														# change 1 number
            next6 = level6dirs[c]													# change 2 numbers
            print ('next6 is %s'% next6)											# change 2 numbers
            targetdir = os.path.join(targetlevel6, next6)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel7()															# change 1 number
            c = c + 1
    numlevel6 = len(level6files)													# change 2 numbers
    print ('numlevel6 = %d'% numlevel6)												# change 2 numbers
    if numlevel6 == 0:
        print 'No files in sourcelevel6'											# change 1 number
    else:
        c = 0
        print 'Files in sourcelevel6 are:'											# change 1 number
        while c < numlevel6:														# change 1 number
            next6 = level6files[c]													# change 2 numbers
            print ('next6 is %s'% next6)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel6, next6)							# change 2 numbers
            print ('copylevel6sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel6, next6)							# change 2 numbers
            print ('copylevel6targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel7():																	# change name
    global next6, next7, sourcelevel7, targetlevel7									# change 4 numbers
    print 'running copylevel7()'													# change 1 number
    level7files = []																# change 1 number
    level7dirs = []																	# change 1 number
    sourcelevel7 = os.path.join(sourcelevel6, next6)								# change 3 numbers
    targetlevel7 = os.path.join(targetlevel6, next6)								# change 3 numbers
    level7dirs, level7files = xbmcvfs.listdir(sourcelevel7)							# change 3 numbers
    print ('sourcelevel7 is: %s'% sourcelevel7)										# change 2 numbers
    numlevel7 = len(level7dirs)														# change 2 numbers
    print ('numlevel7 = %d'% numlevel7)												# change 2 numbers
    if numlevel7 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel7 are:'										# change 1 number
        while c < numlevel7:														# change 1 number
            next7 = level7dirs[c]													# change 2 numbers
            print ('next7 is %s'% next7)											# change 2 numbers
            targetdir = os.path.join(targetlevel7, next7)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel8()															# change 1 number
            c = c + 1
    numlevel7 = len(level7files)													# change 2 numbers
    print ('numlevel7 = %d'% numlevel7)												# change 2 numbers
    if numlevel7 == 0:
        print 'No files in sourcelevel7'											# change 1 number
    else:
        c = 0
        print 'Files in sourcelevel7 are:'											# change 1 number
        while c < numlevel7:														# change 1 number
            next7 = level7files[c]													# change 2 numbers
            print ('next7 is %s'% next7)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel7, next7)							# change 2 numbers
            print ('copylevel7sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel7, next7)							# change 2 numbers
            print ('copylevel7targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel8():																	# change name
    global next7, next8, sourcelevel8, targetlevel8									# change 4 numbers
    print 'running copylevel8()'													# change 1 number
    level8files = []																# change 1 number
    level8dirs = []																	# change 1 number
    sourcelevel8 = os.path.join(sourcelevel7, next7)								# change 3 numbers
    targetlevel8 = os.path.join(targetlevel7, next7)								# change 3 numbers
    level8dirs, level8files = xbmcvfs.listdir(sourcelevel8)							# change 3 numbers
    print ('sourcelevel8 is: %s'% sourcelevel8)										# change 2 numbers
    numlevel8 = len(level8dirs)														# change 2 numbers
    print ('numlevel8 = %d'% numlevel8)												# change 2 numbers
    if numlevel8 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel8 are:'										# change 1 number
        while c < numlevel8:														# change 1 number
            next8 = level8dirs[c]													# change 2 numbers
            print ('next8 is %s'% next8)											# change 2 numbers
            targetdir = os.path.join(targetlevel8, next8)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel9()															# change 1 number
            c = c + 1
    numlevel8 = len(level8files)													# change 2 numbers
    print ('numlevel8 = %d'% numlevel8)												# change 2 numbers
    if numlevel8 == 0:
        print 'No files in sourcelevel8'											# change 1 number
    else:
        c = 0
        print 'Files in sourcelevel8 are:'											# change 1 number
        while c < numlevel8:														# change 1 number
            next8 = level8files[c]													# change 2 numbers
            print ('next8 is %s'% next8)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel8, next8)							# change 2 numbers
            print ('copylevel8sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel8, next8)							# change 2 numbers
            print ('copylevel8targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel9():																	# change name
    global next8, next9, sourcelevel9, targetlevel9									# change 4 numbers
    print 'running copylevel9()'													# change 1 number
    level9files = []																# change 1 number
    level9dirs = []																	# change 1 number
    sourcelevel9 = os.path.join(sourcelevel8, next8)								# change 3 numbers
    targetlevel9 = os.path.join(targetlevel8, next8)								# change 3 numbers
    level9dirs, level9files = xbmcvfs.listdir(sourcelevel9)							# change 3 numbers
    print ('sourcelevel9 is: %s'% sourcelevel9)										# change 2 numbers
    numlevel9 = len(level9dirs)														# change 2 numbers
    print ('numlevel9 = %d'% numlevel9)												# change 2 numbers
    if numlevel9 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel9 are:'										# change 1 number
        while c < numlevel9:														# change 1 number
            next9 = level9dirs[c]													# change 2 numbers
            print ('next9 is %s'% next9)											# change 2 numbers
            targetdir = os.path.join(targetlevel9, next9)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel10()															# change 1 number
            c = c + 1
    numlevel9 = len(level9files)													# change 2 numbers
    print ('numlevel9 = %d'% numlevel9)												# change 2 numbers
    if numlevel9 == 0:
        print 'No files in sourcelevel9'											# change 1 number
    else:
        c = 0
        print 'Files in sourcelevel9 are:'											# change 1 number
        while c < numlevel9:														# change 1 number
            next9 = level9files[c]													# change 2 numbers
            print ('next9 is %s'% next9)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel9, next9)							# change 2 numbers
            print ('copylevel9sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel9, next9)							# change 2 numbers
            print ('copylevel9targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel10():																	# change name
    global next9, next10, sourcelevel10, targetlevel10									# change 4 numbers
    print 'running copylevel10()'													# change 1 number
    level10files = []																# change 1 number
    level10dirs = []																	# change 1 number
    sourcelevel10 = os.path.join(sourcelevel9, next9)								# change 3 numbers
    targetlevel10 = os.path.join(targetlevel9, next9)								# change 3 numbers
    level10dirs, level10files = xbmcvfs.listdir(sourcelevel10)							# change 3 numbers
    print ('sourcelevel10 is: %s'% sourcelevel10)										# change 2 numbers
    numlevel10 = len(level10dirs)														# change 2 numbers
    print ('numlevel10 = %d'% numlevel10)												# change 2 numbers
    if numlevel10 == 0:																# change 1 number
        print 'No subfolders - end of the line'
    else:
        c = 0
        print 'Subfolders in sourcelevel10 are:'										# change 1 number
        while c < numlevel10:														# change 1 number
            next10 = level10dirs[c]													# change 2 numbers
            print ('next10 is %s'% next10)											# change 2 numbers
            targetdir = os.path.join(targetlevel10, next10)							# change 2 numbers
            if not os.path.isdir(targetdir):
                os.mkdir(targetdir)
            copylevel11()															# change 1 number
            c = c + 1
    numlevel10 = len(level10files)													# change 2 numbers
    print ('numlevel10 = %d'% numlevel10)												# change 2 numbers
    if numlevel10 == 0:
        print 'No files in sourcelevel10'											# change 1 number
    else:
        c = 0
        print 'Files in sourcelevel10 are:'											# change 1 number
        while c < numlevel10:														# change 1 number
            next10 = level10files[c]													# change 2 numbers
            print ('next10 is %s'% next10)											# change 2 numbers
            sourcefile = os.path.join(sourcelevel10, next10)							# change 2 numbers
            print ('copylevel10sourcefile is %s'% sourcefile)						# change 1 number
            targetfile = os.path.join(targetlevel10, next10)							# change 2 numbers
            print ('copylevel10targetfile is %s'% targetfile)						# change 1 number
            xbmcvfs.copy(sourcefile, targetfile)                # overwrites existing file if present
            c = c + 1  
			
def copylevel11():                                                                   # change 1 number
    global problem, listproblemfolders, next10, sourcelevel10						                        # change 2 numbers
    sourcefoldernotprocessed = os.path.join(sourcelevel10, next10)	                # change 2 numbers
    listproblemfolders.append(sourcefoldernotprocessed)
    print 'running copylevel11'                                                      # change 1 number
    print 'That means not everything has been copied!'
    problem = 'true'

def removesmashingfolder():
    # delete a folder from smashing/userdata
    global DELETEFOLDER
    print 'running removesmashingfolder()'
    header = 'Remove from userdata/smashing:'
    options = []
    all = 'Remove all folders'
    cancel = 'Cancel operation'
    options = os.listdir(SMASHINGFOLDER)
    if len(options) == 0:
        cancel = 'There are no folders in userdata/smashing'
    else:
        options.append(all)
    options.append(cancel)
    CHOOSE = xbmcgui.Dialog().select(header, options)
    CHOICE = options[CHOOSE]
    if CHOOSE == -1:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Script, cancelled)')
        cleanup()
    elif CHOICE == cancel:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Script, cancelled)')
        cleanup()
    elif CHOICE == all:
        DELETEFOLDER = SMASHINGFOLDER
        removefolder()
        os.mkdir(SMASHINGFOLDER)
        xbmc.executebuiltin('Notification(All, done)')
        cleanup()
    else:
        DELETEFOLDER = os.path.join(SMASHINGFOLDER, CHOICE)
        removefolder()
        xbmc.executebuiltin('Notification(All, done)')
        cleanup()
    
# remove a folder recursively
def removefolder():
    global DELETEFOLDER
    print 'running removedeletefolder()'
    print ('DELETEFOLDER is %s'% DELETEFOLDER)
    # delete folder
    # DELETEFOLDER = the full path of the folder to be removed
    if os.path.exists(DELETEFOLDER):
        count = 0
        while count < 50:
            try:
                shutil.rmtree(DELETEFOLDER)
            except:
                pass
            print ('checking for %s'% DELETEFOLDER)
            if not os.path.exists(DELETEFOLDER):
                print 'DELETEFOLDER has been removed'
                count = count + 50
            xbmc.sleep(300)
            count = count + 1
    if os.path.exists(DELETEFOLDER):
        print ('Failed to delete %s'% DELETEFOLDER)
        xbmcgui.Dialog().ok('Problem deleting folder', 'Delete relevant subfolder in userdata/smashing manually and try again')
        cleanup()       

def choosestuff():
    global smashingsubs, choices, SUBFOLDERNAME, DELETEFOLDER
    print 'running choosestuff()'
    # choose one or more folders to install, or empty SMASHINGTARGET and carry on, or quit script
    choicenumbers = []
    choices = []
    invalid = 'false'
    a = 'Select folders from the master copies'
    b = 'Clear all data and stop the script'
    if a not in smashingsubs:
        smashingsubs.append(a)
    if b not in smashingsubs:
        smashingsubs.append(b)
    choicenumbers = xbmcgui.Dialog().multiselect("Do you want to install already transferred subfolders?", smashingsubs)
    # check choices are valid:
    print ('choicenumbers = %s'% choicenumbers)
    if choicenumbers == None:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Action, cancelled)')
        cleanup()
    elif choicenumbers == []:
        print 'Script cancelled by user'
        xbmc.executebuiltin('Notification(Action, cancelled)')
        cleanup()
    else:
        num = len(choicenumbers)
        if num > 0:
            c = 0
            while c < num:
                nextnumber = choicenumbers[c]
                nextnumber = int(nextnumber)
                next = smashingsubs[nextnumber]
                choices.append(next)
                c = c + 1
            print ('choices = %s'% choices)       
        if num > 1:
            if a in choices:
                invalid = 'true'
            elif b in choices:
                invalid = 'true'
    if invalid == 'true':
        yesnowindow = xbmcgui.Dialog().yesno('Invalid options selected', 'Click yes to try again', 'Click no to cancel script')
        if yesnowindow:
            xbmc.sleep(300)
            choosestuff()
        else:
            print 'Script cancelled by user'
            xbmc.executebuiltin('Notification(Script, cancelled)')
            cleanup()     
#    print ('invalid is %s'% invalid)
#    print ('choices = %s'% choices)    
#    xbmcgui.Dialog().ok('Great', 'stuff')
#    exit()
    # deal with negative choices first:
    if choices[0] == a:
        # delete SMASHINGTARGET, remake it as empty and carry on
        DELETEFOLDER = SMASHINGTARGET
        removefolder()
        os.mkdir(SMASHINGTARGET)
        xbmc.executebuiltin('Notification(Folders, removed)')
        print 'Subfolders removed.  Continuing.'
    elif choices[0] == b:
        # delete SMASHINGTARGET and exit script
        DELETEFOLDER = SMASHINGTARGET
        removefolder()
        xbmc.executebuiltin('Notification(All, done)')
        print 'Subfolders removed.  All done.'
        cleanup()
    else:
        # if we're still here there are folders to copy in
        c = 0
        num = len(choices)
        while c < num:
            SUBFOLDERNAME = choices[c]
            replacefolder()
            c = c + 1
        xbmc.executebuiltin('Notification(All, done)')
        print 'Subfolders moved.  All done.'
        cleanup()
    
def replacefolder():
    global SUBFOLDERNAME, SMASHINGTARGET, DELETEFOLDER
    print 'running replacefolder()'
    NEWFOLDER = os.path.join(SMASHINGTARGET, SUBFOLDERNAME)
    OLDFOLDER = os.path.join(SMASHINGFOLDER, SUBFOLDERNAME)
    TEMP = os.path.join(SMASHINGFOLDER, "temp")
    TEMPFOLDER = os.path.join(TEMP, SUBFOLDERNAME)
    if os.path.exists(OLDFOLDER):
        if not os.path.isdir(TEMP):
            os.mkdir(TEMP)
            xbmc.sleep(300)
        shutil.move(OLDFOLDER, TEMPFOLDER)
        xbmc.sleep(300)
    shutil.move(NEWFOLDER, OLDFOLDER)
    if os.path.isdir(TEMPFOLDER):
        DELETEFOLDER = TEMPFOLDER
        removefolder()
        
def cleanup():
    global DELETEFOLDER
    print 'running cleanup()'
    if os.path.isdir(SMASHINGTARGET):
        contents = os.listdir(SMASHINGTARGET)
        if len(contents) == 0:
            DELETEFOLDER = SMASHINGTARGET
            removefolder()
    TEMP = os.path.join(SMASHINGFOLDER, "temp")
    if os.path.isdir(TEMP):
        DELETEFOLDER = TEMP
        removefolder()
    print 'All cleaned up'    
    exit()
    

    
############################################################################################################################################
############################################################################################################################################

if not os.path.isdir(SMASHINGTARGET):
    maketarget()
else:
    checktarget()
getsmashinglocation()
checkforupdatedaddon()
choosestufftocopy()
if problem == 'true':
    copyproblem()



# Replace existing folder?
yesnowindow = xbmcgui.Dialog().yesno('Do you want to replace the existing', 'folder(s)?', 'Click yes to overwrite')
if not yesnowindow:
    print 'Script finished.  Folders have not been overwritten'
    xbmc.executebuiltin('Notification(All, done)')
    cleanup()
else:
    replacefolders()
    
exit()

