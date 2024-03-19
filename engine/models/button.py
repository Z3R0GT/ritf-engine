from typing_extensions import Literal

from .internal.tool.debug import erase_screen, _chk_window, set_console_font

from .internal.admin_dir import save_node, load_save
from .internal.archives import refresh_saves, start_test, _check_save

from .internal.tool.const import CUR, DEFAULT


from .obj.gen_wns import gen_wns
from .obj.gen_obj import gen_obj, gen_btn, N_NUM, N_ABS

def __loader(*ID):
    
    ld = load_save(CUR[4][int(ID[0][0])-1])
    ...
    
def __main_return__(id=...):
    DEFAULT[1][1] = True
    erase_screen()
    _chk_window()

    if type(id) == type(...):
        CUR[0][0].start_cast()
    else:
        CUR[0][id[0]].start_cast()
        
def __continue__():
    erase_screen()
    DEFAULT[1][2] = True
    _chk_window()

    #REEPLANTEARSE EL CODGIO LOGICO PARA EL INICIO DEL JUEGO       

def __queque__():
    import sys    
    sys.exit()

def __load__():
    if _check_save():  
        lst = refresh_saves(CUR)
        
        from.page import Page
        
        if len(max(lst)) < CUR[0][0].vec[0] or len(max(lst)) < CUR[0][0].vec[1]:
            pgn = Page(CUR[0][0].vec[0], CUR[0][0].vec[1], CUR[0][0].character)
        else:
            pgn = Page(len(max(lst)), len(lst)+7, CUR[0][0].character)
            
        for text in lst:
            pgn.create_text(text[:len(text)-4], "UPPER")
        btn = Button(1, pgn.vec[1]-5, "Cargar", __loader)
        btn.cast(("Ingrese el archivo a cargar",))
        
        btn_1 = Button(1, pgn.vec[1]-3, DEFAULT="BACK")
        btn_1.cast()

        pgn.add_btn(btn)
        pgn.add_btn(btn_1)

        pgn.start_cast()
    
def __save__():
    temp = {}
    for mapa in CUR[2]:
        temp[f"{mapa.id}"] = mapa.meta
    
    temp["1"]["node_lst"]["pla"] = [DEFAULT[0].meta]
    
    if start_test():
        save_node(temp)
        
    __main_return__()
    return

class Button(gen_wns, gen_obj, gen_btn):
    def __init__(self, 
                 X:int, 
                 Y:int, 
                 CHR:str="", 
                 ACTION=..., 
                 DEFAULT:Literal["EXIT",
                                 "LOAD", 
                                 "SAVE", 
                                 "BACK", 
                                 "CONTINUE",
                                 "CUSTOM"]=...,
                 NMO="",
                 ) -> None:
        N_NUM[1] +=1
        super().__init__(X, Y, CHR, N_ABS[1], N_NUM[1], NMO)
        
        self.select = DEFAULT

        if self.id == 1:
            super().__default__()
        
        match self.select:
            case "SAVE":
                if CHR == "":
                    self.character = "Guardar"
                super().__action__(__save__)
            case "EXIT":
                if CHR == "":
                    self.character = "Salir"
                super().__action__(__queque__)
            case "LOAD":
                if CHR == "":
                    self.character = "Cargar"
                super().__action__(__load__)
            case "BACK":
                if CHR == "":
                    self.character = "Regresar"
                super().__action__(__main_return__)
            case "CONTINUE":
                if CHR == "":
                    self.character = "Continuar"
                super().__action__(__continue__)
            case "CUSTOM":
                super().__action__(ACTION)
            case _:
                super().__action__(ACTION)
    
    def cast(self, msg:tuple=("")):
        self.cast = msg
        
