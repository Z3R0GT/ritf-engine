#for checks
from os import listdir, path, getcwd, chdir
    
global root
root = getcwd()

#all chapter´s name
lst_nmod = open(root+f"/chapters_include.txt", "rt")
lst_chapter = lst_nmod.read().split(";")

chdir(root+"/game/mods")
lst_mods = list(filter(path.isdir, listdir()))


lst_nmod.close()
del lst_chapter[-1]

#banned characters
table:dict = {
    "-": ",",
    91: "", #ANSI
    93: "", #ANSI
    92: "", #ANSI
}

def deco_info(info:list, nme:str) -> list:
    """
    Base for decodificade .info archives for RITF game
    """
    _tmp = []
    for data in info:
        data:str
        info_mod = list(data.split(",")) #separate the data of mod´s info
        if info_mod[0] == "" or info_mod[0] == " ":
            break
                    
        #idk why, but if i don´t write this, appear a unknow error
        info_mod.append("s")
        info_mod.append("s")
        info_mod.append("s")

        #line to jump
        ln_to_jump = list(info_mod[1].replace("-", ",").replace("]","").replace("[", "").replace("\\ n".replace(" ", ""), "").replace("\\ ".replace(" ", ""),"").split(","))

        #list names
        _lst_nme = list(info_mod[2].translate(table)) 
        #final name
        _fn_nme = ""  

        lst_jump = [] #list jumps

        #Convert "list names" to a separate "name" into a new list
        for chr_nme in _lst_nme:
            if chr_nme == "-":
                lst_jump.append(_fn_nme)
                _fn_nme = ""
            elif chr_nme == ".":
                _fn_nme = lst_jump[-1]
            else:
                _fn_nme += chr_nme
        lst_jump.append(_fn_nme)

        #¿is can archive do whatever it want?
        all_flow = str(info_mod[3].translate(table))
        if all_flow == "y":
            all_flow = True
        else:
            all_flow = False   

        _tmp.append([nme, info_mod[0], ln_to_jump, lst_jump, all_flow])

    return _tmp

def super_deco() -> dict:
    """
    Super decodificator in base of "deco_info()", but with "dicts"
    """
    base = {}
    c=-1
    for name in lst_mods:
        c+=1
        chdir(f"{name}")
        file = open(f"{getcwd()}/base.info", "rt") #open the mod´s info
        info = file.read().split(";")

        base[f"{c}"] = deco_info(info, name) # capture the result and save the separete the statements 
        file.close()
        chdir("..")

    return base

sim_var = [["add_history_mod",2,True], ["new_chr_mod", 1, True], ["translate_mod",4,True], ["new_aspect_mod",3,True]] 

def _lst_coincidense(lst_from:list, lst_to:list) -> list:
    """
    Search and return the coincidence btw both lst
    (return 0 if not has coincidense)
    """
    c_from, c_to = -1, -1
    rst = 0
    for _from in lst_from:
        c_from +=1
        for _to in lst_to:
            c_to += 1
            if _from == _to:
                if rst == 0:
                    rst = []

                rst.append((c_from, c_to))
                c_from, c_to = -1, -1
                break
    return rst


def evaluate(lst_to_run:list, info_mods:dict) -> tuple:
    """
    Return a tuple with coincidence of .info archives, and the tag.
    could be: ([ID: line, ID:Line],[ID: line, ID:line])
    the order of the tuple is determinate by "lst_to_run"
    """
    lst_nme_run = [0]

    #Runner
    for nme_run in lst_to_run:
        nme_run:list
        for id in info_mods:
            for info in info_mods[id]:
                info:list
                #Create priority btw mods
                if info[0] == nme_run[0]: #Name check
                    if nme_run[2]: #¿Can execute?

                        if len(lst_nme_run) == 1:
                            for i in range(nme_run[1]):
                                lst_nme_run.append(0)
                        elif nme_run[1] > len(lst_nme_run):
                            for i in range(len(lst_nme_run)-nme_run[1]):
                                lst_nme_run.append(0)
                                
                        print(lst_nme_run, nme_run[1], len(lst_nme_run))
                        lst_nme_run[nme_run[1]] = nme_run[0]

    nme_c = {}  #name coincidence
    #Search the coinciden btw mods.
    for id in info_mods:
        id:str
        c_mod_to = -1

        #Search the position of the mod´s name
        c_name = -1
        for i in range(len(lst_nme_run)):
            c_name+=1
            if lst_nme_run[i] == info_mods[id][0]:
                break

        #Not pass the limit
        if int(id)+1 == len(info_mods):
            break

        info_from = info_mods[str(int(id)+1)]
        while not c_mod_to == len(info_mods):

            c_mod_to+=1
            #Skip the postion of the mod
            if c_mod_to == c_name:
                continue

            for info_to in info_mods[f"{c_mod_to}"]:
                #the next staments evaluates all possibles coincidence btw .info archives.
                for info_lst in info_from:
                    if info_lst[1] == info_to[1] and info_lst[0] != info_to[0]:
                        #THE HELL
                        if info_lst[4] == False and info_to[4] == False:
                            pal_c = 0
                        elif info_lst[4]:
                            pal_c = [1,0]
                        elif info_to[4]:
                            pal_c = [0,1]
                        else:
                            #start to erase the label before of.
                            ...


                        #Search coinciden btw position 
                        num_c = _lst_coincidense(info_lst[2], info_to[2]) #position of num coincidence
                        #Search coindicense btw labels (future changes)
                        lab_c = _lst_coincidense(info_lst[3], info_to[3]) #position of label coincidence

                        if (num_c == lab_c == pal_c): #¿has difference?
                            nme_c[f"{info_lst[0]}-{info_to[0]}"] = {"con":False,
                                                                    "ach":info_lst[1]}
                        else:
                            nme_c[f"{info_lst[0]}-{info_to[0]}"] = {"num":num_c,
                                                                    "lab":lab_c,
                                                                    "pal":pal_c,
                                                                    "ach":info_lst[1]}
        
        print(nme_c)
    #print(lst_nme_run)
