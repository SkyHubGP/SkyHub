# Code par : Yoann HOARAU
import numpy as np
import pygame
import matplotlib.pyplot as plt

from numpy import cos, sin, radians, degrees, pi
from pygame.locals import K_z, K_q, K_s, K_d, K_RIGHT, K_LEFT, K_ESCAPE, KEYDOWN, QUIT



# CONSTANTS -------------------------------------------------------------------
WIDTH, HEIGHT = 1280*1.2, 720*1.2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (74, 167, 225)


Cx = .37
G = 6.6743e-11

SCALE = .00004
SPEED = 1


# CLASS -----------------------------------------------------------------------
class Roquet:
    def __init__(self, x=0, y=0, m_fuel=105e3, m_craft=20.25e3, ISP=940, lenth=21, thickness=5):
        
        self.longitude = np.radians(0)
        self.d = 6371e3 + 508e3
        self.x, self.y = x, y
        
        self.draw_x = self.x*SCALE+terre.x
        self.draw_y = self.y*SCALE-(SCALE-1)*terre.y
        
        self.theta_roquet = radians(0)
        self.theta_roquet_v = 0
        self.calage_engine = 0
        
        self.v = 7.9e3
        self.vx, self.vy = self.v * cos(self.theta_roquet), -self.v * sin(self.theta_roquet)
        
        self.start_fuel_mass = m_fuel
        self.m_fuel = m_fuel
        self.m_craft = m_craft
        self.m = m_fuel + m_craft
        
        self.thrust = self.m * 9.81 * 0
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
        self.thrust_speed = 150e3
        
        
    def update_traj(self, n=1):
        global time, time_
        t = 1/(60 * n) * SPEED
        time_.append(time_[-1] + t)
        
        # ATMOSPHERE ----------
        self.g = terre.g(self.d)
        self.rho = terre.rho(self.d)
        
        for i in range(n):
            time += t
            alpha = self.theta_roquet - np.arccos(self.vx / self.v) if self.v != 0 else 0
            self.S = self.thickness_roquet * self.lenth_roquet * abs(sin(alpha)) + pi * self.thickness_roquet ** 2 / 4 * abs(cos(alpha))
            #  MOUVEMENT ----------
            self.vx += (self.thrust / self.m * cos(self.theta_roquet + self.calage_engine) - .5 / self.m * self.rho * self.S * Cx * self.v * self.vx - G * terre.m * self.x / self.d**3) * t
            self.vy += (-G * terre.m * self.y / self.d**3 - self.thrust / self.m * sin(self.theta_roquet + self.calage_engine) - .5 / self.m * self.rho * self.S * Cx * self.v * self.vy) * t
            self.v = np.sqrt(self.vx**2 + self.vy**2)
            
            self.x += self.vx * t
            self.y += self.vy * t
            
            self.d = np.sqrt((self.x)**2 + (self.y)**2)
            
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
        t = 2
        vx, vy = self.vx, self.vy
        x, y, d = self.x, self.y, self.d
        points = []
        for i in range(1500*3):
            points.append(((x-center.x)*SCALE + terre.x, (y-center.y)*SCALE-(SCALE-1)*terre.y))
            if True:
                vy += (- G * terre.m * y / d**3) * t
                vx += (- G * terre.m * x / d**3) * t
            else:
                lmbd = 400
                vx = vx * np.exp(-lmbd / self.m * t)
                vy = (vy - self.m * self.g / lmbd) * np.exp(-lmbd / self.m * t) + self.m * self.g / lmbd
            
            x += vx * t
            y += vy * t
            d = np.sqrt(x**2 + y**2)

        
        pygame.draw.lines(screen, RED, False, points, width=1)
        # pygame.draw.lines(screen, YELLOW, False, points2, width=1)
    
    
    def draw(self):
        self.lenth_engine = self.thrust / (self.m*self.g) * SCALE
        self.draw_x = self.x * SCALE + terre.x
        self.draw_y = self.y * SCALE - (SCALE - 1) * terre.y
        
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
                x = (x-center.x) * SCALE + terre.x
                y = (y-center.y) * SCALE - (SCALE-1)*terre.y
                updated.append((x, y))
            pygame.draw.lines(screen, GREEN, False, updated, width=2)
        
        
        pygame.draw.circle(screen, BLUE, ((terre.x - center.x)*SCALE+WIDTH/2, (terre.y - center.y)*SCALE + HEIGHT/2), 6371e3*SCALE) # Astre
        pygame.draw.line(screen, WHITE, (int(Xstart*SCALE + terre.x), int(Ystart*SCALE-(SCALE-1)*terre.y)), (int(Xend*SCALE + terre.x), int(Yend*SCALE-(SCALE-1)*terre.y)), int(self.thickness_roquet * SCALE))
        pygame.draw.line(screen, WHITE, (int(Xstart*SCALE + terre.x), int(Ystart*SCALE-(SCALE-1)*terre.y)), (int(CXend*SCALE + terre.x), int(CYend*SCALE-(SCALE-1)*terre.y)), int(self.thickness_engine * SCALE))
        pygame.draw.circle(screen, GREEN, ((self.x - center.x)*SCALE + WIDTH/2, (self.y - center.y)*SCALE-(SCALE-1)*terre.y), int(self.thickness_roquet)) # CDG
        
    
    
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
        FONT = pygame.font.Font('arial.ttf', 20)
        # control
        text0 = FONT.render(f'Time : {int(time)} s', True, WHITE)
        text01 = FONT.render(f'Speed : x{SPEED}', True, WHITE)
        
        text1 = FONT.render(f'Thrust : {int(self.thrust / 1000)} kN', True, WHITE)
        text2 = FONT.render(f'Gimbal : {int(degrees(self.calage_engine))} °', True, WHITE)
        
        # craft
        text3 = FONT.render(f'Fuel : {int(self.m_fuel / self.start_fuel_mass * 100)} %', True, WHITE)
        text4 = FONT.render(f'Angle : {int(degrees(self.theta_roquet % (2 * np.pi)))} °', True, WHITE)
        text5 = FONT.render(f'Mass : {round(self.m, 1)} kg', True, WHITE)
        text6 = FONT.render(f'TWR : {round(self.thrust / (self.m*self.g), 2)} N/kg', True, WHITE)
        text7 = FONT.render(f'Speed : {int(self.v)} m/s', True, WHITE)
        text8 = FONT.render(f'Altitude : {round((self.d - 6371e3)/1000, 1)} km', True, WHITE)
        
        # atmosphere
        text9 = FONT.render(f'air : {round(self.rho, 2)} kg/m3', True, WHITE) if self.rho > 10e-2 else FONT.render(f'air : {round(self.rho*1000, 1)} g/m3', True, WHITE)
        text10 = FONT.render(f'gravity : {round(self.g, 2)} m/s²', True, WHITE)
        text11 = FONT.render(f'Temperature : {int(terre.temperature(self.d)-273.15)} °C', True, WHITE)
        text12 = FONT.render(f'Pressure : {int(terre.pressure(self.d)/100)} hPa', True, WHITE) if terre.pressure(HEIGHT - self.y) > 100 else FONT.render(f'Pressure : {round(terre.pressure(HEIGHT - self.y), 1)} Pa', True, WHITE)
        
        
        screen.blit(text0, (10, 5))
        screen.blit(text01, (10, 30))
        
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



