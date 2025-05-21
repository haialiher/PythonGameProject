import pygame
import sys
from player import Player
from input import get_pressed_keys  # Import the helper function

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("AdventureGame")

        # Screen dimensions
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 700

        # Colors
        self.PALE_SAGE_GREEN = (152, 193, 153)

        # Set up the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Initialize the player with a specific size (e.g., 64x64 pixels)
        self.player = Player(
            "assets/MC.png", 
            self.SCREEN_WIDTH // 2, 
            self.SCREEN_HEIGHT // 2, 
            5, 
            scale=(60, 60), 
            frame_size=(32, 35)  #32x35 for characters pixels slicing
        )

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Game state
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # Use the helper function to get key presses
        keys = get_pressed_keys()
        self.player.move(keys)
        dt = self.clock.get_time()
        self.player.update_animation(dt)
        print(f"Player position: {self.player.rect.topleft}, dt: {dt}")

    def draw(self):
        # Fill the screen with the background color
        self.screen.fill(self.PALE_SAGE_GREEN)

        # Draw the player
        try:
            self.player.draw(self.screen)
        except Exception as e:
            print(f"Error in draw method: {e}")

        # Update the display
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()
        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
