from os import chdir, path, listdir, mkdir, getcwd
from time import sleep

from engine import *
from engine.config.gen_arch import *
from engine.models.internal.tool.debug import erase_screen, print_debug

root_global = getcwd()
COMPILER = "7093c49658620b64e78973b1def66a8e2f704520"
web ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

#procces functions
def check_proyects() -> dict:
    global root_global
    
    try:
        chdir(root_global+"/proyects")
    except:
        mkdir(root_global+"/proyects")
        chdir(root_global+"/proyects")

    info={}
    for nme in list(filter(path.isdir, listdir())):
        chdir(f"{nme}")
        try:
            info[nme] = open(f"{getcwd()}/meta.info", "rt").read().split(";")
        except FileNotFoundError:
            info[nme] = "Error!"
        chdir("..")
    return info

def proyect_new_pro(*mn):
    nme:str; vers:str; cre:str; ch:list; ctn:str; VER:int; SIZE:int
    nme, vers, cre, ch, ctn, VER, SIZE = mn[1]

    if not check_proyects().__contains__(nme):
        mkdir(root_global+f"/proyects/{nme}")
        chdir(root_global+f"/proyects/{nme}")

        open(getcwd()+"/base.info", "w").close()
        open(getcwd()+"/main.rpy", "w").close()

        mkdir(getcwd()+"/.config")
        mkdir(getcwd()+"/.config/autosaves")

        meta = open(getcwd()+"/meta.info", "w")
        meta.write(f"{cre};{vers};{ctn}")
        meta.close()

    _procces([nme, vers, cre, ch, ctn, VER, SIZE])

def proyect_lst_pro(*nm):
    num = nm[1][2]
    nme = nm[1][1][num]
    info = nm[1][0][nme]

    _procces([nme, info[1], info[0], True, info[2], nm[1][3], nm[1][4]])

#################################################
#                FINAL FUNCTIONS                #
#################################################
def _save_all(*n): #or compile
    root:str;lib:dict;nme_arch:str
    root, lib, nme_arch = n

    a = open(root+f"/{nme_arch}.rpy", "w")
    a.write("")
    a.close()

    with open(root+f"/{nme_arch}.rpy", "a") as f:
        for nme in lib["root"]:
            
            for ch in lib["root"][nme]["character"][0]:
                for line in ch:
                    f.write(line)
            
            for dia in lib["root"][nme]["dialog"]:
                for line in dia:
                    f.write(line)

        f.close()

