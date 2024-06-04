from os import chdir, path, listdir, mkdir, getcwd
from time import sleep

from engine import *
from engine.config.gen_arch import *
from engine.models.internal.tool.debug import _chk_window, print_debug

root_global = getcwd()
web ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

size = [100, 15]

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
    nme:str; vers:str; cre:str; ch:list; ctn:str
    nme = mn[1][0]
    vers = mn[1][1]
    cre= mn[1][2]
    ch= mn[1][3]
    ctn = mn[1][5]

    if nme == "":
        from random import randint
        nme = "mod_"+str(randint(0,100))
    if vers.replace(" ", "") == "":
        vers = "1.0"
    if cre.replace(" ", "") == "":
        cre = "Anonymus"
    if ctn.replace(" ", "") == "":
        ctn = web

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

    _procces([nme, vers, cre, ch, ctn])

def proyect_lst_pro(*nm):
    num = nm[1][2]
    nme = nm[1][1][num]
    info = nm[1][0][nme]

    _procces([nme, info[1], info[0], True, info[2]])

#final functions
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

_pre_acro = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
_pre_all  = ["Snowy", "Magma", "Vivian", "Margaret", "Asher", "Ember", "Opal", "Thomas"]
_yes = ["y", "Y", "yes"]
_lb_all = []
CUR_:int=0

ver : str = "a1.1.5.1"

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

def _lb_procc(*nm):
    info=nm[0]
    menu:Page = nm[1][0]

    _lb_all.append(label_statemnt(info[0], int(info[1]), int(info[2]), int(info[3])))
        
    __refresh_lb(menu, (1, 4), f"Current label that working on: {_lb_all[-1].nme}")
    menu.start_cast()

def _lb_sec(*nm):
    menu:Page=nm[1][0]
    _chk_window()
    if not len(_lb_all) == 0:
        c = -1
        for nme in _lb_all:
            nme:label_statemnt
            c+=1
            print("NAME: ", nme.nme, "ID: ", c)

        CUR_=int(input("What label u want to work? \n>"))
        __refresh_lb(menu, (1, 4), f"Current label that working on: {_lb_all[CUR_].nme}")
    else:
        print("u need create a label first")
        sleep(5)
    
    menu.start_cast()
    

def _chararacter(*nm):
    menu:Page=nm[1][0]
    _chk_window()
    if not len(_lb_all) == 0:
        lab:label_statemnt = _lb_all[CUR_]
        lab.character(input("What's the name of your character?\n>"))

        __refresh_lb(menu, (1, 10), f"Character num: {len(_lb_all[-1].char_hard)}")

    menu.start_cast()
        
def _say(*nm):
    menu:Page=nm[1][0]

    _chk_window()
    if not len(_lb_all) == 0:
        print("REMEMBER, HERE U CAN USE \\n or special character like that")
        sleep(5)
        lab:label_statemnt = _lb_all[CUR_]
        if input("Do you want to use pre-define characters? (y/n)\n> ") in _yes :
            c = -1
            for nme in _pre_all:
                c+=1
                print("NAME: ", nme, "ID: ", c)

            lab.say(_pre_acro[int(input("What's the ID (number)? \n>"))], 
                    True, 
                    input("What do u want that this character say? \n>"))
        elif input("is your character still exits? (y/n) \n>") in _yes:
            c = -1
            for nme in lab.char_hard:
                c+=1
                print("NAME: ", nme, "ID: ", c)
            lab.say(lab.char_simple[int(input("What's the ID (number)? \n>"))], 
                    True, 
                    input("What do u want that this character say? \n>"))
        else:
            print("We recommend u use 'Character' option to don't repeat many time this... (wait a few seconds)")
            sleep(5)

            if input("Do u want use a character's name (we don't save it)? (y/n) \n>") in _yes:
                lab.say(input("What's the name?: >"), 
                        False,
                        input("What do u want that this character say? \n>"))
            else:
                lab.say(None, 
                        False,
                        input("What do u want that this character say? \n>"))

    menu.start_cast()

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
    
def _procces(info):
    nme:str;ver_:str;aut:str;ch:list|bool;ctn:str
    nme, ver_, aut, ch, ctn = info

    chdir(root_global+f"/proyects/{nme}")
    start_()

    if ch == True:
        _nm = open("base.info", "rt").read().split(",")
        ch = []
        for nm in _nm: 
            if nm[:7] == "chapter":
                ch.append(nm[8:].replace(".rpy", ""))
        del _nm, nm
    else:
        ch = info[3]

    inf = _get_lst()
    lst_final = inf[0]

    menu = Page(X=size[0], Y=size[1], CHR="#")
    menu.create_text(f"Hello, this the version: {ver}", "CUSTOM", (1, 1))

    btn = Button(1, 2, "Select label", _lb_sec, DEFAULT="CUSTOM")
    btn.caster((""), menu)
    menu.add_btn(btn)

    menu.create_text("Current label that working on: Non","CUSTOM", (1,4))

    btn = Button(1, 5, "Create a label", _lb_procc, DEFAULT="CUSTOM")
    btn.caster(("What's name of your label?", 
                "TEST: enter the number of the line",
                "What's the level of your label? (tabulator)",
                "What chapter this must appear?"), menu)
    menu.add_btn(btn)

    btn = Button(1, 8, "Add character", _chararacter, DEFAULT="CUSTOM")
    btn.caster((""), menu)
    menu.add_btn(btn)

    menu.create_text("character: ", "CUSTOM", (1,10))

    btn = Button(1, 11, "add say to a character", _say, DEFAULT="CUSTOM")
    btn.caster((""), menu)
    menu.add_btn(btn)

    btn = Button(1, 12, "export", _end_proces, DEFAULT="CUSTOM")
    btn.caster((""), inf[1], menu, ch)
    menu.add_btn(btn)

    btn = Button(1, 13, TEXT="Back", DEFAULT="BACK")
    menu.add_btn(btn)

    menu.start_cast()