from engine import *
from engine.models.internal.tool.debug import _chk_window, print_debug
#from proyect_func import *
#from redirection import *
from rec import *
from time import sleep

ver : str = "a1.1.5.1"
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
        nme = f"Mod's name: {lst_pro[_in_-1][:16]}..."
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

def _is_in_range(is_new:bool,
                 space_screen:int,
                 cur_num:int, 
                 rgn_in:range, 
                 cur_list:dict) -> bool:
    return not is_new and (cur_num-space_screen <= 0 or rgn_in[-1] >= cur_list["lst"][1]+space_screen)

def __archive_lst(*nm):
    menu:Page;cur_list:dict;is_foward:bool;cur_num:int;is_new:bool
    ln_y:int; ln_x:int;num:int;lim_x:int

    menu, cur_list, is_foward, cur_num, is_new, ln_y, ln_x, num, lim_x = nm[1]
    
    SPACE_SCREEN  :int = 10
    SPACE_LIMIT_X :int = lim_x

    #RANGE TO UPDATE THE LIST
    if is_foward:
        rgn_in = range(cur_num-SPACE_SCREEN, cur_num)
    else:
        rgn_in = range(cur_num, cur_num+SPACE_SCREEN)
    
    if not _is_in_range(is_new, SPACE_SCREEN, cur_num, rgn_in, cur_list):

        for nme in range(SPACE_SCREEN): #ERASER SECTION
            menu.create_text(" "*(menu.meta["panel"][1]["transform"][0]-2), "CUSTOM", (ln_x, nme+ln_y))
    
        
        for in_ in rgn_in: #ADD TEXT
            #TRIGGER WHEN THE "MAX" CASE COME
            if in_ >= cur_list["lst"][1]:
                ch = True 
                break

            if len(cur_list["lst"][0][in_]) < menu.meta["panel"][1]["transform"][0]-SPACE_LIMIT_X:
                menu.create_text(f"{in_%SPACE_SCREEN+num+1}) "+cur_list["lst"][0][in_], "CUSTOM", (ln_x, (in_%SPACE_SCREEN)+ln_y))
            else:
                menu.create_text(f"{in_%SPACE_SCREEN+num+1}) "+cur_list["lst"][0][in_][:16]+"...", "CUSTOM", (ln_x, (in_%SPACE_SCREEN)+ln_y))

            ch = False

        if not is_new:
            if is_foward:
                if not menu.btns[0].var[3] >= cur_num+SPACE_SCREEN:
                    menu.btns[1].caster((""), menu, cur_list, False, menu.btns[1].var[3]-SPACE_SCREEN, False, 5, 1, 0, 5)
                    menu.add_btn(menu.btns[0], False)

                    menu.btns[0].caster((""), menu, cur_list, True, menu.btns[0].var[3]+SPACE_SCREEN, False, 5, 1, 0, 5)
                    menu.add_btn(menu.btns[1], False)

                if ch:
                    menu.del_btn(1, False)
            elif not menu.btns[1].var[3] <= cur_num-SPACE_SCREEN:
                menu.del_btn(2, False)
            else:
                menu.btns[0].caster((""), menu, cur_list, False, menu.btns[0].var[3]-SPACE_SCREEN, False, 5, 1, 0, 5)
                menu.add_btn(menu.btns[1], False)

                menu.btns[1].caster((""), menu, cur_list, True, menu.btns[1].var[3]+SPACE_SCREEN, False, 5, 1, 0, 5)
                menu.add_btn(menu.btns[0], False)
        else:
            # THIS EXECUTE JUST ON THE START
            menu.btns[0].caster((""), menu, cur_list, True, menu.btns[0].var[3]+SPACE_SCREEN, False, 5, 1, 0, 5)
            menu.add_btn(menu.btns[0], False)
            return

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
    btn.caster((""), "default", "1.0", "Z3R0_GT", ["1"], web) 
    menu.add_btn(btn)

    btn = Button(X=84, Y=17, TEXT="Back", DEFAULT="BACK")
    menu.add_btn(btn)

    menu.add_panel(68, 4, 32, 8, 0)
    menu.create_text("Tutorial:", "CUSTOM", (71,5))

    menu.start_cast()

