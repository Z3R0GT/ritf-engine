sim_var = [["add_history_mod",2,True], 
           ["new_chr_mod",    1,True], 
           ["translate_mod",  4,True], 
           ["new_aspect_mod", 3,True]
           ] 

from os import listdir, path, getcwd, chdir

global root
root = getcwd()

lst_chapter = open(root+f"/chapters_include.txt", "rt").read().split(";")
del lst_chapter[-1]

##########################
#        PART 1          #
##########################
#Prepare the info to copy...

def _trans(lst):
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

def _coind(lst_from:list, lst_to:list) -> list:
    c_from, c_to = -1, -1
    rst = 0
    for _from in lst_from:
        c_from += 1
        for _to in lst_to:
            c_to += 1
            if _from == _to:
                if rst == 0:
                    rst = []

                rst.append((c_from, c_to))
                c_from, c_to = -1, -1
                break
    return rst

def _zero(lst):
    num_erase = []
    for pos in range(len(lst)):
        if lst[pos] == 0:
            num_erase.append(pos)

    num_erase.sort(reverse=True)
    for i in num_erase:
        del lst[i]

    return lst

def deco_info(info:list)->list:
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
        if info_mod[0] == "" or info_mod[0] == " ":
            break

        info_mod.append("s")
        info_mod.append("s")
        info_mod.append("s")

        if info_mod[0] == "chapter_1.rpy":
            archive_mod = info_mod[0]
        else:
            archive_mod = info_mod[0]

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

        base[name] = deco_info(info)
        chdir("..")

    return base

def evaluate(lst_nme_run:list, info_mods:dict) -> tuple:
    lst_to_run = [0]

    #keep out replies
    if len(lst_nme_run[0]) == 3:
        #Runner
        for nme_run in lst_nme_run:
            nme_run:list

            for id in info_mods:
                for info in info_mods[id]:
                    if nme_run[0] == id:
                        if lst_nme_run[2]:
                            legt = len(lst_to_run)
                            if  legt == 1:
                                for pos in range(nme_run[1]):
                                    lst_to_run.append(0)
                            elif nme_run[1] >= legt:
                                for pos in range(legt*2-nme_run[1]):
                                    lst_to_run.append(0)
                            lst_to_run[nme_run[1]] = nme_run[0]
    else:
        lst_to_run = lst_nme_run

    nme_c = {}
    nme_a = []
    c=-1
    lst_to_run = _zero(lst_to_run)

    for nme_from in info_mods:
        
        for nme_to in info_mods:
            if nme_from == nme_to:
                continue

            for info_to in info_mods[nme_to]:
                for info_from in info_mods[nme_from]:
                    if info_to[0] == info_from[0]:
                        equals = False
                        if (info_from[3] == False) and (info_to[3] == False):
                            pal_c = 0
                        elif info_from[3] == True and info_from[3] == False:
                            pal_c = [1,0]
                        elif not info_from[3] == True and info_from[3] == False:
                            pal_c = [0,1]
                        else:
                            equals = True

                        num_c = _coind(info_from[1], info_to[1])
                        lab_c = _coind(info_from[2], info_to[2])

                        if (num_c == lab_c == pal_c):
                            continue
                        else:
                            nme_to_put = f"{nme_to}-{nme_from}"
                            if not nme_c.__contains__(nme_to_put):
                                if not info_from[0] in nme_a:
                                    nme_a.append(info_from[0])
                                    nme_a.sort()

                                if equals:
                                    for pos in range(len(lst_to_run)):
                                        pos_1 = pos
                                        if lst_to_run[pos] == nme_to:
                                            break
                                    
                                    for pos in range(len(lst_to_run)):
                                        pos_2 = pos
                                        if lst_to_run[pos] == nme_to:
                                            break

                                    if pos_1 > pos_2:
                                        lst_to_run[pos_2] = 0       
                                    else:
                                        lst_to_run[pos_1] = 0
                                    pal_c = 1
                                
                                c+=1
                                nme_c[f"{nme_from}-{nme_to}"] = {"ach":info_from[0],
                                                                        "num":num_c,
                                                                        "lab":lab_c,
                                                                        "pal":pal_c, 
                                                                        "id":str(c)}
                            else:
                                if not nme_c[nme_to_put]["num"] == num_c:
                                    nme_c[nme_to_put]["num"] = num_c

                                if not nme_c[nme_to_put]["lab"] == lab_c:
                                    nme_c[nme_to_put]["lab"] = lab_c
                                
                                nme_c[nme_to_put]["id"] = str(c)
                 
    if len(lst_nme_run[0]) == 3:
        lst_to_run = _zero(lst_to_run)

    return lst_to_run, nme_c, nme_a

def ftp_deco_info(var_to_exe:list)-> dict:
    
    info_final = ...

    m = -1
    er=-1
    all_info = super_deco()
    while True:
        filter_info = evaluate(var_to_exe, all_info)
        m+=1
        print(f"\nDuring: {m}")
        print(f">>>>>Start {m} code<<<<<<")
        print("\nList to run:")
        print(filter_info[0])

        print("\nSuper Info (Without filter):")
        for i in all_info:
            print(i, all_info[i])

        print("\nCoincidence is info:")
        for i in filter_info[1]:
            print(i, filter_info[1][i])
        er+=1
        for nme in filter_info[1]:
            nme_lst = nme.split("-")
            pos = []
            for i in range(2):
                for pos_nme in range(len(filter_info[0])):
                    if nme_lst[i] == filter_info[0][pos_nme]:
                        pos.append(pos_nme)

            from random import randint
            if pos[0] > pos[1]:
                info_from = all_info[nme_lst[1]]
                info_to = all_info[nme_lst[0]]
                pos_num = 1
                plus_num = randint(-2, -1)
            else:
                info_from = all_info[nme_lst[0]]
                info_to = all_info[nme_lst[1]]
                pos_num = 0
                plus_num = randint(1, 2)

            #Filter of chapters
            for dta_from in info_from:
                if dta_from[0] == filter_info[1][nme]["ach"]:
                    for dta_to in info_to:
                        if dta_to[0] == filter_info[1][nme]["ach"]:
                            
                            if not filter_info[1][nme]["num"] == 0:
                                for replace in filter_info[1][nme]["num"]:
                                    re = int(dta_to[1][replace[pos_num]])+plus_num
                                    dta_to[1][replace[pos_num]] = str(re)
        print(f">>>>>end {m} code<<<<<<")

        filter_info = evaluate(var_to_exe, all_info)
        if len(filter_info[1]) == 0:
            print(">>>>>End code<<<<<<")
            return all_info

        if er == 1000:
            print("error")
            break

a = ftp_deco_info(sim_var)
for i in a:
    print(i, a[i])