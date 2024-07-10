# READ BUTTONS NUM 
# #(LITERAL) - (INSIDE PAGE)

from tabnanny import check
from engine import *
from engine.config.gen_arch import *

#DEV[0] = False
DEV[1] = True

from os import chdir, path, listdir, mkdir, getcwd, remove
from time import sleep

#GEN  VARIABLES
VER     :str = "1.3.0"
VER_COM :str = "1.10.0"
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
CUR_CH                = []

JUMP_LINE = "\n>  "

################################################
#               FUNTIONS SIDE                  #
################################################

#GLOBAL SIDE
def _erase_sec(menu:Page, sec:tuple[int, int], ln:int):
    menu.create_text(" "*ln, "CUSTOM", sec)

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
        _erase_sec(menu, (3, 6+i), 50)

    menu.create_text(f"{nme}", "CUSTOM",  (3, 6))
    menu.create_text(f"{vers}", "CUSTOM", (3, 8))
    menu.create_text(f"{aut}",  "CUSTOM", (3, 10))
    menu.create_text(f"{ch}",   "CUSTOM", (3, 12))
    menu.create_text(f"{lnk}",  "CUSTOM", (3, 14))
    
    menu.btns[1].var = [{"name":nme, "version":vers, "creator":aut, "chapter":ch, "web":lnk}]
    del nme, vers, aut, ch, lnk
    menu.start_cast()

def _procces_load(*nm):



    print(nm)

#MODDER SIDE
def proyect_new_pro(*nm):
    global ROOT_GLOBAL, ROOT_LOCAL

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
    else:
        chdir(ROOT_GLOBAL+f"/proyects/{nm[1][0]["creator"]}")
        ROOT_LOCAL = getcwd()

    modder_menu(nm[1][0]["name"], nm[1][0]["version"], nm[1][0]["creator"], nm[1][0]["chapter"], nm[1][0]["web"])

def proyect_lst_pro(*nm):


    print(nm)


#################################################
#                MODDER 1                       #
#################################################


#################################################
#                MODDER 2                       #
#################################################

################################################
#               WINDOW SIDE                    #
################################################
def credits(*nm):


    ...



def main_menu():
    menu = Page(SIZE[0], SIZE[1])
    menu.create_text("RenTgen (Roses In The Flame's mod engine)", "CUSTOM", (3, 1))
    menu.create_text(f"Version {VER}", "CUSTOM", (menu.vec[0]-len(VER)-12, 1))

    btn = Button(3, 3, "Create new proyect", proyect_new)
    menu.add_btn(btn)

    btn = Button (3, 5, "Load proyect's list", proyect_lst)
    menu.add_btn(btn)

    btn = Button(3, 7, "Website main", WEB_MAIN_GAME, DEFAULT="LINK")
    menu.add_btn(btn)

    btn = Button(3, 9, "Website tale", WEB_TALE_GAME, DEFAULT="LINK")
    menu.add_btn(btn)

    btn = Button(3,11, "Exit", DEFAULT="EXIT")
    menu.add_btn(btn)

    del btn

    menu.start_cast()

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
    btn.caster(("Enter proyect's number"), menu, lst_pro, info)
    menu.add_btn(btn)    

    #2-1
    btn = Button(70, 17, "Load", proyect_lst_pro)
    btn.caster((""), info, lst_pro, 0)
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
               (2, 3),
               (4),
               (10, 20),
               [True, info],
               False)
    menu.add_btn(btn)

    #5-4
    btn = Button(15, 17, "Back", _con)
    btn.caster((""), menu,
               1,
               10, 
               lst_pro,
               (2, 3),
               (4),
               (0, 10),
               [True, info],
               False)
    menu.add_btn(btn)

    #6-5
    btn = Button(84, 17, "Back", DEFAULT="BACK")
    menu.add_btn(btn)

    del info, lst_pro
    menu.start_cast()

def modder_menu(nme:str, vers:str, aut:str, ch:list|bool, lnk:str):

    print(nme, vers, aut, ch, lnk)



main_menu()