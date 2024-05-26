import pygame as pg

class FileSlider:
    def __init__(self, program: object, pos: tuple, max_pos: int, height: int, offset: tuple) -> None:
        self.prog: object = program
        self.pos: list = list(pos)
        self.min: int = self.pos[1]
        self.max: int = max_pos
        self.height: int = height
        self.range: int = self.max - self.min - self.height
        self.val: float = (self.pos[1] - self.min) / self.range
        self.offset: tuple = offset
        self.slider: pg.Surface = pg.Surface((30, self.height))
        self.slider.fill((180, 180, 180))
        pg.draw.rect(self.slider, (150, 150, 150), (0, 0, 30, self.height), width=1)
        self.rect: pg.Rect = pg.Rect(self.pos[0] + self.offset[0], self.pos[1] + self.offset[1], 30, self.height)
        self.collide: bool = False
        self.click_offset: int = 0
        self.click_offset = 0

    def check_collision(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        self.collide = self.rect.collidepoint(mouse_pos)

        if pg.mouse.get_pressed()[0]:  # Linke Maustaste gedrückt
            if self.collide and self.click_offset == 0:
                self.click_offset = mouse_pos[1] - self.rect.top

            if self.click_offset != 0:
                new_y_pos = mouse_pos[1] - self.click_offset

                # Begrenzen Sie die neue Position auf die min und max Werte
                if new_y_pos < self.min:
                    new_y_pos = self.min
                if new_y_pos > self.max - self.height:
                    new_y_pos = self.max - self.height

                self.pos[1] = new_y_pos
                self.rect.topleft = (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1])
                self.val = (self.pos[1] - self.min) / self.range
                print(f"Value: {self.val}, Slider Pos: {self.pos}")

        else:
            self.click_offset = 0
            self.rect.topleft = (self.pos[0] + self.offset[0], self.pos[1] + self.offset[1])

    def get_value(self) -> float:
        return self.val

    def render(self, surf: pg.Surface) -> None:
        # Debugging-Ausgaben zur Überprüfung der Position
        print(f"Rendering Slider at Position: {self.rect.topleft}")
        surf.blit(self.slider, self.rect.topleft)
        pg.draw.rect(surf, "red", self.rect, 1)

# Beispielinitialisierung und -aufruf des Sliders:
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

# Dummy-Programmobjekt mit einem main_window-Attribut für Beispielzwecke
class Program:
    def __init__(self):
        self.main_window = screen

program = Program()
slider = FileSlider(program, (50, 50), 550, 100, (0, 0))

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((30, 30, 30))
    
    slider.check_collision()
    slider.render(screen)
    
    pg.display.flip()
    clock.tick(30)

pg.quit()