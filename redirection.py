from os import chdir, path, listdir, mkdir, getcwd
from time import sleep
from tkinter import Menu

from engine import *
from engine.config.gen_arch import *
from engine.models.internal.tool.debug import _chk_window, print_debug

root = getcwd()
web ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

size = [100, 15]

#procces functions
def check_proyects() -> dict:
    global root
    
    try:
        chdir(root+"/proyects")
    except:
        mkdir(root+"/proyects")
        chdir(root+"/proyects")

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
    print(mn)
    nme, vers, cre, ch, ctn = mn[1][0]

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
        mkdir(root+f"/proyects/{nme}")
        chdir(root+f"/proyects/{nme}")

        open(getcwd()+"/base.info", "w").close()
        dr = open(getcwd()+"/base.info", "a")
        for inf in ch:
            dr.write(f"chapter_{inf}.rpy,")
        dr.close()
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

def _save_all(lib:dict, 
              nme_arch:str): #or compile
    root = getcwd()

    a = open(root+f"/{nme_arch}.rpy", "w")
    a.write("")
    a.close()

    with open(root+f"/{nme_arch}.rpy", "a") as f:
        for nme in lib["root"]:
            
            for ch in lib["root"][nme]["character"]:
                for line in ch:
                    f.write(line)
            
            for dia in lib["root"][nme]["dialog"]:
                for line in dia:
                    f.write(line)

        f.close()

_pre_acro = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
_pre_all  = ["Snowy", "Magma", "Vivian", "Margaret", "Asher", "Ember", "Opal", "Thomas"]
_lb_all = []

ver : str = "a1.1.4.4"

#MENU
#BUG -1: TEMPORALMENTE SE AGREGARA LA LINEA DE MANERA LITERAL
#SOLUCIÓN -1: Calificar cada escena/cosa que ocurre en el juego con
#base a que tan fuerte (se requiere una base de datos para hacerlo más facil)






def _procces(info):
    global ver
    #DEV[0] = False
    nme:str;ver_:str;aut:str;ch:list|bool;ctn:str
    nme, ver_, aut, ch, ctn = info

    chdir(root+f"/proyects/{nme}")
    if ch == True:
        _nm = open("base.info", "rt").read().split(",")
        ch = []
        for nm in _nm: 
            if nm[:7] == "chapter":
                ch.append(nm[8:].replace(".rpy", ""))
        del _nm, nm
    else:
        ch = info[3]
    menu = Page(X=size[0]+40, Y=size[1]+20, CHR="#")
    
    menu.create_text(f"version {ver}", "CUSTOM", (menu.vec[0]-len(ver)-12, 1))

    lst_dir = list(filter(path.isdir, listdir()))
    lst_arc = list(filter(path.isfile, listdir()))

    menu.create_text("Current archive (<)", "CUSTOM", (4,1)) #CONVERTIR A BOTON
    menu.create_text("Info mod/archive", "CUSTOM", (30,1)) #CONVERTIR A BOTON
    
    menu.create_text("Line to insert (temp)", "CUSTOM",(58,1))
    menu.create_text("len char/ima (<)", "CUSTOM",(60,6))

    menu.create_text("Character created", "CUSTOM", (83,1))


    #arch
    menu.add_panel(1,  2, 22, 12, 0)
    #inf_mod
    menu.add_panel(28, 2, 28, 12, 0)
    #char
    menu.add_panel(83, 2, 22,12, 0)
    
    ##stats
    #line
    menu.add_panel(62, 2, 10, 3, 0)
    #ln_ch
    menu.add_panel(62,7, 10, 3, 0)
    #ln_ima
    menu.add_panel(62,11,10, 3, 0)

    #lst_cur_lab
    menu.add_panel(2,16,70,16,0)
    #lst_cur_var_info
    menu.add_panel(80,16,58,15,0)


    #JUST FOR REFERENCE
    menu.create_text("LLISTS", "CUSTOM", (4,3))
    menu.create_text("ARCHIVE", "CUSTOM", (4,4))
    
    
    menu.create_text("NAME MOD", "CUSTOM", (31,3))
    menu.create_text("VERSION MOD", "CUSTOM", (31, 4))
    menu.create_text("LABEL WORKING ON ARCHIVE", (31,5))


    menu.create_text("NUM", "CUSTOM", (65,3))
    menu.create_text("NUM", "CUSTOM", (65,8))
    menu.create_text("NUM", "CUSTOM", (65,12))

    menu.create_text("CHAR", "CUSTOM", (84,3))

    menu.create_text("ID   NAME  PJs-IN   addons-dialog", "CUSTOM", (3, 17))

    menu.create_text("BTN", "CUSTOM", (3,15))
    menu.create_text("BTN", "CUSTOM",(9,15))

    menu.create_text("BTN", "CUSTOM", (30,15))
    menu.create_text("BTN", "CUSTOM", (38, 15))

    menu.create_text("BTN", "CUSTOM", (85,15))
    menu.create_text("BTN", "CUSTOM", (90,15))

    menu.create_text("BTN", "CUSTOM", (4, 33))
    menu.create_text("BTN", "CUSTOM", (20,33))
    menu.create_text("BTN_SAVE", "CUSTOM", (127,33))

    menu.create_text("CUR_INFO", "CUSTOM", (82,17))

    menu.create_text("CREATED BY:Z3R0_GT V1.0 INFERNO", "CUSTOM", (106, 3))
    menu.create_text("A special thanks to Cringle,", "CUSTOM", (106, 5))
    menu.create_text("ScottTheFox, ArchangelCGA and", "CUSTOM", (106, 6))
    menu.create_text("ScoStudio for this ", "CUSTOM", (106, 7))
    menu.create_text("opportunity and help me a lot", "CUSTOM", (106, 8))


    menu.get_pre_view()

    #sleep(10)

