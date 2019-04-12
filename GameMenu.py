#encoding:utf-8
from cocos import menu
from cocos import director
from cocos.audio import pygame

class BaseMenu(menu.Menu):
    pygame.mixer.init()
    select_sound = pygame.mixer.Sound('sounds/card.ogg')

    def __init__(self):
        super(BaseMenu, self).__init__()
        self.font_item['font_size'] = 40
        self.font_item_selected['font_size'] = self.font_item['font_size']
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (192, 192, 192, 255)
        # self.start_menu = menu.ImageMenuItem('img/btn1.png', self.start_game)
        self.end_menu = menu.ImageMenuItem('img/btn3.png', self.end_game)

        menu_items = self.menu_items()
        menu_items.append(self.end_menu)
        self.create_menu(menu_items, selected_effect=menu.shake(),
                         activated_effect=menu.shake_back())

    def menu_items(self):
        raise NotImplementedError


    def end_game(self):
        director.director.terminate_app = True
        #print('end game')
