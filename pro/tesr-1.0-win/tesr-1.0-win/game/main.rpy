python:
    
    #Only if a mod exits (this must be in the start of the all chapters)
    def list_to_start():
        #List of currents mods
        lst_mod = open(root+f"/game/mods/archive_lst.txt", "rt")
        chr_mod = lst_mod.read().split(";")
        lst_mod.close()

        #List of all chapters
        lst_nmod = open(root+f"/chapters_include.txt", "rt")
        chr_nmod = lst_nmod.read().split(";")
        lst_nmod.close()

        #List of labels to run
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
                    
        #Read the chapters to run
        lst_run = open(root+"/run.txt", "rt")
        chr_lst_run = lst_run.read().split(";")
        lst_run.close()

        del chr_lst_run[-1]
"""
        for name in chr_lst_run:
            #run the chapters
            renpy.call_in_new_context(name)
"""

#COPY
label start:
    #Only need this function
    #Here end the game
    return