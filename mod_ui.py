from engine import *
from engine.config.gen_arch import *

#NEED TO WORK
#DEV[0] = False
DEV[1] = True

from os import chdir, path, listdir, mkdir, getcwd, remove
from time import sleep

WEB_MOD_DEFAULT = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

VER : str = "1.3.0"
VER_COM :str = "1.1.8.8"
COMPILER : str = "944c5d561e60c5e6c1667dae8c214141517a19a7"

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

def de_cip(word:str) -> int:
    c=0
    for _in in word:
        c+=1
        if _in == "_":
            break
    return c

def _str_say_menu(LIM_TEXT=35, obj:list=...) -> list[str]:
    temp = []
    for line in obj:
        if f"{line}".isnumeric():
            temp.append(f"{line} {LB_CUR._if_obj[line].name[:LIM_TEXT]}")
            continue

        if line[:11] == "init python":
            continue

        if not line.replace(" ", "")[:6] == "return":
            temp.append(line[len(LB_CUR.tab):LIM_TEXT+len(LB_CUR.tab)].replace("\n", "").replace("\"", ""))
    return temp


def _btn_on(menu:Page, ID_NEXT, ID_BACK, lst, LIM_TEXT=35, execute=True):
    menu.btns[ID_NEXT].var[3] = _str_say_menu(LIM_TEXT, lst)
    menu.btns[ID_BACK].var[3] = _str_say_menu(LIM_TEXT, lst)
    menu.btns[ID_BACK].var[8] = True

    if execute:
        menu.execute_btn(ID_BACK+1)

    menu.btns[ID_BACK].var[8] = False

def __eval_mod_(choice:str):
    match choice:
        case eval_mod if eval_mod == "1" or eval_mod == "==" or eval_mod == "equal":
            eval_mod = "equal"
        case eval_mod if eval_mod == "2" or eval_mod == ">=" or eval_mod == "geater":
            eval_mod = "geater"
        case eval_mod if eval_mod == "3" or eval_mod == "<=" or eval_mod == "smaller":
            eval_mod = "smaller"
        case eval_mod if eval_mod == "4" or eval_mod == "!=" or eval_mod == "not":
            eval_mod = "not"
        case _:
            eval_mod = "equal"

    return eval_mod

def _edi_(*nm):
    menu:Page = nm[1][0]

    if nm[1][1] == "non":
        menu.execute_btn(nm[1][2])
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
                    LB_CUR.edit_say(nm[1][3]+1, nm[1][4], choice, value)
                    _btn_on(nm[1][5], 10, 11, LB_CUR.dialog)

                case "if":
                    LB_CUR.edit_say(nm[1][3],   nm[1][4], choice, value, nm[1][6], nm[1][7])
                    _lst = []

                    for i in LB_CUR._if_obj[nm[1][6]-1].dialog:
                        _lst.append(LB_CUR.tab+f"{i}_con\n")
                        for n in LB_CUR._if_obj[nm[1][6]-1].dialog[i]:
                            _lst.append(n[4:])

                    _btn_on(nm[1][5], 6, 7, _lst, execute=False)

    menu.start_cast()

def paths_finder() -> tuple[list[str], bool, list[str]]:
    global ROOT_LOCAL

    chdir(ROOT_LOCAL+"/.config/autosaves")
    info = list(filter(path.isfile, listdir()))

    if len(info) == 0:
        chdir(ROOT_LOCAL)
        return ["pass"]
    
    if "end.json" in info:
        name_loaded = ["end.json"]
        ch = True
    else:
        name_loaded = ["temp_ñ_0.json"]

        for names in info:
            name_from = names[5:].replace(".json", "")
            if not names in name_loaded:
                name_to = name_loaded[-1][5:].replace(".json", "")

                num_from, num_to = de_cip(name_from), de_cip(name_to)
                if name_from[:num_from-1] == name_to[:num_to-1] and \
                    int(name_from[num_from:]) >= int(name_to[num_to:]):

                    name_loaded[-1] = names
                else:
                    name_loaded.append(names)
        if name_loaded[0] == "temp_ñ_0.json":
            del name_loaded[0]
        ch = False

    lst = []
    if not len(name_loaded) == 1:
        for name in name_loaded:
            lst.append(getcwd()+f"/{name}")
    else:
        lst.append(getcwd()+"/"+name_loaded[0])
        
    return lst, ch, info

