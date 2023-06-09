import pygame
import sys
import random
import time
import pandas as pd
import math

# 初始化 Pygame
pygame.init()

# 设置窗口大小
window_size = (400, 800)
screen = pygame.display.set_mode(window_size)

# 读取 data.csv 文件
data = pd.read_csv('data.csv')

Highest_score = data['Score'].max()

# 设置颜色
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# 设置玩家方块
player_width = 100  # 玩家方块宽度为100个像素
player_height = 50
player_pos = [100, window_size[1] - player_height]
player = pygame.Rect(player_pos[0], player_pos[1], player_width, player_height)

# 设置子弹
bullet_width = 20
bullet_height = 50
bullet_color = YELLOW
bullet_pos = [0, 0]
bullet = pygame.Rect(bullet_pos[0], bullet_pos[1], bullet_width, bullet_height)
bullet_state = "ready"  # 子弹状态：ready（准备发射）、fire（发射中）

# 设置随机方块
block_width = 100
block_height = 50
block_color = (255, 0, 0)
block_x_positions = [0, 100, 200, 300]  # 方块的 X 坐标位置

blocks = []  # 存储随机方块的列表

# 设置时间间隔和帧率
bullet_speed = 10  # 子弹的垂直速度（像素/帧）
fall_interval = 1.0 # 生成方塊的速度(塊/秒)
block_speed = 2.0 #方塊移動速度(像素/秒)
fall_interval_speed = 1.0
block_speed_control = 2.0  #方塊掉落速度
bullet_speed_control = 10 #子彈速度

# 设置字体
small_font = pygame.font.Font(None, 34)
font = pygame.font.Font(None, 38)
large_font = pygame.font.Font(None, 56)

# 设置分数、生命
score = 0
lives = 2

# 游戏状态
game_state = "start"  # 开始画面

# 倒计时
countdown = 3
countdown_font = pygame.font.Font(None, 100)
elapsed_time = 0  # 游戏时间

# 游戏主循环
clock = pygame.time.Clock()
last_fall_time = time.time()
difficulty = "Normal"  # 默认难度为普通

