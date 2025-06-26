import pygame


class Button:
    def __init__(self, pos,  text, font, base_color, hovering_color):
        self.x = pos[0]
        self.y = pos[1]
        self.text_str = text
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = font.render(text, True, self.base_color)
        # self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect = self.text.get_rect(center=(self.x, self.y))

    def update(self, screen):
        screen.blit(self.text, self.rect)

    def button_clicked(self, position):
        if position[0] in range(self.rect.left, self.rect.right):
            if position[1] in range(self.rect.top, self.rect.bottom):
                return True
        return False

    def button_hue(self, position):
        if self.button_clicked(position):
            self.text = self.font.render(self.text_str, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_str, True, self.base_color)
