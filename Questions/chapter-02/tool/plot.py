import matplotlib.pyplot as plt
from dataclasses import dataclass

class PlotConstant:
    head_width = 0.2
    head_length = 0.5

@dataclass
class PlotArrowLineConfig:
    face_color : str = "black"
    edge_color : str = "black"
    label : str = ""
    linestyle : str ="-"

    def get_kw_args(self) -> dict[str, str]:
        ret = {}
        ret.update(fc=self.face_color)
        ret.update(ec=self.edge_color)
        ret.update(label=self.label)
        ret.update(linestyle=self.linestyle)
        return ret

class PlotArrowLine:
    list_x : list[int] = []
    list_y : list[int] = []
    ax : plt.Axes = None
    config : PlotArrowLineConfig = PlotArrowLineConfig() 
    def __init__(self, list_x : list[int], list_y : list[int], ax : plt.Axes, config : PlotArrowLineConfig = None):
        assert(len(list_x) == len(list_y))
        assert(len(list_x) >= 2)
        self.list_x = list_x
        self.list_y = list_y
        self.ax = ax
        if config:
            self.config = config
    
    def draw_arrow(self):
        '''
            This method draw the arrow at the tip. This arrow should be the last element of drawing
        '''
        x_from = self.list_x[-2]
        x_to = self.list_x[-1]
        y_from = self.list_y[-2]
        y_to = self.list_y[-1]

        self.ax.arrow(x_from, y_from, x_to - x_from - PlotConstant.head_length, y_to - y_from, head_width=PlotConstant.head_width, head_length=PlotConstant.head_length, **self.config.get_kw_args())
        self.ax.text(self.list_x[0], self.list_y[0], self.config.label, fontsize=12, ha='right', va='bottom')

    def draw(self):
        # Only has 2 elements -> only draw arrows
        if len(self.list_x) == 2:
            self.draw_arrow()
            return
        
        self.ax.plot(self.list_x[:-1], self.list_y[:-1], color=f'tab:{self.config.edge_color}', linestyle=self.config.linestyle, label=self.config.label)
        self.draw_arrow()