def loader_label():
    global ROOT_LOCAL
    from json import load

    info = paths_finder()

    info_load:list[dict] = []
    if info[1]:
        with open(info[0][0], "r") as file:
            dit = load(file)

            for in_ in dit["root"]:
                info_load.append(dit["root"][in_])
    else:
        if len(info[0]) == 1:
            info_load.append(load(open(info[0][0], "r")))
        else:
            for paths in info[0][0]:
                with open(paths, "r") as file:
                    info_load.append(load(file))

    #Eraser of all archive
    for paths in info[2]:
        remove(paths)

    for info in info_load:
        create_instance(info)

    chdir(ROOT_LOCAL)
    return
        

def _char_men(*nm):
    if not len(_LB_STORED) == 0:
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
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        _sel(["y"], nm[1])
        return
    
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
        _sel(["y"], nm[1])
        return
    
    menu.start_cast()

def _c0n(*nm):
    menu:Page = nm[1][0]

    match nm[0][0]:
        case choice if choice == "1" or choice.lower() == "add":
            vr1 = input(f"What's the value?{JUMP_LINE}")
            vr2 = input(f"What's the another value{JUMP_LINE}")

            eval_mod = input(f"What's operator? (equal/==/1, geater/>=/2, smaller/<=/3, not/!=/4){JUMP_LINE}")
            eval_mod = __eval_mod_(eval_mod)

            LB_CUR.edit_condition(nm[1][1], vr1, vr2, "ADD", eval_mod)
        case choice if choice == "2" or choice.lower() == "edit":
            c = int(input(f"What's the condition ID{JUMP_LINE}"))

            vr1 = input(f"What's the value?{JUMP_LINE}")
            vr2 = input(f"What's the another value{JUMP_LINE}")

            eval_mod = input(f"What's operator? (equal/==/1, geater/>=/2, smaller/<=/3, not/!=/4){JUMP_LINE}")
            eval_mod = __eval_mod_(eval_mod)

            LB_CUR.edit_condition(nm[1][1], vr1, vr2, "EDIT", eval_mod, c)

        case choice if choice == "3" or choice.lower() == "del":
            c = int(input(f"What's the condition ID{JUMP_LINE}"))

            LB_CUR.edit_condition(nm[1][1], ..., ..., "DEL", ..., c+1)
        case _:
            vr1 = input(f"What's the value?{JUMP_LINE}")
            vr2 = input(f"What's the another value{JUMP_LINE}")

            eval_mod = input(f"What's operator? (equal/==/1, geater/>=/2, smaller/<=/3, not/!=/4){JUMP_LINE}")
            eval_mod = __eval_mod_(eval_mod)

            LB_CUR.edit_condition(nm[1][1], vr1, vr2, "ADD", eval_mod)
    _lst = []
    for con in LB_CUR._if_obj[nm[1][1]].condition:
        _lst.append(con[0][:6]+con[1]+ con[2][:6])

    menu.btns[4].var[3] = _lst
    menu.btns[5].var[3] = _lst

    menu.btns[5].var[7][0] = True

    menu.execute_btn(6)
    
    menu.btns[5].var[7][0] = False
    
    menu.start_cast()

    
