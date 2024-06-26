from engine import *
from engine.config.gen_arch import *

#NEED TO WORK
#DEV[0] = False
DEV[1] = True
WEB_MOD_DEFAULT = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

VER : str = "1.3.0"
VER_COM :str = "1.1.8.2"
COMPILER : str = "20ed71461bba82440a6e981e1a8799788b21c337"

_LB_STORE :list[Label] = []
LB_CUR :Label = ...

_yes_ = ["Y", "y", "yes"]
JUMP_LINE = "\n>  "

def _select_menu_print(obj:list):
    c=0
    for name in obj:
        c+=1
        print(f"NAME: {name} <---> ID: {c}")
    del c, name


def _char_men(*nm):
    """
    menu = Page(105, 9)
    menu.create_text("TYPE: Character", "UPPER")
    menu.create_text("NAME....", "CUSTOM", (1,3))
    menu.create_text("name...", "CUSTOM", (1,4))

    menu.create_text("COLOR", "CUSTOM", (24, 3))
    menu.create_text("color...", "CUSTOM", (24,4))

    menu.create_text("TEXT SIZE", "CUSTOM", (44, 3))
    menu.create_text("text: num", "CUSTOM", (44, 4))

    menu.create_text("SAVE", "CUSTOM", (1, 7))

    menu.create_text("COMPILED: num", "CUSTOM", (86, 7))
    menu.create_text("APP VER: num", "CUSTOM", (60, 7))

    del menu
    menu:Page=nm[1][0]
    """
    print(nm)

def _char(*nm):
    menu:Page=nm[1][0]
    if not len(_LB_STORE) == 0:
        match nm[0][0]:
            case choice if choice in _yes_:#YES :D
                name:str;text:int
                name, text = [input(f"What's the name of your character?{JUMP_LINE}"), 
                              int(input(f"What's would be the text size?{JUMP_LINE}"))]
                LB_CUR.add_character(name, text_size=text)
            case choice if not choice in _yes_:#NO :c
                _select_menu_print(LB_CUR.char_simple)
                LB_CUR.del_character(int(input(f"What character u want to delete (ID)?{JUMP_LINE}"))-1)
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)

    menu.start_cast()

def _sour(*nm):
    ...

def _if_men(*nm):
    """
    menu = Page(70, 15)
    menu.create_text("TYPE: IF", "UPPER")

    menu.create_text("CONDITIONS CREATED", "CUSTOM", (17, 1))
    menu.add_panel(17, 2, 52, 8, 0)

    menu.create_text("NEXT", "CUSTOM", (17, 11))
    menu.create_text("BACK", "CUSTOM", (30,11))

    menu.create_text("NAME SPACE", "CUSTOM", (1, 3))
    menu.create_text("name", "CUSTOM", (1, 4))

    menu.create_text("EDIT CON", "CUSTOM", (1, 6))
    menu.create_text("EDIT SAY", "CUSTOM", (1, 7))
    menu.create_text("SAVE", "CUSTOM", (1, 13))

    menu.create_text("COMPILED: num", "CUSTOM", (44, 13))
    menu.create_text("APP VER: num", "CUSTOM", (20, 13))
    del menu
    menu:Page=nm[1][0]
    """
    print(nm)

def _say_men(*nm):
    """
    menu = Page(60, 15)
    menu.create_text("TYPE: say", "UPPER")
    menu.create_text("NAME....", "CUSTOM", (1,3))
    menu.create_text("name...", "CUSTOM", (1,4))

    menu.create_text("MESSAGE", "CUSTOM", (1, 6))
    menu.create_text("message", "CUSTOM", (1, 7))

    menu.create_text("SAVE", "CUSTOM", (1,13))

    menu.create_text("COMPILED: num", "CUSTOM", (44, 13))
    menu.create_text("APP VER: num", "CUSTOM", (20, 13))
    del menu
    menu:Page=nm[1][0]
    """
    print(nm)

def _save(*nm):
    ...

def _con(*nm):
    ...

#MENU PRINCIPAL
nme:str;ver:str;aut:str;ch:list|bool;ctn:str
nme, ver, aut, ch, ctn = ["default", "1.0", "me", [1], WEB_MOD_DEFAULT]

MAX_NAME_LABEL = 10
MAX_NAME_CWD   = 10

menu = Page(105, 22)

menu.create_text(f"Current proyect working on: {nme}", "CUSTOM", (1,1))
menu.create_text(f"Current label working on: None", "CUSTOM", (1,2))

menu.create_text("Currect flowchart: Main", "CUSTOM", (46, 2))

menu.add_panel(0, 3, 20, 16, 0)
menu.add_panel(33, 3, 71, 14, 0)

#1
btn = Button(1, 4, "Set character", _char)
btn.caster(("You want add a character? (y/n)"), 
           menu)
menu.add_btn(btn)

#2
btn = Button(1,5, "Edit character", _char_men)
btn.caster((""), 
           menu)
menu.add_btn(btn)

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

menu.create_text(f"Compiled: {COMPILER[:10]}", "CUSTOM", (80, 20))
menu.create_text(f"App ver: {VER}/{VER_COM}", "CUSTOM", (57, 20))

#menu.get_pre_view()
menu.start_cast()


