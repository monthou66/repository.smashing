#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon

settings = xbmcaddon.Addon(id='script.me.testsettings')
check = settings.getSetting("test5")


xbmc.executebuiltin('Notification(test5 is, %s)'% check)
