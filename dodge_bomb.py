import  random
import sys

import pygame as pg


delta = {
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, +1),
    pg.K_RIGHT: (+1, 0),
    pg.K_LEFT: (-1, 0)
        }  # 練習4


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool, bool]:
        """
        オブジェクトが画面外or画面内かを判定し、真理値タプルを返す関数
        引数１：画面Surfaceのrect
        引数２：こうかとんまたは爆弾Surfaceのrect
        戻り値：横方向・縦方向のはみ出し判定結果（画面外：True, 画面内：False）
        """
        yoko, tate = True, True
        if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
             yoko = False
        if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
             tate = False
        return yoko, tate
        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_lose = pg.image.load("ex02/fig/8.png")
    kk_lose = pg.transform.rotozoom(kk_lose, 0, 2.0)
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  # 練習4
    kk_rct.center = 900, 400  # 練習4
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習１
    bb_img.set_colorkey((0, 0, 0))  # 練習１
    x, y = random.randint(0, 1600), random.randint(0, 900)  # 練習2
    #screen.blit(bb_image, [x, y])  # 練習2
    vx, vy = +1, +1  # 練習3
    bb_rct = bb_img.get_rect()  # 練習3
    bb_rct.center = x, y  # 練習3
    tmr = 0

    muki_8 = {
    (0, -1): pg.transform.rotozoom(kk_img, -90, 1.0),
    (+1, -1): pg.transform.rotozoom((pg.transform.flip(kk_img, False, True)), -135, 1.0),
    (+1, 0): pg.transform.rotozoom((pg.transform.flip(kk_img, False, True)), -180, 1.0),
    (+1, +1): pg.transform.rotozoom((pg.transform.flip(kk_img, False, True)), 135, 1.0),
    (0, +1): pg.transform.rotozoom(kk_img, 90, 1.0),
    (-1, +1): pg.transform.rotozoom(kk_img, 45, 1.0),
    (-1, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
    (-1, -1): pg.transform.rotozoom(kk_img, -45, 1.0)
        }  # こうかとんの進行方向から画像の向きを決定する辞書

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1

        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)  # 練習４
                kk_img = muki_8[mv]
        if check_bound(screen.get_rect(), kk_rct) != (True, True):
             for k, mv in delta.items():
                 if key_lst[k]:
                     kk_rct.move_ip(-mv[0], -mv[1])

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 練習3
        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
             vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
             vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習3
        if kk_rct.colliderect(bb_rct):
             # ゲームオーバー後の画像表示
             screen.blit(bg_img, [0, 0])
             screen.blit(kk_lose, kk_rct)
             pg.display.update()
             pg.time.delay(500)
             return
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()