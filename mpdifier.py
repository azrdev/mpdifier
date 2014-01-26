#!/usr/bin/env python2

import subprocess
import mpdserver

def pressKey(key):
    print "sending key %c" % key
    subprocess.call(['sendMediaKeys.exe', key])

class Key: # enum
    VK_VOLUME_MUTE = "m"
    VK_VOLUME_DOWN = "-"
    VK_VOLUME_UP = "+"
    VK_MEDIA_NEXT_TRACK = "n"
    VK_MEDIA_PREV_TRACK = "p"
    VK_MEDIA_STOP = "s"
    VK_MEDIA_PLAY_PAUSE = "t"


# command classes to be registered to mpd

class Status(mpdserver.CommandItems):
    def items(self):
        return [
            ("volume", 50),
            ("state", "pause")
        ]

class SetVol(mpdserver.Command):
    muted = False # educated guess
    formatArg = [("vol", int)]
    def handle_args(self, **args):
        nv = args["vol"]
        if self.muted or nv <= 0:
            pressKey(Key.VK_VOLUME_MUTE)
            self.muted = not self.muted #FIXME: seems not to work
        elif nv < 50:
            pressKey(Key.VK_VOLUME_DOWN)
        else:
            pressKey(Key.VK_VOLUME_UP)

#class Mute(mpdserver.Command):
#    def handle_args(self, **args):
#        pressKey(Key.VK_VOLUME_MUTE)


class Play(mpdserver.Command):
    def handle_args(self, **args):
        pressKey(Key.VK_MEDIA_PLAY_PAUSE)

class Pause(mpdserver.Command):
    def handle_args(self, **args):
        pressKey(Key.VK_MEDIA_PLAY_PAUSE)

class Next(mpdserver.Command):
    def handle_args(self, **args):
        pressKey(Key.VK_MEDIA_NEXT_TRACK)

class Previous(mpdserver.Command):
    def handle_args(self, **args):
        pressKey(Key.VK_MEDIA_PREV_TRACK)

class Stop(mpdserver.Command):
    def handle_args(self, **args):
        pressKey(Key.VK_MEDIA_STOP)

class Idle(mpdserver.Command):
    pass
    
class Close(mpdserver.Command):
    #XXX: should close socket to client, but we have no access to that attribute here
    pass

def main():
    """ setup & usage of mpdserver """
    try:
        mpd = mpdserver.MpdServer(6600)
        mpd.requestHandler.RegisterCommand(mpdserver.Outputs)

        mpd.requestHandler.RegisterCommand(SetVol)

        mpd.requestHandler.RegisterCommand(Play)
        mpd.requestHandler.RegisterCommand(Pause)
        mpd.requestHandler.RegisterCommand(Next)
        mpd.requestHandler.RegisterCommand(Previous)
        mpd.requestHandler.RegisterCommand(Stop)
        mpd.requestHandler.RegisterCommand(Status)
        mpd.requestHandler._MpdRequestHandler__SupportedCommands['idle'] = { 'class':Idle, 'users':['default'], 'group':'read', 'mpdVersion':"0.14", 'neededBy':None }
        mpd.requestHandler._MpdRequestHandler__SupportedCommands['close'] = { 'class':Idle, 'users':['default'], 'group':'read', 'mpdVersion':"0.14", 'neededBy':None }
        mpd.requestHandler.Playlist=mpdserver.MpdPlaylistDummy

        mpd.run()
    except KeyboardInterrupt:
      return

if __name__ == "__main__":
    main()

