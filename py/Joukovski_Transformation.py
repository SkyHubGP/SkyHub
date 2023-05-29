import numpy as np
import matplotlib.pyplot as plt 


c=1
R_0=1.15
R_0_x,R_0_y=-0.15,0
                 #__figure1___#
n=200
x=np.linspace(-R_0+R_0_x,R_0+R_0_x,n)
yu=np.sqrt(R_0**2-(x-R_0_x)**2)+R_0_y    
yl=-np.sqrt(R_0**2-(x-R_0_x)**2)+R_0_y   

zu=x+1j*yu
zl=x+1j*yl

Zu=zu+c**2/zu
Zl=zl+c**2/zl

                 #__figure2___#
Nr=100
radius=np.linspace(R_0,5,Nr)
Ntheta=145
theta=np.linspace(0,2*np.pi,Ntheta)
Radius,Theta=np.meshgrid(radius,theta) 

X=Radius*np.cos(Theta)+R_0_x
Y=Radius*np.sin(Theta)+R_0_y

Z=X+1j*Y
Zeta=Z+c**2/Z

                 #__figure3___#
k=529*np.pi/200 #force du doublet pour un rayon de 1.15
 
def get_stream_function_doublet(k,x_doublet,y_doublet,X,Y):
    psi=(-k/(2*np.pi))*((Y-y_doublet)/((X-x_doublet)**2+(Y-y_doublet)**2))
    return psi

U_unif=1 
  
psi_circle=get_stream_function_doublet(k,R_0_x,R_0_y, X, Y)
psi_airfoil=get_stream_function_doublet(k,R_0_x,R_0_y, Z.real, Z.imag)

psi_freestream=U_unif*Y

psi_tot1=psi_circle+psi_freestream
psi_tot2=psi_airfoil+psi_freestream

                 #__figure4___#                 
U_unif=1
u_freestream=U_unif*np.ones((Ntheta,Nr),dtype=float)
v_freestream=U_unif*np.zeros((Ntheta,Nr),dtype=float)

def get_velovity_double(k,x_doublet,y_doublet,X,Y):
    u=(-k/(2*np.pi))*(((X-x_doublet)**2-(Y-y_doublet)**2)/(((X-x_doublet)**2+(Y-y_doublet)**2)**2))
    v=(-k/(2*np.pi))*((2*(X-x_doublet)*(Y-y_doublet))/(((X-x_doublet)**2+(Y-y_doublet)**2)**2))
    return u,v
          
u_doublet, v_doublet=get_velovity_double(k,R_0_x,R_0_y, X, Y)

u_tot=u_doublet+u_freestream
v_tot=v_doublet+v_freestream

dZeta_div_dz = 1 - (c/Z)**2
W_zeta = (u_tot - v_tot * 1j) / dZeta_div_dz
u_zeta = W_zeta.real
v_zeta = -W_zeta.imag

                 #__figure5__#
            
cp1=1-(u_tot**2+v_tot**2)/U_unif**2
cp2=1-(u_zeta**2+v_zeta**2)/U_unif**2

                 #__figure6___#
AoA=20*np.pi/180

Xa=(X-R_0_x)*np.cos(AoA)+(Y-R_0_y)*np.sin(AoA)
Ya=-(X-R_0_x)*np.sin(AoA)+(Y-R_0_y)*np.cos(AoA)
         
Za=Xa+1j*Ya
Zeta_=Za+c**2/Za

psi_circle_=get_stream_function_doublet(k,0,0, Xa, Ya)
psi_airfoil_=get_stream_function_doublet(k,0,0, Za.real, Za.imag)

psi_freestream_=U_unif*Ya

psi_tot1_=psi_circle_+psi_freestream_
psi_tot2_=psi_airfoil_+psi_freestream_

                 #__figure7___#
u_doubleta, v_doubleta=get_velovity_double(k,0,0, Xa, Ya)

