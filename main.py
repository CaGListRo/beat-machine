from utils import load_image, scale_image, create_beat_button_pattern, Button

import pygame as pg
from time import time

class BeatMachine:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        self.fps: int = 0
        self.run: bool = True

        self.bpm: int = 120
        self.number_of_beats: int = 16
        self.active_instrument_slot: int = 0
        self.beat_duration: float = self.calculate_beat_times()
        self.beat_time: float = 0
        self.play: bool = False
        self.shift: bool = False

        self.dt: float = 0
        self.last_time: float = time()
        self.frames: int = 0
        self.frames_timer: float = 0
        self.instruments: list = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],]        
        
        self.assets: dict = {
            "body": scale_image(load_image(img_name="body"), scalefactor=0.55),
            "bpm +- 1": scale_image(load_image(img_name="bpm plus minus 1"), scalefactor=0.55),
            "bpm +- 10": scale_image(load_image(img_name="bpm plus minus 10"), scalefactor=0.55),
            "button1/active": scale_image(load_image(img_name="button 1 active"), scalefactor=0.55),
            "button1/inactive": scale_image(load_image(img_name="button 1 inactive"), scalefactor=0.55),
            "button234/active": scale_image(load_image(img_name="button 234 active"), scalefactor=0.55),
            "button234/inactive": scale_image(load_image(img_name="button 234 inactive"), scalefactor=0.55),
            "pause/active": scale_image(load_image(img_name="button pause active"), scalefactor=0.55),
            "pause/inactive": scale_image(load_image(img_name="button pause inactive"), scalefactor=0.55),
            "play/active": scale_image(load_image(img_name="button play active"), scalefactor=0.55),
            "play/inactive": scale_image(load_image(img_name="button play inactive"), scalefactor=0.55),
            "stop/active": scale_image(load_image(img_name="button stop active"), scalefactor=0.55),
            "stop/inactive": scale_image(load_image(img_name="button stop inactive"), scalefactor=0.55),
            "slider knob": scale_image(load_image(img_name="slider knob"), scalefactor=0.55),
            "slot light/active": scale_image(load_image(img_name="slot indicator active"), scalefactor=0.55),
            "slot light/inactive": scale_image(load_image(img_name="slot indicator inactive"), scalefactor=0.55),
        }
        
        self.beat_buttons = create_beat_button_pattern(self)
        
    def calculate_beat_times(self) -> float:
        return 60 / (self.bpm * 4)
    
    def slot_shifter(self) -> None:
        if self.shift:
            print(self.active_instrument_slot)
            self.active_instrument_slot += 1
            self.shift = False
            if self.active_instrument_slot > self.number_of_beats - 1:
                self.active_instrument_slot = 0

    def play_instruments(self) -> None:
        pass

    def sum_beat_time(self) -> bool:
        self.beat_time += self.dt
        if self.beat_time >= self.beat_duration:
            self.beat_time = 0
            return True
        else:
            return False
        
    def calculate_fps(self) -> None:
        self.frames += 1
        self.frames_timer += self.dt
        if self.frames_timer >= 1:
            self.fps = self.frames
            self.frames, self.frames_timer = 0, 0

    def calculate_delta_time(self) -> None:
        self.dt = time() - self.last_time
        self.last_time = time()

    def draw_window(self) -> None:
        pg.display.set_caption(f"     Beat Maschine     FPS: {self.fps}")
        self.screen.blit(self.assets["body"], (0,0))

        pg.display.update()

    def main(self) -> None:
        print(self.beat_buttons)    
        while self.run:
            self.calculate_delta_time()
            self.calculate_fps()
            self.beat_duration = self.calculate_beat_times()
            
            if self.play:
                self.play_instruments()

                self.shift = self.sum_beat_time()
                self.slot_shifter()

            
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False

            self.draw_window()

        pg.quit()


if __name__ == "__main__":
    bm = BeatMachine()
    bm.main()