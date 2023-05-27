# Code par : Yoann HOARAU
import numpy as np
import pygame

from numpy import cos, sin, radians, degrees
from pygame.locals import K_z, K_q, K_s, K_d, K_ESCAPE, KEYDOWN, QUIT


# CONSTANTS -------------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

g = 9.81
SCALE = 3


class Roquet(pygame.sprite.Sprite):
    def __init__(self, m_fuel=55, m_craft=30, ISP=800, lenth=100, thickness=5):
        super(Roquet, self).__init__()
        self.x, self.y = WIDTH / (2*SCALE), HEIGHT - 20
        self.theta_roquet = radians(90)
        self.theta_roquet_v = 0
        self.calage_engine = 0
        
        self.vx = self.vy = self.v = 0
        
        self.start_fuel_mass = m_fuel
        self.m_fuel = m_fuel
        self.m_craft = m_craft
        self.m = m_fuel + m_craft
        
        self.thrust = self.m * g * 1.33
        self.ISP = ISP
        
        self.thickness_roquet = int(thickness)
        self.thickness_engine = self.thickness_roquet // 4
        self.lenth_roquet = lenth
        self.lenth_engine = self.lenth_roquet // 2
        
        self.CDG = (self.lenth_roquet / 4, self.lenth_roquet / 2) #  (fuel, craft)
        self.I = (self.thickness_roquet/2)**2 / 4 + self.lenth_roquet**2 / 12
        
        self.traj = []
        self.thrust_speed = 10
        
    
    def update_traj(self, n=1):
        global time
        t = 1/(60 * n)
        for i in range(n):
            time += t
            #  MOUVEMENT ----------
            self.vx = self.thrust / self.m * cos(self.theta_roquet + self.calage_engine) * t + self.vx
            self.vy = (g - self.thrust / self.m * sin(self.theta_roquet + self.calage_engine)) * t + self.vy
            self.v = np.sqrt(self.vx**2 + self.vy**2)
            
            self.x = self.vx * t + self.x
            self.y = self.vy * t + self.y
            
            # ROTATION ----------
            GB = (self.m_craft * self.CDG[1] + self.m_fuel * self.CDG[0]) / self.m
            
            self.theta_roquet_v = -GB * self.thrust / (self.m * self.I) * sin(self.calage_engine) * t + self.theta_roquet_v
            self.theta_roquet = self.theta_roquet_v * t + self.theta_roquet
            
            # MASS ----------
            loss_m = self.thrust / (self.ISP * g) * t
            self.m_fuel -= loss_m
            self.m -= loss_m
            
            self.traj.append((self.x, self.y))
        
    
    def draw(self):
        self.lenth_engine = self.thrust / 110
        
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
            pygame.draw.lines(screen, GREEN, False, updated, width=1)
        
        pygame.draw.line(screen, WHITE, (int(Xstart*SCALE), int(Ystart*SCALE-(SCALE-1)*HEIGHT)), (int(Xend*SCALE), int(Yend*SCALE-(SCALE-1)*HEIGHT)), int(self.thickness_roquet * SCALE))
        pygame.draw.line(screen, WHITE, (int(Xstart*SCALE), int(Ystart*SCALE-(SCALE-1)*HEIGHT)), (int(CXend*SCALE), int(CYend*SCALE-(SCALE-1)*HEIGHT)), int(self.thickness_engine * SCALE))
        pygame.draw.circle(screen, GREEN, (int(self.x * SCALE), int(self.y * SCALE-(SCALE-1)*HEIGHT)), int(self.thickness_roquet/2*SCALE))
    
    
    def update_control(self, key):
        gimbal_speed = radians(.2)
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
        x = 1050
        FONT = pygame.font.SysFont(None, 20)
        # control
        text0 = FONT.render(f'Time : {int(time)} s', True, WHITE)
        text1 = FONT.render(f'Thrust : {int(self.thrust)} N', True, WHITE)
        text2 = FONT.render(f'Gimbal : {round(degrees(self.calage_engine), 1)} °', True, WHITE)
        text3 = FONT.render(f'Fuel : {int(self.m_fuel / self.start_fuel_mass * 100)} %', True, WHITE)
        
        text4 = FONT.render(f'Angle : {int(degrees(self.theta_roquet % (2 * np.pi)))} °', True, WHITE)
        text5 = FONT.render(f'Mass : {round(self.m, 1)} kg', True, WHITE)
        text6 = FONT.render(f'TWR : {round(self.thrust / (self.m*g), 2)} N/kg', True, WHITE)
        text7 = FONT.render(f'Speed : {int(self.v)} m/s', True, WHITE)
        text8 = FONT.render(f'Altitude : {int(HEIGHT - self.y)} m', True, WHITE)
        
        
        screen.blit(text1, (x, 600))
        screen.blit(text2, (x, 625))
        screen.blit(text3, (x, 650))
        
        screen.blit(text0, (10, 5))
        screen.blit(text4, (x, 25))
        screen.blit(text5, (x, 50))
        screen.blit(text6, (x, 75))
        screen.blit(text7, (x, 100))
        screen.blit(text8, (x, 125))



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
            SCALE += scale
            #print(round(SCALE, 2))


# GAME INITIALIZATION ---------------------------------------------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Solide 2.1')

#  ROQUET DESIGN --------------------------------------------------------------
player = Roquet()


#text1 = Text(FONT, 'Thrust', player.thru)
FONT = pygame.font.SysFont(None, 20)

# BUTTONS ---------------------------------------------------------------------
zoom_in = Button(FONT, 15, HEIGHT - 50, text='Zoom +')
zoom_out = Button(FONT, 120, HEIGHT - 50, text='Zoom -')

FPS = pygame.time.Clock()
time = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print(round(time, 2))
                player = Roquet()
        if event.type == pygame.MOUSEBUTTONDOWN:
            zoom_in.on_clic(event.pos, .1)
            zoom_out.on_clic(event.pos, -.1)
    
    screen.fill(BLACK)
    
    pressed_keys = pygame.key.get_pressed()
    
    player.update_control(pressed_keys)
    player.update_traj(10)
    player.draw()
    player.update_text()
    
    zoom_in.show(screen)
    zoom_out.show(screen)
    
    pygame.display.flip()
    
    FPS.tick(60)
    
pygame.quit()
