#OWN DESINGS
from engine import * 
from engine.config.gen_arch2 import *

#NEED TO WORK
#DEV[0] = False
DEV[1] = True

#GEN-IMPORTS
from os import chdir, path, listdir, mkdir, getcwd, remove
from time import sleep

#GEN-STATS
VER : str = "1.0.1"
COMPILER : str = "b85ce8b9b731086fa946d17798e896ad0bf19701"

#GEN-VAR
SIZE = [100, 15]

WEB_MOD_DEFAULT = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
WEB_MAIN_GAME = "https://rosesintheflames.com/"
WEB_TALE_GAME = "https://tales.rosesintheflames.com/"

PATREON_KEY:list = ["BBB"]
"""
in the future, get a list from the future data base
and all of them is encripted
"""


ROOT_GLOBAL = getcwd()
ROOT_LOCAL:str
"""
When you load a mod, change all
"""  

################################################
#               FUNTIONS SIDE                  #
################################################

#GLOBAL SIDE
def de_cip(word:str) -> int:
    c=0
    for _in in word:
        c+=1
        if _in == "_":
            break
    return c

#MODDER SIDE
def start_loading():
    """
    Thi's called just one time
    """
    global CUR_CH
    from json import load

    chdir(ROOT_LOCAL+"/.config/autosaves")
    info = list(filter(path.isfile, listdir()))
    
    if len(info) == 0:
        chdir(ROOT_LOCAL)
        return

    #SEARCH PRIOR FILES
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

    chapters = []

    #CREATE INSTANCES OF LABELS
    for name in name_loaded:
        with open(getcwd()+f"/{name}", "r") as file:
            info_file = load(file)

            if ch:
                data = info_file["root"]
                for name in data:
                    if not data[name]["chapter"] in chapters:
                        chapters.append(str(data[name]["chapter"]))


                    label = label_statemnt(data[name]["name"],
                                           data[name]["section"],
                                           len(data[name]["level"])%INFO["tab"]+1,
                                           data[name]["chapter"]
                                           )

                    label.char_hard = data[name]["character"][0]
                    label.char_simple = data[name]["character"][1]

                    for i in range(len(data[name]["dialog"])):
                        if i == 0:
                            continue

                        label.dialog.append(data[name]["dialog"][i])
                    
                    _LB_STORED.append(label)
            else:
                if not info_file["chapter"] in chapters:
                    chapters.append(str(info_file["chapter"]))

                label = label_statemnt(info_file["name"], 
                                       info_file["section"],
                                       len(info_file["level"])%INFO["tab"]+1,
                                       info_file["chapter"]
                                      )
                
                label.char_hard = info_file["character"][0]
                label.char_simple = info_file["character"][1]

                for i in range(len(info_file["dialog"])):
                    if i == 0:
                        continue

                    label.dialog.append(info_file["dialog"][i])
                
                _LB_STORED.append(label)

    CUR_CH = chapters

    #REMOVE ALL OF TEMP-END FILES
    for i in range(len(info)):
        remove(getcwd()+f"/{info[i]}")

    #CREATE NEW TEMP FILES
    for label in _LB_STORED:
        label:label_statemnt

        label.meta["character"] = [label.char_hard, label.char_simple]
        label.meta["dialog"] = label.dialog

        label.refresh_save()

    chdir(ROOT_LOCAL)
    return

def _cast_all()->dict:
    """
    generate a "end" file when all is done
    """
    from json import dump
    
    with open(ROOT_LOCAL+f"/.config/autosaves/end.json", "w") as file:
        data_save = {"root":{}}

        for label in _LB_STORED:
            label:label_statemnt
            data_save["root"][label.nme] = label.meta

        dump(data_save, file, indent=1) 
        return data_save

