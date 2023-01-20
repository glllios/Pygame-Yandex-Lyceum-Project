import random
import sys
import time

import pygame
from pygame.locals import *

fps = 60
window_w, window_h = 600, 500
block, cup_h, cup_w = 20, 20, 10

side_frequence, down_frequence = 0.15, 0.1

side_margin = int((window_w - cup_w * block) / 2)
top_margin = window_h - (cup_h * block) - 5

colors = ((139, 0, 139), (0, 250, 154), (220, 20, 60), (255, 255, 0))
lightcolors = ((153, 50, 204), (144, 238, 144), (240, 128, 128), (255, 215, 0))
white, gray, black = (255, 255, 255), (185, 185, 185), (0, 0, 0)
board_color, backg_color, text_color, title_color, \
inform_color = white, black, white, white, white

figure_width, figure_height = 5, 5
empty = "o"

matrix = {'S': [['ooooo',
                 'ooooo',
                 'ooxxo',
                 'oxxoo',
                 'ooooo'],
                ['ooooo',
                 'ooxoo',
                 'ooxxo',
                 'oooxo',
                 'ooooo']],
          'Z': [['ooooo',
                 'ooooo',
                 'oxxoo',
                 'ooxxo',
                 'ooooo'],
                ['ooooo',
                 'ooxoo',
                 'oxxoo',
                 'oxooo',
                 'ooooo']],
          'J': [['ooooo',
                 'oxooo',
                 'oxxxo',
                 'ooooo',
                 'ooooo'],
                ['ooooo',
                 'ooxxo',
                 'ooxoo',
                 'ooxoo',
                 'ooooo'],
                ['ooooo',
                 'ooooo',
                 'oxxxo',
                 'oooxo',
                 'ooooo'],
                ['ooooo',
                 'ooxoo',
                 'ooxoo',
                 'oxxoo',
                 'ooooo']],
          'L': [['ooooo',
                 'oooxo',
                 'oxxxo',
                 'ooooo',
                 'ooooo'],
                ['ooooo',
                 'ooxoo',
                 'ooxoo',
                 'ooxxo',
                 'ooooo'],
                ['ooooo',
                 'ooooo',
                 'oxxxo',
                 'oxooo',
                 'ooooo'],
                ['ooooo',
                 'oxxoo',
                 'ooxoo',
                 'ooxoo',
                 'ooooo']],
          'I': [['ooxoo',
                 'ooxoo',
                 'ooxoo',
                 'ooxoo',
                 'ooooo'],
                ['ooooo',
                 'ooooo',
                 'xxxxo',
                 'ooooo',
                 'ooooo']],
          'O': [['ooooo',
                 'ooooo',
                 'oxxoo',
                 'oxxoo',
                 'ooooo']],
          'T': [['ooooo',
                 'ooxoo',
                 'oxxxo',
                 'ooooo',
                 'ooooo'],
                ['ooooo',
                 'ooxoo',
                 'ooxxo',
                 'ooxoo',
                 'ooooo'],
                ['ooooo',
                 'ooooo',
                 'oxxxo',
                 'ooxoo',
                 'ooooo'],
                ['ooooo',
                 'ooxoo',
                 'oxxoo',
                 'ooxoo',
                 'ooooo']]}


def main_function():
    global fps_clock, display_surf, basic_font, big_font
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((window_w, window_h))
    basic_font = pygame.font.SysFont("arial", 20)
    big_font = pygame.font.SysFont("verdana", 45)
    pygame.display.set_caption("ТЕТРИС")
    show_text("ТЕТРИС")

    while True:
        run_tetris()
        screen_pause()
        show_text("GAME OVER")


def run_tetris():
    cup = emptycup()
    ps = 0
    level, fall_speed = speed_calculating(ps)
    falling_fig = get_new_figure()
    next_fig = get_new_figure()
    going_down = False
    going_left = False
    going_right = False
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()

    while True:
        if falling_fig is None:
            falling_fig = next_fig
            next_fig = get_new_figure()
            last_fall = time.time()

            if not checking_position(cup, falling_fig):
                return
        game_quit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    screen_pause()
                    show_text('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:

                if event.key == K_LEFT and checking_position(cup, falling_fig,
                                                             adjX=-1):
                    falling_fig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and checking_position(cup,
                                                                falling_fig,
                                                                adjX=1):
                    falling_fig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                elif event.key == K_UP:
                    falling_fig['rotation'] = (falling_fig[
                                                   'rotation'] + 1) % len(
                        matrix[falling_fig['shape']])
                    if not checking_position(cup, falling_fig):
                        falling_fig['rotation'] = (falling_fig[
                                                       'rotation'] - 1) % len(
                            matrix[falling_fig['shape']])

                elif event.key == K_DOWN:
                    going_down = True
                    if checking_position(cup, falling_fig, adjY=1):
                        falling_fig['y'] += 1
                    last_move_down = time.time()

                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, cup_h):
                        if not checking_position(cup, falling_fig, adjY=i):
                            break
                    falling_fig['y'] += i - 1

        if (
                going_left or going_right) and time.time() - last_side_move > side_frequence:
            if going_left and checking_position(cup, falling_fig, adjX=-1):
                falling_fig['x'] -= 1
            elif going_right and checking_position(cup, falling_fig, adjX=1):
                falling_fig['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > down_frequence and checking_position(
                cup, falling_fig, adjY=1):
            falling_fig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:
            if not checking_position(cup, falling_fig,
                                     adjY=1):
                add_to_cup(cup,
                           falling_fig)
                ps += clear_compl(cup)
                level, fall_speed = speed_calculating(ps)
                falling_fig = None
            else:
                falling_fig['y'] += 1
                last_fall = time.time()

        display_surf.fill(backg_color)
        drawing_title()
        cupgame(cup)
        drawing_info(ps, level)
        drawnextFig(next_fig)
        if falling_fig is not None:
            figure_draw(falling_fig)
        pygame.display.update()
        fps_clock.tick(fps)