u_tot_=u_doubleta+u_freestream
v_tot_=v_doubleta+v_freestream  

u_tota=u_tot_* np.cos(-AoA)+v_tot_*np.sin(-AoA)
v_tota=-u_tot_*np.sin(-AoA)+v_tot_* np.cos(-AoA)   

dZeta_div_dz_ = 1 - (c/Z)**2
W_zeta_ = (u_tota - v_tota * 1j) / dZeta_div_dz_
u_zeta_ = W_zeta_.real
v_zeta_ = -W_zeta_.imag         
                 
                 #__figure8___#
cp3=1-(u_tota**2+v_tota**2)/U_unif**2
cp4=1-(u_zeta_**2+v_zeta_**2)/U_unif**2

                #__figure9__#

gamma=-Ya[0,0]*np.pi*4  
       
def get_stream_function_vortex(gamma,x_vortex,y_vortex,X,Y):
    psi=(gamma/(4*np.pi))*np.log((X-x_vortex)**2+(Y-y_vortex)**2)
    return psi

psi_vortex=get_stream_function_vortex(gamma,0,0,Xa,Ya)

psi_tot11_=psi_circle_+psi_freestream_+psi_vortex
psi_tot22_=psi_airfoil_+psi_freestream_+psi_vortex 
        
                #__figure10__#
def get_velocity_vortex(gamma,x_vortex,y_vortex,X,Y):
    u=(gamma/(2*np.pi))*((Y-y_vortex)/((X-x_vortex)**2+(Y-y_vortex)**2))
    v=-(gamma/(2*np.pi))*((X-x_vortex)/((X-x_vortex)**2+(Y-y_vortex)**2))
    return u,v              
                
u_vortex, v_vortex=get_velocity_vortex(gamma,0,0,Xa,Ya)
U_tot_=u_doubleta+u_freestream+u_vortex
V_tot_=v_doubleta+v_freestream+v_vortex 

U_tota=U_tot_* np.cos(-AoA)+V_tot_*np.sin(-AoA)
V_tota=-U_tot_*np.sin(-AoA)+V_tot_* np.cos(-AoA)   

dZeta_div_dz_ = 1 - (c/Z)**2
W_zeta_2 = (U_tota - V_tota * 1j) / dZeta_div_dz_
U_zeta_ = W_zeta_2.real
V_zeta_ = -W_zeta_2.imag  

                 #__figure11___#
cp5=1-(U_tota**2+V_tota**2)/U_unif**2
cp6=1-(U_zeta_**2+V_zeta_**2)/U_unif**2                
              
