import pygame
from pygame.locals import *
import random

pygame.init()

# Inicializa o mixer de áudio
pygame.mixer.init()

# Carrega a música de fundo e toca em loop
pygame.mixer.music.load('asset/musica_fundo.ogg')
pygame.mixer.music.play(loops=-1, start=0.0)

# Cria a janela do jogo
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('CrashRush')

# Cores
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Tamanhos da estrada e dos marcadores
road_width = 300
marker_width = 10
marker_height = 50

# Coordenadas das faixas
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Marcador de estrada e bordas
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# Para animar o movimento dos marcadores de faixa
lane_marker_move_y = 0

# Coordenadas iniciais do jogador
player_x = 250
player_y = 400

# Configurações do jogo
clock = pygame.time.Clock()
fps = 120
gameover = False
speed = 2
score = 0

# Efeito sonoro de colisão
colisao_sound = pygame.mixer.Sound('asset/colisao.wav')

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image: object, x: object, y: object) -> object:
        pygame.sprite.Sprite.__init__(self)
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('asset/car.png')
        super().__init__(image, x, y)

# Grupos de sprites
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Cria o carro do jogador
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Carrega as imagens dos veículos
vehicle_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for filename in vehicle_filenames:
    image = pygame.image.load('asset/' + filename)
    vehicle_images.append(image)

# Carrega a imagem de colisão
crash = pygame.image.load('asset/crash.png')
crash_rect = crash.get_rect()

# Função do Menu
def show_menu():
    font_title = pygame.font.Font(pygame.font.get_default_font(), 48)
    font_option = pygame.font.Font(pygame.font.get_default_font(), 32)

    # Criando o texto do título e das opções
    title_text = font_title.render('CrashRush', True, red)
    start_text = font_option.render('Pressione Enter para Jogar', True, white)
    quit_text = font_option.render('Pressione Esc para Sair', True, white)

    # Centralizando o texto na tela
    title_rect = title_text.get_rect(center=(width // 2, 100))
    start_rect = start_text.get_rect(center=(width // 2, 200))
    quit_rect = quit_text.get_rect(center=(width // 2, 300))

    # Preenchendo o fundo com a cor verde (grama)
    screen.fill(green)

    # Carrega e exibe a imagem de fundo
    background = pygame.image.load('asset/background_menu.jpg')  # Carregar a imagem
    background = pygame.transform.scale(background, (500, 500))  # Redimensionar para 800x600
    screen.blit(background, (0, 0))  # Exibir a imagem na tela

    # Adicionando sombra no título para destacar
    shadow_title = font_title.render('CrashRush', True, (50, 50, 50))
    screen.blit(shadow_title, (title_rect.x + 5, title_rect.y + 5))

    # teste
    shadow_start = font_option.render('Pressione Enter para Jogar', True, (50, 50, 50))
    screen.blit(shadow_start, (start_rect.x + 5, start_rect.y + 5))

    shadow_quit = font_option.render('Pressione Esc para Sair', True, (50, 50, 50))
    screen.blit(shadow_quit, (quit_rect.x + 5, quit_rect.y + 5))

    # Desenhando o título e as opções
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)

    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return 'quit'  # Se o jogador fechar a janela, sai do jogo
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # Se pressionar Enter, inicia o jogo
                    return 'start'
                if event.key == K_ESCAPE:  # Se pressionar Esc, sai do jogo
                    pygame.quit()
                    return 'quit'

# Função para o loop principal do jogo
def game_loop():
    global score, speed, gameover
    gameover = False
    score = 0
    speed = 2
    player.rect.center = [player_x, player_y]
    vehicle_group.empty()

    pygame.mixer.music.play(loops=-1)

    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_LEFT and player.rect.center[0] > lanes[0]:
                    player.rect.x -= 100
                elif event.key == K_RIGHT and player.rect.center[0] < lanes[2]:
                    player.rect.x += 100
                for vehicle in vehicle_group:
                    if pygame.sprite.collide_rect(player, vehicle):
                        gameover = True
                        colisao_sound.play()
                        crash_rect.center = [player.rect.center[0],
                                             (player.rect.center[1] + vehicle.rect.center[1]) / 2]
        # Desenhos
        screen.fill(green)
        pygame.draw.rect(screen, gray, road)
        pygame.draw.rect(screen, yellow, left_edge_marker)

        pygame.draw.rect(screen, yellow, right_edge_marker)
        for y in range(0, 500, 50):
            pygame.draw.rect(screen, white, (lanes[0] + 45, y, 10, 50))
            pygame.draw.rect(screen, white, (lanes[1] + 45, y, 10, 50))

        player_group.draw(screen)

        # Adiciona veículos
        if len(vehicle_group) < 2:
            if all(vehicle.rect.top >= vehicle.rect.height * 1.5 for vehicle in vehicle_group):
                lane = random.choice(lanes)
                vehicle = Vehicle(random.choice(vehicle_images), lane, -50)
                vehicle_group.add(vehicle)

        # Movimento dos veículos
        for vehicle in vehicle_group:
            vehicle.rect.y += speed
            if vehicle.rect.top >= 500:
                vehicle.kill()
                score += 1
                if score % 5 == 0:
                    speed += 1

        vehicle_group.draw(screen)

        # Pontuação e colisão frontal
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        screen.blit(font.render(f'Score: {score}', True, white), (50, 400))
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            colisao_sound.play()
            crash_rect.center = [player.rect.center[0], player.rect.top]

        # Game Over
        if gameover:
            pygame.mixer.music.stop()
            screen.blit(crash, crash_rect)
            pygame.draw.rect(screen, red, (0, 50, 500, 100))
            game_over_text = 'Game over. Play again? (Y/N)'
            text = font.render(game_over_text, True, white)
            text_rect = text.get_rect()
            text_rect.center = (500 // 2, 50 + 100 // 2)
            screen.blit(text, text_rect)
            pygame.display.update()

            while gameover:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        gameover, running = False, False
                    if event.type == KEYDOWN:
                        if event.key == K_y:
                            gameover = False
                            game_loop()
                        elif event.key == K_n:
                            gameover = False
                            running = False

        pygame.display.update()

# Exibição do menu
menu_result = show_menu()

# Se o jogador escolher "start", inicia o jogo
if menu_result == 'start':
    game_loop()

# Se o jogador escolher "quit", o Pygame será fechado
pygame.quit()
