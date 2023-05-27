"""Objectifs :
    - Gimbal = 0 sauf si on appuie

MAJ :
    - Ajoute des traecjtoires prévisibles en laminaire et sans frottements
"""

import numpy as np
import pygame
import matplotlib.pyplot as plt

from numpy import cos, sin, radians, degrees, pi
from pygame.locals import K_z, K_q, K_s, K_d, K_ESCAPE, KEYDOWN, QUIT



# CONSTANTS -------------------------------------------------------------------
WIDTH, HEIGHT = 1280*1.2, 720*1.2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
RED2 = (255, 255, 0)


Cx = .37
G = 6.6743e-11

SCALE = 3
SPEED = 1


# CLASS -----------------------------------------------------------------------
class Roquet(pygame.sprite.Sprite):
    def __init__(self, m_fuel=20e3, m_craft=15e2, ISP=540, lenth=75, thickness=7):
        super(Roquet, self).__init__()
        
        self.x, self.y = WIDTH / (2*SCALE), HEIGHT * 1
        self.theta_roquet = radians(90)
        self.theta_roquet_v = 0
        self.calage_engine = 0
        
        self.v = 1
        # self.vx, self.vy = self.v * cos(self.theta_roquet), -self.v * sin(self.theta_roquet)
        self.vx, self.vy = self.v * cos(np.radians(45)), -self.v * sin(np.radians(45))
        
        self.start_fuel_mass = m_fuel
        self.m_fuel = m_fuel
        self.m_craft = m_craft
        self.m = m_fuel + m_craft
        
        self.thrust = self.m * 9.81 * 1
        self.ISP = ISP
        
        self.thickness_roquet = int(thickness)
        self.thickness_engine = np.ceil(self.thickness_roquet / 4)
        self.lenth_roquet = lenth
        self.lenth_engine = self.lenth_roquet // 4
        self.S = 0
        
        self.CDG = (self.lenth_roquet / 4, self.lenth_roquet / 2) #  (fuel, craft)
        self.I = (self.thickness_roquet)**2 / 16 + self.lenth_roquet**2 / 12
        
        self.traj = []
        self.angle = []
        self.thrust_speed = 20000
        
        
    def update_traj(self, n=1):
        global time, time_
        t = 1/(60 * n) * SPEED
        time_.append(time_[-1] + t)
        
        # ATMOSPHERE ----------
        self.g = atmosphere.g(HEIGHT - self.y)
        self.rho = atmosphere.rho(HEIGHT - self.y)
        
        for i in range(n):
            time += t
            alpha = self.theta_roquet - np.arccos(self.vx / self.v) if self.v != 0 else 0
            self.S = self.thickness_roquet * self.lenth_roquet * abs(sin(alpha)) + pi * self.thickness_roquet ** 2 / 4 * abs(cos(alpha))
            #  MOUVEMENT ----------
            self.vx += (self.thrust / self.m * cos(self.theta_roquet + self.calage_engine) - .5 / self.m * self.rho * self.S * Cx * self.v * self.vx) * t
            self.vy += (self.g - self.thrust / self.m * sin(self.theta_roquet + self.calage_engine) - .5 / self.m * self.rho * self.S * Cx * self.v * self.vy) * t
            self.v = np.sqrt(self.vx**2 + self.vy**2)
            
            self.x += self.vx * t
            self.y += self.vy * t
            
            # ROTATION ----------
            GB = (self.m_craft * self.CDG[1] + self.m_fuel * self.CDG[0]) / self.m
            GD = GB - self.lenth_roquet / 100000
            
            # -GB * self.thrust / (self.m * self.I) * sin(self.calage_engine) * t + self.theta_roquet_v
            self.theta_roquet_v = -(.5 * self.rho * self.S * Cx * self.v * GD * (self.vx * sin(self.theta_roquet) + self.vy * cos(self.theta_roquet)) + GB * self.thrust * sin(self.calage_engine)) / (self.m * self.I) * t + self.theta_roquet_v
            self.theta_roquet = self.theta_roquet_v * t + self.theta_roquet
            
            # MASS ----------
            loss_m = self.thrust / (self.ISP * self.g) * t
            self.m_fuel -= loss_m
            self.m -= loss_m
            
        self.traj.append((self.x, self.y))
        self.angle.append(self.theta_roquet)
            
    
    def draw_path(self):
        t = 1
        vx1, vy1 = self.vx, self.vy
        x1, y1 = self.x, self.y
        vx2, vy2 = self.vx, self.vy
        x2, y2 = self.x, self.y
        points1 = []
        points2 = []
        for i in range(50):
            points1.append((x1*SCALE, y1*SCALE-(SCALE-1)*HEIGHT))
            points2.append((x2*SCALE, y2*SCALE-(SCALE-1)*HEIGHT))
            
            vy1 += self.g * t
            
            lmbd = 400
            vx2 = vx2 * np.exp(-lmbd / self.m * t)
            vy2 = (vy2 - self.m * self.g / lmbd) * np.exp(-lmbd / self.m * t) + self.m * self.g / lmbd
            
            x1 += vx1 * t
            y1 += vy1 * t
            x2 += vx2 * t
            y2 += vy2 * t
        
        pygame.draw.lines(screen, RED, False, points1, width=1)
        #pygame.draw.lines(screen, RED2, False, points2, width=1)
    
    
    def draw(self):
        self.lenth_engine = self.thrust / (self.m*self.g) * SCALE
        
        GB = (self.m_craft * self.CDG[1] + self.m_fuel * self.CDG[0]) / self.m
        GA = self.lenth_roquet - GB
        
        # print(-1.1 * self.lenth_roquet < GB + GA < self.lenth_roquet * 1.1)
        
        Xstart, Ystart = self.x - GB * cos(self.theta_roquet), self.y + GB * sin(self.theta_roquet)
        Xend, Yend = self.x + GA * cos(self.theta_roquet), self.y - GA * sin(self.theta_roquet)
        
        CXend = Xstart - self.lenth_engine * cos(self.theta_roquet + self.calage_engine)
        CYend = Ystart + self.lenth_engine * sin(self.theta_roquet + self.calage_engine)
        
        if len(self.traj) > 2:
            updated = []
            for point in self.traj:
                x, y = point
                x *= SCALE
                y = y * SCALE - (SCALE-1)*HEIGHT
                updated.append((x, y))
            pygame.draw.lines(screen, GREEN, False, updated, width=2)
        
        pygame.draw.line(screen, WHITE, (int(Xstart*SCALE), int(Ystart*SCALE-(SCALE-1)*HEIGHT)), (int(Xend*SCALE), int(Yend*SCALE-(SCALE-1)*HEIGHT)), int(self.thickness_roquet * SCALE))
        pygame.draw.line(screen, WHITE, (int(Xstart*SCALE), int(Ystart*SCALE-(SCALE-1)*HEIGHT)), (int(CXend*SCALE), int(CYend*SCALE-(SCALE-1)*HEIGHT)), int(self.thickness_engine * SCALE))
        pygame.draw.circle(screen, GREEN, (int(self.x * SCALE), int(self.y * SCALE-(SCALE-1)*HEIGHT)), int(self.thickness_roquet/2*SCALE))
    
    
    def update_control(self, key):
        gimbal_speed = radians(1)
        thrust_speed = self.thrust_speed
        if self.m <= self.m_craft:
            self.thrust = 0
        elif key[K_z]:
            self.thrust += thrust_speed
        elif key[K_s] and self.thrust >= thrust_speed:
            self.thrust -= thrust_speed
        elif key[K_s] and self.thrust < thrust_speed:
            self.thrust = 0
        
        if key[K_q] and self.calage_engine > radians(-10):
            self.calage_engine -= gimbal_speed
        elif key[K_d] and self.calage_engine < radians(10):
            self.calage_engine += gimbal_speed
        
    
    def update_text(self):
        x = WIDTH - 230
        FONT = pygame.font.Font('Chillax-Bold.otf', 20)
        # control
        text0 = FONT.render(f'Time : {int(time)} s', True, WHITE)
        text1 = FONT.render(f'Thrust : {int(self.thrust / 1000)} kN', True, WHITE)
        text2 = FONT.render(f'Gimbal : {int(degrees(self.calage_engine))} °', True, WHITE)
        
        # craft
        text3 = FONT.render(f'Fuel : {int(self.m_fuel / self.start_fuel_mass * 100)} %', True, WHITE)
        text4 = FONT.render(f'Angle : {int(degrees(self.theta_roquet % (2 * np.pi)))} °', True, WHITE)
        text5 = FONT.render(f'Mass : {round(self.m, 1)} kg', True, WHITE)
        text6 = FONT.render(f'TWR : {round(self.thrust / (self.m*self.g), 2)} N/kg', True, WHITE)
        text7 = FONT.render(f'Speed : {int(self.v)} m/s', True, WHITE)
        text8 = FONT.render(f'Altitude : {int(HEIGHT - self.y)} m', True, WHITE)
        
        # atmosphere
        text9 = FONT.render(f'air : {round(self.rho, 2)} kg/m3', True, WHITE) if self.rho > 10e-2 else FONT.render(f'air : {round(self.rho*1000, 1)} g/m3', True, WHITE)
        text10 = FONT.render(f'gravity : {round(self.g, 2)} m/s²', True, WHITE)
        text11 = FONT.render(f'Temperature : {int(atmosphere.temperature(HEIGHT - self.y)-273.15)} °C', True, WHITE)
        text12 = FONT.render(f'Pressure : {int(atmosphere.pressure(HEIGHT - self.y)/100)} hPa', True, WHITE) if atmosphere.pressure(HEIGHT - self.y) > 100 else FONT.render(f'Pressure : {round(atmosphere.pressure(HEIGHT - self.y), 1)} Pa', True, WHITE)
        
        
        screen.blit(text0, (10, 5))
        screen.blit(text4, (x, 25))
        screen.blit(text5, (x, 50))
        screen.blit(text6, (x, 75))
        screen.blit(text7, (x, 100))
        screen.blit(text8, (x, 125))
        
        screen.blit(text9, (x, 300))
        screen.blit(text10, (x, 325))
        screen.blit(text11, (x, 350))
        screen.blit(text12, (x, 375))
        
        screen.blit(text1, (x, 600))
        screen.blit(text2, (x, 625))
        screen.blit(text3, (x, 650))



