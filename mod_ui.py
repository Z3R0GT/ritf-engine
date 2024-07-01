from pickle import TRUE
from engine import *
from engine.config.gen_arch import *

#NEED TO WORK
#DEV[0] = False
DEV[1] = True

from os import chdir, path, listdir, mkdir, getcwd, remove
from time import sleep

WEB_MOD_DEFAULT = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

VER : str = "1.3.0"
VER_COM :str = "1.1.8.2"
COMPILER : str = "20ed71461bba82440a6e981e1a8799788b21c337"

_LB_STORED :list[Label] = []
LB_CUR :Label = ...

_yes_ = ["Y", "y", "yes"]
JUMP_LINE = "\n>  "

_PRE_ACRO_GAME = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
_PRE_ALL_GAME  = ["Snowy", "Magma", "Vivian", "Margaret", 
             "Asher", "Ember", "Opal", "Thomas"]

def _select_menu_print(obj:list):
    c=0
    for name in obj:
        c+=1
        print(f"NAME: {name} <---> ID: {c}")
    del c, name

def _str_say_menu(LIM_TEXT=35, obj:list=...) -> list[str]:
    temp = []
    for line in obj:
        if line[:11] == "init python":
            continue

        if not line.replace(" ", "")[:6] == "return":
            temp.append(line[len(LB_CUR.tab):LIM_TEXT+len(LB_CUR.tab)].replace("\n", "").replace("\"", ""))
    return temp

def _btn_on(menu:Page, ID_NEXT, ID_BACK, lst, LIM_TEXT=35):
    menu.btns[ID_NEXT].var[3] = _str_say_menu(LIM_TEXT, lst)
    menu.btns[ID_BACK].var[3] = _str_say_menu(LIM_TEXT, lst)
    menu.btns[ID_BACK].var[8] = True

    menu.execute_btn(ID_BACK+1)

    menu.btns[ID_BACK].var[8] = True


def _edi_(*nm):
    menu:Page = nm[1][0]

    if nm[1][1] == "non":
        menu.start_cast()

    match nm[1][1]:
        case "name":
            value = input(f"What's the new name?{JUMP_LINE}")
        case "color":
            value = input(f"What's the color?{JUMP_LINE}")
        case "textzs":
            value = int(input(f"What's the new text size?{JUMP_LINE}"))
        case "message":
            value = input(f"What do u want that this character say instead of the other one?{JUMP_LINE}")

    match nm[1][2]:
        case "char":
            match nm[1][1]:
                case choice if choice == "name":
                    menu.btns[0].character = value
                    menu.add_btn(menu.btns[0], False)
                case choice if choice == "color":
                    menu.btns[1].character = value
                    menu.add_btn(menu.btns[1], False)
                case choice if choice == "textzs":
                    menu.btns[2].character = value
                    menu.add_btn(menu.btns[2], False)

            LB_CUR.edit_character(nm[1][3], choice, value)  

        case "say":
            match nm[1][1]:
                case choice if choice == "name":
                    menu.create_text(" "*40, "CUSTOM", (1, 4))
                    menu.btns[0].character = value
                    menu.add_btn(menu.btns[0], False)
                case choice if choice == "message":
                    for i in range(6):
                        menu.create_text(" "*40, "CUSTOM", (1, 7+i))

                    menu.btns[1].character = value
                    menu.add_btn(menu.btns[1], False)

            match nm[1][4]:
                case "normal":
                    LB_CUR.edit_say(nm[1][3]+1, "normal", choice, value)

                    _btn_on(nm[1][5], 10, 11, LB_CUR.dialog)
                case "if":
                    id_if  = int(input("What's the 'if' ID?"))
                    print(id_if)

    menu.start_cast()

