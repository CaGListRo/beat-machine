    def check_collision(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.collide = True
        if pg.mouse.get_pressed()[0] and self.collide:
            new_x = mouse_pos[0] - self.prog.body_surf_pos[0] - self.image.get_width() // 2
            if new_x < self.min:
                new_x = self.min
            elif new_x > self.max - self.image.get_width():
                new_x = self.max - self.image.get_width()
            self.pos[0] = new_x
            self.rect.topleft = (self.prog.body_surf_pos[0] + self.pos[0], self.prog.body_surf_pos[1] + self.pos[1])
            self.val = (new_x - self.min) / self.range
        if not pg.mouse.get_pressed()[0]:
            self.collide = False
            self.rect.topleft = (self.prog.body_surf_pos[0] + self.pos[0], self.prog.body_surf_pos[1] + self.pos[1])

    def check_collision(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.collide = True
        if pg.mouse.get_pressed()[0] and self.collide:
            self.pos[0] = mouse_pos[0] - self.image.get_width() // 2  # Anpassung hier
            if self.pos[0] < self.min:
                self.pos[0] = self.min
            elif self.pos[0] > self.max - self.image.get_width() // 2:
                self.pos[0] = self.max - self.image.get_width() // 2
            self.rect.topleft = (self.prog.body_surf_pos[0] + self.pos[0], self.prog.body_surf_pos[1] + self.y_pos)
        if not pg.mouse.get_pressed()[0]:
            self.collide = False