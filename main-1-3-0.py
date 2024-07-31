# READ BUTTONS NUM 
# #(LITERAL) - (INSIDE PAGE)
from engine import *
from engine.config.gen_arch import *

#DEV[0] = False
DEV[1] = True

from os import chdir, path, listdir, mkdir, getcwd, remove
from time import sleep

#GEN  VARIABLES
VER     :str = "1.3.0"
VER_COM :str = "1.10.3"
COMPILER:str = "2087f702fcc2b23f0b914399cfc6442caafde5e4"

SIZE = [100, 15]
#MENU VARIABLES
ROOT_GLOBAL = getcwd()

WEB_MAIN_GAME  = "https://rosesintheflames.com/"
WEB_TALE_GAME  = "https://tales.rosesintheflames.com/"

MOD_DEFAULT={"name":"default",
             "version":"1.0",
             "creator":"Anonymus",
             "chapter":["1"],
             "web":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"
             }

CREDITS    ={"RiTF":      "CringleDragons",
             "Programmer":"Z3R0_GT",
             "CORE":      "Z3R0_GT & ScottTheFox",
             "VOP (lib)": "ScoStudios"
             }

#MOD  VARIABLE
ROOT_LOCAL:str

PRE_ACRO_NAME = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
PRE_ALL_GAME  = ["Snowy", "Magma", "Vivian", "Margaret", 
                 "Asher", "Ember", "Opal", "Thomas"]

YES                   = ["y", "yes", "si"]
LB_STORED:list[Label] = []
LB_CUR   :Label       

CUR_CH:list[str]      = []
CUR_VR:list[str]      = []


DFT_LB_MSG = "labels not found, create more"
DFT_CH_MSG = "characters not found, create more"

JUMP_LINE = "\n>  "
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

def _select_menu_print(obj:list):
    c=0
    for name in obj:
        c+=1
        print(f"NAME: {name} <---> ID: {c}")
    del c, name

def lb_checker(lst:list, msg:str) -> bool:
    if not len(lst) == 0:
        return True
    else: 
        print_debug(msg)
        sleep(5)
        return False

#MENU SIDE
def _procces_new(*nm):
    nme:str;vers:str;aut:str;ch:str;lnk:str
    nme, vers, aut, ch, lnk = nm[0]

    menu:Page = nm[1][0]
    
    if nme.replace(" ", "")  == "":
        from random import randint
        nme = "mod&"+str(randint(0,100))
    if vers.replace(" ", "") == "":
        vers= MOD_DEFAULT["version"]
    if aut.replace(" ", "") ==  "":
        aut = MOD_DEFAULT["creator"]
    if ch.replace(" ", "")  ==  "":
        ch  = MOD_DEFAULT["chapter"]
    else:
        ch:list = ch.split(",")
    if lnk.replace(" ", "") == "":
        lnk = MOD_DEFAULT["web"]

    for i in range(0, 6, 2):
        menu.create_text(" "*50, "CUSTOM", (3, 6+i))

    menu.create_text(f"{nme[:50]}",  "CUSTOM", (3,  6))
    menu.create_text(f"{vers[:50]}", "CUSTOM", (3,  8))
    menu.create_text(f"{aut[:50]}",  "CUSTOM", (3, 10))
    menu.create_text(f"{ch[:50]}",   "CUSTOM", (3, 12))
    menu.create_text(f"{lnk[:50]}",  "CUSTOM", (3, 14))
    
    menu.btns[1].var = [{"name":nme, "version":vers, "creator":aut, "chapter":ch, "web":lnk}]
    del nme, vers, aut, ch, lnk
    menu.start_cast()