def _end_proces(*nm):
    try:
        root = nm[1][0]
        menu:Page=nm[1][1]
        ch = nm[1][2]
        info = _cast_all()
        keys = list(info["root"].keys())[0]

        _save_all(root, info, keys)    
        open(root+"/base.info", "w").close()
        dic = open(root+"/base.info", "a")
        in_ = []

        for chap in ch:
            ln = []
            lab = []
            for inf in info["root"]:    
                if info["root"][inf]["chapter"] == int(chap):
                    ln.append(info["root"][inf]["section"])
                    lab.append(inf)

            if len(ln) == 0 or len(lab) == 0:
                continue
            in_.append(f"chapter_{chap}.rpy,{ln},{str(lab).replace("'","")},[n];")

        for i in in_:
            dic.write(i)
        dic.close()
        print_debug("INFO SAVED!")
        
    except Exception as e:
        print(e)
        print_debug("NEED CREATE SOMETHING")
    sleep(5)
    menu.start_cast()
   
#################################################
#                INFO FUNCTIONS                 #
#################################################
_pre_acro = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
_pre_all  = ["Snowy", "Magma", "Vivian", "Margaret", "Asher", "Ember", "Opal", "Thomas"]
_yes = ["y", "Y", "yes"]
_lb_all = []

CUR_CH:list

CUR_:int=0


def _get_lst()-> tuple[list, str]:
    root_local = getcwd()
    lst_final = []

    for lst in list(filter(path.isdir, listdir())):
        if not lst in [".config"]: #ADD EXCEPT DIRs
            lst_final.append(lst)

    for lst in list(filter(path.isfile, listdir())):
        if not lst in ["base.info", "meta.info"]: #ADD EXCEPT FOR ARCHIVES
            lst_final.append(lst)

    return lst_final, root_local

def _cast_all()->dict:
    from datetime import datetime as dtime
    from json import dump
    
    with open(getcwd()+f"/.config/autosaves/{dtime.now().day}_{dtime.now().month}_end.json", "w") as f:
        lib = {"root":{}}
        for data in _lb_all:
            data:label_statemnt
            lib["root"][data.nme] = data.meta

        dump(lib, f, indent=1) 
        return lib

def __refresh_lb(menu:Page, pos:tuple[int, int], what:str): 
    menu.create_text(what, "CUSTOM", pos)

def _say_zone(menu:Page) -> list:
    lab:label_statemnt = _lb_all[CUR_]
    SPACE_JUMP = 1
    temp = []
    for i in lab.dialog:
        i:str
        if not (i.replace(" ","")[:5] == "label" or \
                i.replace(" ","")[:6] == "return") \
                and \
           not  (i.replace("\\n","")[len(lab.level):len(i)-SPACE_JUMP] in temp or \
                 i.replace("\\n","")[len(lab.level):len(i)-20-SPACE_JUMP]+"..." in temp):
            if len(i)-len(lab.level) >= 20:
                temp.append(i.replace("\\n","")[len(lab.level):len(i)-20-SPACE_JUMP]+"...")
            else:
                temp.append(i.replace("\\n","")[len(lab.level):len(i)-SPACE_JUMP])
    return temp

#################################################
#                STABLE FUNCTIONS               #
#################################################

def _lb_procc(*nm):
    info=nm[0]
    menu:Page = nm[1][0]
    if int(info[3]) in CUR_CH:
        _lb_all.append(label_statemnt(info[0], int(info[1]), int(info[2]), int(info[3])))
        __refresh_lb(menu, (1, 2), f" Current label: {" "*10}")

        if not len(_lb_all[-1].nme) >= 10:
            __refresh_lb(menu, (1, 2), f" Current label: {_lb_all[-1].nme}")
        else:
            __refresh_lb(menu, (1, 2), f" Current label: {_lb_all[-1].nme[:10]}")
    else:
        print_debug(f"U NEED HAVE CONFIGURATED THIS MOD TO: {int(info[3])} chapter")
        sleep(5)

    menu.start_cast()

def _lb_sec(*nm):
    menu:Page=nm[1][0]
    if not len(_lb_all) == 0:
        c = -1
        for nme in _lb_all:
            nme:label_statemnt
            c+=1
            print("NAME: ", nme.nme, "ID: ", c)
        del c

        CUR_=int(input("What label u want to work? \n>"))

        __refresh_lb(menu, (1, 2), f" Current label: {" "*10}")
        if not len(_lb_all[CUR_].nme) >= 10:
            __refresh_lb(menu, (1, 2), f" Current label: {_lb_all[CUR_].nme}")
        else:
            __refresh_lb(menu, (1, 2), f" Current label: {_lb_all[CUR_].nme[:10]}")

    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        menu.execute_btn(1)
    
    menu.start_cast()
    
#################################################
#                OWN-C FUNCTIONS                #
#################################################
def _chararacter(*nm):
    menu:Page=nm[1][0]
    erase_screen()
    if not len(_lb_all) == 0:
        lab:label_statemnt = _lb_all[CUR_]
        lab.add_character(input("What's the name of your character?\n>"))

        __refresh_lb(menu, (1, 10), f"Character num: {len(_lb_all[-1].char_hard)}")

    menu.start_cast()

def _del_char(*nm):
    menu:Page=nm[1][0]
    if not len(_lb_all) == 0:
        lab:label_statemnt = _lb_all[CUR_]
        c -= 1
        for nme in lab.char_simple:
            c+=1
            print("NAME: ", nme, "ID: ", c)
        del c

        lab.del_character(int(input("What character u want to delete (ID)?\n>")))

    menu.start_cast()


def _say(*nm):
    menu:Page=nm[1][0]

    #erase_screen()
    if not len(_lb_all) == 0:
        print("REMEMBER, HERE U CAN USE \\n or special character like that")
        sleep(5)
        lab:label_statemnt = _lb_all[CUR_]
        if input("Do you want to use pre-define characters? (y/n)\n> ") in _yes :
            c = -1
            for nme in _pre_all:
                c+=1
                print("NAME: ", nme, "ID: ", c)

            lab.add_say(_pre_acro[int(input("What's the ID (number)? \n>"))], 
                    True, 
                    input("What do u want that this character say? \n>"))
        elif input("is your character still exits? (y/n) \n>") in _yes:
            c = -1
            for nme in lab.char_hard:
                c+=1
                print("NAME: ", nme, "ID: ", c)
            lab.add_say(lab.char_simple[int(input("What's the ID (number)? \n>"))], 
                    True, 
                    input("What do u want that this character say? \n>"))
        else:
            print("We recommend u use 'Character' option to don't repeat many time this... (wait a few seconds)")
            sleep(5)

            if input("Do u want use a character's name (we don't save it)? (y/n) \n>") in _yes:
                lab.add_say(input("What's the name?: >"), 
                        False,
                        input("What do u want that this character say? \n>"))
            else:
                lab.add_say(None, 
                        False,
                        input("What do u want that this character say? \n>"))

        menu.btns[7].var[3] = _say_zone(menu)
        menu.btns[8].var[3] = _say_zone(menu)
        menu.btns[8].var[8] = True

        menu.execute_btn(9)

        menu.btns[8].var[8] = False

    menu.start_cast()

def _edit_say(*nm):
    menu:Page=nm[1][0]
    if not len(_lb_all) == 0:
        lab:label_statemnt = _lb_all[CUR_]

        lab.edit_say(int(nm[0][0])+int(nm[1][1])+2, 
                     input("What do u want that this character say instead of the other one? \n>"))

        menu.btns[7].var[3] = _say_zone(menu)
        menu.btns[8].var[3] = _say_zone(menu)
        menu.btns[8].var[8] = True

        menu.execute_btn(9)

        menu.btns[8].var[8] = False

    menu.start_cast()

def _del_say(*nm):
    menu:Page=nm[1][0]
    if not len(_lb_all) == 0:
        lab:label_statemnt = _lb_all[CUR_]

        lab.del_say(int(nm[0][0])+int(nm[1][1])+2)

        menu.btns[7].var[3] = _say_zone(menu)
        menu.btns[8].var[3] = _say_zone(menu)
        menu.btns[8].var[8] = True

        menu.execute_btn(9)

        menu.btns[8].var[8] = False

    menu.start_cast()


def _up_sec(*nm):
    menu:Page=nm[1][0]
    menu.edit_panel_w_btn(nm[1][1],
                          nm[1][2],
                          nm[1][3],
                          nm[1][4], 
                          nm[1][5], 
                          nm[1][6], 
                          nm[1][7])
    
    menu.start_cast()
    
#################################################
#                MAIN FUNCTIONS                 #
#################################################
def _procces(info):
    global CUR_CH
    DEV[0] = False
    nme:str;ver_:str;aut:str;ch:list|bool;ctn:str; VER:int; SIZE:int
    nme, ver_, aut, ch, ctn, VER, SIZE = info

    chdir(root_global+f"/proyects/{nme}")
    start_()

    if ch == True:
        _nm = open("base.info", "rt").read().split(",")
        ch = []
        for nm in _nm: 
            if nm[:7] == "chapter":
                ch.append(int(nm[8:].replace(".rpy", "")))
        del _nm, nm
    else:
        ch = info[3]
    CUR_CH = ch

    inf = _get_lst()
    #lst_final = inf[0]

    menu = Page(X=SIZE[0], Y=SIZE[1]+3, CHR="#")
    if len(VER) >= 10:
        menu.create_text(f"Hello, mod's version: {VER[:10]}", "CUSTOM", (1, 1))
    else:
        menu.create_text(f"Hello, mod's version: {VER}", "CUSTOM", (1, 1))
    
    menu.create_text(f"Compiled version: {COMPILER[:8]}", "CUSTOM", (72, 1))

    #LABEL
    menu.create_text("Current label: None","CUSTOM", (1,2))

    btn = Button(1, 4, "Create a label", _lb_procc, DEFAULT="CUSTOM")
    btn.caster(("What's name of your label?", 
                "TEST: enter the number of the line",
                "What's the level of your label? (tabulator)",
                "What chapter this must appear?"), menu)
    menu.add_btn(btn)

    btn = Button(1, 5, "Select label", _lb_sec, DEFAULT="CUSTOM")
    btn.caster((""), menu)
    menu.add_btn(btn)

    #CHARACTER
    btn = Button(1, 7, "Add character", _chararacter, DEFAULT="CUSTOM")
    btn.caster((""), menu)
    menu.add_btn(btn)

    btn = Button(1, 8, "Delete character", _del_char, DEFAULT="CUSTOM")
    btn.caster((""), menu)
    menu.add_btn(btn)

    #SAY
    btn = Button(1, 10, "Add say to 'character'", _say, DEFAULT="CUSTOM")
    btn.caster((""), menu)
    menu.add_btn(btn)

    btn = Button(1, 11, "Edit say", _edit_say, DEFAULT="CUSTOM")
    btn.caster(("Insert the ID"), menu)
    menu.add_btn(btn)

    btn = Button(1, 12, "Delete say", _del_say, DEFAULT="CUSTOM")
    btn.caster(("Insert the ID"), menu)
    menu.add_btn(btn)

    #INFO SECTOR - 1
    menu.create_text("Dialogues created", "CUSTOM", (38, 1))
    menu.add_panel(38, 2, 52, 12, 0)
    
    #ID : 7 - 8
    btn = Button(38, 15, "Next", _up_sec, DEFAULT="CUSTOM")
    btn.caster((""), menu, 1, 
                          10, 
                          ["Nothing", "Nothing"], 
                          (8, 9), 
                          (6, 7), 
                          (10, 20), 
                          ..., 
                          False)
    menu.add_btn(btn)

    btn = Button(50, 15, "Back", _up_sec, DEFAULT="CUSTOM")
    btn.caster((""), menu, 1, 
                          10, 
                          ["Nothing", "Nothing"], 
                          (8, 9), 
                          (6, 7), 
                          (0, 10), 
                          ..., 
                          False)
    menu.add_btn(btn)
    menu.del_btn(9, False)

    #END BUTTONS
    btn = Button(1, 14, "export", _end_proces, DEFAULT="CUSTOM")
    btn.caster((""), inf[1], menu, ch)
    menu.add_btn(btn)

    btn = Button(1, 15, TEXT="Back", DEFAULT="BACK")
    menu.add_btn(btn)

    menu.start_cast()

#TEST
_procces(["mc", "1.0", "me", True, web, "1.0", [100, 15]])