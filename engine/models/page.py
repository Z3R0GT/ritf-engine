from time import sleep
from .internal.tool.debug import _chk_window, print_debug

from .obj.gen_obj import gen_obj, N_ABS, N_NUM, CUR
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
                         ID=N_NUM, 
                         NMO=NMO)
        super().__wns__()

        CUR[0].append(self)

        self.btns:list=[]
        self._create_square(self.vec)

    def add_btn(self, btn:Button):
        self.btns.append(btn)
        self.create_text(f"{len(self.btns)}) "+btn.character, "CUSTOM", tuple(btn.vec))

    def start_cast(self):
        _chk_window()
        self.get_pre_view()

        try:
            _in = int(input("Enter button's number\n>   "))-1
            self.btns[_in]._input_(self.btns[_in].cast)
        except ValueError:
            print_debug("U MUST ENTER SOME BUTTON'S NUMBER, TRY AGAIN")
            sleep(3)
            self.start_cast()