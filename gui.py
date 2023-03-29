from threading import Timer
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib as mpl
from tinyec import registry
import secrets
import tkinter as tk
from exchange import *

t = np.arange(-5, 5, .01)

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

def draw_eliptic_disc(A,B,ax,figure,mod):
    x = np.arange(0, mod, 1)
    y = calc_eliptic(A,B,x)%mod
    y = np.sqrt(y)
    valid_x = np.where(y == y.round())
    y1 = y[valid_x]
    y2 = (-y1)%mod

    ax.scatter(valid_x, y1)
    ax.scatter(valid_x, y2)
    figure.draw()

def calc_slope(x,y,A):
    return (3*(x**2)+A)/(2*y)

def calc_slope_disc(x,y,A,mod):
    return ((3*(x**2)+A) * pow(2*y,-1,mod))%mod

def calc_tengeant(x,A,B,inv = 1):
    y = inv * calc_eliptic(A,B,x)**(1/2)
    a = calc_slope(x,y,A)
    b = y - a*x
    return a*t+b

def draw_tengeant(x,A,B,ax,figure, inv = 1):
    tengeant = calc_tengeant(x,A,B, inv)
    ax.plot(t, tengeant)
    figure.draw()

def draw_tengeant_disc(x,A,B,ax,figure,mod):
    y = calc_eliptic(A,B,x)%mod
    # slope = calc_slope_disc(x,A,B,mod)
    slope = calc_slope(x,A,B)
    print(calc_slope_disc(x,A,B,mod))
    print(calc_slope(x,A,B))
    height = y - x*slope
    tengeant = (slope * t + height) % mod
    ax.plot(t, tengeant)
    figure.draw()


# Define the window layout
layout = [
    [[
        [sg.Image('ce.png', expand_x=True, expand_y=True )],
        [sg.Text('A'), sg.Input('1', enable_events=True,  key='A',  size=(20, 1)),
         sg.Text('B'), sg.Input('1', enable_events=True,  key='B',  size=(20, 1)),
         sg.Text('mod'), sg.Input('13', enable_events=True,  key='mod',  size=(20, 1)),
         sg.Text('x1'), sg.Input('1', enable_events=True,  key='x1',  size=(20, 1)),
         sg.Text('x2'), sg.Input('2', enable_events=True,  key='x2',  size=(20, 1))],
        [sg.Canvas(key="-CONT-"),
         sg.Canvas(key="-DISC-")],
        [sg.Text('Message'), sg.Input('Salut salut!', enable_events=True,  key='Message')],
    ],
    [
        [sg.Canvas(key="-ARROWS-",size=(700,300), background_color='grey')],
    ]],
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
draw_eliptic_disc(1,1,ax_disc,fig_disc_agg,13)
draw_tengeant(1,1,1,ax_cont,fig_cont_agg)
draw_tengeant(2,1,1,ax_cont,fig_cont_agg)



def drawArrows(message):
    curve = registry.get_curve('brainpoolP256r1')
    canvas_graph_elem = window['-ARROWS-']
    tkc = canvas_graph_elem.TKCanvas

    #cleaning
    tkc.delete("all")

    tkc.create_line(100, 20, 100, 280, fill='red', width=1, arrow=tk.LAST)
    tkc.create_line(600, 20, 600, 280, fill='blue', width=1, arrow=tk.LAST)
    tkc.create_text(100, 20, text="Alice",fill='white', font=('Arial Bold', 10))
    tkc.create_text(600, 20, text="Bob",fill='white', font=('Arial Bold', 10))

    a_private = secrets.randbelow(curve.field.n)
    tkc.create_text(120, 40, text="Private key : " + hex(a_private)[-24:],fill='white', font=('Arial Bold', 8))
    a_public = a_private * curve.g
    tkc.create_text(120, 60, text="Public key : " + compress(a_public)[-24:],fill='white', font=('Arial Bold', 8))

    b_private = secrets.randbelow(curve.field.n)
    tkc.create_text(580, 40, text="Private key : " + hex(b_private)[-24:],fill='white', font=('Arial Bold', 8))
    b_public = b_private * curve.g
    tkc.create_text(580, 60, text="Public key : " + compress(b_public)[-24:],fill='white', font=('Arial Bold', 8))

    tkc.create_line(100, 100, 600, 100, fill='black', width=1, arrow=tk.LAST)
    tkc.create_text(350, 100, text="Alice sending public key" ,fill='white', font=('Arial Bold', 8))
    tkc.create_line(600, 120, 100, 120, fill='black', width=1, arrow=tk.LAST)
    tkc.create_text(350, 120, text="Bob sending public key" ,fill='white', font=('Arial Bold', 8))

    a_shared = a_private * b_public
    tkc.create_text(120, 140, text="Shared secret :" + compress(a_shared)[-24:],fill='white', font=('Arial Bold', 8))
    a_key = derivateKey(a_shared.x, a_shared.y)
    tkc.create_text(120, 160, text="Derived key :" + a_key.hex()[-24:],fill='white', font=('Arial Bold', 8))


    b_shared = b_private * a_public
    tkc.create_text(580, 140, text="Shared secret :" + compress(b_shared)[-24:],fill='white', font=('Arial Bold', 8))
    b_key = derivateKey(b_shared.x, b_shared.y)
    tkc.create_text(580, 160, text="Derived key :" + b_key.hex()[-24:],fill='white', font=('Arial Bold', 8))

    enc_m = encrypt(message, a_key)
    tkc.create_text(120, 200, text="Encrypt message :\nclear : " + message + "\nencrypted :" + enc_m.hex()[-24:],fill='white', font=('Arial Bold', 8))

    tkc.create_line(100, 240, 600, 240, fill='black', width=1, arrow=tk.LAST)
    tkc.create_text(350, 240, text="Alice sending encrypted message" ,fill='white', font=('Arial Bold', 8))

    dec_m = decrypt(enc_m, b_key)
    tkc.create_text(580, 260, text="Decrypt message :\nencrypted : " + enc_m.hex()[-24:] + "\ndecrypted :" + dec_m.decode(),fill='white', font=('Arial Bold', 8))



last_message = "Salut salut!"
timer = Timer(0.5, drawArrows, [last_message])
timer.start()

while True:             # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    new_message = values['Message']
    if not new_message == last_message:
        last_message = new_message
        timer.cancel()
        timer = Timer(1.0, drawArrows, [last_message])
        timer.start()

    ## clean plot
    ax_cont.cla()
    ax_cont.grid(True)
    ax_disc.cla()
    ax_disc.grid(True)

    try:
        A = int(values['A'])
        B = int(values['B'])
        mod = int(values['mod'])
        print("plot eliptic")
        draw_eliptic_cont(A,B,ax_cont,fig_cont_agg)
        draw_eliptic_disc(A,B,ax_disc,fig_disc_agg,mod)

        print("plot tengeant 1 with x1="+values['x1'])
        x1 = int(values['x1'])
        draw_tengeant(x1,A,B,ax_cont,fig_cont_agg)
        # draw_tengeant_disc(x1,A,B,ax_disc,fig_disc_agg,mod)

        print("plot tengeant 2 with x2="+values['x2'])
        x2 = int(values['x2'])
        draw_tengeant(x2,A,B,ax_cont,fig_cont_agg)


    except Exception as e:
        print(e)


window.close()
