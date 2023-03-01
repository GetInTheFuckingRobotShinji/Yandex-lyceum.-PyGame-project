import pygame, sys

pygame.init()
screen = pygame.display.set_mode((1500, 1000))
pygame.display.set_caption('ROBOGO')

sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

tile_width = tile_height = 50


# загрузка картинок
def load_image(name, color_key=None):
    image = pygame.image.load(f'data/{name}')
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


tile_image = {'wall': pygame.transform.scale(load_image('Bricks.png'), (50, 50)),
              'empty': pygame.transform.scale(load_image('Sandstone.png'), (50, 50)),
              'finish': pygame.transform.scale(load_image('finish.png'), (50, 50))}
player_image = pygame.transform.scale(load_image('robot.png'), (50, 50))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * (pos_x + 1), tile_height * (pos_y + 1))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * (pos_x + 1), tile_height * (pos_y + 1))
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * (self.pos[0] + 1),
                                               tile_height * (self.pos[1] + 1))


# все цвета игры
fon_color = pygame.Color((188, 143, 143))
text_color = pygame.Color('#8fbc8f')
COLOR_INACTIVE = pygame.Color('#8f8fbc')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


# окно ввода имени игрока
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def terminate():
    pygame.quit()
    sys.exit()


# начальное окно в начале игры
def start_screen():
    screen.fill(fon_color)
    fon = pygame.transform.scale(load_image('FON.png'), (1500, 1000))
    screen.blit((fon), (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


# окно перехода между уровнями
def next_level_screen():
    fon = pygame.transform.scale(load_image('next_level.png'), (1500, 1000))
    screen.fill(fon_color)
    screen.blit((fon), (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


# конец игры
def end_screen():
    fon = pygame.transform.scale(load_image('win.png'), (1500, 1000))
    screen.fill(fon_color)
    screen.blit((fon), (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


# загрузка уровня
def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


# генерация уровня
def generate_level(level):
    x, y, start_pos, finish = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                Tile('finish', x, y)
                finish = (x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                start_pos = (x, y)
                level[y][x] = '.'
    return x, y, start_pos, finish


# передвижение игрока
def move(hero, movement, start_pos=None):
    global triger
    x, y = hero.pos
    if start_pos != None:
        hero.move(start_pos[0], start_pos[1])
    elif movement == 'up':
        if y > 0 and (level_map[y - 1][x] == '.' or level_map[y - 1][x] == '!'):
            hero.move(x, y - 1)
        else:
            triger = False
    elif movement == 'down':
        if y < max_y - 1 and (level_map[y + 1][x] == '.' or level_map[y + 1][x] == '!'):
            hero.move(x, y + 1)
        else:
            triger = False
    elif movement == 'left':
        if x > 0 and (level_map[y][x - 1] == '.' or level_map[y][x - 1] == '!'):
            hero.move(x - 1, y)
        else:
            triger = False
    elif movement == 'right':
        if x < max_x and (level_map[y][x + 1] == '.' or level_map[y][x + 1] == '!'):
            hero.move(x + 1, y)
        else:
            triger = False


# переменные и объекты
player_name = ''
clock = pygame.time.Clock()
running = True
movements = []
triger = True
check_win = True
mumber_of_levels = 6
max_x, max_y, start_pos, finish = None, None, None, None
fps = 10
hero = Player(0, 0)
button_left = pygame.transform.scale(load_image('left.png'), (50, 50))
button_up = pygame.transform.scale(load_image('up.png'), (50, 50))
button_down = pygame.transform.scale(load_image('down.png'), (50, 50))
button_right = pygame.transform.scale(load_image('right.png'), (50, 50))
button_cancel = pygame.transform.scale(load_image('cancel.png'), (50, 50))
button_start = pygame.transform.scale(load_image('start.png'), (100, 100))
frame = pygame.transform.scale(load_image('frame.png'), (550, 370))
sound1 = pygame.mixer.Sound('data/mp.mp3')
sound2 = pygame.mixer.Sound('data/win.mp3')
sound3 = pygame.mixer.Sound('data/button.mp3')
sound4 = pygame.mixer.Sound('data/wrong.mp3')
sound5 = pygame.mixer.Sound('data/go.mp3')
sound6 = pygame.mixer.Sound('data/battle-over-winner.mp3')


# отрисовка команд робота
def render_text():
    text = pygame.font.Font(None, 36)
    text_output = ''
    for movement in range(len(movements)):
        if movement % 4 == 3:
            text_output += movements[movement] + '-'
        else:
            text_output += movements[movement] + ' '
    text_output = text_output.split('-')[:11]
    for i in range(len(text_output)):
        text_of_movements = text.render(text_output[i], True, 3, fon_color)
        screen.blit(text_of_movements, (1050, 150 + (i * 30)))


# отрисовка всех кнопок
def render_button():
    screen.blit(button_left, (1050, 50))
    screen.blit(button_up, (1110, 50))
    screen.blit(button_down, (1170, 50))
    screen.blit(button_right, (1230, 50))
    screen.blit(button_cancel, (1100, 525))
    screen.blit(button_start, (1170, 500))
    screen.blit(frame, (915, 125))


# начальное окно ввода имени игрока
screen.fill(fon_color)
input_box = InputBox(650, 475, 200, 50)
done = False
ranning = True
font2 = pygame.font.Font(None, 30)
string_rendered = font2.render('Введите своё имя', True, text_color)
intro_rect = string_rendered.get_rect()
intro_rect.x = 660
intro_rect.y = 400
screen.blit(string_rendered, intro_rect)
while not done:
    for event in pygame.event.get():
        screen.blit(string_rendered, intro_rect)
        if event.type == pygame.QUIT:
            done = True
            ranning = False
        text = input_box.handle_event(event)
    if text != None:
        player_name = text.lower()
        if player_name == '':
            player_name = 'None'
        done = True
        break
    input_box.update()
    input_box.draw(screen)
    pygame.display.flip()
    clock.tick(30)

# запись данных игрока и сравнение с базой данных
tableR = open('data/table.txt', 'r')
tableR1 = tableR.read()
tableR = tableR1.split('\n')
number_of_player = 0

for i in range(len(tableR) - 1):
    if player_name == tableR[i].split(' ')[0]:
        number_of_map = tableR[i].split(' ')[1]
        number_of_player = i
        break
else:
    number_of_map = 1
    number_of_player = len(tableR)

# основной игровой цикл
if __name__ == '__main__' and ranning:
    pygame.display.set_caption('gg')
    start_screen()
    player = None
    while ranning:
        render_button()
        render_text()
        pygame.display.update()
        if check_win:
            level_map = load_level(f'maps/map{str(number_of_map)}.txt')
            max_x, max_y, start_pos, finish = generate_level(level_map)
            move(hero, movements, start_pos)
            check_win = False
        for event in pygame.event.get():
            render_button()
            render_text()
            pygame.display.update()
            if event.type == pygame.QUIT:
                ranning = False
                tableW = open('data/table.txt', 'w')
                if int(number_of_player) < len(tableR):
                    tableW.write(
                        '\n'.join(tableR[:int(number_of_player)]) + '\n' + tableR[int(number_of_player)].split(' ')[0]
                        + ' ' + str(number_of_map) + '\n' + '\n'.join(tableR[int(number_of_player) + 1:]))
                else:
                    tableW.write(tableR1 + player_name + ' ' + str(number_of_map) + '\n')
                tableW.close()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # кнопка - влево
                if 1050 <= event.pos[0] and 50 <= event.pos[1] and \
                        1100 >= event.pos[0] and event.pos[1] <= 100:
                    movements.append('left')
                    sound3.play()
                    render_text()
                    pygame.display.update()

                # кнопка - вперёд
                elif event.pos[0] >= 1110 and event.pos[1] >= 50 and \
                        event.pos[0] <= 1160 and event.pos[1] <= 100:
                    movements.append('up')
                    sound3.play()
                    render_text()
                    pygame.display.update()

                # кнопка - назад
                elif event.pos[0] >= 1170 and event.pos[1] >= 50 and \
                        event.pos[0] <= 1220 and event.pos[1] <= 100:
                    movements.append('down')
                    sound3.play()
                    render_text()
                    pygame.display.update()

                # кнопка - направо
                elif event.pos[0] >= 1230 and event.pos[1] >= 50 and \
                        event.pos[0] <= 1280 and event.pos[1] <= 100:
                    movements.append('right')
                    sound3.play()
                    render_text()
                    pygame.display.update()

                # кнопка - отмена
                elif event.pos[0] >= 1050 and event.pos[1] >= 500 and \
                        event.pos[0] <= 1150 and event.pos[1] <= 600:
                    if len(movements) > 0:
                        sound3.play()
                        movements.pop()
                        render_text()
                        pygame.display.update()

                # кнопка - старта
                elif event.pos[0] >= 1170 and event.pos[1] >= 500 and \
                        event.pos[0] <= 1270 and event.pos[1] <= 600:
                    sound3.play()
                    pygame.time.wait(200)
                    for i in range(len(movements)):
                        if triger:
                            move(hero, movements[i])
                            sound1.play()
                            sprite_group.draw(screen)
                            hero_group.draw(screen)
                            pygame.display.flip()
                            render_button()
                            render_text()
                            pygame.display.update()
                            pygame.time.wait(200)
                            render_button()
                            render_text()

                    # проверка, дошёл ли игрок до финиша и загрузка следующего уровня
                    if hero.pos == finish:
                        print("WIN!!!!!")
                        print()
                        if int(number_of_map) == int(mumber_of_levels):
                            end_screen()
                            sound6.play()  # звук для конца игры
                        check_win = True
                        sound2.play()
                        next_level_screen()
                        movements = []
                        if int(number_of_map) < mumber_of_levels:
                            number_of_map = int(number_of_map)
                            number_of_map += 1
                            print(number_of_map)
                            tableW = open('data/table.txt', 'w')
                            if int(number_of_player) < len(tableR):
                                tableW.write(
                                    '\n'.join(tableR[:int(number_of_player)]) + '\n' +
                                    tableR[int(number_of_player)].split(' ')[0]
                                    + ' ' + str(number_of_map) + '\n' + '\n'.join(tableR[int(number_of_player) + 1:]))
                            else:
                                tableW.write(tableR1 + player_name + ' ' + str(number_of_map) + '\n')
                            tableW.close()
                    else:
                        sound4.play()
                        render_button()
                        render_text()
                        pygame.display.update()
                        pygame.time.wait(500)
                        render_button()
                        render_text()
                        move(hero, movements, start_pos)
                        sprite_group.draw(screen)
                        hero_group.draw(screen)
                        pygame.display.flip()
                    triger = True
                    hero.pos = start_pos
        render_button()
        render_text()
        pygame.display.update()
        screen.fill(fon_color)
        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(fps)
        pygame.display.update()
    pygame.quit()