while True:
    # 检查事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 将游戏结果记录到 data.csv 文件
            game_result = {
                "Score": score,
                "Difficulty": difficulty,
                "Elapsed Time": elapsed_time
            }
            # 添加游戏结果到DataFrame
            game_result = pd.DataFrame({'Score': [score], 'Difficulty': [difficulty],
                                        'Elapsed Time': [elapsed_time]})
            data = pd.concat([data, game_result], ignore_index=True)

            # 将结果保存回data.csv文件
            data.to_csv('data.csv', index=False)

            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == "start":
                if event.key == pygame.K_1:
                    difficulty = "Easy"
                    fall_interval = 1.0  # 方块下落间隔时间（秒）
                    block_speed = 2.0
                    lives = 2
                    bullet_speed = 10
                elif event.key == pygame.K_2:
                    difficulty = "Normal"
                    fall_interval = 0.5  # 方块下落间隔时间（秒）
                    block_speed = 2.5
                    lives = 2
                    bullet_speed = 10
                elif event.key == pygame.K_3:
                    difficulty = "Hard"
                    fall_interval = 0.5  # 方块下落间隔时间（秒）
                    block_speed = 3.0
                    lives = 1
                    bullet_speed = 12
                elif event.key == pygame.K_SPACE:
                    game_state = "countdown"
                    countdown = 3
            elif game_state == "countdown":
                if event.key == pygame.K_SPACE:
                    game_state = "playing"
                    last_fall_time = time.time()

            elif game_state == "playing":
                if event.key == pygame.K_LEFT:
                    player.x -= player_width  # 左移一个玩家方块宽度
                    if player.left < 0:  # 防止超出左边界
                        player.left = 0
                elif event.key == pygame.K_RIGHT:
                    player.x += player_width  # 右移一个玩家方块宽度
                    if player.right > window_size[0]:  # 防止超出右边界
                        player.right = window_size[0]
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":  # 如果子弹准备好发射
                        bullet_state = "fire"
                        bullet.x = player.x + player_width // 2 - bullet_width // 2  # 子弹的初始位置在玩家方块的顶部中央
                        bullet.y = player.y - bullet_height

    # 游戏逻辑
    if game_state == "playing":
        # 移动子弹
        if bullet_state == "fire":
            bullet.y -= bullet_speed_control  # 子弹向上移动
            if bullet.y < 0:  # 如果子弹超出窗口上方，重置为准备状态
                bullet_state = "ready"

        # 添加随机方块
        current_time = time.time()
        if current_time - last_fall_time > fall_interval_speed:
            x_pos = random.choice(block_x_positions)
            block = pygame.Rect(x_pos, 40, block_width, block_height)  # 方块初始位置在最顶部上方40个像素的位置
            blocks.append(block)
            last_fall_time = current_time

        # 移动随机方块
        for block in blocks:
            if difficulty == "Easy":
                block.y += block_speed_control  # 方块向下移动
            elif difficulty == "Normal":
                block.y += block_speed_control  # 方块向下移动
            else:
                block.y += block_speed_control  # 方块向下移动
            if block.y > window_size[1]:  # 如果方块超出窗口底部，从列表中移除
                blocks.remove(block)
                lives -= 1
                if lives == 0:
                    game_state = "game_over"
            if bullet.colliderect(block) and bullet_state == "fire":  # 子弹和方块发生碰撞
                blocks.remove(block)  # 移除方块
                bullet_state = "ready"  # 重置子弹状态
                score += 1  # 增加分数

    # 填充背景色
    screen.fill(WHITE)

    if game_state == "start":
        # 绘制开始画面
        difficulty_text = large_font.render(difficulty, True, BLACK)
        difficulty_rect_center = difficulty_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 80))
        screen.blit(difficulty_text, difficulty_rect_center)

        options_text = font.render("1. Easy  2. Normal  3. Hard", True, BLACK)
        options_rect_center = options_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
        screen.blit(options_text, options_rect_center)

        start_text = font.render("Press SPACE to Start", True, BLACK)
        start_rect_center = start_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 + 70))
        screen.blit(start_text, start_rect_center)

    elif game_state == "countdown":
        # 绘制倒计时
        countdown_text = countdown_font.render(str(countdown), True, BLACK)
        countdown_rect_center = countdown_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
        screen.blit(countdown_text, countdown_rect_center)

        if time.time() - last_fall_time > 1:
            countdown -= 1
            last_fall_time = time.time()

        if countdown < 0:
            game_state = "playing"
            start_time = time.time()  # 记录时间
            last_fall_time = time.time()

    elif game_state == "playing":
        # 绘制玩家方块
        pygame.draw.rect(screen, BLUE, player)

        # 绘制子弹
        if bullet_state == "fire":
            pygame.draw.rect(screen, bullet_color, bullet)

        # 绘制随机方块
        for block in blocks:
            pygame.draw.rect(screen, block_color, block)

        # 绘制计分栏背景
        score_rect = pygame.Rect(0, 0, window_size[0], 50)
        pygame.draw.rect(screen, WHITE, score_rect)

        # 绘制蓝色线条
        pygame.draw.line(screen, BLACK, (0, 50), (window_size[0], 50), 2)
        pygame.draw.line(screen, BLACK, (100, 50), (100, window_size[1]), 2)
        pygame.draw.line(screen, BLACK, (200, 50), (200, window_size[1]), 2)
        pygame.draw.line(screen, BLACK, (300, 50), (300, window_size[1]), 2)

        # 绘制分数
        score_text = small_font.render("Score: " + str(score), True, BLACK)
        score_rect_center = score_text.get_rect(center=(window_size[0] // 2 - 140, 25))
        screen.blit(score_text, score_rect_center)

        # 绘制生命
        lives_text = small_font.render("Lives: " + str(lives), True, BLACK)
        lives_rect = lives_text.get_rect(center=(window_size[0] // 2 + 140, 25))
        screen.blit(lives_text, lives_rect)

        # 控制速度
        elapsed_time = round(time.time() - start_time, 1) #經過的秒數
        fall_interval_speed = fall_interval - math.sqrt(elapsed_time)*0.02 #生成方塊/秒
        block_speed_control = block_speed + math.sqrt(elapsed_time)*0.1  #方塊掉落速度
        bullet_speed_control = bullet_speed + math.sqrt(elapsed_time)*0.2 #子彈速度


        elapsed_time_text = small_font.render("Time: " + str(elapsed_time) + "s", True, BLACK)
        elapsed_time_rect = elapsed_time_text.get_rect(center=(window_size[0] // 2, 25))
        screen.blit(elapsed_time_text, elapsed_time_rect)

    elif game_state == "game_over":
        # 绘制游戏结束画面
        game_over_text = large_font.render("Game Over", True, BLACK)
        game_over_rect_center = game_over_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 80))
        screen.blit(game_over_text, game_over_rect_center)

        final_score_text = font.render("Final Score: " + str(score), True, BLACK)
        final_score_rect_center = final_score_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
        screen.blit(final_score_text, final_score_rect_center)

        highest_score_text = font.render("Highest Score: " + str(Highest_score), True, BLACK)
        highest_score_text_center = highest_score_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 + 40))
        screen.blit(highest_score_text, highest_score_text_center)

    # 更新屏幕
    pygame.display.update()
    clock.tick(60)  # 设置帧率为60帧/秒
