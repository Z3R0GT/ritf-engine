from os import chdir, path, listdir, mkdir, getcwd
from time import sleep

"""
from internal.tool.debug import _chk_window, print_debug

from button import Button
from page import Page
"""
from engine import *
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

        meta = open(getcwd()+"/meta.info", "w")
        meta.write(f"{cre};{vers};{ctn}")
        meta.close()

    _procces([nme, vers, cre, ch, ctn])


def proyect_lst_pro(*nm):
    num = nm[1][2]
    nme = nm[1][1][num]
    info = nm[1][0][nme]

    _procces([nme, info[1], info[0], True, info[2]])

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

    menu.get_pre_view()

_procces(["mc", "1.0", "me", True, "uwu.com"])

