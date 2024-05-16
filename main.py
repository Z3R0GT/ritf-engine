from engine import *
from engine.models.internal.tool.debug import _chk_window, print_debug
from engine.models.redirection import *
from time import sleep

ver : str = "a1.1.4.1"
ver_main : str = "1.0"

size = [100, 15]

web ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

DEV[0] = False
in_ = Button(X=12, Y=12, DEFAULT="BACK")

def _procces_new(*nm):
    nme:str; vers:str; cre:str; ch:str; ctn:str
    nme, vers, cre, ch, ctn = nm[0]

    menu:Page = nm[1][0]

    if nme == "":
        from random import randint
        nme = "mod_"+str(randint(0,100))  
    if vers.replace(" ", "") == "":
        vers = "1.0"
    if cre.replace(" ", "") == "":
        cre = "Anonymus"
    if ch.replace(" ", "") == "":
        ch = "1"
    if ctn.replace(" ", "") == "":
        ctn = web

    menu.create_text(f"{nme}", "CUSTOM", (3,6))
    menu.create_text(f"{vers}", "CUSTOM", (3,8))
    menu.create_text(f"{cre}", "CUSTOM", (3,10))

    ch = ch.split(",")
    menu.create_text(f"{ch}", "CUSTOM", (3,12))

    menu.create_text(f"{ctn}", "CUSTOM", (3, 14))
    menu.btns[1].var = [nme, vers, cre, ch, ctn]

    menu.start_cast()

def _procces_lst_info(*nm):
    _in:int; menu:Page; sec:int; info:dict
    _in, menu, sec, info = nm[0][0], nm[1][0], nm[1][1], nm[1][2]
    _in_ = int(_in)

    lst_pro = [i for i in info]

    for i in range(3):
        menu.create_text(" "*25, "CUSTOM", (62, 12+i))

    if sec <= 0:
        pass
    else:
        _in_ += 10*sec

    if len(lst_pro[_in_-1]) >= 32:
        nme = f"Mod's name: {lst_pro[_in_-1][:24]}..."
    else:
        nme = f"Mod's name: {lst_pro[_in_-1]}"

    ref = info[lst_pro[_in_-1]]
    if not ref == "Error!":
        inf = []
        for _in in range(2):
            if len(ref[_in]) >= 25:
                inf.append(ref[_in][:20]+"...")
            else:
                inf.append(ref[_in])

        aut = inf[0]
        ver_ = inf[1]
        lnk = ref[2]
    else:
        aut = "meta not found"
        ver_ = "meta not found"
        lnk = web

    menu.btns[4].var = (info, lst_pro, _in_-1)

    menu.create_text(nme, "CUSTOM", (62, 12))
    menu.create_text(f"Autor: {aut}", "CUSTOM", (62, 13))
    menu.create_text(f"Version: {ver_}", "CUSTOM", (62, 14))

    menu.start_cast()

def _procces_lst_refresh(*nm):
    lst_pro:list; cur_len:int;menu:Page; nro_pg:int
    lst_pro, cur_len, menu, nro_pg = nm[1][0], nm[1][1], nm[1][2], nm[1][3]

    menu.add_btn(menu.btns[0], False)
    menu.add_btn(menu.btns[1], False)

    #ERASER
    for nme in range(10):
        menu.create_text(" "*(menu.meta["panel"][1]["transform"][0]-2), "CUSTOM", (1,nme+5))
    #NME CASE
    for in_ in range(10):
        nme = in_ + len(lst_pro) - cur_len
        if nme >= len(lst_pro):
            break

        if len(lst_pro[nme]) < menu.meta["panel"][1]["transform"][0]-2:
            menu.create_text(lst_pro[nme], "CUSTOM", (1,in_+5)) 
        else:
            menu.create_text(lst_pro[nme][:20]+"...", "CUSTOM", (1,in_+5))

    chk:bool=False
    #RETURN CASE
    if cur_len >= len(lst_pro):
        menu.btns[0].caster((""), lst_pro, len(lst_pro), menu, 0)
        chk = True
        menu.del_btn(1, False)
    else:
        menu.btns[0].caster((""), lst_pro, cur_len+10, menu, nro_pg-1) 
    
    #NEXT CASE
    if cur_len-10 <= 0:
        menu.btns[1].caster((""), lst_pro, cur_len, menu, nro_pg)
        menu.del_btn(2, False)
        if chk:
            menu.btns[3].var = (menu.btns[3].var[0], 0, menu.btns[3].var[2])
        else:
            menu.btns[3].var = (menu.btns[3].var[0], nro_pg+1, menu.btns[3].var[2])

    else:
        menu.btns[1].caster((""), lst_pro, cur_len-10, menu, nro_pg+1)
        menu.btns[3].var = (menu.btns[3].var[0], nro_pg+1, menu.btns[3].var[2])

    menu.start_cast()

