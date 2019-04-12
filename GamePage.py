#encoding:utf-8
from cocos import layer,scene,sprite,director,menu,text
import config,random
from roles import  Hero,BgLay,Bullet,Enemy,Codes_text
from cocos import batch,actions
from events import feiji_event
from cocos.audio import pygame
import pygame
from cocos import collision_model as collision
from GameOver import GameOverScene
from GameMenu import BaseMenu

class GameMenu(menu.Menu):
    def __init__(self):
        super(GameMenu, self).__init__()
        parse_btn = menu.ImageMenuItem("img/pause.png",self.parse_game)
        self.create_menu([parse_btn])

        menu.fixedPositionMenuLayout([(40,config.WINDOS_HEIGHT-40)])(self)

    def parse_game(self):
        feiji_event.dispatch_event("on_game_pause")

class GamePauseMeum(BaseMenu):
    def __init__(self):
        super(GamePauseMeum, self).__init__()

    def menu_items(self):
        resume_menu = menu.ImageMenuItem('img/btn4.png',self.pause_game)
        return [resume_menu]

    def pause_game(self):
        feiji_event.dispatch_event("on_game_resume")

class GameLayer(layer.Layer):
    is_event_handler = True
    def __init__(self):
        super(GameLayer, self).__init__()
        self.hero = Hero()
        self.add(self.hero,z = 1)
        self.bullet_batch = batch.BatchNode()
        self.enemy_batch = batch.BatchNode()
        self.add(self.bullet_batch,z = 1)
        self.add(self.enemy_batch,z = 1)

        # 保存容器
        self.bullet_resuable = []
        self.enemy_resuable = []
        # 子弹和敌机的碰撞
        # 检测区域
        self.enemy_bullet_collision = collision.CollisionManagerGrid(0,config.WINDOS_WIDTH,0,config.WINDOS_HEIGHT,110,110)
        self.enemy_hero_collosion = collision.CollisionManagerGrid(0,config.WINDOS_WIDTH,0,config.WINDOS_HEIGHT,self.hero.width*1.25,self.hero.height*1.25)
        # 在屏幕上的敌机
        self.active_enemies = []
        self.active_bullets = []

        self.codes = Codes_text()
        self.add(self.codes)

        # 每一帧的事件调度

        self.schedule_interval(self.fire_bullet,0.1)
        self.schedule_interval(self.enemy_update,0.3)
        self.schedule(self.run_schedule)

    def run_schedule(self,dt):
        self.enemy_bullet_collision.clear()
        self.enemy_hero_collosion.clear()
        for enemy in self.active_enemies:
            self.enemy_bullet_collision.add(enemy)
            self.enemy_hero_collosion.add(enemy)
        for bullet in self.active_bullets:
            self.enemy_bullet_collision.add(bullet)
        resu = self.enemy_hero_collosion.objs_colliding(self.hero)

        result = self.enemy_bullet_collision.iter_all_collisions()
        for one,two in result:
            if type(one) == type(two):
                continue
            one.explode()
            two.explode()
            self.codes.add_score(100)
        if len(resu) >0:
            self.hero.explode()


    def on_bullet_resuable(self,bullet):
        self.bullet_resuable.append(bullet)
        try:
            self.active_bullets.remove(bullet)
        except:
            pass

    def on_enter(self):
        super(GameLayer, self).on_enter()
        feiji_event.push_handlers(self)


    def on_exit(self):
        super(GameLayer, self).on_exit()
        feiji_event.remove_handlers(self)

    def fire_bullet(self,dt):
        bullet = None
        if len(self.bullet_resuable)<=0:
            bullet = Bullet()
            self.bullet_batch.add(bullet)
            self.active_bullets.append(bullet)
        else:
            bullet = self.bullet_resuable.pop()
            self.active_bullets.append(bullet)
        # bullet.bullet_sound.play()
        hero_x,hero_y = self.hero.position
        bullet.reset_status(hero_x,hero_y,self.hero.height)

    def enemy_update(self,dt):
        enemy = None
        if len(self.enemy_resuable)<=0:
            enemy = Enemy()
            self.enemy_batch.add(enemy)
            self.active_enemies.append(enemy)
        else:
            enemy = self.enemy_resuable.pop()
            self.active_enemies.append(enemy)
            # print(enemy)

        enemy.reset_status()

    def on_enemy_resuable(self,enemy):
        self.enemy_resuable.append(enemy)
        try:
            self.active_enemies.remove(enemy)
        except:
            pass

    def on_game_over(self):
        self.unschedule(self.enemy_update)
        self.unschedule(self.fire_bullet)
        director.director.replace(GameOverScene(self.codes.get_score()))


    def on_mouse_drag(self,x,y,*args,**kwargs):
        self.hero.update_position(x,y)

    def on_game_pause(self):
        self.pause_scheduler()

        for x in self.active_bullets:
            x.pause_scheduler()

        for x in self.active_enemies:
            x.pause_scheduler()

    def on_game_resume(self):
        self.resume_scheduler()
        for x in self.active_enemies:
            x.resume_scheduler()
        for x in self.active_bullets:
            x.resume_scheduler()

class GamePauseLayer(layer.ColorLayer):
    def __init__(self,score):
        super(GamePauseLayer, self).__init__(10,10,10,100)
        score_lable = text.Label(u'得分：%s'%score,font_size=20,font_name='Microsoft Yahei',color=(255,255,255,255),anchor_x="center",anchor_y="center")
        score_lable.position = config.WINDOS_WIDTH // 2, config.WINDOS_HEIGHT - 200
        self.add(score_lable)

        pause_menu = GamePauseMeum()
        self.add(pause_menu)

    def on_enter(self):
        super(GamePauseLayer, self).on_enter()
        game_scene = self.parent
        childrens = game_scene.get_children()
        for node in childrens:
            if node == self:
                continue

            director.director.window.remove_handlers(node)

    def on_exit(self):
        super(GamePauseLayer, self).on_exit()
        game_scene = self.parent
        childrens = game_scene.get_children()
        for node in childrens:
            if node == self:
                continue
            if node.is_event_handler:
                director.director.window.push_handlers(node)

class GameScene(scene.Scene):

    def __init__(self):
        bp_layer = BgLay()
        self.ga_layer = GameLayer()
        parse_layer = GameMenu()
        super(GameScene, self).__init__(bp_layer,self.ga_layer,parse_layer)
        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.music.load('sounds/bg_music.mp3'.encode('utf-8'))

    def on_enter(self):
        super(GameScene, self).on_enter()

        self.music.play()

        feiji_event.push_handlers(self)

    def on_exit(self):
        super(GameScene, self).on_exit()
        self.stop()
        feiji_event.remove_handlers(self)

    def on_game_pause(self):
        pause_layer = GamePauseLayer(self.ga_layer.codes.get_score())
        n = len(self.children)
        self.add(pause_layer,z=n,name='pause_game')

    def on_game_resume(self):
        self.remove('pause_game')
