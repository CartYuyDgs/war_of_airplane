#encoding:utf-8
from cocos import menu,layer,sprite,scene,director
import config
from GamePage import GameScene
#from cocos.audio import pygame
import pygame
from GameMenu import BaseMenu


class StartMenu(BaseMenu):
    def __init__(self):
        super(StartMenu, self).__init__()
        menu.fixedPositionMenuLayout([(config.WINDOS_WIDTH // 2,350),(config.WINDOS_WIDTH // 2,300)])(self)

    def menu_items(self):
        start_menu = menu.ImageMenuItem(u'img/btn1.png',callback_func=self.start_game)
        return [start_menu]

    def start_game(self):
        game_scene = GameScene()
        director.director.replace(game_scene)

    def end_game(self):
        director.director.terminate_app = True
        #print('end game')

class StartLayer(layer.Layer):
    def __init__(self):
        super(StartLayer, self).__init__()
        self.bg = sprite.Sprite('img/bg.png')
        self.bg.position = config.WINDOS_WIDTH//2,config.WINDOS_HEIGHT//2
        self.add(self.bg,z = 0)

        logo = sprite.Sprite('img/logo.png')
        logo.position = config.WINDOS_WIDTH // 2, config.WINDOS_HEIGHT // 2+300
        logo.scale = 0.3
        self.add(logo,z = 2)


        feiji = sprite.Sprite('img/hero/hero2.png')
        feiji.position = config.WINDOS_WIDTH // 2, config.WINDOS_HEIGHT // 2+150
        feiji.scale = 0.5
        self.add(feiji,z=2)

        start_menu = StartMenu()
        self.add(start_menu,z=2)

class StartScene(scene.Scene):
    def __init__(self):
        start_layer = StartLayer()
        super(StartScene, self).__init__(start_layer)



