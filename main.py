import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


#Live and score 
Score = 0 
Lives = 3 

# Player setup
player_size = 20
player_x = (WIDTH - player_size) // 2
player_y = (HEIGHT - player_size) // 2
player_speed = 5

# Food setup
food_size = 20
food_rect = None  # Start with no food

player_add = None
direction = "RIGHT"


# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")

clock = pygame.time.Clock()  # For controlling frame rate

# Function to spawn the player
def spawn_player():
    return pygame.Rect(player_x, player_y, player_size, player_size)

# list of pygame.Rect segments
player_body = []  
position_history = []  # List of (x, y) positions
initial_rect = pygame.Rect(player_x, player_y, player_size, player_size)
player_body.append(initial_rect)

def player_add_size(player_rect, player_x, player_y):
    player_add_x = player_x - player_size
    player_add_y = player_y
    return pygame.Rect(player_add_x,player_add_y, player_size, player_size)
    

# Function to randomly spawn food
def random_spawn_food():
    food_x = random.randint(0, WIDTH - food_size)
    food_y = random.randint(0, HEIGHT - food_size)
    return pygame.Rect(food_x, food_y, food_size, food_size)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and direction != "RIGHT":
        direction = "LEFT"
    if keys[pygame.K_RIGHT] and direction != "LEFT":
        direction = "RIGHT"
    if keys[pygame.K_UP] and direction != "DOWN":
        direction = "UP"
    if keys[pygame.K_DOWN] and direction != "UP":
        direction = "DOWN"
  
    # Move the player
    if direction == "LEFT":
        player_x -= player_speed
    elif direction == "RIGHT":
        player_x += player_speed
    elif direction == "UP":
        player_y -= player_speed
    elif direction == "DOWN":
        player_y += player_speed

    # Clamp player within screen bounds
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))


   
    # Add current head position to history
    position_history.insert(0, (player_x, player_y))

     # Update head
    player_body[0].x = player_x
    player_body[0].y = player_y


    #max_history = len(player_body) * (player_size)
    max_history_length = len(player_body) + 5  # small buffer

    if len(position_history) > max_history_length:
        position_history = position_history[:max_history_length]

   


    for i in range(1, len(player_body)):
        if i < len(position_history):
            pos = position_history[i]
            player_body[i].x = pos[0]
            player_body[i].y = pos[1]

   
    
    # Create player rect
    #player_rect = spawn_player()

    # Spawn food if it doesn't exist
    if food_rect is None:
        food_rect = random_spawn_food()

    # Draw food
    pygame.draw.rect(screen, GREEN, food_rect)

    # Draw player
    #pygame.draw.rect(screen, RED, player_rect)

    for segment in player_body:
        pygame.draw.rect(screen, RED, segment)
        
    
    
    # Check collision
    """ if player_rect.colliderect(food_rect):
        print("Collision!")
        Score += 100
        food_rect = None  # Remove food so new one will spawn
        player_add = player_add_size(player_rect, player_x, player_y)
        pygame.draw.rect(screen, RED, player_add) """

    if player_body[0].colliderect(food_rect):
        print("Ate food!")
        Score += 100
        food_rect = None

        # Add a new segment at the same position as the last one
        last_seg = player_body[-1]
        new_seg = pygame.Rect(last_seg.x, last_seg.y, player_size, player_size)
        player_body.append(new_seg)

    #if player_add is not None:
    #pygame.draw.rect(screen, RED, player_add)   


    font = pygame.font.SysFont(None, 36)

    # Inside the game loop before display.flip():
    score_text = font.render(f"Score: {Score}", True, (0,0,0))
    lives_text = font.render(f"Lives: {Lives}", True, (0,0,0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Detect edge collision
    if player_x == 0:
        print("Touching left edge")
        Lives -=1
        player_x = (WIDTH - player_size) // 2
        player_y = (HEIGHT - player_size) // 2

    if player_x == WIDTH - player_size:
        print("Touching right edge")
        Lives -=1
        player_x = (WIDTH - player_size) // 2
        player_y = (HEIGHT - player_size) // 2

    if player_y == 0:
        print("Touching top edge")
        Lives -=1
        player_x = (WIDTH - player_size) // 2
        player_y = (HEIGHT - player_size) // 2

    if player_y == HEIGHT - player_size:
        Lives -=1
        player_x = (WIDTH - player_size) // 2
        player_y = (HEIGHT - player_size) // 2
        print("Touching bottom edge")

    #Game over conditions
    if Lives == 0:
        font_big = pygame.font.SysFont(None, 72)
        game_over_text = font_big.render("Game Over", True, RED)
        final_score_text = font.render(f"Final Score: {Score}", True, (0, 0, 0))
        instructions_text = font.render("Press Enter to Exit", True, (50, 50, 50))

        screen.fill(WHITE)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 3))
        screen.blit(final_score_text, ((WIDTH - final_score_text.get_width()) // 2, HEIGHT // 2))
        screen.blit(instructions_text, ((WIDTH - instructions_text.get_width()) // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        waiting = False
                        running = False
            clock.tick(15)  # Slow down the waiting loop

        break  # Exit the game loop
       

    # Update screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
