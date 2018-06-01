__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import sys
import pyglet
import pyglet
from pyglet.window import key
pyglet.lib.load_library('avbin')
pyglet.have_avbin=True

def draw_rect(x, y, width, height):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

class Control(pyglet.event.EventDispatcher):
    def __init__(self, parent):
        super(Control, self).__init__()
        self.parent = parent 
      
class Slider(Control): 
    def draw(self):
        draw_rect(self.x, self.y, self.width, self.height)
   
class PlayerWindow(pyglet.window.Window):
    def __init__(self, player):
       super(PlayerWindow, self).__init__(caption='Media Player',visible=False, resizable=True)
       self.player = player
       self.player.push_handlers(self)
       self.slider = Slider(self)
    
    def get_video_size(self):
        if not self.player.source or not self.player.source.video_format:
             return 0,0
       
       video_format = self.player.source.video_format
       width = video_format.width
       height = video_format.height
       if video_format.sample_aspect > 1:
           width *= video_format.sample_aspect
       elif video_format.sample_aspect < 1:
           height /= video_format.sample_aspect
       return width, height
    def on_resize(self, width, height):
       super(PlayerWindow, self).on_resize(width, height)
       
       if height <= 0:
           return
       
       video_width, video_height = self.get_video_size()
       if video_width == 0 or video_height == 0:
           return
       
       display_aspect = width / float(height)
       video_aspect = video_width / float(video_height)
       if video_aspect > display_aspect:
           self.video_width = width
           self.video_height = width / video_aspect
       else:    
           self.video_height = height
           self.video_width = height * video_aspect
       
       self.video_x = (width - self.video_width) / 2
       self.video_y = (height - self.video_height) / 2
       
    def on_key_press(self, symbol, modifiers):
       if symbol == key.SPACE:
           self.on_play_pause()
       elif symbol == key.ESCAPE:
           self.dispatch_event('on_close')
           
    def on_close(self):
       self.player.pause()
       self.close()
       
    def on_play_pause(self):
       if self.player.playing:
           self.player.pause()
       else:
           if self.player.time >= self.player.source.duration:
                self.player.seek(0)
           self.player.play()
           
    def on_draw(self):
       self.clear()
       
       if self.player.source and self.player.source.video_format:
           self.player.get_texture().blit(self.video_x,self.video_y,width=self.video_width,height=self.video_height)
           
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('Usage: media_player.py <filename> [<filename> ...]')
        sys.exit(1)
        
    for filename in sys.argv[1:]:
        player = pyglet.media.Player()
        window = PlayerWindow(player)
        
        source = pyglet.media.load(filename)
        
        player.queue(source)
        window.set_visible(True)
        
        player.play()
        
pyglet.app.run()
