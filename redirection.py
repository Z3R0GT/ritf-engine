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
        mkdir(root_global+f"/proyects/{nme}")
        chdir(root_global+f"/proyects/{nme}")

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
def _save_all(*n): #or compile
    root:str;lib:dict;nme_arch:str
    root, lib, nme_arch = n

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

#NEED RE WORk
def __archive_list(*nm):
    menu:Page;info:dict;is_fow:bool;is_new:bool
    menu, info, is_fow, rn, is_new = nm[1]
 
 #   print(menu.btns[0].var)
  #  print()
  #  if not is_new:
  #      print(menu.btns[1].var)
  #      print()
  #  print(nm)
  #  input()

    if is_fow:
        ran = range(rn-10, rn)
    else:
        ran = range(rn,rn+10)

    tig = False
    if not is_new and (rn-10 <= 0 or ran[-1] >= info["lst"][1]+10):
        tig = True

    if not tig:
        #eraser
        for nme in range(10):
            menu.create_text(" "*(menu.meta["panel"][1]["transform"][0]-2), "CUSTOM", (2, nme+3))
        #adder text
        for in_ in ran:
            if in_ >= info["lst"][1]:
                ch = True
                break

            if len(info["lst"][0][in_]) < menu.meta["panel"][1]["transform"][0]-1:
                menu.create_text(f"{in_%10+1} "+info["lst"][0][in_], "CUSTOM", (4, (in_%10)+3))
            else:
                menu.create_text(f"{in_%10+1} "+info["lst"][0][in_][:19]+"...", "CUSTOM", (4, (in_%10)+3))

            ch = False

        if is_new:
            menu.btns[0].caster((""), menu, info, True, menu.btns[0].var[3]+10, False)
            menu.add_btn(menu.btns[0], False)
            return
        else:
            if is_fow:
             #   input("a")
                if not menu.btns[0].var[3] >= rn+10:
              #      input("add_fow")
                    menu.btns[1].caster((""), menu, info, False, menu.btns[1].var[3]-10, False)
                    menu.add_btn(menu.btns[0], False)
                    
                    menu.btns[0].caster((""), menu, info, True, menu.btns[0].var[3]+10, False)
                    menu.add_btn(menu.btns[1], False)

                if ch:
             #       input("add_back")
                    menu.del_btn(1, False)
            else:
            #    input("b")
                if not menu.btns[1].var[3] <= rn-10:
           #         input("add_fow")
                    menu.del_btn(2, False)
                else:
             #       input("add_back")
                    menu.btns[0].caster((""), menu, info, False, menu.btns[0].var[3]-10, False)
                    menu.add_btn(menu.btns[1], False)

                    menu.btns[1].caster((""), menu, info, True, menu.btns[1].var[3]+10, False)
                    menu.add_btn(menu.btns[0], False)

    menu.start_cast()

_pre_acro = ["Sy", "Ma", "Vn", "Mt", "Ar", "Er", "Op", "Ts"]
_pre_all  = ["Snowy", "Magma", "Vivian", "Margaret", "Asher", "Ember", "Opal", "Thomas"]
_lb_all = []

ver : str = "a1.1.4.4"

#MENU
#BUG -1: TEMPORALMENTE SE AGREGARA LA LINEA DE MANERA LITERAL
#SOLUCIÓN -1: Calificar cada escena/cosa que ocurre en el juego con
#base a que tan fuerte (se requiere una base de datos para hacerlo más facil)

def _refresh_char(*n):
    
    print(n)

def _refresh_info(*n):
    
    print(n)

def _refresh_cur(*n):
    
    print(n)

def _refresh_nu_s(*n):
    
    print(n)

def _procces(info):
    DEV[0] = False

    nme:str;ver_:str;aut:str;ch:list|bool;ctn:str
    nme, ver_, aut, ch, ctn = info

    chdir(root_global+f"/proyects/{nme}")
    if ch == True:
        _nm = open("base.info", "rt").read().split(",")
        ch = []
        for nm in _nm: 
            if nm[:7] == "chapter":
                ch.append(nm[8:].replace(".rpy", ""))
        del _nm, nm
    else:
        ch = info[3]

    lst_final = _get_lst()[0]
    
    menu = Page(X=size[0]+40, Y=size[1]+20, CHR="#")
    
    menu.create_text(f"version {ver}", "CUSTOM", (menu.vec[0]-len(ver)-12, 1))
    
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

    menu.create_text("CUR_INFO", "CUSTOM", (82,17))

    info_arch = {"lst":[lst_final, len(lst_final)]}
    
    #NEXT-1
    btn_arch1 = Button(X=1, Y=15, TEXT="Next",ACTION=__archive_list, DEFAULT="CUSTOM")
    btn_arch1.caster((""), menu, info_arch, True, 10, False)
    menu.add_btn(btn_arch1)
    menu.del_btn(1, False)

    __archive_list((""),[menu, info_arch, False, 0, True])

    btn_arch2 = Button(X=11, Y=15, TEXT="Back", ACTION=__archive_list, DEFAULT="CUSTOM")
    btn_arch2.caster((""), menu, info_arch, False, 10, False)
    menu.add_btn(btn_arch2)
    menu.del_btn(2, False)
    
    #NEXT-2
    btn_func1 = Button(X=30, Y=15, TEXT="sel dir", ACTION=_refresh_info, DEFAULT="CUSTOM")
    menu.add_btn(btn_func1)

    btn_func2 = Button(X=42, Y=15, TEXT="back dir", ACTION=_refresh_info, DEFAULT="CUSTOM")
    menu.add_btn(btn_func2)


    #NEXT-3
    btn = Button(X=83, Y=15, TEXT="Next", ACTION=_refresh_char, DEFAULT="CUSTOM")
    menu.add_btn(btn)
    btn = Button(X=93, Y=15, TEXT="Back", ACTION=_refresh_char, DEFAULT="CUSTOM")
    menu.add_btn(btn)


    #NEXT--4
    btn = Button(X=4, Y=33, TEXT="Next", ACTION=_refresh_nu_s, DEFAULT="CUSTOM")
    menu.add_btn(btn)
    btn = Button(X=20, Y=33, TEXT="Back", ACTION=_refresh_nu_s, DEFAULT="CUSTOM")
    menu.add_btn(btn)

    #NEXT--5



    btn = Button(X=127, Y=33, TEXT="Export", ACTION=_save_all, DEFAULT="CUSTOM")
    menu.add_btn(btn)




    #SECTION'S THANKS
    #menu.create_text("CREATED BY:Z3R0_GT V1.0 INFERNO", "CUSTOM", (106, 3))
    #menu.create_text("A special thanks to Cringle,", "CUSTOM", (106, 5))
    #menu.create_text("ScottTheFox, ArchangelCGA and", "CUSTOM", (106, 6))
    #menu.create_text("ScoStudio for this ", "CUSTOM", (106, 7))
    #menu.create_text("opportunity and help me a lot", "CUSTOM", (106, 8))


    
    menu.start_cast()
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