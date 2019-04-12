#encoding:utf-8
from cocos import scene,layer,menu,sprite,director,text
import config
from GameMenu import BaseMenu
from events import feiji_event


class GameOverLayer(layer.Layer):
    def __init__(self,score):
        super(GameOverLayer, self).__init__()

        self.bg = sprite.Sprite('img/bg.png')
        self.bg.position = config.WINDOS_WIDTH // 2, config.WINDOS_HEIGHT // 2
        self.add(self.bg, z=0)

        feiji = sprite.Sprite('img/hero/hero1.png')
        feiji.position = config.WINDOS_WIDTH//2,config.WINDOS_HEIGHT-200
        feiji.scale = 0.5
        self.add(feiji)

        score_label = text.Label(u'得分：%d'%score,font_size=20,font_name="Microsoft Yahei",color=(10,10,10,255),anchor_x="center",anchor_y="center")
        score_label.position = config.WINDOS_WIDTH//2,config.WINDOS_HEIGHT-300
        self.add(score_label)

class GameOverMenu(BaseMenu):
    def __init__(self):
        super(GameOverMenu, self).__init__()

    def menu_items(self):
        rest_menu = menu.ImageMenuItem('img/btn2.png',callback_func=self.rest_game)
        return [rest_menu]

    def rest_game(self):
        feiji_event.dispatch_event('on_game_start')


class GameOverScene(scene.Scene):
    def __init__(self,score):
        over_layer = GameOverLayer(score)
        over_menu = GameOverMenu()
        super(GameOverScene, self).__init__(over_layer,over_menu)