def text_obj(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def checking_key():
    game_quit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def show_text(text):
    surf_title, recting_title = text_obj(text, big_font, title_color)
    recting_title.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)
    display_surf.blit(surf_title, recting_title)

    pressKeySurf, pressKeyRect = text_obj(
        'Нажмите любую клавишу для продолжения', basic_font, title_color)
    pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 100)
    display_surf.blit(pressKeySurf, pressKeyRect)

    while checking_key() is None:
        pygame.display.update()
        fps_clock.tick()


def game_quit():
    for _ in pygame.event.get(
            QUIT):
        stopGame()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stopGame()
        pygame.event.post(event)


def speed_calculating(points):
    level = int(points / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def get_new_figure():
    shape = random.choice(list(matrix.keys()))
    new_fig = {'shape': shape,
               'rotation': random.randint(0, len(matrix[shape]) - 1),
               'x': int(cup_w / 2) - int(figure_width / 2),
               'y': -2,
               'color': random.randint(0, len(colors) - 1)}
    return new_fig


def add_to_cup(cup, figure):
    for x in range(figure_width):
        for y in range(figure_height):
            if matrix[figure['shape']][figure['rotation']][y][x] != empty:
                cup[x + figure['x']][y + figure['y']] = figure['color']


def emptycup():
    cup = []
    for i in range(cup_w):
        cup.append([empty] * cup_h)
    return cup


def incup(x, y):
    return 0 <= x < cup_w and y < cup_h


def checking_position(cup, fig, adjX=0, adjY=0):
    for x in range(figure_width):
        for y in range(figure_height):
            abovecup = y + fig['y'] + adjY < 0
            if abovecup or matrix[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                return False
    return True


def checking_completed(cup, y):
    for x in range(cup_w):
        if cup[x][y] == empty:
            return False
    return True


def clear_compl(cup):
    removed_lines = 0
    y = cup_h - 1
    while y >= 0:
        if checking_completed(cup, y):
            for pushDownY in range(y, 0, -1):
                for x in range(cup_w):
                    cup[x][pushDownY] = cup[x][pushDownY - 1]
            for x in range(cup_w):
                cup[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


def convet_coords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))


def block_draw(block_x, block_y, color, pixelx=None, pixely=None):
    if color == empty:
        return
    if pixelx is None and pixely is None:
        pixelx, pixely = convet_coords(block_x, block_y)
    pygame.draw.rect(display_surf, colors[color],
                     (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pygame.draw.rect(display_surf, lightcolors[color],
                     (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pygame.draw.circle(display_surf, colors[color],
                       (pixelx + block / 2, pixely + block / 2), 5)


def screen_pause():
    pause = pygame.Surface((600, 500), pygame.SRCALPHA)
    pause.fill((0, 0, 0))
    display_surf.blit(pause, (0, 0))


def cupgame(cup):
    pygame.draw.rect(display_surf, board_color, (
        side_margin - 4, top_margin - 4, (cup_w * block) + 8,
        (cup_h * block) + 8),
                     5)

    pygame.draw.rect(display_surf, backg_color,
                     (side_margin, top_margin, block * cup_w, block * cup_h))
    for x in range(cup_w):
        for y in range(cup_h):
            block_draw(x, y, cup[x][y])


def drawing_title():
    titleSurf = big_font.render('TETЯIS', True, title_color)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (window_w - 380, 30)
    display_surf.blit(titleSurf, titleRect)


def drawing_info(points, level):
    pointsSurf = basic_font.render(f'Points: {points}', True, text_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (window_w - 550, 180)
    display_surf.blit(pointsSurf, pointsRect)

    levelSurf = basic_font.render(f'Level: {level}', True, text_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_w - 550, 250)
    display_surf.blit(levelSurf, levelRect)

    pausebSurf = basic_font.render('Pause: SPACE', True, inform_color)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (window_w - 550, 420)
    display_surf.blit(pausebSurf, pausebRect)

    escbSurf = basic_font.render('Exit: Esc', True, inform_color)
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (window_w - 550, 450)
    display_surf.blit(escbSurf, escbRect)


def figure_draw(fig, pixelx=None, pixely=None):
    figToDraw = matrix[fig['shape']][fig['rotation']]
    if pixelx is None and pixely is None:
        pixelx, pixely = convet_coords(fig['x'], fig['y'])

    for x in range(figure_width):
        for y in range(figure_height):
            if figToDraw[y][x] != empty:
                block_draw(None, None, fig['color'], pixelx + (x * block),
                           pixely + (y * block))


def drawnextFig(fig):
    nextSurf = basic_font.render("Next:", True, text_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (window_w - 150, 180)
    display_surf.blit(nextSurf, nextRect)
    figure_draw(fig, pixelx=window_w - 150, pixely=230)


def stopGame():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_function()
