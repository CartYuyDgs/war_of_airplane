#encoding:utf-8

from cocos import director
from StartPage import StartScene
from GamePage import GameScene
import config
from events import feiji_event



def on_game_start():
    director.director.replace(GameScene())
feiji_event.push_handlers(on_game_start)

def main():
    main_direct = director.director
    main_direct.init(width= config.WINDOS_WIDTH,height=config.WINDOS_HEIGHT,caption=u'飞机大战')
    main_scene = StartScene()

    main_direct.run(main_scene)

if __name__ == '__main__':
    main()