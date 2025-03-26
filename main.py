import pygame
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()

# Carregar músicas e efeitos
pygame.mixer.music.load('som/musica_fundo.ogg')
pygame.mixer.music.play(loops=-1)
colisao_sound = pygame.mixer.Sound('som/colisao.wav')

# Definir configurações de janela e cores
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('CrashRush')
green, gray, yellow, white, red = (76, 208, 56), (100, 100, 100), (255, 232, 0), (255, 255, 255), (200, 0, 0)

# Inicializações de jogo
road, left_lane, center_lane, right_lane = (100, 0, 300, 500), 150, 250, 350
lanes = [left_lane, center_lane, right_lane]
player_x, player_y, speed, score, gameover = 250, 400, 2, 0, False
clock, fps = pygame.time.Clock(), 120
marker_move_y, marker_width, marker_height = 0, 10, 50

# Carregar imagens
player_img = pygame.image.load('imagens/car.png')
vehicle_imgs = [pygame.image.load(f'imagens/{filename}') for filename in ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']]
crash_img = pygame.image.load('imagens/crash.png')

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        scale = 45 / image.get_rect().width
        self.image = pygame.transform.scale(image, (int(image.get_rect().width * scale), int(image.get_rect().height * scale)))
        self.rect = self.image.get_rect(center=(x, y))

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        super().__init__(player_img, x, y)

# Grupos de sprites
player_group, vehicle_group = pygame.sprite.Group(), pygame.sprite.Group()
player_group.add(PlayerVehicle(player_x, player_y))

# Loop principal
while True:
    clock.tick(fps)
    screen.fill(green)
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, (95, 0, marker_width, 500))
    pygame.draw.rect(screen, yellow, (395, 0, marker_width, 500))

    # Movimento dos marcadores
    marker_move_y += speed * 2
    if marker_move_y >= marker_height * 2: marker_move_y = 0
    for y in range(-marker_height * 2, 500, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + marker_move_y, marker_width, marker_height))

    # Movimentação do jogador
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player_group.sprites()[0].rect.centerx > left_lane:
                player_group.sprites()[0].rect.x -= 100
            elif event.key == K_RIGHT and player_group.sprites()[0].rect.centerx < right_lane:
                player_group.sprites()[0].rect.x += 100

    # Adicionar veículos aleatórios
    if len(vehicle_group) < 2 and all(vehicle.rect.top >= vehicle.rect.height * 1.5 for vehicle in vehicle_group):
        vehicle_group.add(Vehicle(random.choice(vehicle_imgs), random.choice(lanes), -50))

    # Movimentação dos veículos e detecção de colisões
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= 500:
            vehicle.kill()
            score += 1
            if score % 5 == 0: speed += 1
        if pygame.sprite.collide_rect(player_group.sprites()[0], vehicle):
            gameover = True
            colisao_sound.play()
            screen.blit(crash_img, crash_img.get_rect(center=(player_group.sprites()[0].rect.centerx, player_group.sprites()[0].rect.top)))

    # Exibe a pontuação
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    screen.blit(font.render(f'Score: {score}', True, white), (50, 400))

    # Game over
    if gameover:
        pygame.mixer.music.stop()
        pygame.draw.rect(screen, red, (0, 50, 500, 100))
        # Centralizando a mensagem de Game Over
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect(center=(250, 100))  # Ajusta a posição para o centro
        screen.blit(text, text_rect)

    vehicle_group.draw(screen)
    player_group.draw(screen)
    pygame.display.update()

    # Verifica entrada para reiniciar ou sair
    while gameover:
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); exit()
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False; score = 0; speed = 2; player_group.sprites()[0].rect.center = [player_x, player_y]
                    vehicle_group.empty(); pygame.mixer.music.play(loops=-1)
                elif event.key == K_n: pygame.quit(); exit()