class Button:
    def __init__(self, FONT, x, y, text='N/A', width=16*6, height=9*4, fg=GREEN, bg=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(bg)
        
        text_surface = FONT.render(text, True, fg)
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)
    
    
    def show(self, screen):
        screen.blit(self.image, self.rect)
    
    
    def on_clic(self, pos, scale):
        global SCALE
        if self.rect.collidepoint(pos):
            SCALE *= scale
            #print(round(SCALE, 2))



class Atmosphere:
    def __init__(self, astre='Terre', mass=5.972e24, size=6371e3):
        self.m = mass
        self.r = size
        if not isinstance(astre, str):
            self.rho = astre
    
    
    def temperature(self, h=0):
        h = h / 1000
        if h <= 11:
            return 15 - 6.5 * h + 273.15
        elif 11 < h <= 20:
            return -56.5 + 273.15
        elif 20 < h <= 32:
            return -56.5 + (h - 20) + 273.15
        elif 32 < h <= 47:
            return -44.5 + 2.8 * (h - 32) + 273.15
        elif 47 < h <= 51:
            return -2.5 + 273.15
        elif 51 < h <= 71:
            return -2.5 - 2.8 * (h - 51) + 273.15
        elif 71 < h <= 86:
            return -58.5 - 2 * (h - 71) + 273.15
        elif 86 < h <= 100:
            return -88.5 + 2.5 * (h - 86) + 273.15
        else:
            return 573.15
    
    
    def pressure(self, h=0):
        if  h <= 40e3:
            return 101325 * (1 - (0.0065 * h) / 290.15)**5.255
        elif 40e3 < h <= 60e3:
            return .68911
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
    
    
    def rho(self, h=0):
        return (self.pressure(h) * 29e-3) / (8.3144621 * self.temperature(h))
    
    
    def g(self, h=0):
        return G * self.m / (h + self.r)**2


def zoom(key):
    global SCALE
    if key == 'up':
        SCALE *= 1.08
    else:
        SCALE *= .92
        


# GAME INITIALIZATION ---------------------------------------------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Solide 2.1')

#  ROQUET DESIGN --------------------------------------------------------------
player = Roquet()
atmosphere = Atmosphere()

#text1 = Text(FONT, 'Thrust', player.thru)
FONT = pygame.font.Font('Chillax-Bold.otf', 20)


FPS = pygame.time.Clock()
time = 0
time_ = [0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("restart")
                player = Roquet()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                SCALE *= 1.08
            elif event.button == 5:
                SCALE *= .92
                
            # zoom_in.on_clic(event.pos, 1.2)
            # zoom_out.on_clic(event.pos, .8)
    
    screen.fill(BLACK)
    
    pressed_keys = pygame.key.get_pressed()
    
    player.update_control(pressed_keys)
    player.update_traj(10)
    if HEIGHT - player.y > 0:
        player.draw_path()
    player.draw()
    player.update_text()
    
    pygame.display.flip()
    
    FPS.tick(60)
    
pygame.quit()


# plt.plot(time_[1:], player.angle)
