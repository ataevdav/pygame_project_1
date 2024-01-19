#подключение модулей
import pygame
import random
import style as s

#инициализация модуля pygame
pygame.init()

pygame.mixer.init()

#размеры окна игры
WIDTH = 600
HEIGHT = 900

#инициализация окна 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Nokia Jump')

#загрузка фона 
if s.bg_image:
    background = pygame.transform.scale(pygame.image.load(s.bg_image), (600, 900))
else:
    background = s.bg_color

#загрузка изображений для окна начала новой игры
logo = pygame.transform.scale(pygame.image.load(s.lg_image), (448, 232))
new_game = pygame.transform.scale(pygame.image.load(s.ng_image), (448, 232))
record = pygame.transform.scale(pygame.image.load(s.hs_image), (448, 232))

#загрузка изображения аватара
player = pygame.transform.scale(pygame.image.load(s.pl_image), (70, 70))

#настройка обновления кадров
fps = 27
timer = pygame.time.Clock()

#статус звука игры
sound = 1

#загрузка шрифтов
font = pygame.font.Font(s.txt_font, 36)
font_h = pygame.font.Font(s.txt_font, 79)

jump_sound = pygame.mixer.Sound(s.jump_sound)
game_over_sound = pygame.mixer.Sound(s.game_over_sound)

#загрузка данных о рекорде
file = open('data.txt')
txt = file.read()
if len(txt) == 0:
    high_score = 0
else:
    high_score = int(txt)
file.close()

#переменная запуска первой игры
first_game = True

#уровень сложности (скорости)
lvl = 1

#начальные значения
#очки и статус игры
score = 0
game_over = False
#положение аватара
plX = 265
plY = 700
#платформы при старте
platforms = [[250, 850, 100, 16], [100, 750, 100, 16], [400, 750, 100, 16], [250, 650, 100, 16], [300, 550, 100, 16], [200, 450, 100, 16], [250, 350, 100, 16], [100, 250, 100, 16], [400, 250, 100, 16], [250, 150, 100, 16], [300, 50, 100, 16]]

#переменные движения аватара
pl_angle = 0
jump = False
y_change = 0
x_change = 0
player_speed = 8

#инициализация группы спрайтов
all_sprites = pygame.sprite.Group()

#класс анимированного спрайта бонуса
class Bonus(pygame.sprite.Sprite):
    #инициализация спрайта: прием изображения, размеров матрицы кадров, положения спрайта
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
    
    #формирование кадров анимации спрайта
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
    
    #смена кадра анимации спрайта
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
    
    def move(self, change):
        self.rect.move_ip(0, -change)


#проверка коллизии аватара с платформами
def check_collisions(b_list, j):
    global plY, plX, y_change
    for i in range(len(b_list)):
        if b_list[i].colliderect(plX, plY + 65, 100, 16) and jump == False and y_change > 6:
            j = True
            jump_sound.play()
    return j

#вертикальное перемещение аватара, прыжок
def update_player(y):
    global jump, y_change
    jump_height = 14
    gravity = .6
    if jump:
        y_change = -jump_height
        jump = False
    y += y_change
    y_change += gravity
    return y

#генерация новых платформ
def update_platforms(p_list, y, change):
    global score
    #движение спрайта бонуса
    if len(all_sprites.sprites()) and change < 0:
        bonus.rect.move_ip(0, -change)
    if y < 700 and change < 0:
        for i in range(len(p_list)):
            p_list[i][1] -= change
    else:
        pass
    for item in range(len(p_list)):
        if p_list[item][1] > 900:
            p_list[item] = [random.randint(10, 490), random.randint(-40, -10), 100, 16]
            score += 1
    return p_list

#проверка коллизии аватара с бонусом, обработка бонуса
def get_bonus():
    global score, plus_txt_ticks
    if len(all_sprites.sprites()):
        if bonus.rect.colliderect((plX + 20, plY + 15, plX + 50, plY + 55)):
            score += 10
            all_sprites.empty()
            return True
    else:
        return False

#отображения окна начала новой игры
def start_new_game():
    #отображение фона
    if s.bg_image:
        screen.blit(background, (0, 0))
    else:
        screen.fill(background)
    #отображение логотипа, указания длян начала новой игры
    screen.blit(logo, (76, 100))
    screen.blit(new_game, (76, 424))
    #отображение уведомления о рекорде
    if high_score == score and not first_game:
        screen.blit(record, (76, 646))
        file = open('data.txt', 'w')
        file.write(str(high_score))
        file.close()
    #удаление спрайта бонуса
    all_sprites.empty()
    #отображение надписи об окончании игры и счета игры
    if not first_game:
        game_over_text = font_h.render(f'ИГРА ОКОНЧЕНА', True, s.txt_color)
        game_over_text2 = font.render(f'СЧЕТ: {score}', True, s.txt_color)
        score_text = font.render(f'Счёт: {score}', True, s.txt_color)
        screen.blit(game_over_text, (73, 330))
        screen.blit(game_over_text2, (251, 400))
        screen.blit(score_text, (5, 32))
    high_score_text = font.render(f'Рекорд: {high_score}', True, s.txt_color)
    screen.blit(high_score_text, (5, 5))
    lvl_text = font.render(f'Уровень сложности: {lvl}', True, s.txt_color)
    screen.blit(lvl_text, (142, 867))