def proyect_new(*nm):
    menu = Page(X=size[0], Y=size[1]+4, CHR="#")

    menu.create_text("Creation mod menu", "CUSTOM", (3, 3))
    menu.create_text(f"version {ver}", "CUSTOM", (menu.vec[0]-len(ver)-12, 1))

    menu.create_text("Mod's name:", "CUSTOM", (3, 5))

    menu.create_text("Version:", "CUSTOM", (3, 7))

    menu.create_text("Author:", "CUSTOM", (3,9))

    menu.create_text("Chapters to mod:", "CUSTOM", (3, 11))

    menu.create_text("Contac:", "CUSTOM", (3, 13))

    btn = Button(X=2, Y=17, TEXT="Enter data",ACTION=_procces_new, DEFAULT="CUSTOM")
    btn.caster(("What's the name of your mod?", "What's version is?", 
                "Who's the creator?", 
                "Enter the chapters to mod (separete by comas)", 
                "Do you have some social network or URL for the mod? (write the URL)"), menu)
    menu.add_btn(btn)
    
    btn = Button(X=70, Y=17, TEXT="Create", ACTION=proyect_new_pro, DEFAULT="CUSTOM")
    btn.caster((""),["", "", "", ["1"], ""]) 
    menu.add_btn(btn)

    btn = Button(X=84, Y=17, TEXT="Back", DEFAULT="BACK")
    menu.add_btn(btn)

    menu.add_panel(68, 4, 32, 8, 0)
    menu.create_text("Tutorial:", "CUSTOM", (71,5))

    menu.start_cast()

def proyect_list(*nm):
    info = check_proyects()
    lst_pro = [i for i in info]
    if not len(lst_pro) == 0:
        menu = Page(X=size[0], Y=size[1]+4, CHR="#")

        menu.create_text("Proyect list menu", "CUSTOM", (3, 3))
        menu.create_text(f"version {ver}", "CUSTOM", (menu.vec[0]-len(ver)-12, 1))

        menu.add_panel(0, 4, 27, 12, 0)
        menu.add_panel(60, 3, 32, 6, 0)


        menu.add_panel(60, 11, 32, 5, 0)
        if len(lst_pro[0]) >= 32:
            nme = f"Mod's name: {lst_pro[0][:24]}..."
        else:
            nme = f"Mod's name: {lst_pro[0]}"

        ref = info[lst_pro[0]]
        if not ref == "Error!":
            inf = []
            for _in in range(2):
                if len(ref[_in]) >= 25:
                    inf.append(ref[_in][:20]+"...")
                else:
                    inf.append(ref[_in])

            aut = inf[0]
            ver_ = inf[1]
            lnk = ref[2]
        else:
            aut = "meta not found"
            ver_ = "meta not found"
            lnk = web

        menu.create_text(nme, "CUSTOM", (62, 12))
        menu.create_text(f"Autor: {aut}", "CUSTOM", (62, 13))
        menu.create_text(f"Version: {ver_}", "CUSTOM", (62, 14))
        
        #NEED FIX
        c=-1
        for nme in range(10):
            c+=1
            if c == len(lst_pro):
                break

            if len(lst_pro[nme]) < menu.meta["panel"][1]["transform"][0]-2:
                menu.create_text(lst_pro[nme], "CUSTOM", (1,nme+5)) 
            else:
                menu.create_text(lst_pro[nme][:20]+"...", "CUSTOM", (1,nme+5))

        btn1 = Button(X=1, Y=17, TEXT="Return", ACTION=_procces_lst_refresh, DEFAULT="CUSTOM") 

        btn2 = Button(X=15, Y=17, TEXT="Next", ACTION=_procces_lst_refresh, DEFAULT="CUSTOM")
        
        nro_pg = 0

        btn1.caster((""), lst_pro, len(lst_pro), menu, nro_pg)
        menu.add_btn(btn1)
        menu.del_btn(1, False)

        if len(lst_pro) >= 10:
            btn2.caster((""), lst_pro, len(lst_pro)-10, menu, nro_pg)
            menu.add_btn(btn2)

        btn = Button(X=62, Y=15, TEXT="Autor site/download", ACTION=lnk, DEFAULT="LINK")
        menu.add_btn(btn)

        btn = Button(X=31, Y=17, TEXT="Archive to load",ACTION=_procces_lst_info, DEFAULT="CUSTOM")
        btn.caster(("Enter proyect's number"), menu, nro_pg, info)
        menu.add_btn(btn)

        btn = Button(X=70, Y=17, TEXT="Load", ACTION=proyect_lst_pro, DEFAULT="CUSTOM")
        btn.caster((""), info, lst_pro, 0)
        menu.add_btn(btn)

        btn = Button(X=84, Y=17, TEXT="Back", DEFAULT="BACK")
        menu.add_btn(btn)

        menu.start_cast()
    else:
        _chk_window()
        print_debug(F"{ver}; DON'T PROYECT FOUND YET; {ver}")
        sleep(5)
        CUR[0][0].start_cast()

page = Page(X=size[0], Y=size[1], CHR="#")
page.create_text("Roses In The Flame's mod engine", "CUSTOM", (3, 3))
page.create_text(f"version {ver}", "CUSTOM", (page.vec[0]-len(ver)-12, 1))

btn = Button(X=5, Y=6, TEXT="Create new proyect", ACTION=proyect_new)
page.add_btn(btn)

btn = Button(X=5, Y=8, TEXT="Load proyect's list", ACTION=proyect_list)
page.add_btn(btn)

btn = Button(X=5, Y=10, TEXT="Exit", DEFAULT="EXIT")
page.add_btn(btn)

btn = Button(X=1, Y=12, TEXT="Website main", ACTION=web, DEFAULT="LINK")
page.add_btn(btn)

btn = Button(X=1, Y=13, TEXT="Website tales", ACTION=web, DEFAULT="LINK")
page.add_btn(btn)

page.add_panel(84, 7, 16, 7, 0)

page.add_panel(64, 7, 16, 7, 0)

btn = Button(X=65, Y=8, TEXT="Open URL", ACTION=web,DEFAULT="LINK")
page.add_btn(btn)

#page.start_cast()