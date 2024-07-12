#OWN DESINGS
from engine import * 
from engine.config.gen_arch import *

#BUG: THE PROGRAM SOMETIME WILL FOLLOW ONE LINE, BUT IN CERTAIN THAT CREATE SOME THREADS THAT
# ALLOW THAT CREATE MULTIPLE, AND WHEN ONE THREATH END, EXECUTE THE BEFORE THREAD AND SO... 
# well, the hell after all 

#NEED TO WORK
DEV[0] = False
#DEV[1] = True

#GEN-IMPORTS
from os import chdir, path, listdir, mkdir, getcwd, remove
from time import sleep

#GEN-STATS
VER : str = "1.2.0"
VER_COM :str = "1.1.9.4"
COMPILER : str = "2087f702fcc2b23f0b914399cfc6442caafde5e4"

#GEN-VAR
SIZE = [100, 15]

WEB_MOD_DEFAULT = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
WEB_MAIN_GAME = "https://rosesintheflames.com/"
WEB_TALE_GAME = "https://tales.rosesintheflames.com/"

ROOT_GLOBAL = getcwd()
ROOT_LOCAL:str
"""
When you load a mod, change all
"""  
################################################
#               FUNTIONS SIDE                  #
################################################

#GLOBAL SIDE
def check_proyects() -> dict:
    """
    Allow you get all current files in "proyects" folder
    """
    global ROOT_GLOBAL

    try:
        chdir(ROOT_GLOBAL+"/proyects")
    except:
        mkdir(ROOT_GLOBAL+"/proyects")
        chdir(ROOT_GLOBAL+"/proyects")

    info={}
    for nme in list(filter(path.isdir, listdir())):
        chdir(f"{nme}")
        try:
            info[nme] = open(f"{getcwd()}/meta.info", "rt").read().split(";")
            info[nme][3] = info[nme][3].replace("]", "").replace("[","").replace("'","").split(",")
        except FileNotFoundError:
            info[nme] = "Error!"
        chdir("..")
    return info

def de_cip(word:str) -> int:
    c=0
    for _in in word:
        c+=1
        if _in == "_":
            break
    return c

def _select_menu_print(obj:list):
    c=0
    for name in obj:
        c+=1
        print(f"NAME: {name} <---> ID: {c}")
    del c, name

#MAIN SIDE
def _refresh_zone(*nm):
    menu:Page; ID:int; item_cul:int;list_to:list
    ID_btn_in:list[int, int];ID_btn_ou:list;NUM_LT:list[int, int];INFO:dict
    is_new:bool

    menu, ID, item_cul,list_to, ID_btn_in,ID_btn_ou, NUM_LT, INFO, is_new = nm[1]
    menu.edit_panel_w_btn(ID,
                          item_cul,
                          list_to,
                          ID_btn_in,
                          ID_btn_ou,
                          NUM_LT,
                          INFO,
                          is_new)
    menu.btns[ID_btn_ou[0]-1].var = [menu, NUM_LT[0],list_to, INFO, False]

    del ID, item_cul,list_to, ID_btn_in,ID_btn_ou, NUM_LT, INFO
    if not is_new:
        menu.start_cast()
    else:
        return

def _procces_lst(*nm):
    menu:Page; lst_nme:list; info:dict;is_new:bool
    menu, lst_nme, info, is_new = nm[1][0], nm[1][2], nm[1][3], nm[1][4]
    num:int = int(nm[0][0])+int(nm[1][1])

    for i in range(3):
        menu.create_text(" "*25, "CUSTOM", (62, 12+i))

    if len(lst_nme[num]) >= 15:
        nme = f"Mod's name: {lst_nme[num][:15]}..."
    else:
        nme = f"Mod's name: {lst_nme[num]}"

    ref = info[lst_nme[num]]
    if not ref == "Error!":
        inf = []
        for _in in range(2):
            if len(ref[_in]) >= 15:
                inf.append(ref[_in][:15]+"...")
            else:
                inf.append(ref[_in])

        aut = inf[0]
        ver_ = inf[1]
        lnk = ref[2]
        del inf
    else:
        aut = "meta not found"
        ver_ = "meta not found"
        lnk = WEB_MOD_DEFAULT

    menu.btns[2].var = lnk
    menu.btns[4].var = (info, lst_nme, num)

    menu.create_text(nme, "CUSTOM", (62, 12))
    menu.create_text(f"Autor: {aut}", "CUSTOM", (62, 13))
    menu.create_text(f"Version: {ver_}", "CUSTOM", (62, 14))

    del ref, lst_nme, info, num, nme, aut, ver_, lnk
    if not is_new:
        menu.start_cast()
    else:
        return

