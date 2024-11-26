import os
import random
import sys
import pygame as pg
import time


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


def gameover(screen: pg.Surface) -> None:
    kkkkkk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    black_out = pg.Surface((WIDTH, HEIGHT))
    
    pg.draw.rect(black_out, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black_out.set_alpha(200)
    screen.blit(black_out, [0, 0])

    screen.blit(txt, [WIDTH/2 - txt.get_width()/2, HEIGHT/2 - txt.get_height()/2])
    screen.blit(kkkkkk_img, [WIDTH/2 - txt.get_width()/2 - kkkkkk_img.get_width() - 20, HEIGHT/2 - kkkkkk_img.get_height()/2])
    screen.blit(kkkkkk_img, [WIDTH/2 + txt.get_width()/2 + kkkkkk_img.get_width() - 10, HEIGHT/2 - kkkkkk_img.get_height()/2])

    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    accs = [a for a in range(1, 11)]

    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    
    return bb_imgs, accs


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

    bb_imgs, bb_accs = init_bb_imgs()

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return  # ゲームオーバー

        # 特定のキーが押されたときにこうかとんが移動
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

        # 爆弾の拡大加速
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        
        bb_inside_x, bb_inside_y = check_bound(bb_rct)
        if not bb_inside_x:
            vx *= -1
        if not bb_inside_y:
            vy *= -1

        screen.blit(bb_img, bb_rct)







        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
