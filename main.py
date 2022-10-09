
import pygame
from datetime import datetime
import math

class Kello:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        self.fontti = pygame.font.SysFont("Arial", 50)

        # viisarien pituudet
        self.radius_sek = self.height / 2 - 20
        self.radius_min = self.radius_sek  - 50
        self.radius_h = self.radius_min - 50

        # tuntiviisarin 60 askelmaa tunnissa 60*12=720
        self.siirtyma_h720 = 2 * math.pi / 720

        # x- ja y-koordinaatit, start_pos
        self.start_pos = (self.width // 2, self.height // 2) 

        self.silmukka()

    # numerot kellotauluunm
    def kellotaulu(self):
        x_origo = self.width / 2
        y_origo = self.height / 2
        etaisyys = self.radius_sek

        iii = self.fontti.render("III", True, (255, 255, 255))
        self.display.blit(iii, (x_origo + etaisyys - iii.get_width(), y_origo - iii.get_height() / 2))

        ix = self.fontti.render("IX", True, (255, 255, 255))
        self.display.blit(ix, (x_origo - etaisyys, y_origo - ix.get_height() / 2))
            
        xii = self.fontti.render("XII", True, (255, 255, 255))
        self.display.blit(xii, (x_origo - xii.get_width() / 2, y_origo - etaisyys))

        vi = self.fontti.render("VI", True, (255, 255, 255))
        self.display.blit(vi, (x_origo - vi.get_width() / 2, y_origo + etaisyys - vi.get_height()))

    # x- ja y-koordinaatit, end_pos
    def end_pos(self, angle: float, radius: int) -> tuple:
        x = math.floor(self.width / 2 + math.cos(angle) * radius)
        y = math.floor(self.height / 2 + math.sin(angle) * radius)
        return (x, y)

    def laske_angle(self, aika: int, askelmat: int, siirtyma: float=0) -> float:
        return (2 * math.pi * aika / askelmat - math.pi / 2) + siirtyma

    # viisarit ja keskusta
    def viisarit(self, x_date: datetime):
        # 12 h -> x_date.hour % 12, 12 (x_date.hour => range(24))
        angle_h = self.laske_angle(x_date.hour % 12, 12, self.siirtyma_h720 * x_date.minute)
        angle_min = self.laske_angle(x_date.minute, 60)
        angle_sek = self.laske_angle(x_date.second, 60)

        # tunnit
        pygame.draw.line(self.display, (255, 0, 0), self.start_pos, self.end_pos(angle_h, self.radius_h), 32)
   
        # minuutit
        pygame.draw.line(self.display, (255, 0, 0), self.start_pos, self.end_pos(angle_min, self.radius_min), 16)

        # sekunnit
        pygame.draw.line(self.display, (255, 0, 0), self.start_pos, self.end_pos(angle_sek, self.radius_sek), 8)
    
        # keskusta
        pygame.draw.circle(self.display, (0, 0, 255), (self.width / 2, self.height / 2), 40)


    def silmukka(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            x_date = datetime.now()
            x_time = x_date.strftime("%A %d.%m.%Y, %H:%M.%S")
            pygame.display.set_caption(f"{x_time}")

            self.display.fill((0, 0, 0))

            self.kellotaulu()
            self.viisarit(x_date)
   
            pygame.display.flip()
            clock.tick(5)
    
   
if __name__ == "__main__":
    Kello(640, 480)