def proyect_list(*nm):
    info = check_proyects()
    lst_pro = [i for i in info]
    info_arch = {"lst":[lst_pro, len(lst_pro)]}

    #SECURITY CHECK
    if len(lst_pro) == 0:
        erase_screen()
        print_debug(f"{ver} YOU DON'T PROYECTS CREATED YET {ver}")
        print_debug(f"{ver} REDIRECTING TO CREATE A NEW... {ver}")
        sleep(5)
        #proyect_new()

    menu = Page(X=size[0], Y=size[1]+4, CHR="#", NMO="Proyect's page")  

    menu.create_text("Proyect's page", "CUSTOM", (3,3))
    menu.create_text(f"version {ver}", "CUSTOM", (menu.vec[0]-len(ver)-12, 1))

    menu.add_panel(0, 4, 27, 12, 0)  #SELECT SECTION
    menu.add_panel(60, 3, 32, 6, 0)  #TUTORIAL ""

    menu.add_panel(60, 11, 32, 5, 0) #META ""

    #FIRST META'S ARCHIVE LOADED
    ref = info[lst_pro[0]]
    if len(lst_pro[0]) >= 32:
        nme = f"Mod's name: {lst_pro[0][:24]}..."
    else:
        nme = f"Mod's name: {lst_pro[0]}"
    
    if not ref == "Error!":
        inf = []
        for _in in range(2):
            if len(ref[_in]) >= 25:
                inf.append(ref[_in][:20]+"...")
            else:
                inf.append(ref[_in])
        
        autor = inf[0]
        ver_mod = inf[1]
        lnk = ref[2]
        del inf, _in
    else:
        autor = "meta not found"
        ver_mod = "meta not found"
        lnk = web
    del ref

    menu.create_text(nme, "CUSTOM", (62, 12))
    menu.create_text(f"Autor: {autor}", "CUSTOM", (62, 13))
    menu.create_text(f"Version: {ver_mod}", "CUSTOM", (62, 14))
    del autor, ver_mod

    #OPTIONS'S SECTION
    for nme in range(10):
        if nme == len(lst_pro):
            break

        if len(lst_pro[nme]) < menu.meta["panel"][1]["transform"][0]-5:
            menu.create_text(f"{nme+1}) "+lst_pro[nme], "CUSTOM", (1,nme+5)) 
        else:
            menu.create_text(f"{nme+1}) "+lst_pro[nme][:16]+"...", "CUSTOM", (1,nme+5))
    del nme

    btn = Button(1, 17, "Next", __archive_lst, DEFAULT="CUSTOM")
    btn.caster((""), menu, info_arch, True, 10, False, 5, 1, 0, 5)
    menu.add_btn(btn)
    menu.del_btn(1, False)

    __archive_lst((""), [menu, info_arch, False, 0, True, 5, 1, 0, 5])

    btn = Button(15, 17, "Back", __archive_lst, DEFAULT="CUSTOM")
    btn.caster((""), menu, info_arch, False, 10, False, 5, 1, 0, 5)
    menu.add_btn(btn)
    menu.del_btn(2, False)

    btn = Button(X=62, Y=15, TEXT="Autor site/download", ACTION=lnk, DEFAULT="LINK")
    menu.add_btn(btn)

    btn = Button(X=31, Y=17, TEXT="Archive to load",ACTION=_procces_lst_info, DEFAULT="CUSTOM")
    btn.caster(("Enter proyect's number"), menu, 0, info)
    menu.add_btn(btn)

    btn = Button(X=70, Y=17, TEXT="Load", ACTION=proyect_lst_pro, DEFAULT="CUSTOM")
    btn.caster((""), info, lst_pro, 0)
    menu.add_btn(btn)

    btn = Button(X=84, Y=17, TEXT="Back menu", DEFAULT="BACK")
    menu.add_btn(btn)
    del btn

    menu.start_cast()

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

page.start_cast()