def _if_men(*nm):
    menu = Page(105, 22, NMO="owo")
    if not len(_LB_STORED) <= 0:
        ID_CUR:int = int(nm[0][0])+nm[1][1]
        _if_ = LB_CUR._if_obj[ID_CUR]

        menu.add_panel(0,  5, 20, 11, 0) #CONTIDTIONS
        menu.add_panel(33, 3, 48, 14, 0) #DIALOG
        menu.add_panel(83, 3, 20, 14, 0) #VAR

        menu.create_text(f"Name Space: {_if_.name[:10]}", "UPPER")

        menu.create_text("CONDITIONS (con)", "CUSTOM", (1,4))

        menu.create_text(f"Currect flowchart: {_if_.name[:10]}", "CUSTOM", (46, 2))
        menu.create_text("Variables Created", "CUSTOM", (85,2))

        #1-0
        btn = Button(20, 6, "Set say", _say)
        btn.caster(("You want add a say? (y/n)"), menu, "if", ID_CUR)
        menu.add_btn(btn)

        #2-1
        btn = Button(20, 7, "Edit say", _say_men)
        btn.caster(("What's the 'if' ID?"), menu)
        menu.add_btn(btn)

        #3-2
        btn = Button(20, 9, "Edit con", _c0n)
        btn.caster(("U want ADD-1/EDIT-2/DEL-3 a condition?"), menu, ID_CUR)
        menu.add_btn(btn)

        #4-3
        btn = Button(20, 10, "Edit vars", _sou_men)
        btn.caster(("What u want change? (name - 1/value -2)",
                    "What's the new value?",
                    "What's the ID",
                    "What's if's ID?"), 
                    menu, False, 0)
        menu.add_btn(btn)

        _lst = []
        for con in LB_CUR._if_obj[ID_CUR].condition:
            _lst.append(con[0][:6]+con[1]+ con[2][:6])

        #5-4
        btn = Button(1, 17, "Next", _con)
        btn.caster((""), menu,
                   1,
                   10,
                   _lst,
                   (5, 6),
                   (3),
                   (10, 20),
                   [True, ID_CUR],
                   False)
        menu.add_btn(btn)

        #6-5
        btn = Button(12, 17, "Back", _con)
        btn.caster((""), menu,
                   1,
                   10,
                   _lst,
                   (5, 6),
                   (3),
                   (0, 10),
                   [True, ID_CUR],
                   False)
        menu.add_btn(btn)

        #7-6
        btn = Button(33, 18, "Next", _con, "next")
        btn.caster((""), menu, 
                2,
                10,
                ["Create a new say!",
                    "That will appear here"],
                (7, 8),
                (1, 2),
                (10, 20),
                [True, "if", ID_CUR],
                False
                )
        menu.add_btn(btn)

        #8-7
        btn = Button(42, 18, "Back", _con, "back")
        btn.caster((""), menu, 
                2,
                10,
                ["Create a new say!",
                    "That will appear here"],
                (7, 8),
                (1, 2),
                (0, 10),
                [True, "if", ID_CUR],
                False
                )
        menu.add_btn(btn)

        #9-8
        btn = Button(85, 18, "Next", _con)
        btn.caster((""), menu,
                3,
                10,
                _str_say_menu(20, LB_CUR.init),
                (9, 10),
                (4),
                (10, 20),
                [True, "if", ID_CUR],
                False
                )
        menu.add_btn(btn)

        #10-9
        btn = Button(95, 18, "Back", _con)
        btn.caster((""), menu, 
                3,
                10,
                _str_say_menu(20, LB_CUR.init),
                (9, 10),
                (4),
                (0, 10),
                [True, "if", ID_CUR],
                False
                )
        menu.add_btn(btn)

        menu.execute_btn(6)
        menu.execute_btn(8)
        menu.execute_btn(10)

        menu.btns[5].var[7][0] = False
        menu.btns[7].var[7][0] = False
        menu.btns[9].var[7][0] = False
        
        #11-10
        btn = Button(1, 20, "Save", ...)
        btn.caster((""), menu)
        menu.add_btn(btn)

        menu.create_text(f"App ver: {VER}/{VER_COM}", "CUSTOM", (50, 20))
        menu.create_text(f"Compiled: {COMPILER[:10]}", "CUSTOM", (80, 20))

        menu.start_cast()
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        _sel(["y"], nm[1])
        return
    