def _procces_new(*nm):
    nme:str; vers:str; cre:str; ch:str; ctn:str
    nme, vers, cre, ch, ctn = nm[0]

    menu:Page = nm[1][0]

    if nme == "":
        from random import randint
        nme = "mod_"+str(randint(0,100))  
    if vers.replace(" ", "") == "":
        vers = "1.0"
    if cre.replace(" ", "") == "":
        cre = "Anonymus"
    if ch.replace(" ", "") == "":
        ch = ["1"]
    else:
        ch:list = ch.split(",")
    if ctn.replace(" ", "") == "":
        ctn = WEB_MOD_DEFAULT

    menu.create_text(f"{nme}", "CUSTOM", (3,6))
    menu.create_text(f"{vers}", "CUSTOM", (3,8))
    menu.create_text(f"{cre}", "CUSTOM", (3,10))

    menu.create_text(f"{ch}", "CUSTOM", (3,12))

    menu.create_text(f"{ctn}", "CUSTOM", (3, 14))
    menu.btns[1].var = [nme, vers, cre, ch, ctn]

    del nme, vers, cre, ch, ctn
    menu.start_cast()

#MODDER SIDE
def proyect_new_pro(*mn):
    global ROOT_GLOBAL, ROOT_LOCAL
    nme:str; vers:str; cre:str; ch:list; ctn:str
    nme, vers, cre, ch, ctn = mn[1]

    if not check_proyects().__contains__(nme):
        mkdir(ROOT_GLOBAL+f"/proyects/{nme}")
        chdir(ROOT_GLOBAL+f"/proyects/{nme}")

        ROOT_LOCAL = getcwd()

        open(ROOT_LOCAL+"/base.info", "w").close()
        open(ROOT_LOCAL+"/main.rpy", "w").close()

        mkdir(ROOT_LOCAL+"/.config")
        mkdir(ROOT_LOCAL+"/.config/autosaves")

        meta = open(getcwd()+"/meta.info", "w")
        meta.write(f"{cre};{vers};{ctn};{ch}")
        meta.close()
    else:
        chdir(ROOT_GLOBAL+f"/proyects/{nme}")
        ROOT_LOCAL = getcwd()

    modder_menu(nme, vers, cre, ch, ctn)

def proyect_lst_pro(*nm):
    global ROOT_GLOBAL, ROOT_LOCAL
    nme:str; vers:str; cre:str; ch:list; ctn:str
    nme = nm[1][1][nm[1][2]]
    info = nm[1][0][nme]

    vers, cre, ch, ctn = info[1], info[0], info[3], info[2]

    chdir(ROOT_GLOBAL+f"/proyects/{nme}")
    ROOT_LOCAL = getcwd()

    modder_menu(nme, vers, cre, ch, ctn)

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
        if len(nm[1]) == 3:
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
                    LB_CUR.edit_say(nm[1][7],   
                                    nm[1][4], 
                                    choice, 
                                    value, 
                                    nm[1][8],
                                    nm[1][6]
                                    )
                    _lst = []

                    for i in LB_CUR._if_obj[nm[1][6]-1].dialog:
                        _lst.append(LB_CUR.tab+f"condition_{i}\n")
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
        return "pass"
    
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

def loader_label() -> bool:
    global ROOT_LOCAL, CUR_CH
    from json import load

    info = paths_finder()
    if info == "pass":
        return True

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
        if not str(info["chapter"]) in CUR_CH:
            CUR_CH.append(str(info["chapter"]))

        _LB_STORED.append(create_instance(info))

    chdir(ROOT_LOCAL)
    return False
        

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

            for line in lib["root"][nme]["dialog"]:
                if type(line) == type(0):
                    inf = lib["root"][nme]["if"][line]
                    for con in inf["condition"]:
                        if not con[3]:
                            file.write(f"{LB_CUR.tab}elif {con[0]} {con[1]} {con[2]}:\n")
                        else:
                            file.write(f"{LB_CUR.tab}if {con[0]} {con[1]} {con[2]}:\n")
                        for di in inf["dialog"][line]:
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

