from pygame.rect import Rect
import pygame.font
class HealthBar:

    def __init__(self, boss, name):
        self.screen = boss.screen
        self.ai_game = boss.horde.ai_game
        self.boss = boss
        self.width = 600
        self.height = 40
        self.name = name
        self.bg_rect = Rect(0, 0, self.width, self.height)
        self.bg_rect.centerx = self.ai_game.settings.screen_width / 2
        self.bg_rect.top = 10
        self.throwaway = self.width
        self.font = pygame.font.SysFont(None, 40)
        self.text_color = (0, 0, 0)
        self.list_of_front_rects = []
        self.previous_rect_edge = self.bg_rect.right - 4
        for x in range(self.width - 8):
            self.list_of_front_rects.append(0)
            self.list_of_front_rects[x] = Rect(self.previous_rect_edge, self.bg_rect.y + 4, 1, self.height - 8)
            self.previous_rect_edge = self.list_of_front_rects[x].left - 1
        self.green_indexes = []
        for x in range(0, self.width - 8):
            self.green_indexes.append(x)
        self.red_indexes = []

    def _prep_name(self):
        self.name_image = self.font.render(self.name, True, self.text_color, self.ai_game.settings.bg_color)
        self.name_image_rect = self.name_image.get_rect()
        self.name_image_rect.top = self.bg_rect.bottom + 10
        self.name_image_rect.centerx = self.bg_rect.centerx

    def _update_health(self):
        self.number_red = self.boss.max_hp - self.boss.health
        if self.number_red >= 592:
            self.number_red = 591
        self.number_green = self.boss.health
        self.red_indexes = []
        for x in range(0, self.number_red + 1):
            self.red_indexes.append(x)
        self.green_indexes = []
        self.final_value = 592
        if self.final_value not in self.red_indexes:
            for x in range(self.red_indexes[-1] + 1, self.boss.max_hp - 8):
                self.green_indexes.append(x)

    def _draw_health_bar(self):
        self.screen.fill((0, 0, 0), self.bg_rect)
        self.screen.blit(self.name_image, self.name_image_rect)
        for x in self.red_indexes:
            self.screen.fill((255, 0, 0), self.list_of_front_rects[x])
        for x in self.green_indexes:
            self.screen.fill((0, 255, 0), self.list_of_front_rects[x])