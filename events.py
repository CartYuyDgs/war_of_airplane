#encoding=utf-8
from pyglet import event

class FJEventDispatcher(event.EventDispatcher):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(FJEventDispatcher, cls).__new__(cls)
        return cls.__instance

feiji_event = FJEventDispatcher()

FJEventDispatcher.register_event_type('on_bullet_resuable')
FJEventDispatcher.register_event_type('on_enemy_resuable')
FJEventDispatcher.register_event_type('on_game_over')
FJEventDispatcher.register_event_type('on_game_start')
FJEventDispatcher.register_event_type('on_game_pause')
FJEventDispatcher.register_event_type('on_game_resume')