def _procces_load(*nm):
    menu:Page=nm[1][0]
    if len(nm[0]) == 0:
        sel = 0
    else:
        sel = int(nm[0][0])+nm[1][1]

    info:dict = nm[1][3][1][nm[1][2][sel]]    
    
    for i in range(3):
        menu.create_text(" "*16, "CUSTOM", (62, 12+i))

    nme = nm[1][2][sel]
    if not info == "Error!":
        aut = info[0]
        vers= info[1]
        lnk = info[2]
    else:
        aut = "meta not found"
        vers= "meta not found"
        lnk = MOD_DEFAULT["web"]

    menu.btns[1].var = [info, nm[1][2][sel]]
    menu.btns[2].var = lnk
    
    menu.create_text(f"Mod's name: {nme[:15]}", "CUSTOM", (62, 12))
    menu.create_text(f"Autor: {aut[:15]}",      "CUSTOM", (62, 13))
    menu.create_text(f"Version: {vers[:15]}",   "CUSTOM", (62, 14))

    del i, info, sel, nme, aut, vers, lnk

    if not nm[1][3][0]:
        menu.start_cast()
    

#MODDER SIDE PRE
def proyect_new_pro(*nm):
    global ROOT_GLOBAL, ROOT_LOCAL

    #IN CASE THE PROYECT IS NEW
    if not check_proyects().__contains__(nm[1][0]["name"]):
        mkdir(ROOT_GLOBAL+f"/proyects/{nm[1][0]["name"]}")
        chdir(ROOT_GLOBAL+f"/proyects/{nm[1][0]["name"]}")

        ROOT_LOCAL = getcwd()

        open(ROOT_LOCAL+"/base.info", "w").close()
        open(ROOT_LOCAL+"/main.rpy",  "w").close()

        mkdir(ROOT_LOCAL+"/.config")
        mkdir(ROOT_LOCAL+"/.config/autosaves")

        meta = open(ROOT_LOCAL+"/meta.info", "w")
        meta.write(f"{nm[1][0]["creator"]};{nm[1][0]["version"]};{nm[1][0]["web"]};{nm[1][0]["chapter"]}")
        meta.close()
    #OTHERWISE, JUST IT CHANGE TO THE CURRENT PROYECT
    else:
        chdir(ROOT_GLOBAL+f"/proyects/{nm[1][0]["creator"]}")
        ROOT_LOCAL = getcwd()

    modder_menu(nm[1][0]["name"], nm[1][0]["version"], nm[1][0]["creator"], nm[1][0]["chapter"], nm[1][0]["web"])

def proyect_lst_pro(*nm):
    global ROOT_GLOBAL, ROOT_LOCAL
    nme:str; vers:str; cre:str; ch:list; lnk:str
    nme = nm[1][1]
    aut, vers, lnk, ch  = nm[1][0]

    modder_menu(nme, vers, aut, ch, lnk)

#MODDER SIDE CUR
def paths_finder() -> tuple[list[str], bool, list[str]] | Literal["pass"]:
    global ROOT_LOCAL
    chdir(ROOT_LOCAL+"/.config/autosaves")
    info = list(filter(path.isfile, listdir()))

    #SECURITY CHECKER
    if len(info) == 0:
        chdir(ROOT_LOCAL)
        return "pass"
    
    if not "end.json" in info:
        name_loaded = ["temp_ñ_0.json"]

        for names in info:
            name_from = names[5:].replace(".json", "")
            if not names in name_loaded:
                name_to = name_loaded[-1][5:].replace(".json", "")

                num_from, num_to = name_from.find("_"), name_to.find("_")
                if name_from[:num_from-1] == name_to[:num_to-1] and \
                    int(name_from[num_from:]) >= int(name_to[num_to:]):
                    name_loaded[-1] = names
                else:
                    name_loaded.append(names)

        if name_loaded[0] == "temp_ñ_0.json":
            del name_loaded[0]
        ch = False
    else:
        name_loaded = ["end.json"]
        ch = True

    lst = []
    if not len(name_loaded) == 1:
        for name in name_loaded:
            lst.append(getcwd()+f"/{name}")
    else:
        lst.append(getcwd()+"/"+name_loaded[0])
        
    return lst, ch, info

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

