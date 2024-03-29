import sys
import pygame
from Bullet import  Bullet
from alien import Alien
from time import sleep
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ship_left > 0:
        # 将ships_left -1s
        stats.ship_left -= 1
        #更新记分牌
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人,并将飞船放到屏幕地段中央
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_setting, stats,sb, screen, ship, aliens, bullets):
    '''检测外星人是否到达屏幕地段'''
    screen_rect  = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #类似飞创被撞击的处理
            ship_hit(ai_setting,stats,sb,screen,ship,aliens,bullets)
            break
def check_keydown_events(event,ai_settings,screen, ship, bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
def fire_bullet(ai_settings, screen, ship, bullets):
    '''如果还没达到限制,就发射一颗子弹'''
    #创建新子弹,并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_high_score(stats, sb):
    '''检查是否产生新的最高得分'''
    if stats.score >stats.high_score:
        stats.high_score = stats.score
        stats.highest_score()
        sb.prep_high_score()
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():#获取事件
        if event.type == pygame.QUIT:#事件为QUIT时调用sys.exit()函数来退出游戏
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x ,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb, play_button, ship, aliens,bullets,mouse_x,mouse_y)
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''玩家单击play按钮时开始游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人,并让飞船居中
        creat_fleet(ai_settings,  screen, ship,aliens)
        ship.center_ship()
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    '''更新子弹的位置,并删除已消失的子弹'''
    #更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen,stats,sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen,stats,sb,ship, aliens, bullets):
    #检查是否有子弹击中外星人
    ##如果是这样,就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens,True,True)
    if collisions :
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    if len (aliens) == 0:
        #删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level += 1
        sb.prep_level()
        creat_fleet(ai_settings,screen,ship,aliens)
def update_screen(ai_settings, screen,stats,sb, ship,wife, aliens, bullets,play_button):
    '''更新屏幕上的图像并切换到新屏幕上'''
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)#使用bg_color填满整个屏幕
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #aliens.blitme()
    wife.blitme()
    #显示得分
    sb.show_score()
    #游戏非活跃状态,显示play按钮
    if not stats.game_active:
        play_button.draw_button()
    #让最近绘制的屏幕可见
    pygame.display.flip()
def get_number_aliens_x(ai_settings, alien_width):
    '''计算每行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x
def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows
def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''创建一个外星人并将其放在当前行'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
def creat_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    #创建一个外星人,并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings,screen)
    #alien_width  = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number, row_number)
def check_fleet_edges(ai_settings,aliens):
    '''外星人到达边缘时采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    '''整群外星人下移,并改变他们的方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''检测外星人和飞船之间的碰撞
        然后更新所有外星人的位置
    '''
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    '''检查外星人是否到达屏幕底端'''
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


