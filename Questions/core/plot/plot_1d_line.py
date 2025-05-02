import matplotlib.pyplot as plt
from dataclasses import dataclass

class PlotConstant:
    head_width = 0.1
    head_length = 0.3

@dataclass
class _InternalLine:
    x_points : list[float]
    y_points : list[float]
    color : str
    label : str
    linestyle : str = "-"

class Plot1DLine:
    '''
        Plot lines in 1D axis and automatically added U-turn for 1D line
    '''
    _lines : list[_InternalLine] = None
    _color_options : list[str] = ["red", "blue", "orange", "green", "black", "yellow", "purple"]
    _min_point : float = 1000000.0
    _max_point : float = -1000000

    def __init__(self):
        self._lines = []
        self._vertical_start = 1
    
    def _get_auto_color(self):
        return self._color_options.pop()

    def add_line(self, points : list[float], label : str, color : str = "auto"):
        assert(len(points) > 0)
        vert_point = self._vertical_start
        if color == "auto":
            color = self._get_auto_color()

        line = _InternalLine([], [], color, label)

        direction = 0   # 0 : not set, -1: to left, +1: to right

        for idx, point in enumerate(points):
            self._min_point = min(point, self._min_point)
            self._max_point = max(point, self._max_point)
            if idx == 0:
                line.x_points.append(point)
                line.y_points.append(vert_point)
                continue
            prev_point = points[idx - 1]
            if prev_point == point:
                # Same point, ignore
                continue
            if direction == 0:
                # direction is not set
                if point - prev_point > 0:
                    direction = 1
                else:
                    direction = -1
                line.x_points.append(point)
                line.y_points.append(vert_point)
                continue
            
            if direction * (point - prev_point) > 0:
                # same direction
                line.x_points.append(point)
                line.y_points.append(vert_point)
            else:
                # direction is not the same, expect U-Turn
                direction = -direction
                # draw vertical line for u-turn
                vert_point += 0.1
                line.x_points.append(prev_point)
                line.y_points.append(vert_point)
                # draw line
                line.x_points.append(point)
                line.y_points.append(vert_point)
    
        self._vertical_start = vert_point + 1
        self._lines.append(line)
    
    def _draw_single_line(self, line : _InternalLine, ax : plt.Axes):
        # Only has 2 elements -> only draw arrows
        if len(line.x_points) > 2:        
            ax.plot(line.x_points[:-1], line.y_points[:-1], color=f'tab:{line.color}', linestyle=line.linestyle, label=line.label)
        
        x_from = line.x_points[-2]
        x_to = line.x_points[-1]
        y_from = line.y_points[-2]
        y_to = line.y_points[-1]

        # Calculate dx based on direction. If to the left, the head_length should be added, to the right, shoule be substract
        if x_to - x_from >= 0:
            dx = x_to - x_from - PlotConstant.head_length
        else:
            dx = x_to - x_from + PlotConstant.head_length

        dy = y_to - y_from

        ax.arrow(x_from, y_from, dx, dy, 
                 head_width=PlotConstant.head_width,    # widtth
                 head_length=PlotConstant.head_length,  # length
                 fc=line.color,                         # Face color
                 ec=line.color)                         # Edge color
        
        ax.text(line.x_points[0], line.y_points[0], line.label, fontsize=12, ha='right', va='bottom')

    def draw(self, axis_label : str, save_file_path : str):
        '''
            Draw the lines, label the x-axis with axis_label. 
            Save file to save_file_path
        '''
        # Create the plot
        _, ax = plt.subplots(figsize=(8, 6))

        # X-axis data
        x_ticks = range(self._min_point, self._max_point + 1, 1)

        for line in self._lines:
            self._draw_single_line(line, ax)

        # Customize the plot
        ax.set_xlabel(axis_label)
        ax.set_xticks(x_ticks)
        ax.set_yticks([])  # Hide y-axis ticks
        ax.set_xlim(min(self._min_point, 0), self._max_point + 2)  # Set x-axis limits
        ax.spines['left'].set_visible(False) # Remove left spine
        ax.spines['top'].set_visible(False)  # Remove top spine
        ax.spines['right'].set_visible(False) # Remove right spine

        # Enable the grid
        ax.grid(True)

        plt.savefig(fname=save_file_path)

if __name__ == "__main__":
    plotter = Plot1DLine()

    A_x = [0, 7]
    B_x = [12, 8]
    C_x = [2, 10, 8, 11]
    D_x = [9, 3, 4]
    
    plotter.add_line(D_x, "D", "orange")
    plotter.add_line(C_x, "C", "red")
    plotter.add_line(A_x, "A", "green")
    plotter.add_line(B_x, "B", "blue")

    plotter.draw("x(m)", "temp.png")