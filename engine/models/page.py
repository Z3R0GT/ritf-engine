import time
from .internal.tool.debug import _chk_window, print_debug

from .obj.gen_obj import gen_obj, N_ABS, N_NUM, CUR
from .obj.gen_wns import gen_wns, gen_ui

class Page(gen_obj, gen_wns, gen_ui):
    
    def __init__(self, 
                 X, 
                 Y, 
                 CHR, 
                 NMO="") -> None:
        N_NUM[0] += 1
        
        super().__init__(X, Y, CHR, N_ABS[0], N_NUM[0], NMO)
        super().__wns__()
        
        CUR[0].append(self)
        
        self.btns = [...]

        self._create_square(self.vec)
        #self._create_line_num()
    
    def add_btn(self, btn:gen_obj):
        self.create_text(btn.character, "CUSTOM", tuple(btn.vec))
        self.btns.append(btn)
    
    def start_cast(self):
        _chk_window()
        self.get_pre_view()
        
        input("VERIFICADO, PRESIONE *ENTER* POR FAVOR... \n>   ")
        try:
            _in = int(input("Ingrese el número de boton \n>   "))
            self.btns[_in]._input_(self.btns[_in].cast)
        except ValueError:
            print_debug("DEBE DE INGRESAR ALGUN NUMERO DE BOTON, INTENTE OTRA VEZ")
            time.sleep(3)
            self.start_cast()
     