import matplotlib.pyplot as plt
from dataclasses import dataclass

# Existing PlotConstant class (unused in this snippet but kept from original)
class PlotConstant:
    head_width = 0.1
    head_length = 0.3

# Existing Line dataclass
@dataclass
class Line:
    x_start : float
    y_start : float
    x_to : float
    y_to : float
    color : str = "black"
    label : str = ""  # This label will be used for the text at the end of the line
    linestyle : str = "-"

# New dataclass for storing arbitrary point labels
@dataclass
class PointLabel:
    x: float
    y: float
    text: str
    color: str = "black"
    fontsize: int = 8 # Default fontsize for point labels

class Plot2DLine:
    '''
        Plot lines in 2D axis, with support for line-end labels and point labels.
    '''
    _lines : list[Line]
    _point_labels : list[PointLabel] # To store custom point labels
    _color_options : list[str] = ["red", "blue", "orange", "green", "black", "yellow", "purple"]
    _min_point : float = 1000000.0
    _max_point : float = -1000000

    def __init__(self):
        self._lines = []
        self._point_labels = [] # Initialize list for point labels
        self.x_axis_label = ""
        self.y_axis_label = ""
        self.enable_x_axis_ticks = True
        self.enable_y_axis_ticks = False # As per set_property default
        # Default appearance for line-end labels
        self.line_end_label_fontsize = 8
        self.line_end_label_offset_points = (5, 5) # (dx, dy) in points
        self.point_label_offset_points = (3,3) # (dx, dy) for general point labels


    def add_line(self,
                 x_from : float,
                 x_to : float,
                 y_from : float,
                 y_to : float,
                 color : str = "black",
                 linestyle  : str = "-",
                 label : str = ""): # Added 'label' parameter
        '''Adds a line to be plotted. The label will be shown at the end of the line.'''
        line = Line(
            x_start=x_from,
            y_start=y_from,
            x_to=x_to,
            y_to=y_to,
            color=color,
            linestyle=linestyle,
            label=label # Store the label for the line
        )
        self._lines.append(line)

    def add_point_label(self, x: float, y: float, label_text: str, color: str = "black", fontsize: int = 8):
        """Adds a custom text label at a specific point (x, y) on the plot."""
        if not isinstance(label_text, str):
            try:
                label_text = str(label_text) # Ensure the label is a string
            except ValueError:
                print(f"Warning: Could not convert label to string for point ({x},{y}). Skipping point label.")
                return
        self._point_labels.append(PointLabel(x=x, y=y, text=label_text, color=color, fontsize=fontsize))

    def set_property(self, x_axis_label : str = "", y_axis_label : str = "", enable_x_axis_ticks : bool = True, enable_y_axis_ticks : bool = False):
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.enable_x_axis_ticks = enable_x_axis_ticks
        self.enable_y_axis_ticks = enable_y_axis_ticks

    def draw(self,
             save_file_path : str):
        '''
            Draw the lines with axes centered at (0,0).
            Adds labels at the end of lines and custom point labels.
            Save file to save_file_path
        '''
        # Create the plot
        _, ax = plt.subplots(figsize=(8, 6))

        # Determine data range
        if not self._lines and not self._point_labels:
            x_min_data, x_max_data = -1.0, 1.0
            y_min_data, y_max_data = -1.0, 1.0
            data_exists = False
        else:
            x_coords = []
            y_coords = []
            if self._lines:
                x_coords.extend([line.x_start for line in self._lines])
                x_coords.extend([line.x_to for line in self._lines])
                y_coords.extend([line.y_start for line in self._lines])
                y_coords.extend([line.y_to for line in self._lines])
            if self._point_labels:
                x_coords.extend([p.x for p in self._point_labels])
                y_coords.extend([p.y for p in self._point_labels])

            if not x_coords or not y_coords: # Should not happen if _lines or _point_labels is not empty
                x_min_data, x_max_data = -1.0, 1.0
                y_min_data, y_max_data = -1.0, 1.0
                data_exists = False
            else:
                x_min_data = min(x_coords)
                x_max_data = max(x_coords)
                y_min_data = min(y_coords)
                y_max_data = max(y_coords)
                data_exists = True


        # Plot all lines and their end labels
        for line_obj in self._lines:
            # Plot the line. The 'label' kwarg is for legend entries.
            ax.plot([line_obj.x_start, line_obj.x_to], [line_obj.y_start, line_obj.y_to],
                    color=line_obj.color, linestyle=line_obj.linestyle, label=line_obj.label)

            # Add label at the end of the line (x_to, y_to) if provided
            if line_obj.label:
                ax.text(line_obj.x_to, line_obj.y_to, line_obj.label,
                        fontsize=self.line_end_label_fontsize,
                        color=line_obj.color, # Use line color for its label
                        ha='left', va='bottom')

        # Plot all additional point labels
        for pt_label in self._point_labels:
            ax.text(pt_label.x + 0.2, pt_label.y - 0.2, pt_label.text,
                    fontsize=pt_label.fontsize,
                    color=pt_label.color,
                    ha='left', va='bottom')

        # ---- MODIFICATIONS FOR CENTERED AXES (from previous response) ----
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        # ---- END OF MODIFICATIONS FOR CENTERED AXES ----

        buffer = 1 if data_exists else 0
        x_tick_min = int(x_min_data - buffer)
        x_tick_max = int(x_max_data + buffer) + 1
        y_tick_min = int(y_min_data - buffer)
        y_tick_max = int(y_max_data + buffer) + 1

        if self.enable_x_axis_ticks:
            ax.set_xlabel(self.x_axis_label)
            ax.xaxis.set_label_coords(1.02, 0.5 + (0.1 if y_min_data <0 < y_max_data else 0))
            ax.set_xticks(range(x_tick_min, x_tick_max))
        else:
            ax.set_xticks([])
            ax.set_xlabel("")

        if self.enable_y_axis_ticks:
            ax.set_ylabel(self.y_axis_label, rotation=0)
            ax.yaxis.set_label_coords(0.5 + (0.1 if x_min_data <0 < x_max_data else 0) , 1.02)
            ax.set_yticks(range(y_tick_min, y_tick_max))
        else:
            ax.set_yticks([])
            ax.set_ylabel("")

        padding = 1.5 if data_exists else 2.0
        final_x_min = min(x_min_data - padding if data_exists else -padding, 0 if x_max_data >= 0 else x_min_data - padding)
        final_x_max = max(x_max_data + padding if data_exists else padding, 0 if x_min_data <= 0 else x_max_data + padding)
        final_y_min = min(y_min_data - padding if data_exists else -padding, 0 if y_max_data >= 0 else y_min_data - padding)
        final_y_max = max(y_max_data + padding if data_exists else padding, 0 if y_min_data <= 0 else y_max_data + padding)

        if final_x_min == final_x_max:
            final_x_min -= padding
            final_x_max += padding
        if final_y_min == final_y_max:
            final_y_min -= padding
            final_y_max += padding

        if data_exists:
             final_x_min = min(final_x_min, 0.0)
             final_x_max = max(final_x_max, 0.0)
             final_y_min = min(final_y_min, 0.0)
             final_y_max = max(final_y_max, 0.0)

        ax.set_xlim(final_x_min, final_x_max)
        ax.set_ylim(final_y_min, final_y_max)

        ax.grid(True, linestyle='--', alpha=0.7)

        plt.savefig(fname=save_file_path)
        plt.close() # Close the plot to free memory

if __name__ == "__main__":
    plotter = Plot2DLine()

    plotter.add_line(x_from=0, y_from=0, x_to=2, y_to=2, label=r"$R_3$")
    plotter.add_line(x_from=0, y_from=0, x_to=-2, y_to=-1, label=r"$R_1$")
    plotter.add_line(x_from=0, y_from=0, x_to=-1.25, y_to=2, label=r"$R_2$")
    plotter.add_point_label(0, 0, "I")
    plotter.set_property(enable_x_axis_ticks=False, enable_y_axis_ticks=False)
    plotter.draw(save_file_path="temp.svg")