def _char_men(*nm):
    _select_menu_print(LB_CUR.char_simple)
    sel = int(input(f"What's the character's ID?{JUMP_LINE}"))
    name  = LB_CUR.char_simple[sel-1][0][:22]
    color = LB_CUR.char_simple[sel-1][1]
    text  = LB_CUR.char_simple[sel-1][2]

    menu = Page(60, 9)

    menu.create_text("TYPE: Character", "UPPER")
    menu.create_text("NAME", "CUSTOM", (1, 3))
    menu.create_text("|",    "CUSTOM", (23,3))
    menu.create_text("|",    "CUSTOM", (23,4))
    #1
    btn = Button(1,4, name , _edi_)
    btn.var = [menu, "name", "char",sel]
    menu.add_btn(btn)

    menu.create_text("COLOR", "CUSTOM", (24,3))
    menu.create_text("|",     "CUSTOM", (43,3))
    menu.create_text("|",     "CUSTOM", (43,4))
    #2
    btn = Button(24, 4, color, _edi_)
    btn.var = [menu, "color", "char",sel]
    menu.add_btn(btn)

    menu.create_text("TEXT SIZE", "CUSTOM", (44, 3))
    menu.create_text("|",         "CUSTOM", (58, 3)) 
    menu.create_text("|",         "CUSTOM", (58, 4)) 
    #3
    btn = Button(44, 4, str(text), _edi_)
    btn.var = [menu, "textzs", "char",sel]
    menu.add_btn(btn)

    #4
    btn = Button(1, 7, "Save", _edi_)
    btn.var = [nm[1][0], "non"]
    menu.add_btn(btn)

    menu.create_text(f"Compiled: {COMPILER[:10]}", "CUSTOM", (38, 7))
    menu.create_text(f"App ver: {VER}/{VER_COM}", "CUSTOM", (14, 7))

    menu.start_cast()

def _char(*nm):
    menu:Page=nm[1][0]

    if not len(_LB_STORED) == 0:
        match nm[0][0]:
            case choice if choice in _yes_:#YES :D
                name:str;text:int
                name, text = [input(f"What's the name of your character?{JUMP_LINE}"), 
                              int(input(f"What's would be the text size?{JUMP_LINE}"))]
                LB_CUR.add_character(name, text_size=text)

            case choice if not choice in _yes_:#NO :c
                _select_menu_print(LB_CUR.char_simple)
                LB_CUR.del_character(int(input(f"What character u want to delete (ID)?{JUMP_LINE}")))
            case _:
                print(nm[1])

    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)

    menu.start_cast()

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

def _if(*nm):

    print(nm)

def _say_men(*nm):
    sel = int(input(f"What's the say's ID?{JUMP_LINE}"))+nm[1][1]
    if not len(LB_CUR._say_obj) == 0 or not "$" in LB_CUR.dialog[sel]:
        menu = Page(60, 15)
        
        type_op:str = nm[1][3][1]
        match type_op:
            case "normal":
                name = [menu, "name",   "say", sel, type_op, nm[1][0]]
                mess = [menu, "message","say", sel, type_op, nm[1][0]]
            case "if":
                name = ...
                mess = ...

        sa = LB_CUR._say_obj[sel]
        
        menu.create_text("TYPE: say", "UPPER")
        menu.create_text("NAME", "CUSTOM", (1,3))
        #1
        btn = Button(1,4, sa.name, _edi_)
        btn.var = name
        menu.add_btn(btn)

        menu.create_text("MESSAGE", "CUSTOM", (1, 6))
        #2
        btn = Button(1,7, sa.message, _edi_)
        btn.var = mess
        menu.add_btn(btn)

        #3
        btn = Button(1, 13, "Save", _edi_)
        btn.var = [nm[1][0], "non"]
        menu.add_btn(btn)

        menu.create_text(f"Compiled: {COMPILER[:10]}", "CUSTOM", (38, 13))
        menu.create_text(f"App ver: {VER}/{VER_COM}", "CUSTOM", (14, 13))
    else:
        print_debug("U NEED CREATE MORE 'say' objects or maybe, your line is not convertable")
        sleep(5)
        menu:Page = nm[1][0]
    
    menu.start_cast()