def _say_zone(menu:Page) -> list:
    lab:label_statemnt = _LB_STORED[CUR_LB]
    LIM_TEXT = 20
    SPACE_JUMP = 1
    temp = []
    for i in lab.dialog:
        i:str
        if not (i.replace(" ","")[:5] == "label" or \
                i.replace(" ","")[:6] == "return") \
                and \
           not (i.replace("\\n","")[len(lab.level):len(i)-SPACE_JUMP] in temp or \
                i.replace("\\n","")[len(lab.level):len(i)-LIM_TEXT-SPACE_JUMP]+"..." in temp):
            
            if len(i)-len(lab.level) >= LIM_TEXT:
                temp.append(i.replace("\\n","")[len(lab.level):len(i)-LIM_TEXT-SPACE_JUMP]+"...")
            else:
                temp.append(i.replace("\\n","")[len(lab.level):len(i)-SPACE_JUMP])
    del lab
    return temp


def _end_proces(*nm):
    import zipfile as zip
    
    menu:Page=nm[1][1]
    try:
        root = nm[1][0]
        ch = nm[1][2]
        info = _cast_all()
        if len(list(info["root"].keys())) == 0:
            raise TypeError("NEED CREATE SOME LABELS")
        keys = list(info["root"].keys())[0]
        
        _save_all(root, info, keys)    
        open(root+"/base.info", "w").close()
        dic = open(root+"/base.info", "w")
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
        with zip.ZipFile(ROOT_LOCAL+f"/dist_{nm[1][3]}.zip", "w", compression=zip.ZIP_DEFLATED) as zip_file:
            zip_file.write(root+"/base.info", arcname=f"./{nm[1][3]}/base.info")
            zip_file.write(root+"/meta.info", arcname=f"./{nm[1][3]}/meta.info")

            zip_file.write(root+f"/{keys}.rpy", arcname=f"./{nm[1][3]}/{keys}.rpy")
            zip_file.close()
            
        del lab, ln, chap, dic, in_, keys, info, ch, root
        print_debug("INFO SAVED!")
        
    except Exception as e:
        print(e)
        print_debug("NEED CREATE SOMETHING")
    
    
    sleep(5)
    menu.start_cast()

def _save_all(root:str,lib:dict,nme_arch:str): #or compile
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

################################################
#               MODDER SIDE                    #
################################################
#PRV-VAR-TO-MOD
_PRE_ACRO_GAME = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
_PRE_ALL_GAME  = ["Snowy", "Magma", "Vivian", "Margaret", 
             "Asher", "Ember", "Opal", "Thomas"]

#PRIV-VAR-SELECT
_yes = ["y", "Y", "yes"]
#PRIV-VAR-TO-STORE-LB
_LB_STORED = []

#GEN-VAR-FOR-MOD
CUR_LB:int=0
CUR_CH:list
"""
chapter's list to work on
"""

#################################################
#                MODDER 1                       #
#################################################

def _lb_procc(*nm):

    info=nm[0]
    menu:Page = nm[1][0]
    if info[3] in CUR_CH:
        _LB_STORED.append(label_statemnt(info[0].replace(" ", "A").replace("_", "B").replace("-","C"), 
                                         int(info[1]), int(info[2]), int(info[3])))
        menu.create_text(f" Current label: {" "*10}", "CUSTOM", (1,2))

        if not len(_LB_STORED[-1].nme) >= 10:
            menu.create_text(f" Current label: {_LB_STORED[-1].nme}", "CUSTOM", (1,2))
        else:
            menu.create_text(f" Current label: {_LB_STORED[-1].nme[:10]}...", "CUSTOM", (1,2))
    
        global CUR_LB
        CUR_LB = len(_LB_STORED)-1
    
    else:
        print_debug(f"U NEED HAVE CONFIGURATED THIS MOD TO: {int(info[3])} chapter")
        sleep(5)

    menu.start_cast()

