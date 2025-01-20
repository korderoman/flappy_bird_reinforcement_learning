import pygame as pg
class Score:
    def __init__(self, screen, base_path, bird, pipe):
        self.screen = screen
        self.base_path = base_path
        self.bird = bird
        self.pipe=pipe
        self.font =pg.font.Font(f"{self.base_path}assets/font.ttf",24)
        self.score_text = self.font.render("Score: 0", True, (0, 0, 0))
        self.score_text_rect = self.score_text.get_rect(center=(100, 30))
        self.score_point = 0

    def restart(self):
        self.score_text = self.font.render("Score: 0", True, (0, 0, 0))

    def update(self, score):
        self.score_text = self.font.render(f"Score: {score}", True, (0, 0, 0))

    def draw(self):
        self.screen.blit(self.score_text, self.score_text_rect)
    def check_score_by_step(self, is_game_over):
        if not is_game_over:
            total_score_for_step=self.check_score_still_alive() + self.check_score_top()+self.check_score_pipe()
            self.score_point= round(total_score_for_step,1)
        return self.score_point

    def  check_score_still_alive(self):
        return 0.1

    def check_score_top(self):
        if self.bird.bird_rect.midtop[1] <= 0:
            return - 0.5
        else:
            return 0

    def check_score_pipe(self):
        """
        Obtiene el puntaje cuando pasa a través de un pipe
        :return:
        """
        if len(self.pipe.pipes)>0:
            pipe_down=self.pipe.pipes[0]['down']
            if pipe_down.right < self.bird.bird_rect.left < pipe_down.right+4:
               return 1
            return 0
        return 0