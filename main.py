# 4.10.2022 versio 2.0
import pygame
from datetime import datetime
import math


pygame.init()
width, height = 640, 640
display = pygame.display.set_mode((width, height))

# päivitys x sek välein
try:
    paivitysvali = int(input("Päivitysväli sek (1-60): "))
except ValueError:
    print("Error: päivitysväli 1 sek")
    paivitysvali = 1

if paivitysvali < 1 or paivitysvali > 60:
    print("Error: päivitysväli 1 sek")
    paivitysvali = 1

paivitys = True
   
# taustakuva
bg = pygame.image.load("kello_tausta.png")

radius_sek = height / 2 - 20
radius_min = radius_sek  - 50
radius_h = radius_min - 50

# tuntiviisarin 60 askelmaa tunnissa 60*12=720
siirtyma_h720 = 2 * math.pi / 720

# x- ja y-koordinaatit, start_pos
start_pos = (width // 2, height // 2) 

# x- ja y-koordinaatit, end_pos
def end_pos(angle: float, radius: int) -> tuple:
    x = math.floor(width / 2 + math.cos(angle) * radius)
    y = math.floor(height / 2 + math.sin(angle) * radius)
    return (x, y)

def laske_angle(aika: int, askelmat: int, siirtyma: float=0) -> float:
    return (2 * math.pi * aika / askelmat - math.pi / 2) + siirtyma


clock = pygame.time.Clock()
eka = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    x_date = datetime.now()

    if x_date.second % paivitysvali == 0: paivitys = True
    else: paivitys = False

    if paivitys or eka:
        eka = False
        x_time = x_date.strftime("%A %d.%m.%Y, %H:%M.%S")
        pygame.display.set_caption(f"{x_time}")

        # 12 h -> x_date.hour % 12, 12 (x_date.hour => range(24))
        angle_h = laske_angle(x_date.hour % 12, 12, siirtyma_h720 * x_date.minute)
        angle_min = laske_angle(x_date.minute, 60)
        angle_sek = laske_angle(x_date.second, 60)

        display.fill((0, 0, 0))

        # taustakuva
        display.blit(bg, (0, 0))
   
        # tunnit
        pygame.draw.line(display, (255, 0, 0), start_pos, end_pos(angle_h, radius_h), 32)
   
        # minuutit
        pygame.draw.line(display, (255, 0, 0), start_pos, end_pos(angle_min, radius_min), 16)

        # sekunnit
        pygame.draw.line(display, (255, 0, 0), start_pos, end_pos(angle_sek, radius_sek), 8)
    
        # keskusta
        pygame.draw.circle(display, (0, 0, 255), (width / 2, height / 2), 40)
        pygame.display.flip()

    clock.tick(5)
    
   