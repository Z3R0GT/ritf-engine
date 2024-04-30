init python:
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

    ##########################
    #        PART 2          #
    ##########################
    #search coincidence btw chapters

    def _zero(lst)->list:
        num_erase = []
        for pos in range(len(lst)):
            if lst[pos] == 0:
                num_erase.append(pos)

        num_erase.sort(reverse=True)
        for i in num_erase:
            del lst[i]

        return lst

    def _lst_maker(lst_nme_run:list[list[str, int, bool]])->list[str]:
        global all_info, lst_cha_mod
        lst_to_run = [0]
        lst_to_del = []

        for nme_run in lst_nme_run:
            nme_run:list

            for id in all_info:
                for info in all_info[id]:
                    if not info[0] in lst_cha_mod:
                        lst_cha_mod.append(info[0])


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
        lst_to_run = _zero(lst_to_run)

        for id in all_info:
            if not id in lst_to_run:
                lst_to_del.append(id)

        for nms_del in lst_to_del:
            all_info.__delitem__(nms_del)

        return lst_to_run

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

    def _coin_num(lst_from:list[int | str], lst_to:list[int | str], invert:bool=False) ->list | int:
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
        return rst

    def _who_not_best(nme_to_eval:list[str], equal:bool=False, pal_c:list[int, int] | int = 0 ) -> tuple[bool, str, int]:
        global lst_to_run
        pos_lst:list = []
        for num in range(2):
            for pos in range(len(lst_to_run)):
                if lst_to_run[pos] == nme_to_eval[num]:
                    pos_lst.append(pos)
                    
        chk = pos_lst[0]<pos_lst[1]
        if equal:
            if chk:
                lst_to_run[pos_lst[1]] = 0
                nme = lst_to_run[pos_lst[0]]
            else:
                lst_to_run[pos_lst[0]] = 0
                nme = lst_to_run[pos_lst[1]]
            pal_c = 1
            lst_to_run = _zero(lst_to_run)
            return True, nme, pal_c
        else:
            if chk:
                return False, lst_to_run[pos_lst[1]], pal_c
            else:
                return False, lst_to_run[pos_lst[0]], pal_c

    def _coincidence_info(id_coin:int=0)->list[coincidece]:
        global lst_cha_mod, all_info
        lst_info = []

        if len(all_info) == 1:
            print("you can not operate with 1 mod")
            return lst_info

        for nme_from in all_info:
            for nme_to in all_info:
                if nme_from == nme_to:
                    continue
                
                for info_to in all_info[nme_to]:
                    for info_from in all_info[nme_from]:

                        if info_to[0] == info_from[0]:
                            equals = False
                            if not info_from[3] and not info_to[3]:
                                pal_c = 0
                            elif not info_from[3] and info_to[3]:
                                pal_c = [1,0]
                            elif info_from and not info_to[3]:
                                pal_c = [0,1]
                            else:
                                equals = True

                            num_c = _coin_num(info_from[1], info_to[1], True)
                            lab_c = 0 #_coin_num(info_from[2], info_to[2], True)
                            if not (num_c == lab_c == pal_c):
                                is_same, nme, pal_c = _who_not_best([nme_from, nme_to], equals, pal_c)
                                
                                if is_same:
                                    print("work in progress")
                                    continue

                                if nme == nme_from:
                                    num_c = _coin_num(info_to[1], info_from[1])
                                    lab_c = 0 #_coin_num(info_to[2], info_from[2], True)
                                    nme_put = nme+"-"+nme_to
                                else:
                                    nme_put = nme+"-"+nme_from

                                chk = False
                                #Trigger alert!
                                for mod in lst_info:
                                    mod:coincidece
                                    if mod.chapter == info_to[0]:
                                        if mod.nme == nme_put:    
                                            chk = True
                                            break
                                if chk:
                                    continue

                                id_coin+=1
                                
                                lst_info.append(coincidece(id_coin, nme_put, info_to[0], num_c, lab_c, pal_c, nme))
                            else:
                                continue
        if len(lst_info) == 1 and len(all_info) >= 3:
            for ln in range(len(lst_info[0].ln_jump)):
                lst_info[0].ln_jump[ln] = (lst_info[0].ln_jump[ln][1], lst_info[0].ln_jump[ln][0])

        return lst_info

    def _del_coincidence():
        global all_info, lst_cha_mod

        id_c = 0

        if len(_coincidence_info()) == 0:
            print("coincidence insuficent")
            return 0

        while not len(_coincidence_info()) == 0:
            coin = _coincidence_info(id_c)
            from random import randint
            
            for cha_mod in lst_cha_mod:
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

            id_c+=1

        return 0

    ##########################
    #        PART 3          #
    ##########################
    #Prepare the info to insert...

    def _insert(old_lst:list[str], to_insert:list[int | str]) -> list:
        for info in to_insert:
            if info[0] <= 0:
                nm = info[0]+ 2
            else:
                nm = info[0]
            _tmp = []

            for num in range(len(old_lst)):
                if num >= nm-1:
                    _tmp.append(old_lst[num])

            for num in range(nm-1, len(old_lst)):
                del old_lst[-1]

            old_lst.append(info[1])

            for lst in _tmp:
                old_lst.append(lst)
        return old_lst

    def order_channel() -> tuple[dict, list]:
        global all_info, lst_cha_mod, lst_to_run, lst_chapter

        info_re = {}
        nme_mod = []

        for chapter in lst_cha_mod:
            for nme in lst_to_run:
                for info in all_info[nme]:
                    if info[0] == chapter:

                        ftc_ = open(root+f"/game/{info[0]}", "rt")
                        ftc_info = ftc_.readlines()

                        for chk in info[1]:
                            if int(chk) >= len(ftc_info):
                                for i in range(int(chk)+2):
                                    ftc_info.append(" "*4)

                        #CREATE NEW JUMP LINES
                        j_list = []
                        for num in range(len(info[1])):
                            _tmp = ""
                            for _chr in ftc_info[int(info[1][num])]:
                                if _chr == " ":
                                    _tmp += _chr

                            if " " in _chr:
                                _tmp += f"jump {info[2][num]}\n"
                            else:
                                _tmp += " "*4+f"jump {info[2][num]}\n"

                            j_list.append([int(info[1][num]), _tmp])

                        ftc_info = _insert(ftc_info, j_list)

                        c=-1
                        for tag in ftc_info:
                            c+=1
                            if tag.replace("label", "").replace(" ", "")[:-2] in lst_chapter:
                                ftc_info[c] = f"{tag[:-2]}_mod:\n"
                                if not tag.replace("label", "").replace(" ", "")[:-2]+"_mod" in nme_mod:
                                    nme_mod.append(tag.replace("label", "").replace(" ", "")[:-2]+"_mod")

                        info_re[info[0]+"_"+nme] = ftc_info
                        ftc_.close()
        return info_re, nme_mod

    ##########################
    #        PART 4          #
    ##########################
    #after of copy, to paste

    def paste_up(info_to:dict) -> dict:
        global lst_cha_mod
        info_re = {}

        for chapter in lst_cha_mod:
            for nme in info_to:
                    nme_cha = chapter[:-4]
                    if nme_cha == nme[:9]:
                        if not info_re.__contains__(nme_cha):
                            info_re[nme_cha] = info_to[nme]
                        else:
                            len_lst = len(info_to[nme])
                            while len(info_re[nme_cha]) < len_lst:
                                info_re[nme_cha].append("\n"+" "*4)

                            for ln in range(len_lst):
                                if info_to[nme][ln].replace(" ", "")[:4] == "jump":
                                    info_re[nme_cha][ln] = info_to[nme][ln]

                            for ln in range(len(info_re[nme_cha])):
                                if len(info_re[nme_cha][ln]) == 4:
                                    info_re[nme_cha][ln] = "\n"


        return info_re

    def paste(info_to:dict) -> dict:
        global lst_cha_mod
        info_re = {}

        for chapter in lst_cha_mod:
            for nme in info_to:
                jump_chr = []
                if nme[:9] == chapter[:-4]:
                    if not info_re.__contains__(chapter[:-4]):
                        info_re[chapter[:-4]] = info_to[nme]
                    else:
                        i_lst = len(info_re[chapter[:-4]])

                        while not len(info_re[chapter[:-4]]) <= len(info_to[nme]):
                            info_to[nme].append(" "*4)

                        for ln in range(i_lst):

                            nm_from = info_re[chapter[:-4]][ln].replace(" ", "")
                            nm_to = info_to[nme][ln].replace(" ", "")
                            if nm_from[:4] == "jump":
                                if not info_re[chapter[:-4]][ln] in jump_chr:
                                    jump_chr.append(nm_from)

                            elif nm_to[:4] == "jump":
                                if not nm_to == nm_from:
                                    info_re[chapter[:-4]] = _insert(info_re[chapter[:-4]], [[ln ,info_to[nme][ln]]])

        return info_re

    def paste_final_archive():
        global info_fin

        for nme in info_fin:
            arch = open(root+f"/game/mods/{nme}_modder.rpy", "w")

            chk = False
            for line in info_fin[nme]:
                if line == "#COPY\n" or chk == True:
                    arch.write(line)
                    chk = True

                if line == "#NOT\n":
                    chk = False

            arch.close()

    ##########################
    #        PART 5          #
    ##########################
    #search if the current file already exits in moddifications

    def mod_nme_include():
        global info_to_pst

        end = ""

        arch = open(root+"/game/mods/archive_lst.txt", "w")
        for cha in info_to_pst[1]:
            end+= cha+";"
        arch.write(end)

    #START
    from os import listdir, path, getcwd, chdir

    root = getcwd()                #-----------------------<
    lst_chapter = open(root+f"/chapters_include.txt", "rt").read().split(";")
    del lst_chapter[-1]

    sim_var = [["add_history_mod",2,True],
            ["new_chr_mod", 1, True],
            ["new_aspect_mod", 3, True],
            ["translate_mod", 4, True]
            ] 

    all_info = super_deco()         #-----------------------<

    lst_cha_mod = []                 #-----------------------<
    lst_to_run = _lst_maker(sim_var) #-----------------------<

    _del_coincidence()

    info_to_pst = order_channel()

    info_fin = paste_up(info_to_pst[0])#-----------------------<

    for i in range(5):
        paste_final_archive()

    mod_nme_include()