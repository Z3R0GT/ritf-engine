from engine import *
from engine.models.internal.tool.debug import _chk_window, print_debug
#from proyect_func import *
#from redirection import *
from rec import *
from time import sleep

VER : str = "a1.1.5.1"
VER_MAIN : str = "1.0"

SIZE = [100, 15]

WEB ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

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
        ctn = WEB

    menu.create_text(f"{nme}", "CUSTOM", (3,6))
    menu.create_text(f"{vers}", "CUSTOM", (3,8))
    menu.create_text(f"{cre}", "CUSTOM", (3,10))

    ch = ch.split(",")
    menu.create_text(f"{ch}", "CUSTOM", (3,12))

    menu.create_text(f"{ctn}", "CUSTOM", (3, 14))
    menu.btns[1].var = [nme, vers, cre, ch, ctn, VER, SIZE]

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
        lnk = WEB

    menu.btns[4].var = (info, lst_pro, _in_-1)

    menu.create_text(nme, "CUSTOM", (62, 12))
    menu.create_text(f"Autor: {aut}", "CUSTOM", (62, 13))
    menu.create_text(f"Version: {ver_}", "CUSTOM", (62, 14))

    menu.start_cast()

def _refresh_zone(*nm):
    menu:Page; ID:int; item_cul:int;list_to:list
    ID_btn:list[int, int, int];NUM_LT:list[int, int]
    is_new:bool

    menu, ID, item_cul,list_to, ID_btn, NUM_LT, is_new = nm[1]

    CUR_PANEL = menu.panel[ID]

    LIMIT_TEXT:int = CUR_PANEL["transform"][0]  #X
    LIMIT_ITEM:int = item_cul                   #Y
    LIMIT_X_OR_Y = 1

    #ERASER
    for in_ in range(LIMIT_ITEM):
        menu.create_text(" "*(LIMIT_TEXT-2), 
                         "CUSTOM", 
                         (CUR_PANEL["vec"][0]+LIMIT_X_OR_Y, in_+CUR_PANEL["vec"][1]+LIMIT_X_OR_Y))

    for in_ in range(NUM_LT[0], NUM_LT[1]):
        if in_ >= len(list_to):
            ch = True
            break

        if len(list_to[in_]) < LIMIT_TEXT-6: #6 -> TEXT ADDED
            menu.create_text(f"{in_%LIMIT_ITEM}) {list_to[in_]}", 
                             "CUSTOM", 
                             (CUR_PANEL["vec"][0]+LIMIT_X_OR_Y, (in_%LIMIT_ITEM)+CUR_PANEL["vec"][1]+LIMIT_X_OR_Y))
        else:
            menu.create_text(f"{in_%LIMIT_ITEM}) {list_to[in_][:LIMIT_TEXT-6]}...", 
                             "CUSTOM", 
                             (CUR_PANEL["vec"][0]+LIMIT_X_OR_Y, (in_%LIMIT_ITEM)+CUR_PANEL["vec"][1]+LIMIT_X_OR_Y))

        ch = False

    if is_new:
        return

    BUTTON_FOW:Button = menu.btns[ID_btn[0]-1]
    BUTTON_BAC:Button = menu.btns[ID_btn[1]-1]
    BUTTON_INP:Button = menu.btns[ID_btn[2]-1]

    BUTTON_INP.var = [menu, NUM_LT[0], list_to]
    menu.add_btn(BUTTON_INP, False)

    #WHEN IS IN THE MAX AND MIN CASE
    if ch:                            #IN THE MAX
        menu.del_btn(ID_btn[0], False)
        menu.add_btn(BUTTON_BAC, False)
    elif NUM_LT[1] == LIMIT_ITEM:     #IN THE MIN
        menu.del_btn(ID_btn[1], False)
        menu.add_btn(BUTTON_FOW, False)
    else:
        BUTTON_BAC.var = [menu, ID, item_cul, list_to, ID_btn, 
                          [BUTTON_FOW.var[5][0]-LIMIT_ITEM, BUTTON_FOW.var[5][1]-LIMIT_ITEM], 
                          False]
        BUTTON_FOW.var = [menu, ID, item_cul, list_to, ID_btn, 
                          [NUM_LT[0]+10, NUM_LT[1]+LIMIT_ITEM], 
                          False]

        menu.add_btn(BUTTON_FOW, False)
        menu.add_btn(BUTTON_BAC, False)
    menu.start_cast()

