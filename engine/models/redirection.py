from os import chdir, path, listdir, mkdir, getcwd
from time import sleep

from .internal.tool.debug import _chk_window, print_debug

from .button import Button
from .page import Page

root = getcwd()
web ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

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
    global size
    nme:str;ver:str;aut:str;ch:list|bool;ctn:str

    nme, ver, aut, ch, ctn = info
    menu = Page(X=size[0], Y=size[1], CHR="#")

    chdir(getcwd()+f"/{nme}")
    print(info)
    print(getcwd())
    print_debug("COMING SOON...")
    sleep(5)

    btn = Button(X=1, Y=2, DEFAULT="BACK")
    btn.execute(0)