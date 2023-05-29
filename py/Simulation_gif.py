import numpy as np
import matplotlib.pyplot as plt 

i=1
c=1
R_0=1.15
R_0_x,R_0_y=-0.15,0.10

AoA=-20*np.pi/180


while AoA<20*np.pi/180:
    OaO=-AoA
                     #__figure1___#
    n=200
    x=(np.linspace(-R_0+R_0_x,R_0+R_0_x,n))
    yu=np.sqrt(R_0**2-(x-R_0_x)**2)+R_0_y    
    yl=-np.sqrt(R_0**2-(x-R_0_x)**2)+R_0_y   
    
    zu=x+1j*yu
    zl=x+1j*yl
    
    Zu=(zu+c**2/zu)*(np.exp(1j*OaO))
    Zl=(zl+c**2/zl)*(np.exp(1j*OaO))
    
                     #__figure2___#
    Nr=100
    radius=np.linspace(R_0,5,Nr)
    Ntheta=145
    theta=np.linspace(0,2*np.pi,Ntheta)
    Radius,Theta=np.meshgrid(radius,theta) 
    
    X=(Radius*np.cos(Theta)+R_0_x)
    Y=(Radius*np.sin(Theta)+R_0_y)
    
    Z=X+1j*Y
    Zeta=(Z+c**2/Z)*(np.exp(1j*OaO))
    
                     #__figure3___#
    k=529*np.pi/200 #force du doublet 
   
    def get_stream_function_doublet(k,x_doublet,y_doublet,X,Y):
        psi=(-k/(2*np.pi))*((Y-y_doublet)/((X-x_doublet)**2+(Y-y_doublet)**2))
        return psi
    
    U_unif=1 
      
    psi_circle=get_stream_function_doublet(k,R_0_x,R_0_y, X, Y)
    psi_airfoil=get_stream_function_doublet(k,R_0_x,R_0_y, Z.real, Z.imag)
    
    psi_freestream=U_unif*Y
    
        
    Xa=(X-R_0_x)*np.cos(AoA)+(Y-R_0_y)*np.sin(AoA)
    Ya=-(X-R_0_x)*np.sin(AoA)+(Y-R_0_y)*np.cos(AoA)
             
    Za=Xa+1j*Ya
    
    
    psi_circle_=get_stream_function_doublet(k,0,0, Xa, Ya)
    psi_airfoil_=get_stream_function_doublet(k,0,0, Za.real, Za.imag)
    
    psi_freestream_=U_unif*Ya
    
    psi_tot1_=psi_circle_+psi_freestream_
    psi_tot2_=psi_airfoil_+psi_freestream_
    
    gamma=-Ya[0,0]*np.pi*4  
           
    def get_stream_function_vortex(gamma,x_vortex,y_vortex,X,Y):
        psi=(gamma/(4*np.pi))*np.log((X-x_vortex)**2+(Y-y_vortex)**2)
        return psi
    
    psi_vortex=get_stream_function_vortex(gamma,0,0,Xa,Ya)
    
    psi_tot11_=psi_circle_+psi_freestream_+psi_vortex
    psi_tot22_=psi_airfoil_+psi_freestream_+psi_vortex
    #
    u_freestream=U_unif*np.ones((Ntheta,Nr),dtype=float)
    v_freestream=U_unif*np.zeros((Ntheta,Nr),dtype=float)

    def get_velovity_double(k,x_doublet,y_doublet,X,Y):
        u=(-k/(2*np.pi))*(((X-x_doublet)**2-(Y-y_doublet)**2)/(((X-x_doublet)**2+(Y-y_doublet)**2)**2))
        v=(-k/(2*np.pi))*((2*(X-x_doublet)*(Y-y_doublet))/(((X-x_doublet)**2+(Y-y_doublet)**2)**2))
        return u,v

    u_doubleta, v_doubleta=get_velovity_double(k,0,0, Xa, Ya)
    
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
    
    
    cp6=1-(U_zeta_**2+V_zeta_**2)/U_unif**2  

    fig9, ax9 = plt.subplots(1,1,figsize=(15, 15))
    fig9.suptitle('airfoil', fontsize=22)
    
    ax9.set_xlim(-3.5,3.5)
    ax9.set_ylim(-3.5,3.5)
    
    
    conf5=ax9.contourf(Zeta.real,Zeta.imag,cp6,levels=np.linspace(-1, 1, 500), extend='both',cmap='cool')
    ax9.plot(Zu.real,Zu.imag,color='#CD2305'), ax9.plot(Zl.real,Zl.imag,color='#CD2305')
    ax9.contour(Zeta.real,Zeta.imag,psi_tot22_,20,colors='black', linewidths=2, linestyles='solid')
    ax9.axis('equal')
    cbar1=plt.colorbar(conf5)
    cbar1.set_label('$Cp$',fontsize=20)
    
    
    
    plt.savefig("airfoir{}".format(i))
    AoA+=0.05*np.pi/180
    i+=1
    