def proyect_new(*nm):
    menu = Page(X=SIZE[0], Y=SIZE[1]+4, CHR="#")

    menu.create_text("Creation mod menu", "CUSTOM", (3, 3))
    menu.create_text(f"version {VER}", "CUSTOM", (menu.vec[0]-len(VER)-12, 1))

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
    btn.caster((""), "default", "1.0", "Z3R0_GT", ["1"], WEB) 
    menu.add_btn(btn)

    btn = Button(X=84, Y=17, TEXT="Back", DEFAULT="BACK")
    menu.add_btn(btn)

    menu.add_panel(68, 4, 32, 8, 0)
    menu.create_text("Tutorial:", "CUSTOM", (71,5))

    menu.start_cast()

def proyect_list(*nm):
    info = check_proyects()
    lst_pro = [i for i in info]

    #SECURITY CHECK
    if len(lst_pro) == 0:
        erase_screen()
        print_debug(f"{VER} YOU DON'T PROYECTS CREATED YET {VER}")
        print_debug(f"{VER} REDIRECTING TO CREATE A NEW... {VER}")
        sleep(5)
        #proyect_new()

    menu = Page(X=SIZE[0], Y=SIZE[1]+4, CHR="#", NMO="Proyect's page")  

    menu.create_text("Proyect's page", "CUSTOM", (3,3))
    menu.create_text(f"version {VER}", "CUSTOM", (menu.vec[0]-len(VER)-12, 1))

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
        lnk = WEB
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

    _refresh_zone([],[menu, 
                1, 
                10, 
                lst_pro, 
                (1, 2, 3), 
                (0, 10),
                True])

    btn = Button(1, 17, "Next", _refresh_zone, DEFAULT="CUSTOM")
    btn.caster((""), menu, 1, 10, lst_pro, (1, 2, 3), (10, 20), False)
    menu.add_btn(btn)

    btn = Button(15, 17, "Back", _refresh_zone, DEFAULT="CUSTOM")
    btn.caster((""), menu, 1, 10, lst_pro, (1, 2, 3), (0, 10), False)
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
    del btn, lst_pro, info

    menu.start_cast()

page = Page(X=SIZE[0], Y=SIZE[1], CHR="#")
page.create_text("Roses In The Flame's mod engine", "CUSTOM", (3, 3))
page.create_text(f"version {VER}", "CUSTOM", (page.vec[0]-len(VER)-12, 1))

btn = Button(X=5, Y=6, TEXT="Create new proyect", ACTION=proyect_new)
page.add_btn(btn)

btn = Button(X=5, Y=8, TEXT="Load proyect's list", ACTION=proyect_list)
page.add_btn(btn)

btn = Button(X=5, Y=10, TEXT="Exit", DEFAULT="EXIT")
page.add_btn(btn)

btn = Button(X=1, Y=12, TEXT="Website main", ACTION=WEB, DEFAULT="LINK")
page.add_btn(btn)

btn = Button(X=1, Y=13, TEXT="Website tales", ACTION=WEB, DEFAULT="LINK")
page.add_btn(btn)

page.add_panel(84, 7, 16, 7, 0)

page.add_panel(64, 7, 16, 7, 0)

btn = Button(X=65, Y=8, TEXT="Open URL", ACTION=WEB,DEFAULT="LINK")
page.add_btn(btn)

page.start_cast()