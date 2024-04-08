init python:

    #current chapter´s name
    i = "chapter_1_start"
    #all chapter´s name
    lst_chapter = ["label chapter_1_start:\n"]

    #for checks
    from os import listdir, path, getcwd

    global root
    root = getcwd()
    
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

                    #Before copy game archive
                    ftc = open(root+f"/game/{info_mod[0]}","rt") #file to copy
                    ftc_info = ftc.readlines()

                    #search the line to put the jump
                    for ln_to_insert in range(len(lst_jump)):
                        _tmp = ""
                        for _chr in ftc_info[int(ln_to_jump[ln_to_insert])]:
                            if _chr == " ":
                                _tmp += _chr
                        _tmp += f"    jump {lst_jump[ln_to_insert]}\n"

                        ftc_info[int(ln_to_jump[ln_to_insert])-1] = _tmp 
                    
                    #search if the current file already exits in moddifications
                    c=-1
                    for tag in ftc_info:
                        c+=1
                        if tag in lst_chapter:
                            ftc_info[c] = f"{tag[:-2]}_mod:\n"

                            #Save the reference in to a file
                            try:
                                #¿exits?
                                lst = open(root+f"/game/mods/archive_lst.txt", "rt")
                                lst_info = lst.read().split(";")
                            except: #Errno 2
                                #not exits
                                lst = open(root+f"/game/mods/archive_lst.txt", "w")
                                lst.write(f"{tag[6:-2]}_mod;")
                                break
                            
                            #keep if the name already exits
                            c = False
                            for nme in lst_info:
                                if nme[:-4] == i:
                                    c = True
                                    break
                            if c:
                                break
                            lst.close()

                            #write the name (in case if don´t exits)
                            lst = open(root+f"/game/mods/archive_lst.txt", "a")
                            lst.write(f"{tag[6:-2]}_mod;")
                            lst.close()
                            break
                    ftc.close()

                    #after of copy, to paste
                    ftp = open(root+f"/game/mods/{name}/{info_mod[0][:-4]}_modder.rpy", "w")#file to paste
                    
                    #search the staments to copy (if start with a #COPY must close with "NOT")
                    c=-1
                    for line in ftc_info:
                        c+=1
                        if line == "#COPY\n":
                            for copy_ln in ftc_info[c-1:]:
                                c+=1
                                if copy_ln == "#NOT\n":
                                    break
                                else:
                                    ftp.write(copy_ln)
                    ftp.close()
    

    #Only if a mod exits (this must be in the start of the all chapters)
    def list_to_start():
        lst_mod = open(root+f"/game/mods/archive_lst.txt", "rt")
        chr_mod = lst_mod.read().split(";")
        lst_mod.close()

        lst_nmod = open(root+f"/chapters_include.txt", "rt")
        chr_nmod = lst_nmod.read().split(";")
        lst_nmod.close()

        lst_run = open(root+f"/run.txt", "w")

        #Create a list for run the chapters
        _pre_lst_run = ""
        chk = False
        for nmod in chr_nmod:
            for mod in chr_mod:
                if nmod == mod[:-4]:
                    _pre_lst_run += mod+";"
                    chk = False
                    break
                else:
                    chk = True

            if chk:
                _pre_lst_run += nmod+";"

        lst_run.write(_pre_lst_run)
        lst_run.close()
                    
        lst_run = open(root+"/run.txt", "rt")
        chr_lst_run = lst_run.read().split(";")
        lst_run.close()

        for name in chr_lst_run:
            renpy.call_in_new_context(name)
                    
    
    #Is it in editor mode?
    if "renpy.exe" in list(filter(path.isfile, listdir())):
        pass
    else:
        check_mods()
        list_to_start()
    

#COPY
label chapter_1_start:
    "owo"









    return








