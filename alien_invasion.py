import sys
import pygame
from pygame.sprite import  Group
from setting import  Settings
from game_stats import  GameStats
from scoreboard import Scoreboard
from button import  Button
from ship import Ship
from alien import Alien
from order import My_order
import  game_functions as gf
def run_game():
    #初始化游戏并且创建一个屏幕对象
    pygame.init()
    icon = pygame.image.load('icons/my_order.png')
    pygame.display.set_icon(icon)
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("爆射安卓")
    #创建play按钮
    play_button = Button(ai_settings, screen, 'start')
    #创建一架飞船
    ship = Ship(ai_settings, screen)
    #创建一个用于储存子弹的编组
    bullets = Group()
    aliens = Group()
    #创建外星人群
    gf.creat_fleet(ai_settings,screen,ship,aliens)
    #设置背景色
    bg_color = (230,230,230)
    #创建一个外星人
    alien =Alien(ai_settings,screen)
    #创建客制图片
    wife = My_order(ai_settings,screen)#非必要功能,XD
    #创建储存游戏统计信息的实力,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #开始游戏的循环
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.updata()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, wife, aliens, bullets,play_button)

run_game()