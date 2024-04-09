init python:
    #for checks
    from os import listdir, path, getcwd
    
    global root
    root = getcwd()

    #all chapter´s name
    lst_nmod = open(root+f"/chapters_include.txt", "rt")
    lst_chapter = lst_nmod.read().split(";")
    lst_nmod.close()
    del lst_chapter[-1]

    def single_mod():
        ...

    def many_mod():
        ...


    #CHECK MODS FOLDER
    def check_mods():
        from os import chdir, mkdir

        #change directory to "mods"
        chdir(root+"/game/mods")
        #get all directory´s names
        lst_mods = list(filter(path.isdir, listdir()))
        
        if not len(lst_mods) == 0:
            #banned characters
            table:dict = {
                "-": ",",
                91: "", #ANSI
                93: "", #ANSI
                92: "", #ANSI
                }
            
            #identify all mods in the folder
            for name in lst_mods:
                chdir(f"{name}")
                file = open(f"{getcwd()}/base.info", "rt") #open the mod´s info
                info = file.read().split(";") # separete the statements
                
                del info[-1]

                for data in info:
                    info_mod = list(data.split(",")) #separate the data of mod´s info
                    
                    #idk why, but if i don´t write this, appear a unknow error
                    info_mod.append("s")
                    info_mod.append("s")
                    info_mod.append("s")


                    ##########################
                    #        PART 1          #
                    ##########################
                    #Decoficade the .info archive

                    #line to jump
                    ln_to_jump = tuple(info_mod[1].replace("-", ",").replace("]","").replace("[", "").replace("\ n".replace(" ", ""), "").replace("\ ".replace(" ", ""),"").split(","))

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
                    
    #Is it in editor mode?
    if "renpy.exe" in list(filter(path.isfile, listdir())):
        pass
    else:
        check_mods()