class Planet:
    def __init__(self, x=0, y=0, m=5.97e24, color=BLUE, radius=6371e3):
        self.x, self.y = x, y
        self.radius = radius
        self.color = color
        self.m = m
    
    
    def temperature(self, h=0):
        h = (h - 6371e3) / 1000
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
        h -= 6371e3
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
        return G * self.m / h**2
    


class Button:
    def __init__(self, x, y, text='N/A', width=16*6, height=9*4, fg=GREEN, bg=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(bg)
        
        FONT = pygame.font.Font('Chillax-Bold.otf', 20)
        text_surface = FONT.render(text, True, fg)
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)
    
    
    def show(self, screen):
        screen.blit(self.image, self.rect)
    
    
    def on_clic(self, pos):
        global center
        #print(center)
        if self.rect.collidepoint(pos):
            if center == terre:
                center = player
            else:
                center = terre

        


# GAME INITIALIZATION ---------------------------------------------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Solide 2.1')

#  ROQUET DESIGN --------------------------------------------------------------


terre = Planet(x=WIDTH/2, y=HEIGHT/2)
player = Roquet(x=terre.x, y=terre.y - (terre.radius + 500e3))

#text1 = Text(FONT, 'Thrust', player.thru)
FONT = pygame.font.Font('Chillax-Bold.otf', 20)

center = player
CHOOSE_CENTER = Button(15, HEIGHT - 50, text='Next')



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
                center = player
                terre = Planet(x=WIDTH/2, y=HEIGHT/2)
                player = Roquet(x=terre.x, y=terre.y - (terre.radius + 500e3))
            if event.key == K_RIGHT:
                SPEED *= 2
            elif event.key == K_LEFT and SPEED > 1:
                SPEED //= 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            CHOOSE_CENTER.on_clic(event.pos)
            
            if event.button == 4:
                SCALE *= 1.08
            elif event.button == 5:
                SCALE *= .92
                
            # zoom_in.on_clic(event.pos, 1.2)
            # zoom_out.on_clic(event.pos, .8)
    
    screen.fill(BLACK)
    
    pressed_keys = pygame.key.get_pressed()
    
    if SPEED == 1:
        player.update_control(pressed_keys)
    player.update_traj(10)
    
    player.draw()
    
    if player.d > terre.radius:
        player.draw_path()
    
    player.update_text()
    CHOOSE_CENTER.show(screen)
    
    pygame.display.flip()
    
    FPS.tick(60)
    #print(SCALE)
pygame.quit()


# plt.plot(time_[1:], player.angle)