def _if(*nm):
    menu:Page = nm[1][0]
    if not len(_LB_STORED) == 0 and not len(LB_CUR._init_obj) == 0:
        eval_mod = __eval_mod_(nm[0][1])

        var_from = LB_CUR._init_obj[int(nm[0][0])+1].name
        if nm[0][2].isnumeric():
            var_to = LB_CUR._init_obj[int(nm[0][2])+1].name
        else:
            var_to = nm[0][2]

        name_space = nm[0][3]

        LB_CUR.add_condition(var_from, var_to, eval_mod, name_space)

        _btn_on(menu, 10, 11, LB_CUR.dialog)
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        _sel(["y"], nm[1])
        return
    menu.start_cast()

def _say_men(*nm):
    if not len(_LB_STORED) == 0:
        sel = int(input(f"What's the say's ID?{JUMP_LINE}"))+nm[1][1]
        type_op:str = nm[1][3][1]

        match type_op:
            case "normal":
                var = not "$" in LB_CUR.dialog[sel]
            case "if":
                sel -= 1
                id_if  = int(nm[0][0])

                var = not "$" in LB_CUR._if_obj[nm[1][3][2]].dialog[id_if][sel]
        if not len(LB_CUR._say_obj) == 0 or var:
            menu = Page(60, 15)
            
            match type_op:
                case "normal":
                    ID = 12
                    name = [menu, "name",   "say", sel, type_op, nm[1][0]]
                    mess = [menu, "message","say", sel, type_op, nm[1][0]]
                    sa:say = LB_CUR._say_obj[sel]
                case "if":
                    ID = 8
                    name = [menu, "name",    "say", sel, type_op, nm[1][0], id_if+1, sel+1]
                    mess = [menu, "message", "say", sel, type_op, nm[1][0], id_if+1, sel+1]
                    id_con = nm[1][3][2]
                    
                    sa:say = LB_CUR._if_obj[id_con]._say_obj[id_if][sel]

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
            btn.var = [nm[1][0], "non", ID]
            menu.add_btn(btn)

            menu.create_text(f"Compiled: {COMPILER[:10]}", "CUSTOM", (38, 13))
            menu.create_text(f"App ver: {VER}/{VER_COM}", "CUSTOM", (14, 13))
        
        else:
            print_debug("U NEED CREATE MORE 'say' objects or maybe, your line is not convertable")
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        if input(f"U want be redirect to create a new label? (y/n){JUMP_LINE}") in _yes_:
            _sel(["y"], nm[1])
            return
        else:
            menu:Page=nm[1][0]
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
                    exists = True    
                case operation  if input(f"Is your character still exits? (y/n){JUMP_LINE}") in _yes_:
                    _select_menu_print(LB_CUR.char_simple)
                    acro_name = int(input(f"What's the ID (number)?{JUMP_LINE}"))
                    exists = True

                case operation if input(f"Do you want just use a character's name (we don't save it)? (y/n){JUMP_LINE}") in _yes_:
                    acro_name = input(f"What's the name?{JUMP_LINE}")
                    exists=False

                case operation:
                    acro_name = ""
                    exists=False
            
            #THIS'S IMPORTANT (case 'say' or 'if')
            message   = input(f"What do u want that this character say?{JUMP_LINE}")
            if operation == "normal":
                LB_CUR.add_say(acro_name, operation, message, exits=exists)
            elif operation == "if":
                id_con = nm[1][3][2]+1
                id_if  = int(input(f"What's the 'if' ID?{JUMP_LINE}"))+1

                LB_CUR.add_say(acro_name, operation, message, id_con, id_if, exists)
        else:
            #DEL CASE
            id_say = int(input(f"What's the say's ID?{JUMP_LINE}"))+nm[1][1]
            match type_op:
                case "normal":
                    LB_CUR.del_say(id_say, "normal")
                    operation = type_op
                
                case "if":
                    operation = type_op
                    id_con = nm[1][3][2]
                    id_if  = int(input(f"What's the 'if' ID?{JUMP_LINE}"))+1

                    LB_CUR.del_say(id_say, "if", id_con, id_if)

        match operation:
            case "normal":
                _btn_on(menu, 10, 11, LB_CUR.dialog)
            case "if":
                _lst = []

                for i in LB_CUR._if_obj[id_con-1].dialog:
                    _lst.append(LB_CUR.tab+f"{i}_con\n")
                    for n in LB_CUR._if_obj[id_con-1].dialog[i]:
                        _lst.append(n[4:])

                _btn_on(menu,  6,  7, _lst)
    
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        _sel(["y"], nm[1])
        return
    
    menu.start_cast()

