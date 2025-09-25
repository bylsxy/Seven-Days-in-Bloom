init python:
    from renpy.audio import sound
    from renpy.display.core import Displayable, IgnoreEvent
    from renpy.display.render import Render, render as render_displayable
    from renpy.exports import redraw, restart_interaction, timeout

    class PongDisplayable(Displayable):
        def __init__(self):
            super().__init__()

            #游戏参数
            self.PADDLE_WIDTH = 22
            self.PADDLE_HEIGHT = 142
            self.PADDLE_X = 360
            self.BALL_WIDTH = 22
            self.BALL_HEIGHT = 22
            self.COURT_TOP = 193
            self.COURT_BOTTOM = 975

            #元素
            self.paddle = Solid("#ffffff", xsize=self.PADDLE_WIDTH, ysize=self.PADDLE_HEIGHT)
            self.ball = Solid("#ffffff", xsize=self.BALL_WIDTH, ysize=self.BALL_HEIGHT)

            #状态
            self.stuck = True
            # 初始化球拍位置于球场中心
            self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2 + self.COURT_TOP
            self.computery = self.playery
            self.computerspeed = 570.0
            self.bx = self.PADDLE_X + self.PADDLE_WIDTH + 15
            self.by = self.playery
            self.bdx = .5
            self.bdy = .5
            self.bspeed = 525.0
            self.oldst = None
            self.winner = None

        def visit(self):
            return [self.paddle, self.ball]

        def render(self, width, height, st, at):
            r = Render(width, height)

            if self.oldst is None:
                self.oldst = st
            dtime = st - self.oldst
            self.oldst = st

            #球移动逻辑
            speed = dtime * self.bspeed
            oldbx = self.bx

            if self.stuck:
                self.by = self.playery
            else:
                self.bx += self.bdx * speed
                self.by += self.bdy * speed

            #电脑移动
            cspeed = self.computerspeed * dtime
            if abs(self.by - self.computery) <= cspeed:
                self.computery = self.by
            else:
                self.computery += cspeed * (self.by - self.computery) / abs(self.by - self.computery)

            #碰撞检测
            ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
            if self.by < ball_top:
                self.by = ball_top + (ball_top - self.by)
                self.bdy = -self.bdy
                if not self.stuck:
                    sound.play("pong_beep.opus", channel=0)

            ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
            if self.by > ball_bot:
                self.by = ball_bot - (self.by - ball_bot)
                self.bdy = -self.bdy
                if not self.stuck:
                    sound.play("pong_beep.opus", channel=0)

            #球拍渲染和碰撞
            def paddle(px, py, hotside):
                pi = render_displayable(self.paddle, width, height, st, at)
                r.blit(pi, (int(px), int(py - self.PADDLE_HEIGHT / 2)))

                if py - self.PADDLE_HEIGHT / 2 <= self.by <= py + self.PADDLE_HEIGHT / 2:
                    hit = False
                    if oldbx >= hotside >= self.bx:
                        self.bx = hotside + (hotside - self.bx)
                        self.bdx = -self.bdx
                        hit = True
                    elif oldbx <= hotside <= self.bx:
                        self.bx = hotside - (self.bx - hotside)
                        self.bdx = -self.bdx
                        hit = True
                    if hit:
                        sound.play("pong_boop.opus", channel=1)
                        self.bspeed *= 1.10

            paddle(self.PADDLE_X, self.playery, self.PADDLE_X + self.PADDLE_WIDTH)
            paddle(width - self.PADDLE_X - self.PADDLE_WIDTH, self.computery, width - self.PADDLE_X - self.PADDLE_WIDTH)

            #?
            ball = render_displayable(self.ball, width, height, st, at)
            r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2), int(self.by - self.BALL_HEIGHT / 2)))

            #结束
            if self.bx < -75:
                self.winner = "computer"
                timeout(0)
            elif self.bx > width + 75:
                self.winner = "player"
                timeout(0)

            redraw(self, 0)
            return r

        def event(self, ev, x, y, st):
            import pygame
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False
                restart_interaction()

            y = max(y, self.COURT_TOP)
            y = min(y, self.COURT_BOTTOM)
            self.playery = y

            if self.winner:
                return self.winner
            raise IgnoreEvent()

screen pong():
    default pong = PongDisplayable()
    add "bg pong" #背景
    add pong #游戏

    #例字
    text "Youtai":
        xpos 360
        xanchor 0.5
        ypos 37
        size 60

    text "电脑":
        xpos 1560
        xanchor 0.5
        ypos 37
        size 60

    #开始提示
    if pong.stuck:
        text "点击开始游戏":
            xalign 0.5
            ypos 75
            size 60

# 游戏入口标签
label play_pong:
    window hide
    $ quick_menu = False

    call screen pong

    $ quick_menu = True
    window show

    if _return == "computer":
        yt "『……』"
        yt "『哈——哈，其实我放水了啦』"
        yt "『我认真起来区区电脑又能怎样』"
        "电脑突然嗡嗡地叫了两声。"
        "看起来机魂大不悦。"

    else:
        yt "『哈哈』"
        yt "『喂，你就是逊啦』"
        "电脑突然嗡嗡地叫了两声。"
        "看起来机魂大不悦。"

    return
