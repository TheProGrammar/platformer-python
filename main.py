import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_name = "Forgotten Origins"
pygame.display.set_caption(game_name)

img = pygame.image.load("assets/bg/1.jpg")
resize_img = pygame.transform.scale(img, (800, 640))

# Define player action variables
moving_left = False
moving_right = False

clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.75

# Define colors
background = (144, 201, 120)
bg = (45, 45, 45)
RED = (255, 0, 0)


def draw_bg():
    screen.blit(resize_img, (0, -160))
    # screen.fill(bg)
    # pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


class Warrior(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        super(Warrior, self).__init__()
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.y_velocity = 0
        self.in_air = True
        self.flip = False
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        self.animation_list = []
        self.frame_index = 0

        # Manage idle animation list
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            # Reset temporary list of images
            temp_list = []
            # Count number of files in the folder
            num_of_frames = len(os.listdir(f"assets/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                image = pygame.image.load(f"assets/{self.char_type}/{animation}/adventurer-{animation}-0{i}.png")
                image = pygame.transform.scale(image, (int(image.get_width() * scale), (int(image.get_height() * scale))))
                temp_list.append(image)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # Reset movement variables
        dx = 0
        dy = 0

        # Assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump and not self.in_air:
            self.y_velocity = -11
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.y_velocity += GRAVITY
        if self.y_velocity > 10:
            self.y_velocity = 10
        dy += self.y_velocity

        # Check collision with floor (TEMPORARY)
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # Update animation
        animation_cooldown = 100
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If the animation has run out reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Warrior("player", 200, 200, 3, 5)

running = True
while running:

    if player.alive:
        if player.in_air:
            player.update_action(2)  # 2 means jump
        elif moving_left or moving_right:
            player.update_action(1)  # 1 means run
        else:
            player.update_action(0)  # 0 means idle
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check if keyboard buttons pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                running = False

        # Check if keyboard buttons released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    draw_bg()
    player.update_animation()
    player.draw()

    pygame.display.update()
    clock.tick(FPS)
