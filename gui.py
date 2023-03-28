import math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib as mpl


# fig = plt.figure(figsize=(5, 4), dpi=100)
t = np.arange(-5, 5, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))


mpl.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def calc_eliptic(A,B,x):
    return x**3 + A*x + B

def draw_eliptic_cont(A,B,ax,figure):
    y, x = np.ogrid[-10:10:100j, -10:10:100j]
    ax.contour(x.ravel(), y.ravel(), pow(y, 2) - calc_eliptic(A,B,x), [0])
    figure.draw()

def draw_eliptic_disc(A,B,ax,figure):
    mod = 5
    x = np.arange(0, mod, 1)
    y = calc_eliptic(A,B,x)%mod
    y = np.sqrt(y)
    valid_x = np.where(y == y.round())
    y1 = y[valid_x]
    y2 = (-y1)%mod

    ax.scatter(valid_x, y1)
    ax.scatter(valid_x, y2)
    figure.draw()

def calc_tengeant(x,A,B,inv = 1):
    y = inv * calc_eliptic(A,B,x)**(1/2)
    a = (3*(x**2)+A)/(2*y)
    b = y - a*x
    return a*t+b

def calc_tengeant_crossing(x,A,B):
    
    el = (x**3 + A*x + B)**(1/2)
    tan = a*x + b



    x3 = calc_eliptic(A,B,x)
    a = (3*(x**2)+A)/(2*y)
    b = y - a*x
    return a*t+b

def draw_tengeant(x,A,B,ax,figure, inv = 1):
    tengeant = calc_tengeant(x,A,B, inv)
    ax.plot(t, tengeant)
    figure.draw()


# Define the window layout
layout = [
    [sg.Image('ce.png',
   expand_x=True, expand_y=True )],
    [sg.Text('A'), sg.Input('', enable_events=True,  key='A')],
    [sg.Text('B'), sg.Input('', enable_events=True,  key='B')],
    [sg.Canvas(key="-CONT-"),sg.Canvas(key="-DISC-")],
    [sg.Text('x1'), sg.Input('', enable_events=True,  key='x1')],
    [sg.Text('x2'), sg.Input('', enable_events=True,  key='x2')],
    [sg.Button('Exit')]
]

# Create the form and show it without the plot
window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

# # Add the plot to the window
# dh_graph = draw_figure(window["-CANVAS-"].TKCanvas, fig)
canvas_cont_elem = window['-CONT-']
canvas_cont = canvas_cont_elem.TKCanvas
fig_cont, ax_cont = plt.subplots()
ax_cont.grid(True)
fig_cont_agg = draw_figure(canvas_cont, fig_cont)

canvas_disc_elem = window['-DISC-']
canvas_disc = canvas_disc_elem.TKCanvas
fig_disc, ax_disc = plt.subplots()
ax_disc.grid(True)
fig_disc_agg = draw_figure(canvas_disc, fig_disc)

draw_eliptic_cont(1,1,ax_cont,fig_cont_agg)
draw_eliptic_disc(1,1,ax_disc,fig_disc_agg)

event, values = window.read()

while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break


    # # if last char entered not a digit
    # if event == 'A' and len(values['A']) and values['A'][-1] not in ('0123456789'):
    #     # delete last char from input
    #     window['A'].update(values['A'][:-1])
    # if event == 'B' and len(values['B']) and values['B'][-1] not in ('0123456789'):
    #     # delete last char from input
    #     window['B'].update(values['B'][:-1])

    ## clean plot
    ax_cont.cla()
    ax_cont.grid(True)

    try:
        A = int(values['A'])
        B = int(values['B'])
        draw_eliptic_cont(A,B,ax_cont,fig_cont_agg)
        draw_eliptic_disc(A,B,ax_disc,fig_disc_agg)

        x1 = int(values['x1'])
        draw_tengeant(x1,A,B,ax_cont,fig_cont_agg, 1)

        x2 = int(values['x2'])
        draw_tengeant(x2,A,B,ax_cont,fig_cont_agg, -1)


    except:
        print("Values cannot be parsed in int")


window.close()
