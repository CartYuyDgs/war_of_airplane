#encoding=utf-8
from cocos import sprite,layer,text
from cocos import collision_model as collision
import config,random
from pyglet.image import Animation
import pyglet
from events import feiji_event
from cocos.audio import pygame

class Bullet(sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__("img/bullet.png")
        self.scale = 0.5
        # self.schedule_interval(self.run_bullet,0.01)
        pygame.mixer.init()
        self.bullet_sound = pygame.mixer.Sound('sounds/bullet.ogg')
        self.cshape = collision.AARectShape(collision.eu.Vector2(0,0),self.width//2,self.height//2)



    def run_bullet(self,dt):
        x,y = self.position
        if y > config.WINDOS_HEIGHT + self.height:
            self.unschedule(self.run_bullet)
            feiji_event.dispatch_event('on_bullet_resuable',self)
        y += 10
        self.position = x,y
        self.cshape.center = collision.eu.Vector2(x,y)

    def reset_status(self,hero_x,hero_y,feiji_height):
        bullet_x = hero_x
        bullet_y = hero_y + self.height // 2 + feiji_height // 2
        self.position = bullet_x, bullet_y
        self.cshape.center = collision.eu.Vector2(bullet_x,bullet_y)
        self.unschedule(self.run_bullet)
        self.schedule_interval(self.run_bullet,0.01)

    def explode(self):
        self.position = 0, -100
        self.unschedule(self.run_bullet)
        self.cshape.center = collision.eu.Vector2(*self.position)
        feiji_event.dispatch_event('on_bullet_resuable', self)

class Hero(sprite.Sprite):

    def __init__(self):
        # self.cshape = collision.AARectShape(collision.eu.Vector2(0, 0), self.width // 2, self.height // 2)
        self.init_image()


    def update_position(self,x,y):
        if x < self.width//2:
            x = self.width//2
        if x > config.WINDOS_WIDTH-self.width//2:
            x = config.WINDOS_WIDTH-self.width//2
        if y < self.height//2:
            y = self.height//2
        if y > config.WINDOS_HEIGHT-self.height//2:
            y = config.WINDOS_HEIGHT - self.height//2
        self.position = x,y

        self.cshape.center = collision.eu.Vector2(x,y)

    def init_image(self):
        frames = []
        for x in range(1, 3):
            texure = pyglet.resource.image('img/hero/hero%d.png' % x)
            frames.append(texure)
        anim = Animation.from_image_sequence(frames, 0.05)
        super(Hero, self).__init__(anim)
        self.scale = 0.5
        self.position = config.WINDOS_WIDTH // 2, 200
        self.cshape = collision.AARectShape(collision.eu.Vector2(*self.position), self.width // 4, self.height // 4)

    def explode(self):
        frames = []
        for x in range(3, 6):
            texure = pyglet.resource.image('img/hero/hero%d.png' % x)
            frames.append(texure)
        anim = Animation.from_image_sequence(frames,0.05,False)
        self.image = anim

        sound = pygame.mixer.Sound('sounds/hero_die.ogg')
        sound.play()

        self.schedule_interval(self._game_over,1)

    def _game_over(self,dt):
        self.kill()
        # self.unschedule(self.update_position)
        self.unschedule(self._game_over)
        #分发事件
        feiji_event.dispatch_event('on_game_over')


class BgLay(layer.Layer):
    def __init__(self):
        super(BgLay, self).__init__()
        self.bp1 = sprite.Sprite("img/bg.png")
        self.bp2 = sprite.Sprite("img/bg.png")

        self.bp1.image_anchor = (0, 0)
        self.bp2.image_anchor = (0, 0)

        self.bp1.position = (0, 0)
        self.bp2.position = (0, config.WINDOS_HEIGHT - 1)

        self.add(self.bp1)
        self.add(self.bp2)
        self.schedule_interval(self.scroll_bg, 0.01)

    def scroll_bg(self,dt):
        x,y = self.bp1.position
        x1,y1 = self.bp2.position
        if y1 <= 0:
            y = 0
            y1 = config.WINDOS_HEIGHT-1
        else:
            y -= 1
            y1 -= 1

        self.bp1.position = x,y
        self.bp2.position = x1,y1

    def on_game_over(self):
        self.unschedule(self.scroll_bg)

    def on_enter(self):
        super(BgLay, self).on_enter()
        feiji_event.push_handlers(self)

    def on_exit(self):
        super(BgLay, self).on_exit()
        feiji_event.remove_handlers(self)

    def on_game_pause(self):
        self.pause_scheduler()

    def on_game_resume(self):
        self.resume_scheduler()


class Enemy(sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__("img/enemy/enemy_small1.png")
        self.scale = 0.6
        # self.schedule_interval(self.run_enemy,2)
        self.cshape = collision.AARectShape(collision.eu.Vector2(0,0),self.width//2,self.height//2)

    def run_enemy(self,dt):
        x,y = self.position
        y -= 10
        self.position = x, y
        self.cshape.center = collision.eu.Vector2(x,y)
        if y <= -self.height:
            self.unschedule(self.run_enemy)
            feiji_event.dispatch_event('on_enemy_resuable',self)

    def explode(self):
        self.unschedule(self.run_enemy)

        frames = []
        for x in range(2,5):
            texure = pyglet.resource.image('img/enemy/enemy_small%d.png' % x)
            frames.append(texure)
        anim = Animation.from_image_sequence(frames,0.05,False)
        self.image = anim

        self.schedule_interval(self._prepare_to_use,0.15)

    def _prepare_to_use(self,dt):
        self.position = 0,-100
        self.cshape.center = collision.eu.Vector2(*self.position)
        feiji_event.dispatch_event('on_enemy_resuable', self)
        self.image = pyglet.resource.image('img/enemy/enemy_small1.png')
        self.unschedule(self._prepare_to_use)



    def reset_status(self):
        x = random.randint(self.width // 2, config.WINDOS_WIDTH - self.width // 2)
        y = config.WINDOS_HEIGHT
        self.position = x, y
        self.cshape.center = collision.eu.Vector2(x, y)
        self.unschedule(self.run_enemy)
        self.schedule_interval(self.run_enemy,0.05)

class Codes_text(text.Label):

    def __init__(self,score=0):
        super(Codes_text, self).__init__(str(score),font_size=20,font_name='Microsoft Yahei',color=(10,10,10,255))
        self._score = score
        self.position = 80,config.WINDOS_HEIGHT-50

    def add_score(self,score):
        self._score += score
        self.element.text = "%d"%self._score

    def get_score(self):
        return self._score






