# 游戏脚本文件：game/minigames/snake.rpy

init python:
    import random
    import pygame
    from renpy.audio import sound
    from renpy.display.core import Displayable, IgnoreEvent
    from renpy.display.render import Render, render as render_displayable
    from renpy.exports import redraw, restart_interaction, timeout
    from renpy.text.text import Text

    class SnakeGame(Displayable):
        def __init__(self):
            super().__init__()

            # 区域参数
            self.LEFT, self.RIGHT = 200, 1300
            self.TOP, self.BOTTOM = 200, 800
            self.SIZE = 30

            # 触摸控制参数
            self.touch_start = None
            self.min_swipe_distance = 50  # 最小滑动距离

            # 初始状态
            self.reset()

            # 音效文件路径
            self.bgm = "audio/snake bgm.MP3"
            self.eat_sound = "audio/snake eat.MP3"
            self.over_sound = "audio/snake game over.MP3"

        def start_music(self):
            """开始播放背景音乐"""
            renpy.music.play(self.bgm, loop=True, fadein=1.0, channel="music")

        def stop_music(self):
            """停止贪吃蛇背景音乐"""
            renpy.music.stop(channel="music")

        def reset(self):
            self.snake = [(400, 400), (370, 400), (340, 400)]
            self.direction = (1, 0)
            self.next_direction = (1, 0)
            self.food = self.new_food()
            self.score = 0
            # 修复：确保 high_score 是整数
            self.high_score = getattr(persistent, "snake_high_score", 0)
            if self.high_score is None:
                self.high_score = 0
            self.speed = 0.12
            self.game_over = False
            self.paused = False
            self.time_accum = 0
            self.old_st = None

        def new_food(self):
            while True:
                x = random.randrange(self.LEFT, self.RIGHT, self.SIZE)
                y = random.randrange(self.TOP, self.BOTTOM, self.SIZE)
                if (x, y) not in self.snake:
                    return (x, y)

        def check_collision(self, head, food):
            """改进的碰撞检测：检查头部与食物的重叠"""
            head_rect = pygame.Rect(head[0], head[1], self.SIZE, self.SIZE)
            food_rect = pygame.Rect(food[0], food[1], self.SIZE, self.SIZE)
            return head_rect.colliderect(food_rect)

        def render(self, width, height, st, at):
            r = Render(width, height)
            if self.old_st is None:
                self.old_st = st
            delta = st - self.old_st
            self.old_st = st

            if not self.game_over and not self.paused:
                self.time_accum += delta
                if self.time_accum > self.speed:
                    self.time_accum -= self.speed
                    self.move()

            # 背景
            bg = Solid("#00000080", xsize=width, ysize=height)
            r.blit(render_displayable(bg, width, height, st, at), (0, 0))

            # 绘制游戏区域边框
            border = Solid("#FFFFFF", xsize=self.RIGHT - self.LEFT + 4, ysize=self.BOTTOM - self.TOP + 4)
            r.blit(render_displayable(border, width, height, st, at), (self.LEFT - 2, self.TOP - 2))
            
            inner_bg = Solid("#000000", xsize=self.RIGHT - self.LEFT, ysize=self.BOTTOM - self.TOP)
            r.blit(render_displayable(inner_bg, width, height, st, at), (self.LEFT, self.TOP))

            # 蛇 - 渐变颜色
            for i, (x, y) in enumerate(self.snake):
                # 蛇头用不同颜色
                if i == 0:
                    color = "#00FFAA"  # 蛇头 - 青色
                else:
                    # 蛇身渐变 - 从亮绿到暗绿
                    progress = i / len(self.snake)
                    green = int(255 * (1 - progress * 0.5))
                    color = f"#00{green:02X}00"
                
                block = Solid(color, xsize=self.SIZE-2, ysize=self.SIZE-2)
                r.blit(render_displayable(block, width, height, st, at), (x+1, y+1))

            # 食物 - 简单样式
            food_size = self.SIZE - 4
            food_x, food_y = self.food
            food_circle = Solid("#FF3333", xsize=food_size, ysize=food_size)
            r.blit(render_displayable(food_circle, width, height, st, at), (food_x+2, food_y+2))

            # 分数面板
            panel_width = 300
            panel_height = 120
            panel = Solid("#000000CC", xsize=panel_width, ysize=panel_height)
            r.blit(render_displayable(panel, width, height, st, at), (self.LEFT, self.TOP - panel_height - 10))

            # 当前分数
            score_text = Text(f"得分: {self.score}", size=32, color="#FFFFFF", outlines=[(2, "#000000")])
            score_rend = render_displayable(score_text, width, height, st, at)
            r.blit(score_rend, (self.LEFT + 20, self.TOP - panel_height))

            # 最高分
            high_score_text = Text(f"最高分: {self.high_score}", size=28, color="#FFFF00", outlines=[(1, "#000000")])
            high_score_rend = render_displayable(high_score_text, width, height, st, at)
            r.blit(high_score_rend, (self.LEFT + 20, self.TOP - panel_height + 40))

            # 长度显示
            length_text = Text(f"长度: {len(self.snake)}", size=24, color="#AAAAAA", outlines=[(1, "#000000")])
            length_rend = render_displayable(length_text, width, height, st, at)
            r.blit(length_rend, (self.LEFT + 20, self.TOP - panel_height + 80))

            # 控制提示
            if not self.game_over and not self.paused:
                controls_text = Text("WASD/方向键控制 | 滑动触摸屏 | P暂停", size=20, color="#CCCCCC")
                controls_rend = render_displayable(controls_text, width, height, st, at)
                r.blit(controls_rend, (width//2 - controls_rend.width//2, self.BOTTOM + 20))

            # 状态提示
            if self.paused:
                # 半透明覆盖层
                overlay = Solid("#00000099", xsize=width, ysize=height)
                r.blit(render_displayable(overlay, width, height, st, at), (0, 0))
                
                pause_text = Text("游戏暂停", size=48, color="#FFFF66", outlines=[(3, "#000000")])
                pause_rend = render_displayable(pause_text, width, height, st, at)
                r.blit(pause_rend, (width//2 - pause_rend.width//2, height//2 - 50))
                
                continue_text = Text("按 P 继续游戏", size=32, color="#FFFFFF", outlines=[(2, "#000000")])
                continue_rend = render_displayable(continue_text, width, height, st, at)
                r.blit(continue_rend, (width//2 - continue_rend.width//2, height//2 + 20))
                
            elif self.game_over:
                # 半透明覆盖层
                overlay = Solid("#00000099", xsize=width, ysize=height)
                r.blit(render_displayable(overlay, width, height, st, at), (0, 0))
                
                over_text = Text("游戏结束!", size=48, color="#FF6666", outlines=[(3, "#000000")])
                over_rend = render_displayable(over_text, width, height, st, at)
                r.blit(over_rend, (width//2 - over_rend.width//2, height//2 - 80))
                
                final_score_text = Text(f"最终得分: {self.score}", size=36, color="#FFFFFF", outlines=[(2, "#000000")])
                final_score_rend = render_displayable(final_score_text, width, height, st, at)
                r.blit(final_score_rend, (width//2 - final_score_rend.width//2, height//2 - 20))
                
                # 修复：确保比较的是整数
                current_score = self.score
                current_high_score = self.high_score if self.high_score is not None else 0
                
                if current_score > current_high_score:
                    new_record_text = Text("新纪录!", size=32, color="#FFFF00", outlines=[(2, "#000000")])
                    new_record_rend = render_displayable(new_record_text, width, height, st, at)
                    r.blit(new_record_rend, (width//2 - new_record_rend.width//2, height//2 + 20))
                
                restart_text = Text("按 R 重新开始 | ESC 返回", size=28, color="#CCCCCC", outlines=[(1, "#000000")])
                restart_rend = render_displayable(restart_text, width, height, st, at)
                r.blit(restart_rend, (width//2 - restart_rend.width//2, height//2 + 80))

            redraw(self, 0)
            return r

        def move(self):
            # 改变方向
            if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction

            head = (self.snake[0][0] + self.direction[0] * self.SIZE,
                    self.snake[0][1] + self.direction[1] * self.SIZE)

            # 撞墙或撞自己
            if (head in self.snake or head[0] < self.LEFT or head[0] >= self.RIGHT or
                head[1] < self.TOP or head[1] >= self.BOTTOM):
                self.game_over = True
                # 更新最高分 - 修复：确保比较的是整数
                current_score = self.score
                current_high_score = self.high_score if self.high_score is not None else 0
                
                if current_score > current_high_score:
                    self.high_score = current_score
                    persistent.snake_high_score = self.high_score
                    renpy.save_persistent()
                sound.play(self.over_sound)
                timeout(0)
                return

            # 吃食物 - 使用改进的碰撞检测
            if self.check_collision(head, self.food):
                sound.play(self.eat_sound)
                self.score += 1
                # 每得5分加速
                if self.score % 5 == 0:
                    self.speed = max(0.05, self.speed - 0.01)
                self.snake = [head] + self.snake
                self.food = self.new_food()
            else:
                self.snake = [head] + self.snake[:-1]

        def handle_swipe(self, start_pos, end_pos):
            """处理滑动方向"""
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            
            # 确定主要滑动方向
            if abs(dx) > abs(dy) and abs(dx) > self.min_swipe_distance:
                # 水平滑动
                if dx > 0:
                    self.next_direction = (1, 0)  # 右
                else:
                    self.next_direction = (-1, 0)  # 左
            elif abs(dy) > abs(dx) and abs(dy) > self.min_swipe_distance:
                # 垂直滑动
                if dy > 0:
                    self.next_direction = (0, 1)  # 下
                else:
                    self.next_direction = (0, -1)  # 上

        def event(self, ev, x, y, st):
            # 触摸事件处理
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.touch_start = (x, y)
                
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.touch_start:
                self.handle_swipe(self.touch_start, (x, y))
                self.touch_start = None

            if self.game_over:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_r:
                        self.reset()
                        restart_interaction()
                    elif ev.key == pygame.K_ESCAPE:
                        self.stop_music()  # 停止音乐
                        return f"score:{self.score}"
                raise IgnoreEvent()

            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_w, pygame.K_UP):
                    self.next_direction = (0, -1)
                elif ev.key in (pygame.K_s, pygame.K_DOWN):
                    self.next_direction = (0, 1)
                elif ev.key in (pygame.K_a, pygame.K_LEFT):
                    self.next_direction = (-1, 0)
                elif ev.key in (pygame.K_d, pygame.K_RIGHT):
                    self.next_direction = (1, 0)
                elif ev.key == pygame.K_p:
                    self.paused = not self.paused
                    restart_interaction()
                elif ev.key == pygame.K_ESCAPE:
                    self.stop_music()  # 停止音乐
                    return f"score:{self.score}"

            raise IgnoreEvent()


# --- screen 部分 ---
screen snake(snake_game):
    add "images/snake eat bg.jpg"
    add snake_game
    text "贪吃蛇小游戏" xpos 0.5 ypos 0.05 xanchor 0.5 size 50 color "#FFFFFF" outlines [(2, "#000")]

label play_snake:
    window hide
    $ quick_menu = False

    # 创建游戏实例并开始音乐
    $ snake_game = SnakeGame()
    $ snake_game.start_music()
    
    call screen snake(snake_game)
    $ result = _return

    $ quick_menu = True
    window show
    
    # 确保在退出游戏时停止音乐
    $ snake_game.stop_music()
    
    if result and result.startswith("score:"):
        $ score = int(result.split(":")[1])
        $ high_score = getattr(persistent, "snake_high_score", 0)
        if high_score is None:
            $ high_score = 0
        
        if score >= 20:
            yt "『太厉害了！你是贪吃蛇大师！』"
        elif score >= 15:
            yt "『很棒的成绩！你的反应真快！』"
        elif score >= 10:
            yt "『不错不错，已经掌握技巧了！』"
        elif score >= 5:
            yt "『有进步！继续加油！』"
        else:
            yt "『第一次玩吧？多练习几次会更好的！』"
            
        # 检查是否打破纪录
        if score > high_score:
            yt "『恭喜你创造了新的最高分纪录！』"
    else:
        yt "『你中途退出了？下次再来挑战吧～』"

    return