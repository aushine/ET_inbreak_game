import  pygame
from pygame.sprite import Sprite
class My_order(Sprite):
    '''单个外星人的类'''
    def __init__(self, ai_settings, screen):
        '''初始化外星人并设置其起始位置'''
        super(My_order, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #加载图片,并设置其rect属性
        self.image = pygame.image.load('images/my_order.png')
        self.rect = self.image.get_rect()
        #每个图片最初都在屏幕左上角附近
        self.rect.x = 20
        self.rect.y = 750
        #存储图片的准确位置
        self.x = float(self.rect.x)
    def blitme(self):
        '''在指定位置绘制图片'''
        self.screen.blit(self.image,self.rect)
