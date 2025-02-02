import pygame
import random
import sys
from concurrent.futures import ThreadPoolExecutor

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Circles")

# Colors
BLACK = (0, 0, 0)

def draw_circle():
    # Random circle properties
    radius = random.randint(10, 100)
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Draw the circle
    pygame.draw.circle(screen, color, (x, y), radius)

def draw_random_circles():
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(draw_circle) for _ in range(100000)]
        # Wait for all circles to be drawn
        for future in futures:
            future.result()

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw random circles in parallel
        draw_random_circles()

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()