def music():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(s.track[lvl])
    pygame.mixer.music.play(loops=-1)

music()

#основной игровой цикл
running = True 
while running == True:
    #смена кадра
    timer.tick(fps)
    #отображение фона
    if s.bg_image:
        screen.blit(background, (0, 0))
    else:
        screen.fill(background)
    #отображение аватара
    screen.blit(player, (plX, plY))
    #отображение счёта и рекорда во время игры
    score_text = font.render(f'Счёт: {score}', True, s.txt_color)
    screen.blit(score_text, (5, 32))
    high_score_text = font.render(f'Рекорд: {high_score}', True, s.txt_color)
    screen.blit(high_score_text, (5, 5))
    #список объектов платформ
    blocks = []

    #заполнение списка объектов платформ и их отрисовка
    for i in range(len(platforms)):
        if s.pf_image:
            block = pygame.transform.scale(pygame.image.load(s.pf_image), (100, 16))
            blocks.append(pygame.Rect(platforms[i]))
            screen.blit(block, (platforms[i][0], platforms[i][1]))
        else:
            block = pygame.draw.rect(screen, s.pf_color, platforms[i], 0, 4)
            blocks.append(block)
    
    #обработка нажатий игрока
    for event in pygame.event.get():
        #закрытие игры
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #начало новой игры
            if event.key == pygame.K_SPACE and game_over:
                #возврат к начальным значениям
                score = 0
                game_over = False
                plX = 265
                plY = 700
                platforms = [[250, 850, 100, 16], [100, 750, 100, 16], [400, 750, 100, 16], [250, 650, 100, 16], [300, 550, 100, 16], [200, 450, 100, 16], [250, 350, 100, 16], [100, 250, 100, 16], [400, 250, 100, 16], [250, 150, 100, 16], [300, 50, 100, 16]]
                first_game = False
            #движение влево(клавиши A и СТРЕЛКА ВЛЕВО)/вправо(клавиши D и СТРЕЛКА ВПРАВО)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                x_change = - player_speed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                x_change = player_speed
            #смена уровня сложности
            if event.key == pygame.K_1 or event.key == pygame.K_KP1 and game_over:
                lvl = 1
                fps = 25
                music()
            if event.key == pygame.K_2 or event.key == pygame.K_KP2 and game_over:
                lvl = 2
                fps = 35
                music()
            if event.key == pygame.K_3 or event.key == pygame.K_KP3 and game_over:
                lvl = 3
                fps = 50
                music()
            #выключение звука
            if event.key == pygame.K_q:
                pygame.mixer.music.set_volume(0)
                game_over_sound.set_volume(0)
                jump_sound.set_volume(0)
                sound = 0
            #включение звука
            if event.key == pygame.K_e:
                pygame.mixer.music.set_volume(1)
                game_over_sound.set_volume(1)
                jump_sound.set_volume(1)
                sound = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                x_change = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                x_change = 0
    
    #горизонтальное перемещение аватара
    plX += x_change

    #обработка прыжка (проверка коллизии)
    jump = check_collisions(blocks, jump)

    
    #генерация спрайта бонуса
    if random.randint(0, 200) == 0 and not game_over:
        all_sprites.empty()
        bonus = Bonus(pygame.image.load("nokia_bn.png"), 4, 2, random.randint(20, 550), -50)
        all_sprites.add(bonus)
        print('Sprite generated')
    
    #обновление спрайта бонуса
    all_sprites.update()
    all_sprites.draw(screen)

    #проверка взятия бонуса
    if get_bonus():
        bonus_text = font_h.render(f'+ 10', True, s.txt_color)
        screen.blit(bonus_text, (73, 340))

    #края игровой области
    if plX < -20:
        plX = -20
    elif plX > 550:
        plX = 550

    #поворот аватара при движении
    if x_change > 0:
        pl_angle = (pl_angle - 2) % 360
        player = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(s.pl_image), (70, 70)), pl_angle)
    elif x_change < 0:
        pl_angle = (pl_angle + 2) % 360
        player = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(s.pl_image), (70, 70)), pl_angle)
    
    #проверка на запуск первой игры
    if first_game:
        game_over = True
        y_change = 0
        x_change = 0
        start_new_game()

    #проверка состояния игры
    if not game_over and plY >= 900:
        game_over_sound.play()
    if plY < 900:
        plY = update_player(plY)
    else:
        #остановка игры при проигрыше
        game_over = True
        y_change = 0
        x_change = 0
        start_new_game()

    #обновление платформ
    platforms = update_platforms(platforms, plY, y_change)

    #обновление значения рекорда
    if score > high_score:
        high_score = score

    #обновление экрана
    pygame.display.flip()

#завершение выполнения программы
pygame.quit()