def loader_label() -> bool:
    global ROOT_LOCAL, CUR_CH, LB_STORED
    from json import load

    info = paths_finder()
    #SECURITY CHECKER
    if info == "pass":
        return True
    
    info_load:list[dict] = []
    if info[1]:
        #CASE "END"
        with open(info[0][0], "r") as file:
            dit = load(file)

            for in_ in dit["root"]:
                info_load.append(dit["root"][in_])
    else:
        #CASE "TEMP"
        if len(info[0]) == 1:
            info_load.append(load(open(info[0][0], "r")))
        else:
            for paths in info[0][0]:
                with open(paths, "r") as file:
                    info_load.append(load(file))

    #ERASE ARCHIVES
    for paths in info[2]:
        remove(paths)

    #LOADER
    for info in info_load:
        if not str(info["chapter"]) in CUR_CH:
            CUR_CH.append(str(info["chapter"]))

        #LABELS
        LB_STORED.append(create_instance(info))

    chdir(ROOT_LOCAL)
    return False

def _process_compiler(root:str, lib:dict, nme_arch:str):
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

def _compiler(*nm):
    global LB_STORED, ROOT_LOCAL
    import zipfile as zip
    from json import dump
    menu:Page=nm[1][0]

    if not len(LB_STORED) == 0:
        try:
            ch = nm[1][1]
            with open(ROOT_LOCAL+f"/.config/autosaves/end.json", "w") as file:
                info = {"root":{}}
                for labe in LB_STORED:
                    labe:Label
                    info["root"][labe.name] = labe.meta

                dump(info, file, indent=1)

            keys = list(info["root"].keys())[0]
            _process_compiler(ROOT_LOCAL, info, keys)
            
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
        #_sel_label(["y"], nm[1])
        return
    sleep(5)
    menu.start_cast()

#################################################
#                MODDER 1                       #
#################################################

def _edi_(*nm):
    

    print(nm)

def _sel_label(*nm):
    ...
#################################################
#                MODDER 2                       #
#################################################

def _char_create(*nm):
    menu:Page=nm[1][0]
    if lb_checker(LB_STORED, DFT_LB_MSG):
        if nm[0][0] in YES:
            name:str;text:int
            name, text = [
                        input(f"What's the name of your character?{JUMP_LINE}"), 
                        int(input(f"What's would be the text size?{JUMP_LINE}"))
                        ]
            LB_CUR.add_character(name, text_size=text)
        else:
            _select_menu_print(LB_CUR.char_simple)
            ID = int(input(f"What character u want to delete?{JUMP_LINE}"))
            LB_CUR.del_character(ID)

    menu.start_cast()

def __char_edito(*nm):
    if lb_checker(LB_STORED, DFT_LB_MSG) and lb_checker(LB_CUR._char_obj,DFT_CH_MSG):
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
        print(nm)
        input()
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
        menu:Page=nm[1][0]
        menu.start_cast()

def _sou_create(*nm):
    ...

def _if_create(*nm):
    ...

def _say_create(*nm):
    ...

################################################
#               WINDOW SIDE                    #
################################################



#MAIN
def main_menu():
    menu = Page(SIZE[0], SIZE[1])
    menu.create_text("RenTgen (Roses In The Flame's mod engine)", "CUSTOM", (3, 1))
    menu.create_text(f"Version {VER}", "CUSTOM", (menu.vec[0]-len(VER)-12, 1))

    btn = Button(3, 3, "Create new proyect", proyect_new)
    menu.add_btn(btn)

    btn = Button (3, 5, "Load proyect's list", proyect_lst)
    menu.add_btn(btn)

    btn = Button(3, 7, "Creadits", credits)
    menu.add_btn(btn)

    btn = Button(3, 9, "Website main", WEB_MAIN_GAME, DEFAULT="LINK")
    menu.add_btn(btn)
    btn = Button(3, 10, "Website tale", WEB_TALE_GAME, DEFAULT="LINK")
    menu.add_btn(btn)

    btn = Button(3,13, "Exit", DEFAULT="EXIT")
    menu.add_btn(btn)
    del btn

    menu.start_cast()