"""               
                  #___plot___#
#figure1#
fig1, ax1 = plt.subplots(1,2,figsize=(20, 10))
fig1.suptitle('figure1', fontsize=22)

ax1[0].plot(R_0_x,R_0_y,"ro")
ax1[0].plot(x, yu), ax1[0].plot(x, yl)
ax1[0].axis('equal'), ax1[0].grid(True)

ax1[1].plot(R_0_x,R_0_y,"ro")
ax1[1].plot(Zu.real,Zu.imag), ax1[1].plot(Zl.real,Zl.imag)
ax1[1].axis('equal'), ax1[1].grid(True)
#figure2#
fig2, ax2 = plt.subplots(1,2,figsize=(20, 10))
fig2.suptitle('figure2', fontsize=22)

ax2[0].plot(R_0_x,R_0_y,"ro")
ax2[0].scatter(X,Y,s=5,marker="o")
ax2[0].axis('equal'), ax2[0].grid(True)

ax2[1].plot(R_0_x,R_0_y,"ro")
ax2[1].scatter(Zeta.real,Zeta.imag,s=5,marker="o")
ax2[1].axis('equal'), ax2[1].grid(True)
#figure3#
fig3, ax3 = plt.subplots(1,2,figsize=(20, 10))
fig3.suptitle('figure3', fontsize=22)

ax3[0].plot(R_0_x,R_0_y,"ro")
ax3[0].contour(X,Y,psi_tot1,50,colors='black', linewidths=2, linestyles='solid')
ax3[0].plot(x, yu,color='#CD2305',lw=3), ax3[0].plot(x, yl,color='#CD2305',lw=3)
ax3[0].axis('equal'), ax3[0].grid(True)

ax3[1].plot(R_0_x,R_0_y,"ro")
ax3[1].contour(Zeta.real,Zeta.imag,psi_tot2,50,colors='black', linewidths=2, linestyles='solid')
ax3[1].plot(Zu.real,Zu.imag,lw=3,color='#CD2305'), ax3[1].plot(Zl.real,Zl.imag,lw=3,color='#CD2305')
ax3[1].axis('equal'), ax3[1].grid(True)
#figure4#
fig4, ax4 = plt.subplots(1,2,figsize=(20, 10))
fig4.suptitle('figure4', fontsize=22)

ax4[0].set_xlim(-1.5,1.5)
ax4[0].set_ylim(-1.5,1.5)
ax4[0].quiver(X,Y,u_tot,v_tot,scale=30)
ax4[0].plot(x, yu,color='#CD2305'), ax4[0].plot(x, yl,color='#CD2305')

ax4[1].set_xlim(-2.5,2.5)
ax4[1].set_ylim(-2.5,2.5)
ax4[1].quiver(Zeta.real,Zeta.imag,u_zeta,v_zeta,scale=60)
ax4[1].plot(Zu.real,Zu.imag,color='#CD2305'), ax4[1].plot(Zl.real,Zl.imag,color='#CD2305')
#figure5#
fig5, ax5 = plt.subplots(1,2,figsize=(20, 10))
fig5.suptitle('figure5', fontsize=22)

conf1=ax5[0].contourf(X,Y,cp1,levels=np.linspace(-1, 1, 500), extend='both')
ax5[0].plot(x, yu,color='#CD2305'), ax5[0].plot(x, yl,color='#CD2305')

conf2=ax5[1].contourf(Zeta.real,Zeta.imag,cp2,levels=np.linspace(-1, 1, 500), extend='both')
ax5[1].plot(Zu.real,Zu.imag,color='#CD2305'), ax5[1].plot(Zl.real,Zl.imag,color='#CD2305')

#cbar1=plt.colorbar(conf1)
#cbar1.set_label('$Cp$',fontsize=20)
#figure6#
fig6, ax6 = plt.subplots(1,2,figsize=(20, 10))
fig6.suptitle('figure6', fontsize=22)

ax6[0].plot(R_0_x,R_0_y,"ro")
ax6[0].contour(X,Y,psi_tot1_,50,colors='black', linewidths=2, linestyles='solid')
ax6[0].plot(x, yu,color='#CD2305',lw=2), ax6[0].plot(x, yl,color='#CD2305',lw=2)
ax6[0].axis('equal'), ax6[0].grid(True)

ax6[1].plot(R_0_x,R_0_y,"ro")
ax6[1].contour(Zeta.real,Zeta.imag,psi_tot2_,50,colors='black', linewidths=2, linestyles='solid')
ax6[1].plot(Zu.real,Zu.imag,lw=2,color='#CD2305'), ax6[1].plot(Zl.real,Zl.imag,lw=2,color='#CD2305')
ax6[1].axis('equal'), ax6[1].grid(True)
#figure7#
fig7, ax7 = plt.subplots(1,2,figsize=(20, 10))
fig7.suptitle('figure7', fontsize=22)

ax7[0].set_xlim(-2,2)
ax7[0].set_ylim(-2,2)
ax7[0].quiver(X,Y,u_tota,v_tota,scale=60)
ax7[0].plot(x, yu,color='#CD2305'), ax7[0].plot(x, yl,color='#CD2305')

ax7[1].set_xlim(-2.5,2.5)
ax7[1].set_ylim(-2.5,2.5)
ax7[1].quiver(Zeta.real,Zeta.imag,u_zeta_,v_zeta_,scale=60)
ax7[1].plot(Zu.real,Zu.imag,color='#CD2305'), ax7[1].plot(Zl.real,Zl.imag,color='#CD2305')
#figure8#
fig8, ax8 = plt.subplots(1,2,figsize=(20, 10))
fig8.suptitle('figure8', fontsize=22)

conf3=ax8[0].contourf(X,Y,cp3,levels=np.linspace(-1, 1, 500), extend='both')
ax8[0].plot(x, yu,color='#CD2305'), ax8[0].plot(x, yl,color='#CD2305')

conf4=ax8[1].contourf(Zeta.real,Zeta.imag,cp4,levels=np.linspace(-1, 1, 500), extend='both')
ax8[1].plot(Zu.real,Zu.imag,color='#CD2305'), ax8[1].plot(Zl.real,Zl.imag,color='#CD2305')

#cbar2=plt.colorbar(conf3)
#cbar2.set_label('$Cp$',fontsize=20)
"""
#figure9#
fig9, ax9 = plt.subplots(1,2,figsize=(20, 10))
fig9.suptitle('figure9', fontsize=22)

