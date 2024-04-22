from os import listdir, path, getcwd, chdir

root = getcwd() #-----------------------<

lst_chapter = open(root+f"/chapters_include.txt", "rt").read().split(";") #-----------------------<
del lst_chapter[-1]

sim_var = [["add_history_mod",2,True],
           ["new_chr_mod", 1, True],
           ["new_aspect_mod", 3, True],
           ["translate_mod", 4, True]
           ] 

##########################
#        PART 1          #
##########################
#Prepare the info to copy...
def _trans(lst)->list:
    _lst = []
    _tmp = ""
    for nme in lst: 
        if nme == "-":
            _lst.append(_tmp)
            _tmp = ""
        elif nme == ".":
            _tmp = lst[-1]
        else:
            _tmp += nme
    _lst.append(_tmp)
    return _lst

def _deco_info(info:list)->list:
    table:dict = {
    "-": ",",
    91: "", #ANSI
    93: "", #ANSI
    "\\": "", #ANSI
    }
    _tmp = []
    for data in info:
        data:str
        info_mod = list(data.split(","))
        if info_mod[0] == "" or info_mod[0] == " " or info_mod[0] == "\\n":
            break

        info_mod.append("s")
        info_mod.append("s")
        info_mod.append("s")

        if info_mod[0] == "chapter_1.rpy":
            archive_mod = info_mod[0]
        else:
            archive_mod = info_mod[0][1:]

        ln_to_jump = _trans(list(info_mod[1].translate(table)))

        ls_to_jump = _trans(list(info_mod[2].translate(table)))
        
        all_flow = str(info_mod[3].translate(table))
        if all_flow == "y":
            all_flow = True
        else:
            all_flow = False

        _tmp.append([archive_mod, ln_to_jump, ls_to_jump, all_flow])

    return _tmp

def super_deco() -> dict:

    chdir(root+"/game/mods")
    lst_mods = list(filter(path.isdir, listdir()))

    base = {}
    for name in lst_mods:
        chdir(f"{name}")
        info = open(f"{getcwd()}/base.info", "rt").read().split(";")

        base[name] = _deco_info(info)
        chdir("..")

    return base

all_info = super_deco() #-----------------------<
#END PART 1

##########################
#        PART 2          #
##########################
#search coincidence btw chapters
#PART 2.1
def _zero(lst)->list:
    num_erase = []
    for pos in range(len(lst)):
        if lst[pos] == 0:
            num_erase.append(pos)

    num_erase.sort(reverse=True)
    for i in num_erase:
        del lst[i]

    return lst

def _lst_maker(lst_nme_run)->list[str]:
    lst_to_run = [0]

    for nme_run in lst_nme_run:
        nme_run:list

        for id in all_info:
            for info in all_info[id]:
                if nme_run[0] == id:
                    if nme_run[2]:
                        legt = len(lst_to_run)
                        if  legt == 1:
                            for pos in range(nme_run[1]):
                                lst_to_run.append(0)
                        elif nme_run[1] >= legt:
                            for pos in range(legt*2-nme_run[1]):
                                lst_to_run.append(0)
                        lst_to_run[nme_run[1]] = nme_run[0]
    return _zero(lst_to_run)

lst_mk = _lst_maker(sim_var)
lst_temp = []

for nms in all_info:
    if not nms in lst_mk:
        lst_temp.append(nms)

for nme_del in lst_temp:
    all_info.__delitem__(nme_del)

#END PART 2.1
#PART 2.2

class coincidece:
    def __init__(self,
                 ID:int,
                 nme_to:str,
                 chapter:str,
                 ln_jump:list|int,
                 ln_labe:list|int,
                 control:list|int,
                 prior:int) -> None:
        
        self.id = ID
        self.nme = nme_to

        self.ln_jump = ln_jump
        self.ln_lab = ln_labe

        self.control = control

        self.chapter = chapter
        self.prior = prior
        

    def get_meta(self) -> dict:
        return {"id":self.id,
                "nme": self.nme,
                "prior":self.prior,
                "ln_jump":self.ln_jump,
                "ln_lab":self.ln_lab,
                "chapter":self.chapter}

def _coin_num(lst_from, lst_to, invert=False) ->list | int:
    rst = 0

    for num_from in range(len(lst_from)):
        for num_to in range(len(lst_to)):
            if lst_from[num_from] == lst_to[num_to]:
                if rst == 0:
                    rst = []

                if invert:
                    rst.append((num_to, num_from))
                else:
                    rst.append((num_from, num_to))
    
    #print(lst_from, lst_to, rst, "tamaños", len(lst_from), len(lst_to))
    return rst


