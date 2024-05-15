from typing_extensions import Literal

from .internal.tool.debug import erase_screen, _chk_window

from .obj.gen_obj import gen_obj, gen_btn, CUR, N_NUM, N_ABS
from .obj.gen_wns import gen_wns

from webbrowser import open

def __main_return__(*nm):
    erase_screen()
    _chk_window()

    if len(nm)==1:
        CUR[0][nm[0]].start_cast()
    else:
        CUR[0][nm[1]].start_cast()

def __save__(*nm):
    ...

def __load__(*nm):
    ...

def __continue__(*nm):
    ...

def __queque__(*nm):
    import sys
    sys.exit()

class Button(gen_obj, gen_wns, gen_btn):
    def __init__(self, *, 
                 X: int, 
                 Y: int, 
                 TEXT: str="",
                 ACTION=...,
                 NMO: str = "",
                 DEFAULT:Literal["EXIT",
                                 "LOAD",
                                 "SAVE",
                                 "BACK",
                                 "LINK",
                                 "CUSTOM"]=...) -> None:
        N_NUM[1] += 1
        super().__init__(X=X, 
                         Y=Y, 
                         CHR=TEXT, 
                         ABS=N_ABS[1], 
                         ID=N_NUM[1], 
                         NMO=NMO)

        self.select = DEFAULT
        self.in_id:int = 0

        match self.select:
            case "SAVE":
                if TEXT == "":
                    self.character = "Guardar"
                self.action = __save__
            case "LOAD":
                if TEXT == "":
                    self.character = "Cargar"
                self.action = __load__
            case "EXIT":
                if TEXT == "":
                    self.character = "Salir"
                self.action = __queque__
            case "BACK":
                if TEXT == "":
                    self.character = "Regresar"
                self.action = __main_return__
            case "LINK":
                if TEXT == "":
                    self.character = "Abrir URL"
                self.action = self.__link__
                self.url = ACTION
            case "CUSTOM":
                self.action = ACTION    
            case _:
                self.action = ACTION
        
        self.cast = ("")
        self.var = 0

    def caster(self, msg:tuple[str]=(""), *var):
        self.cast = msg
        self.var = var

    def __link__(self, *nm):
        open(self.url)
        __main_return__()