#MAIN-SUB-1
def proyect_new(*nm):
    del nm
    menu = Page(SIZE[0], SIZE[1]+4)

    menu.create_text("Creation mod menu", "CUSTOM", (3, 3))
    menu.create_text(f"Version {VER}",    "CUSTOM", (menu.vec[0]-len(VER)-12, 1))

    menu.create_text("Mod's name:",      "CUSTOM", (3, 5))
    menu.create_text("Version:",         "CUSTOM", (3, 7))    
    menu.create_text("Author:",          "CUSTOM", (3, 9))
    menu.create_text("Chapters to mod:", "CUSTOM", (3,11))
    menu.create_text("Contac:",          "CUSTOM", (3,13))

    #1-0
    btn = Button(2, 17, "Enter information", _procces_new)
    btn.caster(("What's the name of your mod?",
                "What's version is?",
                "Who's the creator",
                "Enter the chapters to mod",
                "Do you have some social network? (URL/or just press 'Enter')"),
                menu)
    menu.add_btn(btn)

    #2-1
    btn = Button(70, 17, "Create",proyect_new_pro)
    btn.caster((""), MOD_DEFAULT)
    menu.add_btn(btn)

    #3-2
    btn = Button(84, 17, "Back", DEFAULT="BACK")
    menu.add_btn(btn)

    #INFO PANEL-1
    menu.add_panel(68, 4, 
                   32, 8, 
                   0)
    menu.create_text("Tutorial:", "CUSTOM", (71, 5))
    del btn

    menu.start_cast()
    
#MAIN-SUB-2
def proyect_lst(*nm):
    del nm
    info = check_proyects()
    lst_pro = list(info.keys())

    if len(lst_pro) == 0:
        erase_screen()
        print_debug(f"{VER} YOU DON'T HAVE PROYECTS CREATED YET {VER}")
        print_debug(F"{VER}     REDIRECTING TO CREATE A NEW...  {VER}")
        sleep(5)
        proyect_new()
        return
    
    menu = Page(SIZE[0], SIZE[1]+4)

    menu.create_text("Proyect's page", "CUSTOM", (3,3))
    menu.create_text(f"Version {VER}",  "CUSTOM", (menu.vec[0]-len(VER)-12, 1))

    menu.add_panel(0,  4, 27,12, 0)  #SELECT SECTION
    menu.add_panel(60, 3, 32, 6, 0)  # TUTORIAL

    menu.add_panel(60, 11,32, 5, 0)  #META

    #1-0
    btn = Button(31, 17, "Select Proyect", _procces_load)
    btn.caster(("Enter proyect's number"))
    menu.add_btn(btn)    

    #2-1
    btn = Button(70, 17, "Load", proyect_lst_pro)
    btn.caster((""), info[lst_pro[0]], lst_pro[0])
    menu.add_btn(btn)

    #3-2
    btn = Button(62, 15, "Autor url", info[lst_pro[0]][2], DEFAULT="LINK")
    menu.add_btn(btn)

    #4-3
    btn = Button(1, 17, "Next", _con)
    btn.caster((""), menu,
               1,
               10,
               lst_pro,
               (4, 5),
               (1),
               (10, 20),
               [False, info],
               False
               )
    menu.add_btn(btn)

    #5-4
    btn = Button(15, 17, "Back", _con)
    btn.caster((""), menu,
               1,
               10, 
               lst_pro,
               (4, 5),
               (1),
               (0, 10),
               [True, info],
               False
               )
    menu.add_btn(btn)

    #6-5
    btn = Button(84, 17, "Back", DEFAULT="BACK")
    menu.add_btn(btn)


    menu.execute_btn(5)
    menu.btns[4].var[7][0] = False
    _procces_load([], [menu, 0, lst_pro, [True, info]])
    del info, lst_pro
    
    menu.start_cast()

#MAIN-SUB-3
def credits(*nm):
    del nm
    name = list(CREDITS.keys())

    menu = Page(50, 15)
    menu.create_text("Credits", "CUSTOM", (20, 1))

    for i in range(0, len(name)):
        menu.create_text(f"{name[i-1]}: {CREDITS[name[i-1]]}", "CUSTOM", (10, 3+i*2))

    btn = Button(1, 13, "Back", DEFAULT="BACK")
    menu.add_btn(btn)

    menu.start_cast()

