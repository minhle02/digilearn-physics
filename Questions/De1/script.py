import os
import sys
core_inc = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(core_inc)
from core import PlotCosine

import math

import schemdraw
import schemdraw.elements as elm

import numpy as np
def get_static_folder():
    return os.path.join(os.path.dirname(__file__), "static")

def draw_pic_for_q70():
    with schemdraw.Drawing(show=False) as drawing:

        drawing += elm.Resistor(label="R").right()
        drawing += elm.MeterA(label="A").right()
        drawing += elm.Line().down()
        drawing += elm.Line().left()
        drawing += elm.SourceV().left().label(r'$\xi, r$')
        drawing += elm.Line().up()

        drawing.save(
            fname=os.path.join(get_static_folder(), "pic70.svg"), 
            transparent=False
        )

def draw_pic_for_q72():
    T = 2.0
    plot = PlotCosine(
        amplitude=4.0,
        period=T,
        omega=2*np.pi/T,
        x_offset=np.pi / 3
    )
    plot.draw("t(s)", "x(cm)", os.path.join(get_static_folder(), "pic72.svg"))

if __name__ == "__main__":
    draw_pic_for_q70()
    draw_pic_for_q72()