ax9[0].plot(R_0_x,R_0_y,"ro")
ax9[0].contour(X,Y,psi_tot11_,50,colors='black', linewidths=2, linestyles='solid')
ax9[0].plot(x, yu,color='#CD2305',lw=2), ax9[0].plot(x, yl,color='#CD2305',lw=2)
ax9[0].axis('equal'), ax9[0].grid(True)

ax9[1].plot(R_0_x,R_0_y,"ro")
ax9[1].contour(Zeta.real,Zeta.imag,psi_tot22_,50,colors='black', linewidths=2, linestyles='solid')
ax9[1].plot(Zu.real,Zu.imag,lw=2,color='#CD2305'), ax9[1].plot(Zl.real,Zl.imag,lw=2,color='#CD2305')
ax9[1].axis('equal'), ax9[1].grid(True)

#figure10#
fig10, ax10 = plt.subplots(1,2,figsize=(20, 10))
fig10.suptitle('figure10', fontsize=22)

ax10[0].set_xlim(-2,2)
ax10[0].set_ylim(-2,2)
ax10[0].quiver(X,Y,U_tota,V_tota,scale=60)
ax10[0].plot(x, yu,color='#CD2305'), ax10[0].plot(x, yl,color='#CD2305')

ax10[1].set_xlim(-2.5,2.5)
ax10[1].set_ylim(-2.5,2.5)
ax10[1].quiver(Zeta.real,Zeta.imag,U_zeta_,V_zeta_,scale=60)
ax10[1].plot(Zu.real,Zu.imag,color='#CD2305'), ax10[1].plot(Zl.real,Zl.imag,color='#CD2305')

#figure11#
fig11, ax11 = plt.subplots(1,2,figsize=(20, 10))
fig11.suptitle('figure11', fontsize=22)

ax11[0].set_xlim(-3,3)
ax11[0].set_ylim(-3,3)
conf5=ax11[0].contourf(X,Y,cp5,levels=np.linspace(-1, 1, 500), extend='both')
ax11[0].plot(x, yu,color='#CD2305'), ax11[0].plot(x, yl,color='#CD2305')

ax11[1].set_xlim(-3.5,3.5)
ax11[1].set_ylim(-3.5,3.5)
conf6=ax11[1].contourf(Zeta.real,Zeta.imag,cp6,levels=np.linspace(-1, 1, 500), extend='both')
ax11[1].plot(Zu.real,Zu.imag,color='#CD2305'), ax11[1].plot(Zl.real,Zl.imag,color='#CD2305')

#cbar3=plt.colorbar(conf5)
#cbar3.set_label('$Cp$',fontsize=20)
