from engine import *
from time import sleep

SIZE = [100, 15]
WEB ="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

                        #CHANGE THIS NUMBER
list_t = [str(i) for i in range(31)]


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

    menu.get_pre_view()

menu = Page(SIZE[0], SIZE[1]+4)

menu.add_panel(0, 4, 27, 12, 0)  #SELECT SECTION
for in_ in range(10):
    menu.create_text("a", "CUSTOM", (1, in_+5))

_refresh_zone([],[menu, 
              1, 
              10, 
              list_t, 
              (1, 2, 3), 
              (0, 10),
              True])

btn_1 = Button(1, 17, "Next", _refresh_zone, DEFAULT="CUSTOM")
btn_1.caster((""), menu, 1, 10, list_t, (1, 2, 3), (10, 20), False)
menu.add_btn(btn_1)

btn_2 = Button(15, 17, "Back", _refresh_zone, DEFAULT="CUSTOM")
btn_2.caster((""), menu, 1, 10, list_t, (1, 2, 3), (0, 10), False)
menu.add_btn(btn_2)
menu.del_btn(2, False)

btn_3 = Button(X=31, Y=17, TEXT="Archive to load",ACTION=_procces_lst_info, DEFAULT="CUSTOM")
btn_3.caster(("Enter proyect's number"), menu, 0, list_t)
menu.add_btn(btn_3)

menu.start_cast()