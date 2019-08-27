#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import wx
from wx.adv import TaskBarIcon
from PyHook3 import HookManager
from pythoncom import PumpMessages
from win32clipboard import OpenClipboard
from win32clipboard import EmptyClipboard
from win32clipboard import SetClipboardText
from win32clipboard import CloseClipboard
from win32api import keybd_event
from win32con import KEYEVENTF_KEYUP as KET_RELEASE
from re import match
from subprocess import Popen
import logo
from win32gui import GetForegroundWindow
from win32gui import GetWindowText
from time import localtime
from time import strftime


def ShowMessageBox(information, title):
    dlg = wx.MessageDialog(None, information, title)
    dlg.ShowModal()
    dlg.Destroy()


def InitTemplateStrFromFile():
    global TemplateStr
    global path
    global Name
    global Description
    global EipNumber

    timeStamp = os.path.getmtime(path)
    DateStr = strftime('%Y%m%d', localtime(timeStamp))

    with open(path, "r") as s:
        line = s.readline()

        try:
            g = match(r"^(?P<Name>\w+)\s+(?P<Desc>\w+)\s*(?P<Eip>\d*)\s*$", line)

            Name = g.group("Name")
            Description = g.group("Desc")
            EipNumber = g.group("Eip")
            EIP = EipNumber

            if EIP != "":
                EIP = "_EIP" + EIP

            TemplateStr = "CN_D{Date}_{Name}_{Desc}{Eip}".format(Date=DateStr, Name=Name,
                                                                 Desc=Description, Eip=EIP)
        except AttributeError:
            ShowMessageBox("Please Check the Setting: Name Description [EIPNo.]", "Invalid Setting")


def ChangeTemplate():
    global TemplateStr
    global ChangeFlag
    global path
    try:
        ChangeFlag = True
        cmd = "notepad.exe " + r"./Template.txt"
        Popen(cmd, shell=True)
        TemplateStr = ""
    except:
        ShowMessageBox("Open File Edit Fail!", "Fail")


# Declare the Task Bar Icon
class MyTaskBarIcon(TaskBarIcon):
    ID_CHANGE = wx.NewId()
    ID_EXIT = wx.NewId()
    TITLE = "Insert Label"

    def __init__(self):
        TaskBarIcon.__init__(self)
        self.SetIcon(logo.logo.getIcon(), self.TITLE)
        self.Bind(wx.EVT_MENU, self.onChange, id=self.ID_CHANGE)
        self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)

    def onChange(self, event):
        # For User Modify the Input Template
        ChangeTemplate()
        pass

    def onExit(self, event):
        # Exit listening the Key
        wx.Exit()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        for menuAttr in self.getMenuAttrs():
            menu.Append(menuAttr[1], menuAttr[0])
        return menu

    def getMenuAttrs(self):
        return [('修改配置模板', self.ID_CHANGE),
                ('退出', self.ID_EXIT)]


def OnKeyboardEvent(event):
    global TemplateStr
    global ChangeFlag
    global path
    global BeforeStamp
    global Name
    global Description
    global EipNumber

    if event.Key == "F2":
        # Check if the Template File has been modified
        CurrentStamp = os.path.getmtime(path)
        if ChangeFlag is True or CurrentStamp != BeforeStamp:
            InitTemplateStrFromFile()
            ChangeFlag = False

        # Check if the Template File is valid
        if TemplateStr == "":
            ShowMessageBox("Please Check the Setting: Name Description [EIPNo.]", "Invalid Setting")
            return True

        # Check current cursor on what file
        window = GetForegroundWindow()
        title = GetWindowText(window)

        # Copy the Template Str to cursor position
        OpenClipboard()
        EmptyClipboard()

        if ".sdl" in title:
            SetClipboardText("#" + TemplateStr + ">>\n\n" + "#" + TemplateStr + "<<\n")
        elif "Commit - TortoiseGit" in title:
        
            if EipNumber != "":
                CommitStr = "**  [M00x]\n     Issue        : [EIP"+EipNumber+"] "+Description
            else:
                CommitStr = "**  [M00x]\n     Issue        : "+Description

            CommitStr += "\n     Cust.Ref.No. :"
            CommitStr += "\n     Label        : " + TemplateStr
            CommitStr += "\n     File         : "
            SetClipboardText(CommitStr)
            
        else:
            SetClipboardText("//" + TemplateStr + ">>\n\n" + "//" + TemplateStr + "<<\n")

        CloseClipboard()
        keybd_event(17, 0, 0, 0)  # key Ctrl
        keybd_event(86, 0, 0, 0)  # key v
        keybd_event(17, 0, KET_RELEASE, 0)  # release Key Ctrl
        keybd_event(86, 0, KET_RELEASE, 0)  # release Key v

    return True


class MyApp(wx.App):
    def OnInit(self):
        MyTaskBarIcon()
        return True

    def ListenHotKey(self):
        hm = HookManager()
        hm.KeyDown = OnKeyboardEvent
        hm.HookKeyboard()
        PumpMessages()

    def InitTemplateStr(self):
        InitTemplateStrFromFile()


if __name__ == "__main__":
    # Variable for global use
    TemplateStr = ""
    Name = ""
    Description = ""
    EipNumber = ""
    ChangeFlag = False
    path = os.path.join(os.getcwd(), "Template.txt")  # Get path of "Template.txt" on this work directory

    # Initialize the App instance
    app = MyApp()

    try:
        # Try to open "Template.txt", if exists get it's time stamp
        with open(path, "r") as f:
            pass
        BeforeStamp = os.path.getmtime(path)
    except FileNotFoundError:
        # if "Template.txt" does not exist, create and initialize it
        with open(path, "w") as f:
            f.write("Name Description 111111")
        BeforeStamp = os.path.getmtime(path)

    # Initialize the Label
    app.InitTemplateStr()

    # Listen the user's hot key
    app.ListenHotKey()

    app.MainLoop()
