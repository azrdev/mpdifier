#!/usr/bin/env python2

import subprocess
import mpdserver

""" pressing media keys using WinAPI """
#code from http://code.google.com/p/pywinauto/
import ctypes
from ctypes import *

WORD = ctypes.c_ushort
DWORD = ctypes.c_ulong

class KEYBDINPUT(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('wVk', WORD),
        ('wScan', WORD),
        ('dwFlags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', DWORD),
    ]

#dummys, don't need those structures here
class MOUSEINPUT(ctypes.Structure):
    pass

class HARDWAREINPUT(ctypes.Structure):
    pass

class UNION_INPUT_STRUCTS(ctypes.Union):
    _fields_ = [
        ('mi', MOUSEINPUT),
        ('ki', KEYBDINPUT),
        ('hi', HARDWAREINPUT),
    ]

class INPUT(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('type', DWORD),
        ('_', UNION_INPUT_STRUCTS),
    ]

INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 2

""" param  key - the key to press, must be a WORD """
def pressKey(key):
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp._.ki.wScan = 0
    inp._.ki.time = 0
    inp._.ki.dwExtraInfo = 0
    inp._.ki.wVk = key
    inp._.ki.dwFlags = 0

    ctypes.windll.user32.SendInput(1,
                                   ctypes.pointer(inp),
                                   ctypes.sizeof(inp))

    inp._.ki.dwFlags = KEYEVENTF_KEYUP

    ctypes.windll.user32.SendInput(1,
                                   ctypes.pointer(inp),
                                   ctypes.sizeof(inp))


class Key: # enum
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF
    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PREV_TRACK = 0xB1
    VK_MEDIA_STOP = 0xB2
    VK_MEDIA_PLAY_PAUSE = 0xB3


# command classes to be registered to mpd

class VolumeUp(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VK_VOLUME_UP)

class VolumeDown(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VK_VOLUME_DOWN)

class Mute(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VK_VOLUME_MUTE)


class Play(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VK_MEDIA_PLAY_PAUSE)

class Pause(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VK_MEDIA_PLAY_PAUSE)

class Next(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VK_MEDIA_NEXT_TRACK)

class Previous(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VK_MEDIA_PREV_TRACK)

class Stop(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VK_MEDIA_STOP)


""" setup & usage of mpdserver """
def main():
    mpd = mpdserver.MpdServerDaemon(6600)
    mpd.requestHandler.RegisterCommand(mpdserver.Outputs)
    #TODO: setvol command
    #mpd.requestHandler.RegisterCommand(VolumeUp)
    #mpd.requestHandler.RegisterCommand(VolumeDown)
    #mpd.requestHandler.RegisterCommand(Mute)

    mpd.requestHandler.RegisterCommand(Play)
    mpd.requestHandler.RegisterCommand(Pause)
    mpd.requestHandler.RegisterCommand(Next)
    mpd.requestHandler.RegisterCommand(Previous)
    mpd.requestHandler.RegisterCommand(Stop)
    mpd.requestHandler.Playlist=mpdserver.MpdPlaylistDummy

    try:
        while mpd.wait(1):
            pass
    except KeyboardInterrupt:
        print 'caught ctrl+c, aborting'
        mpd.quit()

if __name__ == "__main__":
    main()

