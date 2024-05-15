from time import sleep
from typing_extensions import Literal
from .internal.tool.debug import _chk_window, print_debug, _insert

from .obj.gen_obj import gen_obj, N_ABS, N_NUM, CUR, DEV
from .obj.gen_wns import gen_wns, gen_ui

from .button import Button

class Page(gen_obj, gen_wns, gen_ui):
    def __init__(self, *, 
                 X: int, 
                 Y: int, 
                 CHR: str,
                 NMO: str = "") -> None:
        N_NUM[0]+=1

        super().__init__(X=X, 
                         Y=Y, 
                         CHR=CHR, 
                         ABS=N_ABS[0], 
                         ID=N_NUM[0], 
                         NMO=NMO)
        super().__wns__()

        CUR[0].append(self)

        self.btns:list=[]
        self.panel:list=[{"vec":[0,0], "transform":[0,0], "chr":"#"}]

        self._set_meta("panel", self.panel)

        self._create_square(self.vec)
        if DEV[0]:
            self._create_line_num()

    def add_btn(self, btn:Button, complete:bool=True):
        if complete:
            btn.in_id = len(self.btns)
            self.btns.append(btn)

        self.create_text(f"{btn.in_id+1}) "+btn.character, "CUSTOM", tuple(btn.vec))

    def del_btn(self, ID:int, complete:bool=True)->None:
        if complete:
            self.btns[ID-1] = f"del_obj_{self.btns[ID-1].name}"

        self.create_text(" "*(self.btns[ID-1].in_id+len(self.btns[ID-1].character)+3), "CUSTOM", tuple(self.btns[ID-1].vec))
        
    def add_panel(self, 
                  X:int, 
                  Y:int, 
                  SZ_X:int,
                  SZ_Y:int,
                  bug:Literal[0,1],
                  CHR:str="#"):
        
        if X >= self.vec[0] or Y <= self.vec[1] or X <= 0 or Y <= 0:
            if SZ_X >= self.vec[0] or SZ_Y <= self.vec[1]:
                self.panel.append({"vec":[X, Y],"transform":[SZ_X, SZ_Y],"chr":CHR})
                self._edit_meta(nme="panel", kwr=self.panel)

                for y in range(SZ_Y+1):
                    if not(y == 0 or y == SZ_Y-bug):
                        line = self._create_square([SZ_X, SZ_Y], "start")
                    else:
                        line = self._create_square([SZ_X, SZ_Y], "last")

                    self.square[Y+y] = _insert(self.square[Y+y], line, X, len(line)+X)
            else:
                print("Coordenadas insuficientes")
        else:
            print("Coordenadas incorrectas")



    def del_panel(self, ID:int):
        
        
        self._edit_meta(nme="panel", kwr=self.panel)
        ...

    def start_cast(self):
        _chk_window()
        self.get_pre_view()

        try:
            _in = int(input("Enter button's number\n>   "))-1
            self.btns[_in]._input_(self.btns[_in].cast)
        except (ValueError, IndexError):
            print_debug("U MUST ENTER SOME BUTTON'S NUMBER, TRY AGAIN")
            sleep(3)
            self.start_cast()
