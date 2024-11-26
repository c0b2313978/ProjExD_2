import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, 5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (5, 0)}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(surface_rect: pg.Rect) -> tuple[bool, bool]:
    """
    画面内or画面外の判定をする
    - 引数: こうかとんRect or 爆弾Rect
    - 戻り値: 横方向・縦方向の真理値タプル（True: 画面内 / False: 画面外）
    """
    screen_inside_x = True
    screen_inside_y = True
    if surface_rect.left < 0 or WIDTH < surface_rect.right:
        screen_inside_x = False
    if surface_rect.top < 0 or HEIGHT < surface_rect.bottom:
        screen_inside_y = False
    return screen_inside_x, screen_inside_y


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for pressing_key in DELTA:
            if key_lst[pressing_key]:
                sum_mv[0] += DELTA[pressing_key][0]
                sum_mv[1] += DELTA[pressing_key][1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_inside_x, bb_inside_y = check_bound(bb_rct)
        if not bb_inside_x:
            vx *= -1
        if not bb_inside_y:
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)

        

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
