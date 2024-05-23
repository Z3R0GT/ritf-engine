from os import chdir, path, listdir, mkdir, getcwd
from time import sleep

from engine import *
from engine.config.gen_arch import *
from engine.models.internal.tool.debug import _chk_window, print_debug

root = getcwd()
web ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

size = [100, 15]

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



_pre = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
_lb_all = []

#MENU
def _procces(info):
    #DEV[0] = False
    nme:str;ver:str;aut:str;ch:list|bool;ctn:str
    nme, ver, aut, ch, ctn = info

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
    menu = Page(X=size[0], Y=size[1], CHR="#")

    lst_dir = list(filter(path.isdir, listdir()))
    lst_arc = list(filter(path.isfile, listdir()))

    print(f"U ACTUALLY ARE EDITING THE MOD: {nme} (wait few seconds)")
    sleep(5)

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
                        for nme in _pre:
                            c+=1
                            print("NAME: ", nme, "ID: ", c)
                        lab.say(_pre[int(input("What's the ID (number)?: >"))], 
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
                print(a)

            print("TYSM for use this test, all end here (wait few seconds)")
            sleep(5)
            break

    btn = Button(X=1, Y=2, DEFAULT="BACK")
    btn.execute(0)