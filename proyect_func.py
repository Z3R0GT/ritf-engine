from engine.models.internal.tool.debug import *
from rec import *

ver : str = "a1.1.5.1"
size = [100, 15]
web ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"



#<-----OPTIMIZED VERSION----->#

def _refresh_meta_sec(menu:Page, what:str, coord:list[int, int]):
    menu.create_text(what, "CUSTOM", coord)

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
                menu.create_text(f"{in_%SPACE_SCREEN+num}) "+cur_list["lst"][0][in_], "CUSTOM", (ln_x, (in_%SPACE_SCREEN)+ln_y))
            else:
                menu.create_text(f"{in_%SPACE_SCREEN+num}) "+cur_list["lst"][0][in_][:16]+"...", "CUSTOM", (ln_x, (in_%SPACE_SCREEN)+ln_y))

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
            menu.create_text(f"{nme}) "+lst_pro[nme], "CUSTOM", (1,nme+5)) 
        else:
            menu.create_text(lst_pro[nme][:16]+"...", "CUSTOM", (1,nme+5))
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

proyect_list(...)