def _say(*nm):
    menu:Page   = nm[1][0]
    type_op:str = nm[1][3][1]


    if not len(_LB_STORED) == 0:
        if nm[0][0] in _yes_:
            match type_op:
                case operation if input(f"Do you want to use pre-define characters? (y/n){JUMP_LINE}") in _yes_:
                    _select_menu_print(_PRE_ALL_GAME)
                    acro_name = _PRE_ACRO_GAME[int(input(f"What's the ID (number)?{JUMP_LINE}"))-1]
                
                case operation  if input(f"Is your character still exits? (y/n){JUMP_LINE}") in _yes_:
                    _select_menu_print(LB_CUR.char_simple)
                    acro_name = int(input(f"What's the ID (number)?{JUMP_LINE}"))
                
                case operation if input(f"Do you want just use a character's name (we don't save it)? (y/n){JUMP_LINE}") in _yes_:
                    acro_name = input(f"What's the name?{JUMP_LINE}")

                case operation:
                    acro_name = ""

            message   = input(f"What do u want that this character say?{JUMP_LINE}")
            if operation == "normal":
                LB_CUR.add_say(acro_name, operation, message)
            elif operation == "if":
                id_con = nm[1][2]
                id_if  = int(input("What's the 'if' ID?"))

                #LB_CUR.add_say(acro_name, operation, message, id_con, id_if)
                print(acro_name, operation, message, id_con, id_if)
        else:
            id_say = int(input(f"What's the say's ID?{JUMP_LINE}"))+nm[1][1]
            match type_op:
                case "normal":
                    LB_CUR.del_say(id_say, "normal")
                
                case "if":
                    id_con = nm[1][2]
                    id_if  = int(input("What's the 'if' ID?"))
                
                    #LB_CUR.del_say(id_say, "if", id_con, id_if)
                    print(id_say, "if", id_con, id_if)

        match operation:
            case "normal":
                _btn_on(menu, 10, 11, LB_CUR.dialog)
            case "if":
                print("if")
    
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)

    menu.start_cast()

def _sou_men(*nm):
    menu:Page=nm[1][0]

    if not len(_LB_STORED) <= 0 or len(LB_CUR._init_obj) <= 0:
        type_op = input(f"What's the mode? (ADD-1; EDIT-2; DEL-3; INSERT-4){JUMP_LINE}")
        match type_op:
            case choice if choice == "1" or choice == "ADD":
                choice = "ADD"
                dia = 0
            case choice if choice == "2" or choice == "EDIT":
                choice = "EDIT"
                dia = int(input(f"Where's the dialog?{JUMP_LINE}"))
            case choice if choice == "3" or choice == "DEL":
                choice = "DEL"
                dia = int(input(f"Where's the dialog?{JUMP_LINE}"))
            case choice if choice == "4" or choice == "INSERT":
                choice = "INSERT"
                dia = int(input(f"Where's the dialog?{JUMP_LINE}"))
            case _:
                choice = "ADD"
                dia = 0

        mode = nm[0][0]
        match mode:
            case "1":
                mode = "name"
            case "2":
                mode = "value"
            case _:
                mode = "name"

        type_obj = nm[1][3][1]
        ID_SEL:int = int(nm[0][2])+nm[1][1]


        match type_obj:
            case "normal":
                LB_CUR.edit_source(ID_SEL, mode, 
                                   nm[0][1], 
                                   type_obj, 
                                   choice, 
                                   dia)
                
                _btn_on(menu, 10, 11, LB_CUR.dialog)
            case "if":
                ...

    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)

    menu.start_cast()

def _sou(*nm):
    menu:Page = nm[1][0]
    if not len(_LB_STORED) == 0:
        qu = f"Are you sure (this acction may erase all reference of your variable, but if/condition){JUMP_LINE}"
        if nm[0][0] in _yes_:
            nm = input(f"What's the name of your variable?{JUMP_LINE}")
            vl = input(f"What's the value?{JUMP_LINE}")
            LB_CUR.add_source(nm, vl)

        elif not len(LB_CUR._init_obj) <= 0 and input(qu) in _yes_:

            ID = int(input("What's the ID?"))
            LB_CUR.del_source(ID)

        _btn_on(menu, 12, 13, LB_CUR.init, 12)
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
    menu.start_cast()
    
def _save(*nm):
    

    print(*nm)

def _con(*nm):
    menu:Page=nm[1][0]

    menu.edit_panel_w_btn(nm[1][1],
                          nm[1][2],
                          nm[1][3],
                          nm[1][4], 
                          nm[1][5], 
                          nm[1][6], 
                          nm[1][7],
                          nm[1][8])
    if not nm[1][7][0]:
        menu.start_cast()

def _sel(*nm):
    menu:Page=nm[1][0]
    print(nm)


chdir(getcwd()+"/proyects/default")
ROOT_LOCAL = getcwd()
global_config(cwd=ROOT_LOCAL)

#FOR TEST
_LB_STORED.append(Label(1, "owo", [1], 1))
_LB_STORED[0].add_character("pedro")
LB_CUR = _LB_STORED[-1]

