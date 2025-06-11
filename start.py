import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tamagotchi Style UI")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 230, 0)
PINK = (255, 100, 180)
BLUE = (0, 180, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BG_PINK = (255, 200, 220)

# 시계
clock = pygame.time.Clock()

# 알 크기 및 위치
egg_w, egg_h = 500, 580
egg_x = (WIDTH - egg_w) // 2
egg_y = (HEIGHT - egg_h) // 2
egg_center_x = egg_x + egg_w // 2
egg_center_y = egg_y + egg_h // 2

# 다마고치 이미지 크기
tama_width, tama_height = 100, 100
tama_speed = 5
tama_x = egg_center_x - tama_width // 2
tama_y = egg_center_y - tama_height // 2

# 먹이 정보
food = None
food_radius = 10
eating = False
eat_timer = 0

# 폰트
font = pygame.font.SysFont("Arial", 24, bold=True)

# 이미지 로드 (tama_stage1)
tama_img = pygame.image.load("assets/tama_stage1.png").convert_alpha()

# 크기 확장
scale_factor = 2
tama_width *= scale_factor
tama_height *= scale_factor
tama_img = pygame.transform.scale(tama_img, (tama_width, tama_height))

# 위치 재조정
tama_x = egg_center_x - tama_width // 2
tama_y = egg_center_y - tama_height // 2

state = "start"

nickname = ""
input_active = True

def draw_start_screen():
    screen.fill(BG_PINK)
    title = font.render("Welcome to Tamagotchi!", True, RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    prompt = font.render("Enter your nickname:", True, BLACK)
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 120))

    # 입력 상자
    input_box = pygame.Rect(WIDTH // 2 - 100, 160, 200, 40)
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)

    text_surface = font.render(nickname, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    # 버튼
    start_btn = pygame.Rect(WIDTH // 2 - 100, 240, 200, 40)
    instr_btn = pygame.Rect(WIDTH // 2 - 100, 300, 200, 40)
    pygame.draw.rect(screen, BLUE, start_btn)
    pygame.draw.rect(screen, GRAY, instr_btn)
    
    start_text = font.render("Start Game", True, WHITE)
    instr_text = font.render("Instructions", True, BLACK)
    screen.blit(start_text, (start_btn.x + 50, start_btn.y + 5))
    screen.blit(instr_text, (instr_btn.x + 50, instr_btn.y + 5))

    return input_box, start_btn, instr_btn

def draw_instruction_screen():
    screen.fill(WHITE)
    
    # 기존 기본 폰트
    font = pygame.font.SysFont("Arial", 24)

    # 새로 큰 제목용 폰트 생성
    title_font = pygame.font.SysFont("Arial", 36, bold=True)

    # Controls 제목 렌더링 (크고 파란색으로)
    title_text = title_font.render("Controls", True, (255, 10, 10))  # 진한 빨간색
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))

    lines = [
        "",
        "Arrow Keys: Move",
        "Spacebar: Spawn Food",
        "",
        "Move near food to eat it automatically.",
        "",
        "Press any key to start the game"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 80 + i * 40))

def reset_game():
    global tama_x, tama_y, food, eat_timer
    tama_x = egg_center_x - tama_width // 2
    tama_y = egg_center_y - tama_height // 2
    food = None
    eat_timer = 0



def spawn_food(screen_rect):
    margin = 20
    x = random.randint(screen_rect.left + margin, screen_rect.right - margin)
    y = random.randint(screen_rect.top + margin, screen_rect.bottom - margin)
    return (x, y)


def draw_hearts(screen_rect, count=3):
    for i in range(count):
        x = screen_rect.left + 20 + i * 30
        y = screen_rect.top + 20
        pygame.draw.circle(screen, RED, (x, y), 8)
        pygame.draw.circle(screen, RED, (x + 10, y), 8)
        points = [(x - 5, y + 5), (x + 15, y + 5), (x + 5, y + 20)]
        pygame.draw.polygon(screen, RED, points)

def smooth_color_transition(current, target, speed=10):
    for i in range(3):
        if current[i] < target[i]:
            current[i] = min(current[i] + speed, target[i])
        elif current[i] > target[i]:
            current[i] = max(current[i] - speed, target[i])
    return current

