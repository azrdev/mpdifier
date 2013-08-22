#!/usr/bin/env python2

import subprocess
import mpdserver

""" pressing media keys, using external C binary """
def pressKey(key):
    subprocess.call(['sendMediaKeys.exe', key])

class Key:
   VolumeUp = "+"
   VolumeDown = "-"
   Mute = "m"

   TogglePause = "t"
   Next = "n"
   Previous = "p"
   Stop = "s"


# command classes to be registered to mpd

class VolumeUp(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VolumeUp)

class VolumeDown(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.VolumeDown)

class Mute(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.Mute)


class Play(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.TogglePause)

class Pause(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.TogglePause)

class Next(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.Next)

class Previous(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.Previous)

class Stop(mpdserver.Command):
    def handle_args(self):
        pressKey(Key.Stop)


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

