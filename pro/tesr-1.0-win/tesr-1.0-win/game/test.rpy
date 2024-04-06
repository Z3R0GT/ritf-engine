init python:
    i = "chapter_1_start"
    lst_chapter = ["label chapter_1_start:\n"]
    from os import listdir, path, getcwd

    global root
    root = getcwd()
    
    def check_mods():
        from os import chdir, mkdir

        chdir(root+"/game/mods")
        lst_mods = list(filter(path.isdir, listdir()))
        
        if not len(lst_mods) == 0:
            cur_file = []
            table:dict = {
                "-": ",",
                91: "", 
                93: "", 
                92: "", 
                }
                
            for name in lst_mods:
                chdir(f"{name}")
                file = open(f"{getcwd()}/base.info", "rt") #open the mod info
                info = file.read().split(";") # separete the statements
                
                del info[-1]

                for data in info:
                    info_mod = list(data.split(",")) #separate the data
                    
                    info_mod.append("s")
                    info_mod.append("s")

                    ln_to_jump = tuple(info_mod[1].replace("-", ",").replace("]","").replace("[", "").replace("\ n".replace(" ", ""), "").replace("\ ".replace(" ", ""),"").split(","))

                    _lst_nme = list(info_mod[2].translate(table)) #list names
                    _fn_nme = ""  #final name

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

                    ftc = open(root+f"/game/{info_mod[0]}","rt")
                    ftc_info = ftc.readlines()

                    for ln_to_insert in range(len(lst_jump)):
                        _tmp = ""
                        for _chr in ftc_info[int(ln_to_jump[ln_to_insert])]:
                            if _chr == " ":
                                _tmp += _chr
                        _tmp += f"    jump {lst_jump[ln_to_insert]}\n"

                        ftc_info[int(ln_to_jump[ln_to_insert])-1] = _tmp 
                    
                    c=-1
                    for tag in ftc_info:
                        c+=1
                        if tag in lst_chapter:
                            ftc_info[c] = f"{tag[:-2]}_mod:\n"
                            #Save the reference in a file
                            try:
                                lst = open(root+f"/game/mods/archive_lst.txt", "rt")
                                lst_info = lst.read().split(";")
                            except: #Errno 2
                                lst = open(root+f"/game/mods/archive_lst.txt", "w")
                                lst.write(f"{tag[6:-2]}_mod;")
                                break
                            
                            c = False
                            for nme in lst_info:
                                if nme[:-4] == i:
                                    c = True
                                    break
                            if c:
                                break


                            lst.close()
                            lst = open(root+f"/game/mods/archive_lst.txt", "a")
                            lst.write(f"{tag[6:-2]}_mod;")
                            lst.close()
                            break
                    
                    ftc.close()

                    #to paste
                    ftp = open(root+f"/game/mods/{name}/{info_mod[0][:-4]}_modder.rpy", "w")
                    
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

    #Is it in editor mode?
    if "renpy.exe" in list(filter(path.isfile, listdir())):
        pass
    else:
        check_mods()

    def as_mods():
        lst_mod = open(root+f"/game/mods/archive_lst.txt", "rt")
        chr_mod = lst_mod.read().split(";")

        lst_nmod = open(root+f"/chapters_include.txt", "rt")
        chr_nmod = lst_nmod.read().split(";")

        renpy.call_in_new_context(i+"_mod")

label start:
    $ m = as_mods()

#COPY
label chapter_1_start:
    "h" "no estoy modificado papa"



