def draw_shell_ui(keys):
    pygame.draw.ellipse(screen, BG_PINK, [egg_x, egg_y, egg_w, egg_h])

    screen_w, screen_h = 320, 350
    screen_x = egg_center_x - screen_w // 2
    screen_y = egg_y + 110
    pygame.draw.rect(screen, WHITE, [screen_x, screen_y, screen_w, screen_h], border_radius=10)
    pygame.draw.rect(screen, BLACK, [screen_x, screen_y, screen_w, screen_h], 2, border_radius=10)
    screen_rect = pygame.Rect(screen_x, screen_y, screen_w, screen_h)

    draw_hearts(screen_rect)

    logo_text = font.render("Tamagotchi Friends", True, RED)
    screen.blit(logo_text, (egg_center_x - logo_text.get_width() // 2, egg_y + 40))

    button_y = egg_y + egg_h - 60
    pygame.draw.circle(screen, GRAY, (egg_center_x - 130, button_y - 30), 15)
    pygame.draw.circle(screen, GRAY, (egg_center_x - 100, button_y + 10), 15)

    base_x = egg_center_x + 100
    base_y = button_y - 10
    size = 12
    offset = 22

    def draw_dir_button(dx, dy, keycode):
        color = BLACK if keys[keycode] else GRAY
        pygame.draw.rect(screen, color, [base_x + dx, base_y + dy, size, size])

    draw_dir_button(0, -offset, pygame.K_UP)
    draw_dir_button(0, offset, pygame.K_DOWN)
    draw_dir_button(-offset, 0, pygame.K_LEFT)
    draw_dir_button(offset, 0, pygame.K_RIGHT)

    restart_btn = pygame.Rect(20, 20, 100, 30)  # ← 왼쪽 위로 이동

    # 마우스 오버 감지
    mouse_pos = pygame.mouse.get_pos()
    if restart_btn.collidepoint(mouse_pos):
        restart_color = [155, 0, 0]  # 진진한 빨강
        restart_text_color = [155, 155, 155]
    else:
        restart_color = [255, 0, 0]  # 기본 빨강
        restart_text_color = [255, 255, 255]

    #버튼 그리기기
    pygame.draw.rect(screen, restart_color, restart_btn, border_radius=5)
    restart_text = font.render("Restart", True, restart_text_color)
    screen.blit(restart_text, (restart_btn.x + 15, restart_btn.y))    

    return screen_rect, restart_btn


# 다마고치 이미지 그리기
def draw_tamagotchi(x, y):
    screen.blit(tama_img, (x, y))


def draw_food(x, y):
    pygame.draw.circle(screen, RED, (x, y), food_radius)



# 메인 루프
running = True
while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "start":
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass  # 엔터로는 아무것도 안 함
                    else:
                        if len(nickname) < 12:
                            nickname += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_btn.collidepoint(mouse_pos):
                    state = "game"
                elif instr_btn.collidepoint(mouse_pos):
                    state = "instruction"

        elif state == "instruction":
            if event.type == pygame.KEYDOWN:
                state = "game"

    if state == "start":
        input_box, start_btn, instr_btn = draw_start_screen()

    elif state == "instruction":
        draw_instruction_screen()

    elif state == "game":
        screen_rect, restart_btn = draw_shell_ui(keys)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not food:
                food = spawn_food(screen_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_btn.collidepoint(event.pos):
                reset_game()
                state = "start"

        if keys[pygame.K_LEFT]:
            tama_x -= tama_speed
        if keys[pygame.K_RIGHT]:
            tama_x += tama_speed
        if keys[pygame.K_UP]:
            tama_y -= tama_speed
        if keys[pygame.K_DOWN]:
            tama_y += tama_speed

        if tama_x < screen_rect.left:
            tama_x = screen_rect.left
        if tama_x + tama_width > screen_rect.right:
            tama_x = screen_rect.right - tama_width
        if tama_y < screen_rect.top:
            tama_y = screen_rect.top
        if tama_y + tama_height > screen_rect.bottom:
            tama_y = screen_rect.bottom - tama_height

        eating = False
        if food:
            food_x, food_y = food
            tama_center = (tama_x + tama_width // 2, tama_y + tama_height // 2)
            dist = ((food_x - tama_center[0]) ** 2 + (food_y - tama_center[1]) ** 2) ** 0.5
            if dist < food_radius + 20:
                food = None
                eating = True
                eat_timer = pygame.time.get_ticks()

        if food:
            draw_food(*food)
        draw_tamagotchi(tama_x, tama_y)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
