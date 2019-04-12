#encoding:utf-8

from cx_Freeze import setup,Executable
import sys

# base = None
# if sys.platform == 'win32':
#     base = 'Win32GUI'
#
# build_options={
#     'build_exe':{
#         "packages":['pyglet',"pygame",'cocos'],
#         "include_files":['img','sounds']
#     }
# }
#
# setup(
#     name=u'WarOfAircraft',
#     version = '1.0',
#     description='feijidazhan',
#     options = build_options,
#     executables=[Executable('main.py', base=base, icon="imgs/icon.ico")],
# )

base = None
if sys.platform == "win32":
    base = "Win32GUI"


build_options = {
    "build_exe":{
        "packages":["pyglet","pygame","cocos"],
        "include_files": ['img','sounds']
    }
}


setup(
    name = "WarOfAircraft",
    version = "0.1",
    description = "feijidazhan",
    options = build_options,
    executables = [Executable('main.py',base=base,icon="img/icon.ico")],
)