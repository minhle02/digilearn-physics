import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from core import Plot1DLine

def get_static_folder():
    folder = os.path.join(os.path.dirname(__file__), "static")
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def gen_image_1():
    plotter = Plot1DLine()

    A_x = [0, 7]
    B_x = [12, 8]
    C_x = [2, 10, 8, 11]
    D_x = [9, 3, 4]
    
    plotter.add_line(D_x, "D", "orange")
    plotter.add_line(C_x, "C", "red")
    plotter.add_line(A_x, "A", "green")
    plotter.add_line(B_x, "B", "blue")

    plotter.draw("x(m)", os.path.join(get_static_folder(), "figure-c2-m1-e1.png"))

if __name__ == "__main__":
    gen_image_1()