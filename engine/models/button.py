from typing_extensions import Literal

from .internal.tool.debug import erase_screen, _chk_window

from .obj.gen_obj import gen_obj, gen_btn, CUR, DEFAULT, N_NUM, N_ABS
from .obj.gen_wns import gen_wns

def __main_return__(ID:int=0):
    erase_screen()
    _chk_window()

    CUR[0][ID].start_cast()

def __save__():
    ...

def __load__():
    ...

def __continue__():
    ...

def __queque__():
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
                                 "CUSTOM"]=...) -> None:
        N_NUM[1] += 1
        super().__init__(X=X, 
                         Y=Y, 
                         CHR=TEXT, 
                         ABS=N_ABS[1], 
                         ID=N_NUM[1], 
                         NMO=NMO)

        self.select = DEFAULT

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
            case "CUSTOM":
                self.action = ACTION    
            case _:
                self.action = ACTION
        
        self.cast = ("")

    def caster(self, msg:tuple[str]=("")):
        self.cast = msg