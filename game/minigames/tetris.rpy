# 文件：game/minigames/tetris.rpy

default persistent.tetris_high_score = 0

init python:
    import random
    import pygame
    from renpy.audio import sound
    from renpy.display.core import Displayable, IgnoreEvent
    from renpy.display.render import Render, render as render_displayable
    from renpy.exports import redraw, restart_interaction, timeout
    from renpy.text.text import Text

    # 俄罗斯方块形状
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 1], [1, 0, 0]],  # L
        [[1, 1, 1], [0, 0, 1]],  # J
        [[0, 1, 1], [1, 1, 0]],  # S
        [[1, 1, 0], [0, 1, 1]]   # Z
    ]

    # 颜色
    COLORS = [
        "#00FFFF",  # I - 青色
        "#FFFF00",  # O - 黄色
        "#800080",  # T - 紫色
        "#FFA500",  # L - 橙色
        "#0000FF",  # J - 蓝色
        "#00FF00",  # S - 绿色
        "#FF0000"   # Z - 红色
    ]

    class TetrisGame(Displayable):
        def __init__(self):
            super().__init__()
            
            # 游戏区域参数
            self.BLOCK_SIZE = 30
            self.GRID_WIDTH = 10
            self.GRID_HEIGHT = 20
            self.GAME_WIDTH = self.GRID_WIDTH * self.BLOCK_SIZE
            self.GAME_HEIGHT = self.GRID_HEIGHT * self.BLOCK_SIZE
            self.LEFT, self.RIGHT, self.TOP, self.BOTTOM = 0, 0, 0, 0
            self.initialized = False
            
            # 游戏状态
            self.reset()
            
            # 音效
            self.bgm = "audio/tetris_bgm.mp3"  # 需要准备音效文件
            self.clear_sound = "audio/tetris_clear.mp3"
            self.drop_sound = "audio/tetris_drop.mp3"

        def start_music(self):
            """开始播放背景音乐"""
            if renpy.loadable(self.bgm):
                renpy.music.play(self.bgm, loop=True, fadein=1.0, channel="music")

        def stop_music(self):
            """停止音乐"""
            renpy.music.stop(channel="music")

        def reset(self):
            """重置游戏"""
            self.board = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
            self.current_piece = self.new_piece()
            self.next_piece = self.new_piece()
            self.score = 0
            self.level = 1
            self.lines_cleared = 0
            self.game_over = False
            self.paused = False
            self.fall_time = 0
            self.fall_speed = 0.5  # 初始下落速度（秒）
            self.old_st = None
            
            # 最高分
            self.high_score = getattr(persistent, "tetris_high_score", 0)
            if self.high_score is None:
                self.high_score = 0

        def new_piece(self):
            """创建新方块"""
            shape_idx = random.randint(0, len(SHAPES) - 1)
            return {
                'shape': SHAPES[shape_idx],
                'color': COLORS[shape_idx],
                'x': self.GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
                'y': 0
            }

        def valid_move(self, piece, x_offset=0, y_offset=0):
            """检查移动是否有效"""
            shape = piece['shape']
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        new_x = piece['x'] + x + x_offset
                        new_y = piece['y'] + y + y_offset
                        
                        if (new_x < 0 or new_x >= self.GRID_WIDTH or 
                            new_y >= self.GRID_HEIGHT or 
                            (new_y >= 0 and self.board[new_y][new_x])):
                            return False
            return True

        def rotate_piece(self):
            """旋转当前方块"""
            # 转置矩阵并反转每一行来实现旋转
            shape = self.current_piece['shape']
            rotated = [[shape[y][x] for y in range(len(shape)-1, -1, -1)] 
                        for x in range(len(shape[0]))]
            
            old_shape = self.current_piece['shape']
            self.current_piece['shape'] = rotated
            
            if not self.valid_move(self.current_piece):
                self.current_piece['shape'] = old_shape

        def lock_piece(self):
            """将方块锁定到棋盘上"""
            shape = self.current_piece['shape']
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        board_y = self.current_piece['y'] + y
                        if board_y >= 0:  # 只在有效区域内锁定
                            self.board[board_y][self.current_piece['x'] + x] = self.current_piece['color']
            
            # 检查并清除完整的行
            lines_to_clear = []
            for y in range(self.GRID_HEIGHT):
                if all(self.board[y]):
                    lines_to_clear.append(y)
            
            if lines_to_clear:
                self.clear_lines(lines_to_clear)
                if renpy.loadable(self.clear_sound):
                    sound.play(self.clear_sound)
            
            # 生成新方块
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            
            # 检查游戏是否结束
            if not self.valid_move(self.current_piece):
                self.game_over = True
                # 更新最高分
                if self.score > self.high_score:
                    self.high_score = self.score
                    persistent.tetris_high_score = self.high_score
                    renpy.save_persistent()

        def clear_lines(self, lines):
            """清除完整的行并计分"""
            lines.sort(reverse=True)
            for line in lines:
                del self.board[line]
                self.board.insert(0, [0 for _ in range(self.GRID_WIDTH)])
            
            # 计分系统
            cleared = len(lines)
            self.lines_cleared += cleared
            self.score += [100, 300, 500, 800][min(cleared-1, 3)] * self.level
            
            # 升级系统
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.1, 0.5 - (self.level - 1) * 0.05)

        def move(self, dx, dy):
            """移动当前方块"""
            if self.valid_move(self.current_piece, dx, dy):
                self.current_piece['x'] += dx
                self.current_piece['y'] += dy
                return True
            return False

        def drop(self):
            """快速下落"""
            while self.move(0, 1):
                pass
            self.lock_piece()
            if renpy.loadable(self.drop_sound):
                sound.play(self.drop_sound)

        def setup_positions(self, screen_width, screen_height):
            """在第一次渲染时计算游戏区域并设置初始位置"""
            self.LEFT = (screen_width - self.GAME_WIDTH) // 2
            self.TOP = (screen_height - self.GAME_HEIGHT) // 2
            self.RIGHT = self.LEFT + self.GAME_WIDTH
            self.BOTTOM = self.TOP + self.GAME_HEIGHT
            self.initialized = True

        def render(self, width, height, st, at):
            if not self.initialized:
                self.setup_positions(width, height)

            r = Render(width, height)
            
            if self.old_st is None:
                self.old_st = st
            delta = st - self.old_st
            self.old_st = st

            # 游戏逻辑更新
            if not self.game_over and not self.paused:
                self.fall_time += delta
                if self.fall_time >= self.fall_speed:
                    self.fall_time = 0
                    if not self.move(0, 1):
                        self.lock_piece()

            # 背景
            bg = Solid("#00000080", xsize=width, ysize=height)
            r.blit(render_displayable(bg, width, height, st, at), (0, 0))

            # 绘制游戏区域边框
            border_width = self.GRID_WIDTH * self.BLOCK_SIZE + 4
            border_height = self.GRID_HEIGHT * self.BLOCK_SIZE + 4
            border = Solid("#FFFFFF", xsize=border_width, ysize=border_height)
            r.blit(render_displayable(border, width, height, st, at), 
                    (self.LEFT - 2, self.TOP - 2))
            
            # 游戏区域背景
            game_bg = Solid("#000000", xsize=border_width-4, ysize=border_height-4)
            r.blit(render_displayable(game_bg, width, height, st, at), 
                    (self.LEFT, self.TOP))

            # 绘制已锁定的方块
            for y in range(self.GRID_HEIGHT):
                for x in range(self.GRID_WIDTH):
                    if self.board[y][x]:
                        block = Solid(self.board[y][x], 
                                    xsize=self.BLOCK_SIZE-2, 
                                    ysize=self.BLOCK_SIZE-2)
                        r.blit(render_displayable(block, width, height, st, at),
                                (self.LEFT + x * self.BLOCK_SIZE + 1,
                                self.TOP + y * self.BLOCK_SIZE + 1))

            # 绘制当前方块
            if not self.game_over:
                shape = self.current_piece['shape']
                for y, row in enumerate(shape):
                    for x, cell in enumerate(row):
                        if cell:
                            block = Solid(self.current_piece['color'],
                                        xsize=self.BLOCK_SIZE-2,
                                        ysize=self.BLOCK_SIZE-2)
                            r.blit(render_displayable(block, width, height, st, at),
                                    (self.LEFT + (self.current_piece['x'] + x) * self.BLOCK_SIZE + 1,
                                    self.TOP + (self.current_piece['y'] + y) * self.BLOCK_SIZE + 1))

            # 绘制信息面板
            self.draw_info_panel(r, width, height, st, at)

            # 绘制游戏状态
            if self.paused:
                self.draw_pause_screen(r, width, height, st, at)
            elif self.game_over:
                self.draw_game_over_screen(r, width, height, st, at)

            redraw(self, 0)
            return r

        def draw_info_panel(self, r, width, height, st, at):
            """绘制信息面板"""
            panel_x = self.LEFT + self.GRID_WIDTH * self.BLOCK_SIZE + 20
            panel_width = 200
            
            # 下一个方块预览
            next_text = Text("下一个:", size=24, color="#FFFFFF")
            next_rend = render_displayable(next_text, width, height, st, at)
            r.blit(next_rend, (panel_x, self.TOP))
            
            # 绘制下一个方块
            next_shape = self.next_piece['shape']
            preview_x = panel_x + 20
            preview_y = self.TOP + 40
            for y, row in enumerate(next_shape):
                for x, cell in enumerate(row):
                    if cell:
                        block = Solid(self.next_piece['color'],
                                    xsize=self.BLOCK_SIZE-2,
                                    ysize=self.BLOCK_SIZE-2)
                        r.blit(render_displayable(block, width, height, st, at),
                                (preview_x + x * self.BLOCK_SIZE,
                                preview_y + y * self.BLOCK_SIZE))

            # 分数信息
            info_y = preview_y + len(next_shape) * self.BLOCK_SIZE + 30
            
            score_text = Text(f"分数: {self.score}", size=24, color="#FFFFFF")
            score_rend = render_displayable(score_text, width, height, st, at)
            r.blit(score_rend, (panel_x, info_y))
            
            high_score_text = Text(f"最高分: {self.high_score}", size=20, color="#FFFF00")
            high_score_rend = render_displayable(high_score_text, width, height, st, at)
            r.blit(high_score_rend, (panel_x, info_y + 40))
            
            level_text = Text(f"等级: {self.level}", size=20, color="#00FF00")
            level_rend = render_displayable(level_text, width, height, st, at)
            r.blit(level_rend, (panel_x, info_y + 70))
            
            lines_text = Text(f"消除行: {self.lines_cleared}", size=20, color="#00FFFF")
            lines_rend = render_displayable(lines_text, width, height, st, at)
            r.blit(lines_rend, (panel_x, info_y + 100))

            # 控制提示
            controls_y = self.TOP + self.GRID_HEIGHT * self.BLOCK_SIZE - 100
            controls_text = Text("方向键移动\n上键旋转\n空格键快速下落\nP暂停", 
                                size=18, color="#CCCCCC")
            controls_rend = render_displayable(controls_text, width, height, st, at)
            r.blit(controls_rend, (panel_x, controls_y))

        def draw_pause_screen(self, r, width, height, st, at):
            """绘制暂停屏幕"""
            overlay = Solid("#00000099", xsize=width, ysize=height)
            r.blit(render_displayable(overlay, width, height, st, at), (0, 0))
            
            pause_text = Text("游戏暂停", size=48, color="#FFFF66")
            pause_rend = render_displayable(pause_text, width, height, st, at)
            r.blit(pause_rend, (width//2 - pause_rend.width//2, height//2 - 50))
            
            continue_text = Text("按 P 继续游戏", size=32, color="#FFFFFF")
            continue_rend = render_displayable(continue_text, width, height, st, at)
            r.blit(continue_rend, (width//2 - continue_rend.width//2, height//2 + 20))

        def draw_game_over_screen(self, r, width, height, st, at):
            """绘制游戏结束屏幕"""
            overlay = Solid("#00000099", xsize=width, ysize=height)
            r.blit(render_displayable(overlay, width, height, st, at), (0, 0))
            
            over_text = Text("游戏结束!", size=48, color="#FF6666")
            over_rend = render_displayable(over_text, width, height, st, at)
            r.blit(over_rend, (width//2 - over_rend.width//2, height//2 - 80))
            
            score_text = Text(f"最终分数: {self.score}", size=36, color="#FFFFFF")
            score_rend = render_displayable(score_text, width, height, st, at)
            r.blit(score_rend, (width//2 - score_rend.width//2, height//2 - 20))
            
            if self.score > self.high_score:
                record_text = Text("新纪录!", size=32, color="#FFFF00")
                record_rend = render_displayable(record_text, width, height, st, at)
                r.blit(record_rend, (width//2 - record_rend.width//2, height//2 + 20))
            
            restart_text = Text("按 R 重新开始 | ESC 返回", size=28, color="#CCCCCC")
            restart_rend = render_displayable(restart_text, width, height, st, at)
            r.blit(restart_rend, (width//2 - restart_rend.width//2, height//2 + 80))

        def event(self, ev, x, y, st):
            if self.game_over:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_r:
                        self.reset()
                        restart_interaction()
                    elif ev.key == pygame.K_ESCAPE:
                        self.stop_music()
                        return f"score:{self.score}"
                raise IgnoreEvent()

            if ev.type == pygame.KEYDOWN:
                if not self.paused:
                    if ev.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    elif ev.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    elif ev.key == pygame.K_DOWN:
                        self.move(0, 1)
                    elif ev.key == pygame.K_UP:
                        self.rotate_piece()
                    elif ev.key == pygame.K_SPACE:
                        self.drop()
                
                if ev.key == pygame.K_p:
                    self.paused = not self.paused
                    restart_interaction()
                elif ev.key == pygame.K_ESCAPE:
                    self.stop_music()
                    return f"score:{self.score}"

            raise IgnoreEvent()

# 屏幕定义
screen tetris(tetris_game):
    add "images/cg/bg tetris.jpg"  # 可以准备一个俄罗斯方块背景图
    add tetris_game xalign 0.5 yalign 0.5
    text "俄罗斯方块" xpos 0.5 ypos 0.05 xanchor 0.5 size 50 color "#FFFFFF" outlines [(2, "#000")]

# 游戏标签
label play_tetris:
    window hide
    $ quick_menu = False

    # 创建游戏实例并开始音乐
    $ tetris_game = TetrisGame()
    $ tetris_game.start_music()
    
    call screen tetris(tetris_game)
    $ result = _return

    $ quick_menu = True
    window show
    
    # 停止音乐
    $ tetris_game.stop_music()
    
    # 处理游戏结果
    if result and result.startswith("score:"):
        $ score = int(result.split(":")[1])
        $ high_score = getattr(persistent, "tetris_high_score", 0)
        if high_score is None:
            $ high_score = 0
        
        if score >= 5000:
            yt "『太厉害了！你是俄罗斯方块大师！』"
        elif score >= 3000:
            yt "『很棒的成绩！你的反应真快！』"
        elif score >= 1500:
            yt "『不错不错，已经掌握技巧了！』"
        elif score >= 500:
            yt "『有进步！继续加油！』"
        else:
            yt "『第一次玩吧？多练习几次会更好的！』"
            
        if score > high_score:
            yt "『恭喜你创造了新的最高分纪录！』"
    else:
        yt "『你中途退出了？下次再来挑战吧～』"

    return