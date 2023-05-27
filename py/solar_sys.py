"""
Ce programme vient de 'Tech with Tim - Planet Simulation In Python - Tutorial'.
C'est un exemple de simulation de trajectoire sur PyGame, en l'occurrence le système solaire.

Pour ajouter un corps :
    - créer une nouvelle variable dans main() et appeler la class Planet
    - entrer les arguments :
        ⋅ position x (en unité astronomique)
        ⋅ position y (en unité astronomique)
        ⋅ rayon du corps (pas à l'echelle. Faire au feeling)
        ⋅ couleur d'affichage
        ⋅ masse du corps (à l'echelle en kg)
Code par : Yoann HOARAU
"""


import pygame
import math
pygame.init()

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 255)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
LIGHT_GREY = (230, 230, 230)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e9
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24  # 1 day
    
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
    
        self.orbit = []    
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 1)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/self.AU, 4)} u.a", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
    
        
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        


def main():
    run = True
    clock = pygame.time.Clock()
    
    
    sun = Planet(0, 0, 30, YELLOW, 1.98892e30)
    sun.sun = True
    
    mercury = Planet(-.387 * Planet.AU, 0, 8, DARK_GREY, 3.3e24)
    mercury.y_vel = 47400
    
    venus = Planet(-.723 * Planet.AU, 0, 14, LIGHT_GREY, 4.8685e24)
    venus.y_vel = 35020
    
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.974e24)
    earth.y_vel = 29783
    
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39e23)
    mars.y_vel = 24077
    
    jupiter = Planet(-5.2 * Planet.AU, 0, 20, RED, 1.898e27)
    jupiter.y_vel = 13058
    
    saturne = Planet(-9.5 * Planet.AU, 0, 18, RED, 5.683e26)
    saturne.y_vel = 9141
    
    
    # lune = Planet(-8.6e-1 * Planet.AU, 0, 4, WHITE, 8.972e26)
    # lune.y_vel = 38.38e3
    
    planets = [sun, mercury, venus, earth, mars, jupiter, saturne]
    
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update()
            
    pygame.quit()
     

main()