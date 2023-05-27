import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
window=Tk()


#Création de la figure matplot lib 
fig = Figure(figsize = (5,5), dpi=100)
ax=fig.add_subplot(111)
#Intégration dans TKINTER
canvas = FigureCanvasTkAgg(fig, master = window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()





angle_d_attaque = IntVar()

def test(a=10):
    # entry= Entry(window, bd=5, bg='red')



    # recup=entry.get()
    # if recup.isdigit():
    #     angle_d_attaque=int(recup)
    
    # entry.pack(side=BOTTOM)

    resolution = 100
    
    alpha = angle_d_attaque.get() * 2*np.pi/360 #.get() pour transformer IntVar() en valeur
    b= 1.1             # a mieux comprendre
    v_infini = 1        # vitesse des particules entrantes
    centre_x = -0.1
    centre_y = 0.1
    rayon = np.linspace(b,4*b,resolution)          # array < liste rayon 1 à 4 pour b = 1  # pas bien compris
    angle = np.linspace(0,2*np.pi,resolution)      # array < la liste angle 0 à 2*pi
    RAYON, ANGLE = np.meshgrid(rayon,angle) # sparse=True ???? matrices à partir de la liste rayon et de la liste angle
    Xi  = centre_x + RAYON * np.cos(ANGLE)
    Eta = centre_y + RAYON * np.sin(ANGLE)
    Zeta = Xi + 1j*Eta
    potentiel = np.imag(v_infini*(np.exp(-1j*alpha)*Zeta + np.divide(np.exp(1j*alpha)*b**2,Zeta) + 2*np.sin(alpha)*b*1j*np.log(Zeta/b)))
    Zeta = Zeta + 1/Zeta
    x = np.real(Zeta)
    y = np.imag(Zeta)
    #plt.contourf(x,y,potentiel,30)
    ax.contourf(x,y,potentiel,30)
    canvas.draw()
    
# Création d'un widget Label
Label1 = Label(window, text = 'Lignes de courants', fg = 'red')
Label1.pack()

# Création d'un widget Button




toolbar = NavigationToolbar2Tk(canvas, window) 
toolbar.update() 


window.geometry("700x700")



scale = Scale(master=window,label="Angle d'attaque", orient=HORIZONTAL,  variable = angle_d_attaque, from_=-360, to=360 )
scale.pack()


plot_button = tk.Button(master = window ,height = 4, width = 20, text = "Affichage Joukowski", command = test) 
plot_button.pack(side= 'left') 


 # Lancement de la boucle infinie (gestionnaire d'événements)

window.mainloop()