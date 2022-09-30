from py_compile import _get_default_invalidation_mode
import pygame
from pygame.locals import *
from circle import Circle
from knife import *
import os


pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_GREY = (60, 60, 60)
DARK_RED = (107, 0, 0)
BLACK = (0, 0, 0)

high_score = 0


small_font = pygame.font.SysFont('Verdana', 30)
big_font = pygame.font.SysFont('Verdana', 45)
game_name = big_font.render('KNIFE HIT', True, LIGHT_GREY)
start_text = small_font.render('START', True, BLACK)


def menu_screen(tick, image_index, myScreen, last_score=-1):
    if tick == 5:
        tick = 0
        image_index += 1
        if image_index > 11:
            image_index = 1
        menu_img = pygame.image.load(
            "resources/menu_images/frame_{}.gif".format(image_index)).convert_alpha()
        menu_img = pygame.transform.scale(menu_img, (600, 600))
        myScreen.blit(menu_img, (0, 0))

    pygame.draw.rect(myScreen, BLACK, [
        SCREEN_WIDTH/4, SCREEN_HEIGHT/4-90, 300, 60])

    if last_score == -1:
        myScreen.blit(game_name, (SCREEN_WIDTH/4+30, SCREEN_HEIGHT/4-90))
    else:
        last_score_text = big_font.render(
            "SCORE: {}".format(last_score), True, LIGHT_GREY)
        myScreen.blit(last_score_text, (SCREEN_WIDTH/4+30, SCREEN_HEIGHT/4-90))

    pygame.draw.rect(myScreen, DARK_RED, [
                     SCREEN_WIDTH/3+30, SCREEN_HEIGHT/2-100, 140, 40])
    myScreen.blit(start_text, (SCREEN_WIDTH/3+50, SCREEN_HEIGHT/2-100))

    high_score_text = small_font.render(
        'HIGH SCORE: {}'.format(high_score), True, BLACK)
    pygame.draw.rect(myScreen, DARK_RED, [
                     SCREEN_WIDTH/3-40, SCREEN_HEIGHT-100, 300, 40])
    myScreen.blit(high_score_text, (SCREEN_WIDTH/3-10, SCREEN_HEIGHT-100))
    return tick, image_index


def main():

    s = 'sound'
    # SCREEN_WIDTH = 600
    # SCREEN_HEIGHT = 600

    FPS = 60

    pSizeX = 30
    pSizeY = 30

    global myScreen
    global high_score

    myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Example 1")

    clock = pygame.time.Clock()

    music = pygame.mixer.music.load(os.path.join(s, 'menu.mp3'))
    pygame.mixer.music.play(-1)
    change_music = False
    # circle = pygame.image.load("circle.png").convert_alpha()
    # circle = pygame.transform.scale(circle, (200, 200) )

    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(0, 0))

    kA = KnivesAirbourne(myScreen, circle)
    knife_obj = Knife((0, 1), 10)
    kA.add(knife_obj)
    running = True

    game_start = False

    # print(high_score)
    tick = 0
    animation_tick = 0
    image_index = 1
    start_image_index = 0
    start_animation = False

    user_score = 0
    last_score = -1
    score_updatable = False

    while running:

        # get high score
        with open("high_scores.txt", 'r+') as w:
            lines = w.readlines()
            high_score = int(lines[-1])

        if change_music:
            pygame.mixer.music.play(-1)
            change_music = False

        clock.tick(60)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_start:
                    if event.button == 1:  # if left click
                        kA.handle_click()
                elif SCREEN_WIDTH/3+30 <= mouse[0] <= SCREEN_WIDTH/3+170 and SCREEN_HEIGHT/2-100 <= mouse[1] <= SCREEN_HEIGHT/2-60:
                    game_start = True

                    start_animation = True
                    animation_tick = 0

            elif event.type == pygame.KEYDOWN and game_start:

                if event.key == pygame.K_UP:
                    circle.increase_speed()
                if event.key == pygame.K_DOWN:
                    circle.decrease_speed()

        if game_start and not(start_animation):

            myScreen.fill(DARK_RED)
            game_over, user_score = kA.update(user_score)
            circle.show(myScreen)
            score_text = small_font.render(
                'SCORE: {}'.format(user_score), True, BLACK)
            myScreen.blit(score_text, (SCREEN_WIDTH/3+20, SCREEN_HEIGHT/4-100))

            # resets game
            if game_over:
                if user_score > high_score:
                    high_score = user_score
                    with open("high_scores.txt", 'w') as w:
                        w.write(str(high_score))

                last_score = user_score
                user_score = 0
                game_start = False
                tick = 0
                myScreen.fill((0, 0, 0))
                kA = KnivesAirbourne(myScreen, circle)
                knife_obj = Knife((0, 1), 10)
                kA.add(knife_obj)

                change_music = True
                music = pygame.mixer.music.load(os.path.join(s, 'menu.mp3'))
        else:
            tick, image_index = menu_screen(
                tick, image_index, myScreen, last_score)

            if start_animation:

                if animation_tick == 1:
                    animation_tick = 0
                    start_image_index += 1
                    if start_image_index > 150:
                        start_animation = False
                        change_music = True
                        music = pygame.mixer.music.load(
                            os.path.join(s, 'sound_1.mp3'))

        pygame.display.update()
        tick += 1
        animation_tick += 1
     # pygame.display.flip()


if __name__ == '__main__':
    main()
