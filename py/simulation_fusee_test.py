"""
Ce programme permet d'afficher en 3D ou en 2D la simulation souhaitée.

Cette simulation prend en compte :
    - Masse volumique de l'air en fonction de l'altitude jusqu'à  640 km sur Terre
    - Intensité de gravitation en fonction de l'altitude sur Terre
    - Frottements turbulents, laminaires, aucun.

Méthode numérique : Euler
Codé par : Yoann HOARAU & Chloé MEYNAUD
"""


import numpy as np
from numpy import sin, cos, tan, arccos, pi, sqrt, radians
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d



    

def force_vent(vent, r, theta, phi=0):
    f, a, b, alpha, beta = vent[0], min(vent[1]), max(vent[1]), radians(vent[2][0]), radians(vent[2][1])
    if 6371e3 + a <= r <= 6371e3 + b:
        c = .5 * .47 * rho(r) * S * f
        x = c * cos(alpha) * cos(phi) * (sin(beta) * cos(theta) - cos(beta) * tan(phi) + sin(alpha) * sin(theta))
        y = c * S * f * (cos(alpha) * (cos(beta) * cos(phi) + sin(beta) * cos(theta) * sin(phi)) + sin(alpha) * sin(theta) * sin(phi))
        z = c * (-cos(alpha) * sin(beta) * sin(theta) + sin(alpha) * cos(theta))
        return x, y, z,
    else:
        return 0,0,0,


def acc_x(g, theta, phi, p, k, v_x):
    
    if frottement == "Sans" or r[-1] > 6371e3 + 640e3:
        return -g * sin(theta) * cos(phi)
    
    if frottement == "Turbulent":
        return g * sin(theta) * cos(phi) * p - k * v_x + force_vent(vent, r[-1], theta, phi=phi)[0] / M
    
    if frottement == "Laminaire":
        return g * sin(theta) * cos(phi) * p - q * rho(h) / (2 * M) * v_x + force_vent(vent, r[-1], theta, phi=phi)[0] / M



def acc_y(g, theta, phi, p, k, v_y):
    
    if frottement == "Sans" or r[-1] > 6371e3 + 640e3:
        return -g * sin(theta) * sin(phi)
    
    if frottement == "Turbulent":
        return g * sin(theta) * sin(phi) * p - k * v_y + force_vent(vent, r[-1], theta, phi=phi)[1] / M
    
    if frottement == "Laminaire":
        return g * sin(theta) * sin(phi) * p - q * rho(h) / (2 * M) * v_y + force_vent(vent, r[-1], theta, phi=phi)[1] / M


def acc_z(g, theta, p, k, v_z):
    
    if frottement == "Sans" or r[-1] > 6371e3 + 640e3:
        return -g * cos(theta)
    
    if frottement == "Turbulent":
        return g * cos(theta) * p - k * v_z + force_vent(vent, r[-1], theta)[2] / M
    
    if frottement == "Laminaire":
        return g * cos(theta) * p - q * rho(h) / (2 * M) * v_z + force_vent(vent, r[-1], theta, phi=phi)[2] / M


def g(h):
    return (6.6742e-11 * 5.972e24) / h**2




def rho(h):
    
    def temperature_air(h):
        h = (h - 6371e3) / 1000  # altitude par rapport au sol
        if h <= 11:
            return 15 - 6.5 * h + 273.15
        if 11 < h <= 20:
            return -56.5 + 273.15
        if 20 < h <= 32:
            return -56.5 + (h - 20) + 273.15
        if 32 < h <= 47:
            return -44.5 + 2.8 * (h - 32) + 273.15
        if 47 < h <= 51:
            return -2.5 + 273.15
        if 51 < h <= 71:
            return -2.5 - 2.8 * (h - 51) + 273.15
        if 71 < h <= 86:
            return -58.5 - 2 * (h - 71) + 273.15
        if 86 < h <= 100:
            return -88.5 + 2.5 * (h - 86) + 273.15
        else:
            return 573.15

    def pression_air(h):
        h -= 6371e3
        if  h <= 40e3:
            return 101325 * (1 - (0.0065 * h) / 290.15)**5.255
        elif 40e3 < h <= 60e3:
            return 25
        elif 60e3 < h <= 100e3:
            return 1e-2
        elif 100e3 < h <= 200e3:
            return 1.3e-4
        elif 200e3 < h <= 300e3:
            return 2e-5
        elif 300e3 < h <= 400e3:
            return 4.4e-6
        elif 400e3 < h <= 500e3:
            return 1.1e-8
        elif 500e3 < h <= 640e3:
            return 1e-10
        else:
            return 0
    return (pression_air(h) * 29e-3) / (8.3144621 * temperature_air(h))