################################################
#               MODDER SIDE                    #
################################################
#PRV-VAR-TO-MOD
_PRE_ACRO_GAME = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
_PRE_ALL_GAME  = ["Snowy", "Magma", "Vivian", "Margaret", 
             "Asher", "Ember", "Opal", "Thomas"]

#PRIV-VAR-SELECT
_yes_ = ["y", "Y", "yes"]
#PRIV-VAR-TO-STORE-LB
_LB_STORED :list[Label] = []
LB_CUR :Label = ...
CUR_CH = []

#GEN-VAR-FOR-MOD
JUMP_LINE = "\n>  "

#################################################
#                MODDER 1                       #
#################################################

def _sel(*nm):
    global _LB_STORED, LB_CUR, CUR_CH
    menu:Page= nm[1][0]
    
    match nm[0][0]:
        case choice if choice in _yes_:
            name = input(f"What's name of your label?{JUMP_LINE }").replace(" ", "A").replace("_", "B").replace("-","C")
            ln_n = int(input(f"enter the number of the line?{JUMP_LINE}"))
            ln_b = int(input(f"What's the level of your label? (tabulator){JUMP_LINE}"))
            cha_ = input(f"What chapters this must appear?{JUMP_LINE}")

            if cha_ in CUR_CH:
                _LB_STORED.append(Label(ln_b, name, [int(cha_)], ln_n))
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
                ln_n = int(input(f"What label u want to work?{JUMP_LINE}"))-1
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
    
#################################################
#                MODDER 2                       #
#################################################

def _char_men(*nm):
    if not len(_LB_STORED) == 0:
        if not len(LB_CUR._char_obj) == 0:
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
            print_debug("U NEED CREATE MORE CHARACTERS FIRST")
            sleep(5)
            menu:Page=nm[1][0]
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


def _say_men(*nm):
    if not len(_LB_STORED) == 0:
        sel = int(input(f"What's the say's ID?{JUMP_LINE}"))+nm[1][1]
        type_op:str = nm[1][3][1]

        if not len(LB_CUR._say_obj) == 0:
            match type_op:
                case "normal":
                    var = not "$" in LB_CUR.dialog[sel]
                case "if":
                    id_if  = int(nm[0][0])

                    var = not "$" in LB_CUR._if_obj[nm[1][3][2]].dialog[id_if][sel]
            if var:
                menu = Page(60, 15)
                
                match type_op:
                    case "normal":
                        ID = 12
                        name = [menu, "name",   "say", sel, type_op, nm[1][0]]
                        mess = [menu, "message","say", sel, type_op, nm[1][0]]
                        sa:say = LB_CUR._say_obj[sel]
                    case "if":
                        ID = 8
                        id_con = nm[1][3][2]
                        name = [menu, "name",    "say", sel, type_op, nm[1][0], id_if, sel+1, id_con]
                        mess = [menu, "message", "say", sel, type_op, nm[1][0], id_if, sel+1, id_con]

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
                print_debug("your line is not convertable")
                menu:Page=nm[1][0]
        else:
            print_debug("U NEED CREATE MORE 'say' OBJECTS")
            sleep(5)
            menu:Page=nm[1][0]
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
                    _lst.append(LB_CUR.tab+f"condition_{i}\n")
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

def _c0n(*nm):
    menu:Page = nm[1][0]

    if not len(LB_CUR._init_obj) == 1:
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
    else:
        print_debug("U NEED CREATE MORE VARIABLES")
        sleep(5)

    menu.start_cast()


