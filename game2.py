import pygame
import sys
import random


# ⚙️ تهيئة Pygame
pygame.init()
pygame.mixer.init()

# 🎵 تشغيل الموسيقى الخلفية
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)  # تتكرر بدون توقف

# 🔊 تحميل صوت العملة
coin_sound = pygame.mixer.Sound("coin.wav")

# إعداد الشاشة
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Younes Jump")

# الألوان
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
brown=(142, 69, 19)
pink=(255, 105, 180) 

# تحميل الصور
player_img = pygame.image.load("player2.png")
player_img = pygame.transform.scale(player_img, (65, 65))

coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (35, 35))

background_img = pygame.image.load("background2.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, 600))


# الخط
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

# دالة لإعادة تعيين اللعبة

def reset_game():
    player = pygame.Rect(200, 500, 50, 50)
    velocity_y = 0
    scroll = 0
    score = 0
    platforms = [pygame.Rect(200, 550, 80, 10)]
    for i in range(6):
        x = random.randint(0, WIDTH - 80)
        y = 550 - i * 100
        platforms.append(pygame.Rect(x, y, 80, 10))
    coins = []
    for plat in platforms:
        if random.random() < 0.5:
            cx = plat.x + random.randint(10, 40)
            cy = plat.y - 30
            coins.append(pygame.Rect(cx, cy, 30, 30))
    return player, velocity_y, scroll, score, platforms, coins
 
# أول تشغيل
player, velocity_y, scroll, score, platforms, coins = reset_game()
gravity = 0.5
jump_force = -12
running = True
game_over = False
shake_offset = 0
scroll_offset = int(scroll)
bg_y = -scroll_offset % 1200
screen.blit(background_img, (0, bg_y - 1200))
screen.blit(background_img, (0, bg_y))

while running:
    clock.tick(60)
    screen.blit(background_img, (0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # حركة اللاعب
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if player.x < -50:
            player.x = WIDTH
        elif player.x > WIDTH:
            player.x = -50

        # الجاذبية
        velocity_y += gravity
        player.y += velocity_y

        # القفز عند المنصات
        for plat in platforms:
            if player.colliderect(plat) and velocity_y > 0 and player.bottom <= plat.bottom:
                velocity_y = jump_force

        # صعود الشاشة
        if player.y < HEIGHT / 3:
            diff = HEIGHT / 3 - player.y
            player.y = HEIGHT / 3
            for plat in platforms:
                plat.y += diff
            for coin in coins:
                coin.y += diff
            scroll += diff
            score = int(scroll)

        # توليد المنصات
        while len(platforms) < 8:
            x = random.randint(0, WIDTH - 80)
            y = platforms[-1].y - random.randint(80, 120)
            new_platform = pygame.Rect(x, y, 80, 10)
            platforms.append(new_platform)
            if random.random() < 0.5:
                cx = x + random.randint(10, 40)
                cy = y - 30
                coins.append(pygame.Rect(cx, cy, 30, 30))

        # إزالة القديم
        platforms = [p for p in platforms if p.y < HEIGHT]
        coins = [c for c in coins if c.y < HEIGHT]

        # جمع العملات
        for coin in coins[:]:
            if player.colliderect(coin):
                score += 10
                coin_sound.play()
                coins.remove(coin)

        # رسم المنصات
        for plat in platforms:
            pygame.draw.rect(screen,pink , plat)

        # رسم العملات
        for coin in coins:
            screen.blit(coin_img, (coin.x, coin.y))

        # رسم الشخصية
        screen.blit(player_img, (player.x, player.y))

        # عرض النقاط
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # نهاية اللعبة إذا طاح
        if player.y > HEIGHT:
            game_over = True
            shake_offset = 10

    else:
        # تأثير اهتزاز عند الخسارة
        if shake_offset > 0:
            shake_x = random.randint(-shake_offset, shake_offset)
            shake_y = random.randint(-shake_offset, shake_offset)
            screen.blit(font.render("Game Over!", True, BLACK), (WIDTH//2 - 60 + shake_x, HEIGHT//2 - 30 + shake_y))
            shake_offset -= 1
        else:
            screen.blit(font.render("Game Over!", True, BLACK), (WIDTH//2 - 60, HEIGHT//2 - 30))

        # التعليمات
        screen.blit(font.render("Press R to Restart or ESC to Quit", True, pink), (WIDTH//2 - 150, HEIGHT//2 + 10))

        # إعادة أو خروج
        if keys[pygame.K_r]:
            player, velocity_y, scroll, score, platforms, coins = reset_game()
            game_over = False
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    pygame.display.update()

pygame.quit()