#  Initialisation
frottement = "Turbulent"
dt = 1

S = pi * (.075/2)**2
V = 4/3 * pi * (.075/2)**3
q = .47 * S

vent = (0, (0, 400000), (0, 0))  # (vitesse, (inf, sup), (inclinaison+, orientation->S))
M = 11e3
alpha = [radians(0)]  # inclinaison
beta = [radians(0)]  # orientation
phi = [radians(75)]  # Longitude
theta = [radians(90)]  # Latitude
r = [6371e3 + 150e3]
v = [8500]

v_x = [v[0] * cos(alpha[0]) * cos(phi[0]) * (-cos(beta[0]) * tan(phi[0]) + sin(beta[0]) * cos(theta[0]) + sin(alpha[0]) * sin(theta[0]))]
v_y = [v[0] * (cos(alpha[0]) * (cos(beta[0]) * cos(phi[0]) + sin(beta[0]) * cos(theta[0]) * sin(phi[0])) + sin(alpha[0]) * sin(theta[0]) * sin(phi[0]))]
v_z = [v[0] * (-cos(alpha[0]) * sin(beta[0]) * sin(theta[0]) + sin(alpha[0]) * cos(theta[0]))]
X = [r[0] * sin(theta[0]) * cos(phi[0])]
Y = [r[0] * sin(theta[0]) * sin(phi[0])]
Z = [r[0] * cos(theta[0])]

temps = 0
time = [0]

# Méthode numérique d'Euler
while r[-1] >= 6371e3 and temps < 19030:
    temps += 1
    time.append(temps * dt)
    h = r[-1]
    p = rho(h) * V - 1
    k = q * rho(h) * v[-1] / (2 * M)
    v_x.append(acc_x(g(h), theta[-1], phi[-1], p, k, v_x[-1]) * dt + v_x[-1])
    v_y.append(acc_y(g(h), theta[-1], phi[-1], p, k, v_y[-1]) * dt + v_y[-1])
    v_z.append(acc_z(g(h), theta[-1], p, k, v_z[-1]) * dt + v_z[-1])
    
    X.append(v_x[-1] * dt + X[-1])
    Y.append(v_y[-1] * dt + Y[-1])
    Z.append(v_z[-1] * dt + Z[-1])
    r.append(sqrt(X[-1]**2 + Y[-1]**2 + Z[-1]**2))
    
    
    phi.append(arccos(X[-1] / (sqrt( X[-1]**2 + Y[-1]**2)))) if Y[-1] >= 0 else phi.append(2*pi - arccos(X[-1] / (sqrt( X[-1]**2 + Y[-1]**2))))
    theta.append(arccos(Z[-1] / r[-1]))
    v.append(sqrt(v_x[-1]**2 + v_y[-1]**2 + v_z[-1]**2))
    



plot = "2D"


if plot == "3D":
    fig = plt.figure(figsize=(16/1.5, 9/1.5))
    ax = fig.add_subplot(projection='3d')
    
    u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
    x = np.cos(u) * np.sin(v) * 6371e3
    y = np.sin(u) * np.sin(v) * 6371e3
    z = np.cos(v) * 6371e3
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
    
    theta = np.linspace(0, 2 * np.pi, 201)
    y = 6371e3*np.cos(theta)
    z = 6371e3*np.sin(theta)

    ax.plot(y, z, '--k', lw=.4, zorder=3)
    
    ax.plot(X, Y, Z, 'r', label='Courbe', lw=2, zorder=10)  # TracÃ© de la courbe 3D
    plt.title("Orbite géostationnaire")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.tight_layout()
    

    

    
elif plot == "2D":
    plt.figure(figsize=(12,9))
    axes = plt.subplot()
    draw_Terre = plt.Circle((0,0), 6371e3)
    axes.add_artist(draw_Terre)
    axes.set_aspect(1)
    plt.xlim()
    plt.ylim()
    
    axes.plot(X, Y, 'r', lw=1, label='Trajectoire')
    plt.xlabel('mètres')
    plt.ylabel('mètres')
    plt.title("Orbite d'un satellite de communication autour de la Terre")
    #plt.grid()
    #plt.legend()
    

#  https://datatofish.com/matplotlib-charts-tkinter-gui/