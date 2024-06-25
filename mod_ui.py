from engine import *
from engine.config.gen_arch import *

#NEED TO WORK
#DEV[0] = False
DEV[1] = True

menu = Page(105, 22)
menu.create_text("PROYECT NAME: name", "CUSTOM", (1,1))
menu.create_text("LABEL NAME:name", "CUSTOM", (1,2))

menu.create_text("CURRENT WORK DIRECTORY: name", "CUSTOM", (46, 2))

menu.add_panel(0, 3, 20, 16, 0)
menu.add_panel(33, 3, 71, 14, 0)

menu.create_text("SET CHAR", "CUSTOM", (1, 4))
menu.create_text("EDIT CHAR", "CUSTOM", (1,5))

menu.create_text("SET SOURCE", "CUSTOM", (1,7))
menu.create_text("EDIT SOURCE", "CUSTOM", (1,8))

menu.create_text("SET IF", "CUSTOM", (1, 10))
menu.create_text("EDIT IF", "CUSTOM", (1,11))

menu.create_text("SET SAY", "CUSTOM", (1, 13))
menu.create_text("EDIT SAY", "CUSTOM", (1, 14))

menu.create_text("EXPORT MOD", "CUSTOM", (1,16))
menu.create_text("BACK MENU", "CUSTOM", (1, 18))

menu.create_text("NEXT", "CUSTOM", (33, 18))
menu.create_text("BACK", "CUSTOM", (40, 18))

menu.create_text("BACK MAIN WORK DIR", "CUSTOM", (81, 18))

menu.create_text("COMPILED: num", "CUSTOM", (86, 20))
menu.create_text("APP VER: num", "CUSTOM", (60, 20))

menu.get_pre_view()