#MOD
def modder_menu(nme:str, vers:str, aut:str, ch:list|bool, lnk:str):
    global ROOT_GLOBAL, ROOT_LOCAL, LB_STORED, LB_CUR, CUR_CH
    chdir(ROOT_GLOBAL+f"/proyects/{nme}")
    ROOT_LOCAL = getcwd()

    global_config(cwd=ROOT_LOCAL)
    chk = loader_label()

    say_lst = ["Create a new say!", "That will appear here"]
    var_lst = ["Create vars", "Here"]

    if not chk:
        LB_CUR = LB_STORED[0]
        mne = LB_CUR.name
        if not len(LB_CUR.dialog) == 0:
            say_lst = _str_say_menu(obj=LB_CUR.dialog)
        if not len(LB_CUR.init) == 1:
            var_lst = _str_say_menu(15, LB_CUR.init)
    else:
        CUR_CH = ch
        mne = None

    menu = Page(105, 22)

    #TAGS-1
    menu.create_text(f"Current proyect working on: {nme}", "CUSTOM", (1,1))
    menu.create_text(f"Current label working on: {mne}",   "CUSTOM", (1,2))

    #TAGS-2
    menu.create_text("Currect flowchart: Main", "CUSTOM", (46, 2))
    menu.create_text("Variables Created", "CUSTOM", (85,2))

    #PANELS
    menu.add_panel(0,  3, 20, 16, 0) #BTNs
    menu.add_panel(33, 3, 48, 14, 0) #DIALOG
    menu.add_panel(83, 3, 20, 14, 0) #VAR



    
    #1-0
    btn = Button(1, 4, "Set character", _char_create, "char_nm")
    btn.caster(("You want add a character? (y/n)"), 
            menu)
    menu.add_btn(btn)
    
    #2-1
    btn = Button(1,5, "Edit character", __char_edito, "char_men")
    btn.caster((""), 
            menu, "normal, char")
    menu.add_btn(btn)

    #3-2
    btn = Button(1,7, "Set source", _sou_create, "sou_nm")
    btn.caster(("You want add a 'source'? (y/n)"), 
            menu, "normal", "if")
    menu.add_btn(btn)

    #4-3
    btn = Button(1, 8, "Set if", _if_create, "if_nm")
    btn.caster(("What's the varible's ID?", 
                "What's operator? (equal/==/1, geater/>=/2, smaller/<=/3, not/!=/4)", 
                "What's the Variable's ID/variable?",
                "What's name of this condition?"), 
            menu, "normal", "if")
    menu.add_btn(btn)

    #5-4
    btn = Button(1, 10, "Set say", _say_create, "say_nm")
    btn.caster(("You want add a say? (y/n)"), 
            menu, "normal", "say")
    menu.add_btn(btn)

    #6-5
    btn = Button(1, 12, "Edit statement", _edi_, "edit_nm")
    btn.caster(("What's the ID"), 
               menu, "normal")
    menu.add_btn(btn)


    btn = Button(1, 16, "Export mod", _compiler, "save")
    btn.caster((""), menu, ch, nme)
    menu.add_btn(btn)


    btn = Button(1, 18, "Back menu", DEFAULT="BACK")
    menu.add_btn(btn)



    #...-...
    btn = Button(1, 20, "Select Label", _sel_label)
    btn.caster(("U want add a label? (y/n)?"), menu, ch)
    menu.add_btn(btn)

    #TAGS-3
    menu.create_text(f"App ver: {VER}/{VER_COM}", "CUSTOM", (50, 20))
    menu.create_text(f"Compiled: {COMPILER[:10]}", "CUSTOM", (80, 20))

    menu.start_cast()


#main_menu()
modder_menu("RenTgenTest", "1.0", "Z3R0_GT", ["1"], "https://www.youtube.com/watch?v=dQw4w9WgXcQ")