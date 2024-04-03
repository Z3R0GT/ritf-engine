
define t = Character("iwi")


#DEFINE ENTORNO PYTHON
init python:
    lst_run = []

    def abcd():
        return "1"

    from os import listdir, path

    #Is it in editor mode?
    if "renpy.exe" in list(filter(path.isfile, listdir())):
        pass
    else:
        from os import getcwd, chdir, mkdir
        
        root = getcwd()

        chdir(root+"/mods")
        cur_mods = list(filter(path.isdir, listdir()))

        cur_file = []

        for name in cur_mods:
            chdir(f"{name}")
            file = open(f"{getcwd()}/base.info", "rt")
            info = file.read().split(";")
            for i in info:
                info_mod = list(i.split(","))

                n = open(root+f"/mods/{name}/n.txt", "a")
                info_mod.append("s")
                info_mod.append("s")
                n.write(f"{info_mod[1]}")

                ln = list(info_mod[1].replace(
                    "-", ",").replace(
                        "[","").replace(
                            "]", "").replace("\ n".replace(" ", ""), "").replace(
                                "\ ".replace(" ", ""),"").split(","))

                lb_jmp = list(info_mod[2].replace(
                    "-", ",").replace(
                        "[","").replace(
                            "]", "").replace(
                                "\ n".replace(" ", ""), "").replace(
                                    "\ ".replace(" ", ""),"").split(","))
   
        
        #n = open(root+f"/mods/{name}/n.txt", "w")
        #n.write(info_mod, line, lb)  
  
"""
        if len(cur_mods) == 0:
            pass #VARIABLE FOR VERIFICATION
        else:
            for name in cur_mods:
                chdir(f"{name}")
                file =  open(f"{getcwd()}/base.info", "rt")
                info = file.read().split(";")

                for i in info:
                    info_mod = list(i.split(",")) #info_modands
                    chdir(root+"/game")
                    ftc = open(root+f"/game/{info_mod[0]}","rt") #file_to_copy   
                    ftc_inf = ftc.readlines()

                    #Convert all files
                    line = list(info_mod[1].replace("-", ",").replace("[","").replace("]", "").split(","))
                    
                    lb = list(info_mod[2].replace("-", ",").replace("[","").replace("]", "").split(","))

                    #if ftc_inf[int(com[0])-1].replace("\n", "").replace("\", ") ==com[1]: # DO YOU HAVE THE REFERENCE info_modAND?
                    for k in lb:
                        ftc_inf[int(line[0])] = f"jump {k}"

                    with open(root+f"/mods/{name}/{info_mod[0][:-4]}_modder.rpy", "w") as ftp:  #file_to_paste
                        for m in ftc_inf:
                            ftp.write(m)
                    
                    ftp.close()

                    chdir(root+f"/mods/{name}")
"""

label start:
    scene hola

    show t sad

    t "miau"
    
    #DECLARACIÓN DE VARIABLE DE PYTHON-RENPY
    $ ans = abcd()

    #CODIGO PARA ENLAZAR PYTHON CON RENPY
    "h" "[ans]"
    



