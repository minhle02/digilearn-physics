import matplotlib.pyplot as plt
from dataclasses import dataclass
from .plot import *
import os

def get_static_folder():
    # Use when testing, save file to current dir
    if __name__ == "__main__":
        return ""

    # TODO: think a better way to get static folder
    for folder in os.listdir(os.getcwd()):
        # found folder static
        if folder == "static":
            break
    else:
        # not found -> create
        os.mkdir("static")

    return os.path.join(os.path.abspath(os.getcwd()), "static")


def gen_image_for_e1():
    # Create the plot
    _, ax = plt.subplots(figsize=(8, 6))

    # X-axis data
    x_ticks = range(0, 13, 1)

    # Data for the lines
    A_x = [0, 7]
    A_y = [5, 5]
    draw_a = PlotArrowLine(A_x, A_y, ax, PlotArrowLineConfig("green", "green", "A"))
    draw_a.draw()

    B_x = [12, 8]
    B_y = [6, 6]
    draw_b = PlotArrowLine(B_x, B_y, ax, PlotArrowLineConfig("blue", "blue", "B"))
    draw_b.draw()


    C_x = [2, 10, 10, 8, 8, 11]
    C_y = [3, 3, 3.5, 3.5, 4, 4]
    draw_c = PlotArrowLine(C_x,  C_y, ax, PlotArrowLineConfig("red", "red", "C"))
    draw_c.draw()

    D_x = [9, 3, 3, 4]
    D_y = [1, 1, 1.5, 1.5]
    draw_d = PlotArrowLine(D_x, D_y, ax, PlotArrowLineConfig("orange", "orange", "D"))
    draw_d.draw()

    # Customize the plot
    ax.set_xlabel('x (m)')
    ax.set_xticks(x_ticks)
    ax.set_yticks([])  # Hide y-axis ticks
    ax.set_xlim(0, 12.5)  # Set x-axis limits
    ax.spines['left'].set_visible(False) # Remove left spine
    ax.spines['top'].set_visible(False)  # Remove top spine
    ax.spines['right'].set_visible(False) # Remove right spine

    # Enable the grid
    ax.grid(True)

    plt.savefig(fname=os.path.join(get_static_folder(), "figure-c2-m1-e1.png"))

if __name__ == "__main__":
    print(__name__)