#MENU PRINCIPAL
nme:str;ver:str;aut:str;ch:list|bool;ctn:str
nme, ver, aut, ch, ctn = ["default", "1.0", "me", [1], WEB_MOD_DEFAULT]

MAX_NAME_LABEL = 10
MAX_NAME_CWD   = 10

menu = Page(105, 22)

menu.create_text(f"Current proyect working on: {nme}", "CUSTOM", (1,1))
menu.create_text(f"Current label working on: None", "CUSTOM", (1,2))

menu.create_text("Currect flowchart: Main", "CUSTOM", (46, 2))
menu.create_text("Variables Created", "CUSTOM", (85,2))

menu.add_panel(0,  3, 20, 16, 0)
menu.add_panel(33, 3, 48, 14, 0)
menu.add_panel(83, 3, 20, 14, 0)

#1-0
btn = Button(1, 4, "Set character", _char, "char_nm")
btn.caster(("You want add a character? (y/n)"), 
           menu)
menu.add_btn(btn)

#2-1
btn = Button(1,5, "Edit character", _char_men, "char_men")
btn.caster((""), 
           menu)
menu.add_btn(btn)

#3-2
btn = Button(1,7, "Set source", _sou, "sou_nm")
btn.caster(("You want add a 'source'? (y/n)"), 
           menu)
menu.add_btn(btn)

#4-3
btn = Button(1,8, "Edit source", _sou_men, "sou_men")
btn.caster(("What u want change? (name - 1 /value - 2)", 
            "What's the new value?", 
            "What's the ID?"),
           menu, True, 0)
menu.add_btn(btn)

#5-4
btn = Button(1, 10, "Add if", _if, "if_nm")
btn.caster(("What's the varible's name?", "What's the value?", "What's name of this condition?"), 
           menu)
menu.add_btn(btn)

#6-5
btn = Button(1, 11, "Edit if", _if_men, "if_men")
btn.caster(("What's ID of the condition?"), menu)
menu.add_btn(btn)

#7-6
btn = Button(1, 13, "Set say", _say, "say_nm")
btn.caster(("You want add a say? (y/n)"), 
           menu, "normal")
menu.add_btn(btn)

#8-7
btn = Button(1, 14, "Edit say", _say_men, "say_men")
btn.caster((""), menu)
menu.add_btn(btn)

#9-8
btn = Button(1, 16, "Export mod", _save, "save")
btn.caster((""), menu)
menu.add_btn(btn)

#10-9
btn = Button(1, 18, "Back menu", DEFAULT="BACK")
menu.add_btn(btn)


#11-10
btn = Button(33, 18, "Next", _con, "next")
btn.caster((""), menu, 
           2,
           10,
           ["Create a new say!",
            "That will appear here"],
           (11, 12),
           (5, 6, 7, 8),
           (10, 20),
           [True, "normal"],
           False
           )
menu.add_btn(btn)

#12-11
btn = Button(42, 18, "Back", _con, "back")
btn.caster((""), menu, 
           2,
           10,
           ["Create a new say!",
            "That will appear here"],
           (11, 12),
           (5, 6, 7, 8),
           (0, 10),
           [True, "normal"],
           False
           )
menu.add_btn(btn)


#13-12
btn = Button(85, 18, "Next", _con)
btn.caster((""), menu,
           3,
           10,
           ["Create vars", 
            "Here"],
           (13, 14),
           (3, 4),
           (10, 20),
           [True, "normal"],
           False
           )
menu.add_btn(btn)

#14-13
btn = Button(95, 18, "Back", _con)
btn.caster((""), menu, 
           3,
           10,
           ["Create vars",
            "Here"],
           (13, 14),
           (3, 4),
           (0, 10),
           [True, "normal"],
           False
           )
menu.add_btn(btn)

#15-14
btn = Button(1, 20, "Select flowchart", _sel)
btn.caster(("You want change to a 'if'? (y/n)"), menu)
menu.add_btn(btn)

menu.create_text(f"App ver: {VER}/{VER_COM}", "CUSTOM", (50, 20))
menu.create_text(f"Compiled: {COMPILER[:10]}", "CUSTOM", (80, 20))

menu.execute_btn(12)
menu.execute_btn(14)

menu.btns[11].var[8] = False
menu.btns[13].var[8] = False

menu.btns[11].var[7][0] = False
menu.btns[13].var[7][0] = False


menu.start_cast()
#menu.get_pre_view()