"""
    #TEST
    start_()

    while True:
        if not len(_lb_all) <= 1:
            if input("Do you want create a new label? (y/n): >") in ["y", "Y", "yes"]:
                _lb_all.append(label_statemnt(input("What's name of your label?: >")))
                cur = -1
            else:
                while True:
                    for nme in _lb_all:
                        print(nme)

                    _in = input("What's the name of your label?: >")
                    c= -1
                    for nme in _lb_all:
                        nme:label_statemnt
                        c+=1
                        if nme.nme == _in:
                            cur = c
                            break
                        else:
                            print("Not found!, try again (Wait a couple of seconds)")
                            sleep(5)
        else:
            _lb_all.append(label_statemnt(input("What's name of your label?: >")))
            cur = -1

        while True:
            lab:label_statemnt = _lb_all[cur]
            match int(input("do u want create a: \
                \nCharacter (1) \
                \nSay something (2) \
                \nEnd with this label (3) \n: >")):
                case 1:
                    lab.character(input("What's the name of your character?: >"))
                case 2:
                    if input("Do you want to use pre-define characters? (y/n): ") in ["y", "Y", "yes"]:
                        c = -1
                        for nme in _pre_all:
                            c+=1
                            print("NAME: ", nme, "ID: ", c)
                        lab.say(_pre_acro[int(input("What's the ID (number)?: >"))], 
                                        True, 
                                        input("What do u want that this character say?: \n>"))
                    elif input("is your character still exits? (y/n): >") in ["y", "Y", "yes"]:    
                        c = -1
                        for nme in lab.char:
                            c+=1
                            print("NAME: ", nme, "ID: ", c)
                        lab.say(lab.char[int(input("What's the ID (number)?: >"))], 
                                True, 
                                input("What do u want that this character say?: \n>"))
                    else:
                        print("We recommend u use 'Character' option to don't repeat many time this... (wait a few seconds)")
                        sleep(5)

                        if input("Do u want use a character's name? (y/n): >") in ["Y", "y", "yes"]:
                            lab.say(input("What's the name?: >"), 
                                    False,
                                    input("What do u want that this character say?: \n>"))
                        else:
                            lab.say(None, 
                                    False,
                                    input("What do u want that this character say?: \n>"))
                    
                case 3:
                    print("Ty for using! (wait a few seconds)")
                    sleep(3)
                    break
            
            _chk_window()

        if input("Do u want exit rn? (y/n): >") in ["y", "Y", "yes"]:
            from datetime import datetime as dtime
            from json import dump

            with open(getcwd()+f"/.config/autosaves/{dtime.now().day}_{dtime.now().month}_end.json", "w") as f:
                a = {"root":{}}
                for data in _lb_all:
                    data:label_statemnt
                    a["root"][data.nme] = data.meta
                
                dump(a, f, indent=1)

            print("TYSM for use this test, all end here (wait few seconds)")
            sleep(5)
            break
    
    _save_all(a, "test")
    #btn = Button(X=1, Y=2, DEFAULT="BACK")
   # btn.execute(0)
"""

_procces(["mc", "1.0", "me", True, web])