"""
                        print(info, nme_run)

                        file = open(root+f"game/mods/{info[1]}/base.info", "rt")
                        ln_info = deco_info(file.read().split(";"), info[0])[2]
                        file.close()
"""

                    
evaluate(sim_var, super_deco())

def execute_lb(chr_lst_run:list):
    for name in chr_lst_run:
        #renpy.call_in_new(name)
        print(f"Execute: {name}")

def single_mod():
    ...

def many_mod():
    ...


    #CHECK MODS FOLDER
def check_mods():
    

    #change directory to "mods"
    chdir(root+"/game/mods")
    #get all directory´s names
    lst_mods = list(filter(path.isdir, listdir()))
        
    if not len(lst_mods) == 0:

        #identify all mods in the folder
        for name in lst_mods:
            chdir(f"{name}")
            file = open(f"{getcwd()}/base.info", "rt") #open the mod´s info
            info = file.read().split(";") # separete the statements

            del info[-1]


"""
                ##########################
                #        PART 2          #
                ##########################
                #preparatives before copy the game archive

                #Before copy game archive
                ftc = open(root+f"/game/{info_mod[0]}","rt") #file to copy
                ftc_info = ftc.readlines()

                #search the line to put the jump
                for ln_to_insert in range(len(lst_jump)):
                    _tmp = ""
                    for _chr in ftc_info[int(ln_to_jump[ln_to_insert])]:
                        if _chr == " ":
                            _tmp += _chr

                    if " " in _chr:
                        _tmp += f"jump {lst_jump[ln_to_insert]}\n"
                    else:
                        _tmp += f"    jump {lst_jump[ln_to_insert]}\n"

                    ftc_info[int(ln_to_jump[ln_to_insert])-1] = _tmp
                        
                #TODO: NEED OPTIMZATION HERE (CODE ONLY)

                    #when the reader is near to the end, start check if the 
                    #mod has all control of the chapter.
                    if ln_to_insert == len(lst_jump)-1:
                        if all_flow:
                            if " " in _tmp:
                                #search the character j of "jump" to erase after.
                                c=-1
                                _nw_tmp = ""
                                chk = False
                                for _chr in _tmp:
                                    c+=1
                                    if _chr == "j":
                                        _nw_tmp += "return\n"
                                        chk = True
                                    elif not chk:
                                        _nw_tmp += _chr
                                    else:
                                        _nw_tmp += ""
                                _tmp = _nw_tmp
                            else:
                                _tmp = "return\n"
                            #TODO: THIS MUST BE REPLACE BY ANOTHER
                            ftc_info[int(ln_to_jump[ln_to_insert])] = _tmp

                ##########################
                #        PART 3          #
                ##########################
                #search if the current file already exits in moddifications

                #TODO: NEED OPTIMAZATION IN THE NAMES AND FLOW
                c=-1
                for tag in ftc_info:
                    c+=1
                    if tag.replace("label", "").replace(" ","")[:-2] in lst_chapter:
                        #replace the original label name with "name"+_mod
                        ftc_info[c] = f"{tag[:-2]}_mod:\n"
                            
                        #Save the reference in to a file
                        try:
                            #¿exits?
                            lst = open(root+f"/game/mods/archive_lst.txt", "rt")
                            lst_info = lst.read().split(";")
                            del lst_info[-1]
                        except: #Errno 2
                            #not exits
                            lst = open(root+f"/game/mods/archive_lst.txt", "w")
                            lst.write(f"{tag[6:-2]}_mod;")
                            break
                            
                        #keep if the name already exits
                        c = False
                        for nme in lst_info:
                            #Name of the label to replace 
                            lb_nme = tag.replace("label", "").replace(" ","")[:-2]
                            #¿Is the name that i have equals to the lb to replace?
                            if nme[:-4] == lb_nme:
                                c = True
                                break
                        if c:
                            lst.close()
                            break
                        lst.close()

                        #write the name (in case if don´t exits)
                        lst = open(root+f"/game/mods/archive_lst.txt", "a")
                        lst.write(f"{tag[6:-2]}_mod;")
                        lst.close()
                        break
                ftc.close()


                ##########################
                #        PART 5          #
                ##########################
                #after of copy, to paste
                ftp = open(root+f"/game/mods/{name}/{info_mod[0][:-4]}_modder.rpy", "w")#file to paste
                    
                #search the staments to copy (if start with a #COPY must close with "NOT")
                c=-1
                for line in ftc_info:
                    c+=1
                    if line.replace(" ", "") == "#COPY\n":
                        for copy_ln in ftc_info[c-1:]:
                            c+=1
                            if copy_ln == "#NOT\n":
                                break
                            else:
                                ftp.write(copy_ln)
                ftp.close()
"""
         
    #Is it in editor mode?
if "renpy.exe" in list(filter(path.isfile, listdir())):
    pass
else:
    #check_mods()
    ...