def _sou_men(*nm):
    menu:Page=nm[1][0]

    if not len(_LB_STORED) == 0 and not len(LB_CUR._init_obj) == 0:
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
                LB_CUR.edit_source(ID_SEL, mode,
                                   nm[0][1],
                                   type_obj,
                                   choice,
                                   dia,
                                   nm[1][3][2]+1,
                                   int(nm[0][3])+1
                                   )
                _lst = []

                for i in LB_CUR._if_obj[nm[1][3][2]].dialog:
                    _lst.append(LB_CUR.tab+f"{i}_con\n")
                    for n in LB_CUR._if_obj[nm[1][3][2]].dialog[i]:
                        _lst.append(n[4:])

                _btn_on(menu, 6, 7, _lst)
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        _sel(["y"], nm[1])
        return
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
        _sel(["y"], nm[1])
        return
    
    menu.start_cast()
   
def _save_menu(root:str, lib:dict, nme_arch:str):
    with open(root+f"/{nme_arch}.rpy", "w") as file:
        file.write("")
        file.close()
    
    with open(root+f"/{nme_arch}.rpy", "a") as file:
        for nme in lib["root"]:

            for ch in lib["root"][nme]["character"][0]:
                for line in ch:
                    file.write(line)

            lst = lib["root"][nme]["init"].copy()
            del lst[0]

            if len(lst) >= 1:
                for init in lib["root"][nme]["init"]:
                    for line in init:
                        file.write(line)
            else:
                file.write(lib["root"][nme]["init"][0])
                file.write("    pass\n")

            file.write(f"label {lib["root"][nme]["name"]}:\n")

            if len(lib["root"][nme]["dialog"]) <= 0:
                file.write("    return\n")
                continue

            for dia in lib["root"][nme]["dialog"]:
                for line in dia:
                    if type(line) == type(0):
                        inf = lib["root"][nme]["if"][line]
                        print(inf)
                        for con in inf["condition"]:
                            file.write(f"{LB_CUR.tab}if {con[0]} {con[1]} {con[2]}:\n")
                            for di in inf["dialog"][str(line)]:
                                file.write(di)
                    else:   
                        file.write(line)
            
            file.close()