def _who_not_best(nme_from:str, nme_to:str, equals:bool=False) -> tuple[bool, str | int]:
    """
    Retorna el nombre con menor jerarquia dentro de la lista
    de mods
    """
    global lst_mk
    for pos in range(len(lst_mk)):
        pos_1 = pos
        if lst_mk[pos] == nme_from:
            break
                                    
    for pos in range(len(lst_mk)):
        pos_2 = pos
        if lst_mk[pos] == nme_to:
            break

    if pos_1 < pos_2:
        if equals:
            lst_mk[pos_2] = 0     
            nme =  lst_mk[pos_1]
        else:
            return False, lst_mk[pos_2], lst_mk[pos_2]
    else:
        if equals:
            lst_mk[pos_1] = 0
            nme =  lst_mk[pos_2]
        else:
            return False, lst_mk[pos_1], lst_mk[pos_1]
        
    pal_c = 1
    lst_mk = _zero(lst_mk)

    return True, pal_c, nme

lst_cha :list=[]#-----------------------<

def _coincidence_info(id_coin:int=0)->list[coincidece]:
    
    global lst_cha
    lst_info = []

    if len(all_info) == 1:
        print("you can not operate with 1 info")
        return lst_info

    for nme_from in all_info:
        for nme_to in all_info:
            if nme_from == nme_to:
                continue

            for info_to in all_info[nme_to]:
                for info_from in all_info[nme_from]:

                    if info_to[0] == info_from[0]:
                        equals = False
                        if (info_from[3] == False) and (info_to[3] == False):
                            pal_c = 0
                        elif info_from[3] == True and info_to[3] == False:
                            pal_c = [1,0]
                        elif not info_from[3] == True and info_to[3] == False:
                            pal_c = [0, 1]
                        else:
                            equals = True
                            
                        num_c = _coin_num(info_from[1], info_to[1], True)
                        lab_c = 0 #_coind(info_from[2], info_to[2])

                        if not info_from[0] in lst_cha:
                            lst_cha.append(info_from[0])
                            lst_cha.sort()

                        if not (num_c == lab_c == pal_c):
                            info = _who_not_best(nme_from, nme_to, equals)
                            
                            if info[0]:
                                #replace in the future
                                continue
                                #nme_replace = info[2]
                                #pal_c = info[1]

                            if info[1] == nme_from:
                                lab_c = 0 #_coind(info_from[2], info_to[2]) 
                                num_c = _coin_num(info_to[1], info_from[1])
                                nme_put = info[1]+"-"+nme_to
                            else:
                                nme_put = info[1]+"-"+nme_from

                            chk = False
                            for mod in lst_info:
                                mod:coincidece
                                if mod.chapter == info_to[0]:
                                    if mod.nme == nme_put:    
                                        chk = True
                                        break
                            
                            if chk:
                                continue

                            id_coin+=1
                            lst_info.append(coincidece(id_coin, nme_put, info_to[0], num_c, lab_c, pal_c, info[2]))
                        else:
                            continue

    if len(lst_info) == 1 and len(all_info) >= 3:
        for ln in range(len(lst_info[0].ln_jump)):
            invert = (lst_info[0].ln_jump[ln][1], lst_info[0].ln_jump[ln][0])
            lst_info[0].ln_jump[ln] = invert

    return lst_info


#END PART 2.2
#START PART 2.3

#for nme in coin:
 #   print(nme.get_meta())

er = 0

def app_dif():
    global all_info, er, lst_cha
    er+=1
    test = er
    coin = _coincidence_info()#-----------------------<

    if len(coin) == 0:
        print("coincidence insuficent")
        return 0

    from random import randint
    
    for cha_mod in lst_cha:
        for nme_info in all_info:

            for nme_mod in coin:
                nme_mod:coincidece
                
                if nme_info == nme_mod.prior and nme_mod.chapter == cha_mod:

                    for info_to_mod in all_info[nme_info]:    
                        if nme_mod.chapter == info_to_mod[0]:
                            

                            if not nme_mod.ln_jump == 0:
                                for replace in nme_mod.ln_jump:
                                    try:
                                        re = int(info_to_mod[1][replace[0]])+randint(-2, 2)
                                        info_to_mod[1][replace[0]] = str(re)
                                        while not re >= 0:
                                            re+=1
                                    except IndexError:
                                        re = int(info_to_mod[1][replace[1]])+randint(-2, 2)
                                        while not re >= 0:
                                            re+=1
                                        info_to_mod[1][replace[1]] = str(re)  
                                    
                                                              

    print("coincidence info:")
    for i in coin:
        print(i.get_meta())
    print("-----------------")

    if len(_coincidence_info()) == 0:
        print("end")
        return 0
    else:
        app_dif()
        print("test", test, "passed")

"""
for i in range(5):
    print(i)
    app_dif()
"""

a = _coincidence_info()
for n in a:
    print(n.get_meta())