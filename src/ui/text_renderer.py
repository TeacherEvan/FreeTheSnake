from pygame import font

class TextRenderer:
    def __init__(self, font_name='Arial', font_size=24, color=(255, 255, 255)):
        self.font = font.SysFont(font_name, font_size)
        self.color = color

    def render_text(self, surface, text, position, center=False):
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position
        surface.blit(text_surface, text_rect)

    def set_color(self, color):
        self.color = color

    def set_font_size(self, size):
        self.font = font.SysFont(self.font.get_name(), size)