def _save(*nm):
    import zipfile as zip
    from json import dump
    menu:Page=nm[1][0]

    if not len(_LB_STORED) == 0:
        try:
            global ROOT_LOCAL

            ch = nm[1][1]
            with open(ROOT_LOCAL+f"/.config/autosaves/end.json", "w") as file:
                info = {"root":{}}
                for labe in _LB_STORED:
                    labe:Label
                    info["root"][labe.name] = labe.meta

                dump(info, file, indent=1)

            keys = list(info["root"].keys())[0]
            _save_menu(ROOT_LOCAL, info, keys)
            
            open(ROOT_LOCAL+"/base.info", "w").close()
            dic = open(ROOT_LOCAL+"/base.info", "w")
            in_ = []

            for chap in ch:
                ln = []
                lb = []
                for inf in info["root"]:
                    if int(chap) in info["root"][inf]["chapter"]:
                        ln.append(info["root"][inf]["section"])
                        lb.append(inf)
                
                if len(ln) == 0 or len(lb) == 0:
                    continue
                in_.append(f"chapter_{chap}.rpy,{ln},{str(lb).replace("'", "")},[n];")
            
            for i in in_:
                dic.write(i)
            dic.close()
            with zip.ZipFile(ROOT_LOCAL+f"/dist_{nm[1][2]}.zip", "w", compression=zip.ZIP_DEFLATED) as zip_file:
                zip_file.write(ROOT_LOCAL+"/base.info", arcname=f"./{nm[1][2]}/base.info")
                zip_file.write(ROOT_LOCAL+"/meta.info", arcname=f"./{nm[1][2]}/meta.info")

                zip_file.write(ROOT_LOCAL+f"/{keys}.rpy", arcname=f"./{nm[1][2]}/{keys}.rpy")
                zip_file.close()

            del lb, ln, dic, in_, keys, info, ch
            print_debug("INFO SAVED!")
        except Exception as e:
            print(e)
            print_debug("NEED CREATE SOMETHING")
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        _sel(["y"], nm[1])
        return
    sleep(5)
    menu.start_cast()

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
    global _LB_STORED, LB_CUR
    menu:Page= nm[1][0]

    match nm[0][0]:
        case choice if choice in _yes_:
            name = input(f"What's name of your label?{JUMP_LINE }").replace(" ", "A").replace("_", "B").replace("-","C")
            ln_n = int(input(f"enter the number of the line?{JUMP_LINE}"))
            ln_b = int(input(f"What's the level of your label? (tabulator){JUMP_LINE}"))
            cha_ = [int(input(f"What chapters this must appear?{JUMP_LINE}"))]

            if cha_[0] in nm[1][1]:
                _LB_STORED.append(Label(ln_b, name, cha_, ln_n))
                LB_CUR = _LB_STORED[-1]
            else:
                print_debug(f"U NEED CONFIGURE THIS MOD TO {cha_} CHAPTER")
                sleep(5)

        case _:
            if not len(_LB_STORED) == 0:
                lst = []
                for nme in _LB_STORED:
                    lst.append(nme.name)
                _select_menu_print(lst)
                ln_n = int(input(f"What label u want to work?{JUMP_LINE}"))
                LB_CUR = _LB_STORED[ln_n]

                _btn_on(menu, 10, 11, LB_CUR.dialog)
                _btn_on(menu, 12, 13, LB_CUR.init)
            else:
                print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
                sleep(5)
                _sel(["y"], nm[1])
                return

    menu.create_text(f"Current label working on:"+" "*20, "CUSTOM", (1,2))
    menu.create_text(f"Current label working on: {LB_CUR.name}", "CUSTOM", (1,2))
    menu.start_cast()
    


chdir(getcwd()+"/proyects/default")
ROOT_LOCAL = getcwd()
global_config(cwd=ROOT_LOCAL)
#loader_label()
menu = Page(105, 22)

#MENU PRINCIPAL
nme:str;ver:str;aut:str;ch:list|bool;ctn:str
nme, ver, aut, ch, ctn = ["default", "1.0", "me", [1], WEB_MOD_DEFAULT]

menu.create_text(f"Current proyect working on: {nme}", "CUSTOM", (1,1))
menu.create_text(f"Current label working on: None", "CUSTOM", (1,2))

menu.create_text("Currect flowchart: Main", "CUSTOM", (46, 2))
menu.create_text("Variables Created", "CUSTOM", (85,2))

menu.add_panel(0,  3, 20, 16, 0) #BTNs
menu.add_panel(33, 3, 48, 14, 0) #DIALOG
menu.add_panel(83, 3, 20, 14, 0) #VAR

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
btn.caster(("What's the varible's ID?", 
            "What's operator? (equal/==/1, geater/>=/2, smaller/<=/3, not/!=/4)", 
            "What's the Variable's ID/variable?",
            "What's name of this condition?"), 
           menu)
menu.add_btn(btn)

#6-5
btn = Button(1, 11, "Edit if", _if_men, "if_men")
btn.caster(("What's condition's ID?"), menu)
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
btn.caster((""), menu, ch, nme)
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
btn.caster(("U want add a label? (y/n)?"), menu, ch)
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