def _if_men(*nm):
    menu = Page(105, 22, NMO="owo")
    if not len(_LB_STORED) <= 0:
        if not len(LB_CUR._if_obj) == 0:
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

            con_lst = []
            for con in LB_CUR._if_obj[ID_CUR].condition:
                con_lst.append(con[0][:6]+con[1]+ con[2][:6])

            say_lst = ["Create a new say!", "That will appear here"]
            var_lst = ["Create vars", "Here"]
            if not len(_if_._say_obj) == 0:
                _lst = []
                for i in _if_.dialog:
                    _lst.append(LB_CUR.tab+f"condition_{i}\n")
                    for n in _if_.dialog[i]:
                        _lst.append(n[4:])

                say_lst = _str_say_menu(obj=_lst)
            if not len(LB_CUR.init) == 1:
                var_lst = _str_say_menu(20, LB_CUR.init)

            #5-4
            btn = Button(1, 17, "Next", _con)
            btn.caster((""), menu,
                    1,
                    10,
                    con_lst,
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
                    con_lst,
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
                    say_lst,
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
                    say_lst,
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
                    var_lst,
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
                    var_lst,
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
            btn = Button(1, 20, "Save", _edi_)
            btn.var = [nm[1][0], "non"]
            menu.add_btn(btn)

            menu.create_text(f"App ver: {VER}/{VER_COM}", "CUSTOM", (50, 20))
            menu.create_text(f"Compiled: {COMPILER[:10]}", "CUSTOM", (80, 20))

            menu.start_cast()
        else:
            print_debug("NEED CREATE MORE 'if' FIRST")
            sleep(5)
            menu:Page=nm[1][0]
            menu.start_cast()
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        _sel(["y"], nm[1])
        return
    
def _if(*nm):
    menu:Page = nm[1][0]
    if not len(_LB_STORED) == 0:
        if not len(LB_CUR._init_obj) <= 1:
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
            print_debug("NEED CREATE MORE VARIABLE FIRST")
            sleep(5)
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        _sel(["y"], nm[1])
        return
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
  
################################################
#               WINDOW SIDE                    #
################################################

#MAIN
def main_menu():   
    menu = Page(X=SIZE[0], Y=SIZE[1], CHR="#")
    menu.create_text("RenTgen (Roses In The Flame's mod engine)", "CUSTOM", (3, 1))
    menu.create_text(f"version {VER}", "CUSTOM", (menu.vec[0]-len(VER)-12, 1))
    menu.create_text("CREATED BY: Z3R0_GT/OFFZ3R0           ENGINE (VOP): ScoStudios", "LOWER")

    btn = Button(X=3, Y=3, TEXT="Create new proyect", ACTION=proyect_new)
    menu.add_btn(btn)

    btn = Button(X=3, Y=5, TEXT="Load proyect's list", ACTION=proyect_list)
    menu.add_btn(btn)

    btn = Button(X=3, Y=7, TEXT="Website main", ACTION=WEB_MAIN_GAME, DEFAULT="LINK")
    menu.add_btn(btn)

    btn = Button(X=3, Y=9, TEXT="Website tales", ACTION=WEB_TALE_GAME, DEFAULT="LINK")
    menu.add_btn(btn)

    btn = Button(X=3, Y=11, TEXT="Exit", DEFAULT="EXIT")
    menu.add_btn(btn)
    

    #INFO-1
    menu.add_panel(84, 7, 16, 7, 0)

    #INFO-2
    menu.add_panel(64, 7, 16, 7, 0)

    #btn = Button(X=65, Y=8, TEXT="Open URL", ACTION=WEB,DEFAULT="LINK")
    #menu.add_btn(btn)

    del btn
    menu.start_cast()
    #menu.get_pre_view()

#MAIN-SUB-1
def proyect_list(*nm):
    del nm

    info = check_proyects()
    lst_pro = [i for i in info]

    #SECURITY CHECK
    if len(lst_pro) == 0:
        #REDIRECTS TO "NEW_MENU"
        erase_screen()
        print_debug(f"{VER} YOU DON'T HAVE PROYECTS CREATED YET {VER}")
        print_debug(f"{VER} REDIRECTING TO CREATE A NEW... {VER}")
        sleep(5)
        proyect_new()
        return

    menu = Page(X=SIZE[0], Y=SIZE[1]+4, CHR="#", NMO="Proyect's page")  

    menu.create_text("Proyect's page", "CUSTOM", (3,3))
    menu.create_text(f"version {VER}", "CUSTOM", (menu.vec[0]-len(VER)-12, 1))

    menu.add_panel(0, 4, 27, 12, 0)  #SELECT SECTION
    menu.add_panel(60, 3, 32, 6, 0)  #TUTORIAL ""

    menu.add_panel(60, 11, 32, 5, 0) #META ""

    #OPTIONS'S SECTION
    for nme in range(10):
        if nme == len(lst_pro):
            break

        if len(lst_pro[nme]) < menu.meta["panel"][1]["transform"][0]-5:
            menu.create_text(f"{nme+1}) "+lst_pro[nme], "CUSTOM", (1,nme+5)) 
        else:
            menu.create_text(f"{nme+1}) "+lst_pro[nme][:16]+"...", "CUSTOM", (1,nme+5))
    del nme

    btn = Button(1, 17, "Next", _refresh_zone, DEFAULT="CUSTOM")
    btn.caster((""), menu, 1, 10, lst_pro, (1, 2), [4], (10, 20), info, False)
    menu.add_btn(btn)

    btn = Button(15, 17, "Back", _refresh_zone, DEFAULT="CUSTOM")
    btn.caster((""), menu, 1, 10, lst_pro, (1, 2), [4], (0, 10), info, False)
    menu.add_btn(btn)

    btn = Button(X=62, Y=15, TEXT="Autor site/download", ACTION=WEB_MOD_DEFAULT, DEFAULT="LINK")
    menu.add_btn(btn)

    btn = Button(X=31, Y=17, TEXT="Archive to load",ACTION=_procces_lst, DEFAULT="CUSTOM")
    btn.caster(("Enter proyect's number"), menu, 0, lst_pro, info, False)
    menu.add_btn(btn)

    btn = Button(X=70, Y=17, TEXT="Load", ACTION=proyect_lst_pro, DEFAULT="CUSTOM")
    btn.caster((""), info, lst_pro, 0)
    menu.add_btn(btn)

    btn = Button(X=84, Y=17, TEXT="Back menu", DEFAULT="BACK")
    menu.add_btn(btn)

    _procces_lst([0], [menu, 0, lst_pro, info, True])
    _refresh_zone([], [menu, 1, 10, lst_pro, (1, 2), [4], (0, 10), info, True])

    del btn, lst_pro, info

    menu.start_cast()
    #menu.get_pre_view()

#MAIN-SUB-2
def proyect_new(*nm):
    del nm
    menu = Page(X=SIZE[0], Y=SIZE[1]+4, CHR="#")

    menu.create_text("Creation mod menu", "CUSTOM", (3, 3))
    menu.create_text(f"version {VER}", "CUSTOM", (menu.vec[0]-len(VER)-12, 1))

    menu.create_text("Mod's name:", "CUSTOM", (3, 5))

    menu.create_text("Version:", "CUSTOM", (3, 7))

    menu.create_text("Author:", "CUSTOM", (3,9))

    menu.create_text("Chapters to mod:", "CUSTOM", (3, 11))

    menu.create_text("Contac:", "CUSTOM", (3, 13))

    btn = Button(X=2, Y=17, TEXT="Enter data",ACTION=_procces_new, DEFAULT="CUSTOM")
    btn.caster(("What's the name of your mod?", "What's version is?", 
                "Who's the creator?", 
                "Enter the chapters to mod (separete by comas)", 
                "Do you have some social network or URL for the mod? (write the URL)"), menu)
    menu.add_btn(btn)
    
    btn = Button(X=70, Y=17, TEXT="Create", ACTION=proyect_new_pro, DEFAULT="CUSTOM")
    btn.caster((""), "default", "1.0", "Z3R0_GT", ["1"], WEB_MOD_DEFAULT) 
    menu.add_btn(btn)

    btn = Button(X=84, Y=17, TEXT="Back", DEFAULT="BACK")
    menu.add_btn(btn)

    menu.add_panel(68, 4, 32, 8, 0)
    menu.create_text("Tutorial:", "CUSTOM", (71,5))
    del btn

    menu.start_cast()
    #menu.get_pre_view()

#MOD
def modder_menu(nme:str, ver:str, aut:str, ch:list|bool, ctn:str):
    global _LB_STORED, CUR_CH, LB_CUR
    _LB_STORED = []
    CUR_CH     = []

    #MENU PRINCIPAL
    global_config(cwd=ROOT_LOCAL)
    chk = loader_label()

    say_lst = ["Create a new say!", "That will appear here"]
    var_lst = ["Create vars", "Here"]

    if chk:
        CUR_CH = ch
        mne = None
    else:
        LB_CUR = _LB_STORED[0]
        mne = LB_CUR.name
        if not len(LB_CUR.dialog) == 0:
            say_lst = _str_say_menu(obj=LB_CUR.dialog)
        if not len(LB_CUR.init) == 1:
            var_lst = _str_say_menu(15, LB_CUR.init)

    menu = Page(105, 22)

    menu.create_text(f"Current proyect working on: {nme}", "CUSTOM", (1,1))
    menu.create_text(f"Current label working on: {mne}", "CUSTOM", (1,2))

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
            say_lst,
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
            say_lst,
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
            var_lst,
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
            var_lst,
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
    #menu.get_pre_view()

################################################
#                 MAIN SIDE                    #
################################################
main_menu()