def _lb_sec(*nm):
    global CUR_LB
    menu:Page=nm[1][0]
    if not len(_LB_STORED) == 0:
        c = -1
        for nme in _LB_STORED:
            nme:label_statemnt
            c+=1
            print("NAME: ", nme.nme, "ID: ", c)
        del c

        CUR_LB=int(input("What label u want to work? \n>"))

        if not len(_LB_STORED[CUR_LB].nme) >= 10:
            menu.create_text(f" Current label: {_LB_STORED[CUR_LB].nme}", "CUSTOM", (1,2))
        else:
            menu.create_text(f" Current label: {_LB_STORED[CUR_LB].nme[:10]}...", "CUSTOM", (1,2))

        menu.btns[7].var[3] = _say_zone(menu)
        menu.btns[8].var[3] = _say_zone(menu)
        menu.btns[8].var[8] = True

        menu.execute_btn(9)
    else:
        print_debug("LABELS NOT FOUND, REDIRECTING TO CREATE A NEW ONE...")
        sleep(5)
        menu.execute_btn(1)
    
    menu.start_cast()
    
#################################################
#                MODDER 2                       #
#################################################

def _chararacter(*nm):
    menu:Page=nm[1][0]
    if not len(_LB_STORED) == 0:
        lab:label_statemnt = _LB_STORED[CUR_LB]
        lab.add_character(input("What's the name of your character?\n>"))

        menu.create_text(f"Character num: {len(_LB_STORED[-1].char_hard)}", "CUSTOM", (1,9))

    menu.start_cast()

def _del_char(*nm):
    menu:Page=nm[1][0]
    if not len(_LB_STORED) == 0:
        lab:label_statemnt = _LB_STORED[CUR_LB]
        c -= 1
        for nme in lab.char_simple:
            c+=1
            print("NAME: ", nme, "ID: ", c)
        del c

        lab.del_character(int(input("What character u want to delete (ID)?\n>")))

    menu.start_cast()


def _say(*nm):
    menu:Page=nm[1][0]

    if not len(_LB_STORED) == 0:
        print("REMEMBER, HERE U CAN USE \\n or special character like that")
        sleep(5)
        lab:label_statemnt = _LB_STORED[CUR_LB]
        if input("Do you want to use pre-define characters? (y/n)\n> ") in _yes :
            c = -1
            for nme in _PRE_ALL_GAME:
                c+=1
                print("NAME: ", nme, "ID: ", c)

            lab.add_say(_PRE_ACRO_GAME[int(input("What's the ID (number)? \n>"))], 
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
    if not len(_LB_STORED) == 0:
        lab:label_statemnt = _LB_STORED[CUR_LB]

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
    if not len(_LB_STORED) == 0:
        lab:label_statemnt = _LB_STORED[CUR_LB]

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
   
################################################
#               WINDOW SIDE                    #
################################################

#MOD
def modder_menu(info):
    global CUR_CH, CUR_LB, _LB_STORED
    CUR_LB = 0
    CUR_CH = []
    _LB_STORED = []
    nme:str;ver:str;aut:str;ch:list|bool;ctn:str
    nme, ver, aut, ch, ctn = info
    
    start_path(ROOT_LOCAL)
    chk = start_loading()
    if not chk:
        CUR_CH = ch


    menu = Page(X=SIZE[0], Y=SIZE[1]+3, CHR="#")
    if len(VER) >= 10:
        menu.create_text(f"Hello, mod's version: {ver[:10]}", "CUSTOM", (1, 1))
    else:
        menu.create_text(f"Hello, mod's version: {ver}", "CUSTOM", (1, 1))
    
    menu.create_text(f"Compiled version: {COMPILER[:8]}", "CUSTOM", (72, 1))
    menu.create_text(f"App version: {VER}", "CUSTOM", (80, 16))

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
    btn.caster((""), menu, 1, 10, ["Nothing", "Nothing"], (8, 9), (6, 7), (10, 20), ..., False)
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
    btn.caster((""), ROOT_LOCAL, menu, ch, nme)
    menu.add_btn(btn)

    btn = Button(1, 15, TEXT="Back", DEFAULT="BACK")
    menu.add_btn(btn)

    menu.start_cast()
    #menu.get_pre_view()
