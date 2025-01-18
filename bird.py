import pygame as pg

class Bird:
    def __init__(self,screen, base_path_files):
        self.screen = screen
        self.base_path_files = base_path_files
        self.bird_index=0
        self.bird_image=None
        self.bird_sprites=[]
        self.bird_rect=None
        self.anim_counter=0
        self.y_vel=0
        self.gravity=10
        self.flap_velocity=250
        self.flap=False
        self.create()

    def create(self):
        bird_assets = [f"{self.base_path_files}assets/sprites/bluebird-downflap.png", f"{self.base_path_files}assets/sprites/bluebird-midflap.png", f"{self.base_path_files}assets/sprites/bluebird-upflap.png"]
        self.bird_sprites =[pg.image.load(x).convert_alpha() for x in bird_assets]
        self.bird_image=self.bird_sprites[self.bird_index]
        self.bird_rect=self.bird_image.get_rect(center=(100,100))

    def draw(self):
        self.screen.blit(self.bird_image, self.bird_rect)

    def update(self, dt):
        self.update_animation()
        self.update_position(dt)
        self.update_flap(dt)
        self.update_when_position_is_zero()

    def update_when_position_is_zero(self):
        if self.bird_rect.y <= 0 and self.flap_velocity == 250:
            self.bird_rect.y = 0
            self.flap_velocity = 0
            self.y_vel = 0
        elif self.bird_rect.y > 0 and self.flap_velocity == 0:
            self.flap_velocity = 250
            
    def update_animation(self):
        if self.anim_counter == 5:
            self.bird_image = self.bird_sprites[self.bird_index]
            if self.bird_index == 0:
                self.bird_index = 1
            elif self.bird_index == 1:
                self.bird_index = 2
            else:
                self.bird_index = 0
            self.anim_counter = 0
        self.anim_counter += 1

    def update_position(self,dt):
        self.y_vel += self.gravity * dt
        self.bird_rect.y+=self.y_vel

    def reset(self):
        self.bird_rect.center = (100, 100)
        self.y_vel = 0
        self.anim_counter = 0

    def flap_by_keyboard(self):
        self.flap=True

    def update_flap(self,dt):
        if self.flap:
            self.y_vel-=self.flap_velocity*dt
            self.flap=False
    def restart(self):
        self.bird_index = 0
        self.anim_counter = 0
        self.y_vel = 0
        self.gravity = 10
        self.flap_velocity = 250
        self.flap = False
        self.create()