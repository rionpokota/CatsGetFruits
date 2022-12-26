#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple
from random import randint
import pyxel

Point = namedtuple("Point", ["w", "h"])  # 猫の向き　正の数で左向き　負の数で右向き

UP = Point(-16, 16)
DOWN = Point(-16, 16)
RIGHT = Point(-16, 16)
LEFT = Point(-16, 16)

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Cats Get Fruits", fps=30)
        pyxel.load("./assets/chara.pyxres")
        self.timer = 0

        # 初期化
        self.start_flg = False
        self.direction = RIGHT
        self.shot_flg = False
        self.shot_holdflg = False
        self.shot_x = 0
        self.shot_y = 0
        self.score = 0
        self.cat_life = 3
        self.cat_is_active = True
        self.cat_x = 42
        self.cat_y = 60
        self.cat_vy = 0
        self.dokuro_hitflg = False
        self.apple = [(i * 60, randint(0, 104), True) for i in range(4)]
        self.dokuro = [(j * 60, randint(0, 104), True) for j in range(4)]
        self.oneup = [(k, randint(0, 104), False) for k in range(1)]

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_RETURN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START):
            self.start_flg = True

        self.update_cat()

        for i, v in enumerate(self.apple):
            self.apple[i] = self.update_apple(*v)

        for j, w in enumerate(self.dokuro):
            self.dokuro[j] = self.update_dokuro(*w)

        if self.timer >= 300:
            for k, x in enumerate(self.oneup):
                self.oneup[k] = self.update_oneup(*x)

        self.timer += 1

    def update_cat(self):
        if self.start_flg and self.cat_is_active:
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.cat_x = max(self.cat_x - 3, 0)
                self.direction = LEFT

            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.cat_x = min(self.cat_x + 3, pyxel.width - 16)
                self.direction = RIGHT

            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.cat_y = max(self.cat_y - 3, 0)
                self.direction = UP

            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                self.cat_y = min(self.cat_y + 3, pyxel.height - 16)
                self.direction = DOWN

            if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
                self.shot_flg = True

        else:
            if pyxel.btn(pyxel.KEY_RETURN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START):
                # 初期化
                self.timer = 0
                self.direction = RIGHT
                self.shot_flg = False
                self.shot_holdflg = False
                self.shot_x = 0
                self.shot_y = 0
                self.score = 0
                self.cat_life = 3
                self.cat_is_active = True
                self.cat_x = 42
                self.cat_y = 60
                self.cat_vy = 0
                self.dokuro_hitflg = False
                self.apple = [(i * 60, randint(0, 104), True) for i in range(4)]
                self.dokuro = [(j * 60, randint(0, 104), True) for j in range(4)]
                self.oneup = [(k * 60, randint(0, 104), False) for k in range(1)]

                pyxel.playm(0, loop=True)
                pyxel.run(self.update, self.draw)

    def draw(self):
        # 背景カラー
        pyxel.cls(12)

        if not self.start_flg:
            title = "Cats Get Fruits"
            pyxel.text(53, 50, title, 1)
            pyxel.text(52, 50, title, 7)
            press_start = "PRESS ENTER or START"
            pyxel.text(43, 80, press_start, 1)
            pyxel.text(42, 80, press_start, 7)

        else:
            # フルーツを描く
            for x, y, is_active in self.apple:
                if is_active and self.cat_is_active:
                    pyxel.blt(x, y, 0, 16, 0, 16, 16, 7)

            # ドクロを描く
            for x, y, is_active in self.dokuro:
                if is_active and self.cat_is_active:
                    pyxel.blt(x, y, 0, 32, 0, 16, 16, 7)

            # 1UPを描く
            for x, y, is_active in self.oneup:
                if is_active and self.cat_is_active:
                    pyxel.blt(x, y, 0, 0, 16, 16, 16, 7)

            # 猫を描く
            if self.cat_is_active:
                pyxel.blt(
                    self.cat_x,
                    self.cat_y,
                    0,
                    16 if self.cat_vy > 0 else 0,
                    0,
                    self.direction[0],
                    self.direction[1],
                    7,
                )

                # 玉を描く
                if self.shot_flg:
                    self.shot()
                    if self.shot_x > 0:
                        pyxel.blt(self.shot_x, self.shot_y, 0, 48, 0, 16, 16, 7)

            # スコアを表示
            s = "Score {:>4}".format(self.score)
            pyxel.text(5, 4, s, 1)
            pyxel.text(4, 4, s, 7)

            # 猫の数を表示
            l = "Cats {:>2}".format(self.cat_life)
            pyxel.text(80, 4, l, 1)
            pyxel.text(79, 4, l, 7)

            # ゲームオーバーになった時表示
            if not self.cat_is_active:
                gameover = "GAME OVER"
                pyxel.text(65, 50, gameover, 1)
                pyxel.text(64, 50, gameover, 7)
                press = "RETRY PRESS ENTER or START"
                pyxel.text(30, 80, press, 1)
                pyxel.text(29, 80, press, 7)

    def update_apple(self, x, y, is_active):
        # 猫に触れたかどうかの判定
        if is_active and self.cat_is_active and abs(x - self.cat_x) < 12 and abs(y - self.cat_y) < 12:
            is_active = False
            self.score += 100
            self.cat_vy = min(self.cat_vy, -8)
            return x, y, is_active

        x -= 2

        # 端まで行ったら戻す
        if x < -40:
            x += 240
            y = randint(0, 104)
            is_active = True

        return x, y, is_active

    def update_dokuro(self, x, y, is_active):
        # 猫に触れたかどうかの判定
        if is_active and self.cat_is_active and abs(x - self.cat_x) < 12 and abs(y - self.cat_y) < 12:
            is_active = False
            self.cat_life -= 1
            # ゲームオーバー
            if self.cat_life == 0:
                self.cat_is_active = False

            self.cat_vy = min(self.cat_vy, -8)
            pyxel.play(3, 4)

        # 玉に当たったかどうかの判定
        if is_active and self.shot_flg and self.cat_is_active and abs(x - self.shot_x) < 12 and abs(
                y - self.shot_y) < 12:
            is_active = False
            self.dokuro_hitflg = True
            self.score += 10
            return x, y, is_active

        x -= 3

        # 端まで行ったら戻す
        if x < -40:
            x += 240
            y = randint(0, 104)
            is_active = True

        return x, y, is_active

    def update_oneup(self, x, y, is_active):
        # 猫に触れたかどうかの判定
        if is_active and self.cat_is_active and abs(x - self.cat_x) < 12 and abs(y - self.cat_y) < 12:
            is_active = False
            self.cat_life += 1
            self.timer = 0

        x += 2

        # 端まで行ったら戻す
        if x > 200:
            x -= 240
            y = randint(0, 104)
            is_active = True
            self.timer = 0

        return x, y, is_active

    def shot(self):
        if self.shot_flg:
            # 玉を出した地点の猫の座標を取る
            if not self.shot_holdflg:
                self.shot_x = self.cat_x
                self.shot_y = self.cat_y
                self.shot_holdflg = True

            self.shot_x += 4

            # ドクロにヒットするか端まで行ったら消す
            if self.dokuro_hitflg or self.shot_x > 200:
                self.shot_flg = False
                self.dokuro_hitflg = False
                self.shot_x = 0
                self.shot_holdflg = False

        return


if __name__ == "__main__":
    App()
