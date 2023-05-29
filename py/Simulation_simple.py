import numpy as np
import matplotlib.pyplot as plt                                                                                                                                                                                                                                            

c=1  #si c=1 == profile d'aile   /  si c=0 == cercle  /  entre 0 et 1  entre un cercle et un profil d aile
R_0=1.15   # rayon du cercle 
R_0_x,R_0_y=-0.15,0.15 # centre du cercle 

AoA=15*np.pi/180   # angle d'incidence 

OaO=-AoA          
                 #__figure1___#
n=200    #bombre de point pour tracer le cercle ou le profil d'ail
x=(np.linspace(-R_0+R_0_x,R_0+R_0_x,n))  #liste des point sur x
yu=np.sqrt(R_0**2-(x-R_0_x)**2)+R_0_y      #liste des point sur y+
yl=-np.sqrt(R_0**2-(x-R_0_x)**2)+R_0_y   #liste des point sur y-

zu=x+1j*yu              # equation complexe 
zl=x+1j*yl

Zu=(zu+c**2/zu)*(np.exp(1j*OaO))   #transformation de joukoski
Zl=(zl+c**2/zl)*(np.exp(1j*OaO))

                 #__figure2___#    creation des points d'evaluation pour les calules suivants
Nr=100       #nombre de point à placer 
radius=np.linspace(R_0,5,Nr)   # liste de x=1.15 a 5 avec Nr elements 
Ntheta=145                       #le nombre de divison du cercle 
theta=np.linspace(0,2*np.pi,Ntheta)     # liste des angles entre 0 et 2pi avec Ntheta angles dedans
Radius,Theta=np.meshgrid(radius,theta)  #changer la forme de la matrice pour ne pas avoir de probleme de dimension, matrice de meme taille 

X=(Radius*np.cos(Theta)+R_0_x)  #ensenble des point selon x
Y=(Radius*np.sin(Theta)+R_0_y)  #ensemble des point selon y

Z=X+1j*Y      #ecriture complexe
Zeta=(Z+c**2/Z)*(np.exp(1j*OaO))    # transformation de joukoski 

                 #__figure3___#    tracer les lignes de courant
k=529*np.pi/200 #force du doublet 
   
def get_stream_function_doublet(k,x_doublet,y_doublet,X,Y):  #fonction qui permet d'avoir le flux autour d'un doublet, element simulant un puit et une source
    psi=(-k/(2*np.pi))*((Y-y_doublet)/((X-x_doublet)**2+(Y-y_doublet)**2))
    return psi

U_unif=1   #flux a l'origine
 
Xa=(X-R_0_x)*np.cos(AoA)+(Y-R_0_y)*np.sin(AoA)     #on depalce le repere sur le centre du cercle qui subis la transformation de Joukosjy et on y applique l'angle d'attaque
Ya=-(X-R_0_x)*np.sin(AoA)+(Y-R_0_y)*np.cos(AoA)
         
Za=Xa+1j*Ya   #ecriture complexe

psi_airfoil_=get_stream_function_doublet(k,0,0, Za.real, Za.imag)  #obtenir les valeurs du flux en fonction du doublet en chaque point de l'espace defini dans le nouveau repere

psi_freestream_=U_unif*Ya #obtenir les valeurs du flux en chaque point de l'espace dans le champ uniforme


gamma=-Ya[0,0]*np.pi*4  #on modelise un vortex , en voici la norme
       
def get_stream_function_vortex(gamma,x_vortex,y_vortex,X,Y):  #fonction qui determine le flux de l'espace en fonction du vortex
    psi=(gamma/(4*np.pi))*np.log((X-x_vortex)**2+(Y-y_vortex)**2)
    return psi

psi_vortex=get_stream_function_vortex(gamma,0,0,Xa,Ya) #obtenir les valeurs du flux en chaque point de l'espace dans genere par le vortex

psi_tot_=psi_airfoil_+psi_freestream_+psi_vortex

#clacul du champ de pression
#champ de vecteur (u,v)
u_freestream=U_unif*np.ones((Ntheta,Nr),dtype=float) #matrice de 1 de la taille de l'espace etudie
v_freestream=U_unif*np.zeros((Ntheta,Nr),dtype=float) #matrice de 0 de la taille de l'espace etudie

def get_velovity_double(k,x_doublet,y_doublet,X,Y):  #fonction qui donne le champ de vitesse en fonction du doublet
    u=(-k/(2*np.pi))*(((X-x_doublet)**2-(Y-y_doublet)**2)/(((X-x_doublet)**2+(Y-y_doublet)**2)**2))
    v=(-k/(2*np.pi))*((2*(X-x_doublet)*(Y-y_doublet))/(((X-x_doublet)**2+(Y-y_doublet)**2)**2))
    return u,v

u_doubleta, v_doubleta=get_velovity_double(k,0,0, Xa, Ya) #on obtient les valeurs du champ de vitesse dans l'espace, champ de vecteur donc deux composante(u,v) du doublet

def get_velocity_vortex(gamma,x_vortex,y_vortex,X,Y): #fonction qui donne le champ de vitesse en fonction du vortex
    u=(gamma/(2*np.pi))*((Y-y_vortex)/((X-x_vortex)**2+(Y-y_vortex)**2))
    v=-(gamma/(2*np.pi))*((X-x_vortex)/((X-x_vortex)**2+(Y-y_vortex)**2))
    return u,v              
                
u_vortex, v_vortex=get_velocity_vortex(gamma,0,0,Xa,Ya) #on obtient les valeurs du champ de vitesse dans l'espace, champ de vecteur donc deux composante(u,v) du vortex
U_tot_=u_doubleta+u_freestream+u_vortex
V_tot_=v_doubleta+v_freestream+v_vortex #valeur totale du champ vectorielle dans le plan decale sur le centre du cercle 

U_tota=U_tot_* np.cos(-AoA)+V_tot_*np.sin(-AoA) #on applique l'angle d'incidance 
V_tota=-U_tot_*np.sin(-AoA)+V_tot_* np.cos(-AoA)   

dZeta_div_dz_ = 1 - (c/Z)**2 #transformation de joukosky du champ de vitese
W_zeta_2 = (U_tota - V_tota * 1j) / dZeta_div_dz_  
U_zeta_ = W_zeta_2.real
V_zeta_ = -W_zeta_2.imag  


cp6=1-(U_zeta_**2+V_zeta_**2)/U_unif**2  #calcul du champ de pression

fig9, ax9 = plt.subplots(1,1,figsize=(15, 15))  #creation de la figure qui reçoit le plot
fig9.suptitle('airfoil', fontsize=22)   #titre et taille

ax9.set_xlim(-3.5,3.5)    #limite des axes sur x et sur y 
ax9.set_ylim(-3.5,3.5)


conf5=ax9.contourf(Zeta.real,Zeta.imag,cp6,levels=np.linspace(-1, 1, 500), extend='both',cmap='cool')  #afficher le champ de pression
ax9.plot(Zu.real,Zu.imag,color='#CD2305'), ax9.plot(Zl.real,Zl.imag,color='#CD2305')  #tracer le profil d'aile
ax9.contour(Zeta.real,Zeta.imag,psi_tot_,60,colors='black', linewidths=2, linestyles='solid')  #tracer les lignes de courant
ax9.axis('equal')

    


    