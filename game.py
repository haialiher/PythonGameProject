import pygame
import sys
from npc import NPC
from player import Player
from input import get_pressed_keys  # Import the helper function
from objects import Inventory, Item, Tree, Bush, House  # Import Tree, Bush, and House classes


class Game:
    def __init__(self):
    # Pygame
        pygame.init()
        pygame.display.set_caption("AdventureGame")
        self.inventory = Inventory() 
        self.inventoryOpen = False 
    # Screen dimensions
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 700
    # Colors
        self.PALE_SAGE_GREEN = (152, 193, 153)
        self.DARK_RED = (40, 0, 0)
    # Set up the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    # player pixels
        self.player = Player(
            "assets/MC.png", 
            714,  # X position
            1000, # Y position
            5, 
            scale=(50, 50), 
            frame_size=(32, 35)  #32x35 for characters pixels slicing
        )
     
    # Camera
        self.camera_offset = [0, 0]
        self.clock = pygame.time.Clock()
        self.running = True

    # Obstacles (trees, bushes, house)
        self.obstacles = []
        self.forest_obstacles = []  # Store forest-specific obstacles
        self.house_obstacles = []   # Store house-specific obstacles

    # NPCs
        self.forest_npcs = []  # List to store NPCs in the forest
        self.npc_positions = {}  # Dictionary to remember NPC positions

    # Call load_world_objects to initialize world objects
        self.load_world_objects()

    # Call the new method to set up the background and scaling
        self.setup_background_and_scaling("assets/forrest.png", "assets/path.png")

    # Initialize font for dialog
        self.dialog_font = pygame.font.Font(None, 36)

    def display_dialog(self, dialog):
        """Display dialog in a text box at the bottom of the screen."""
        text_box = pygame.Rect(50, self.SCREEN_HEIGHT - 100, self.SCREEN_WIDTH - 100, 50)
        for line in dialog:
            self.screen.fill((0, 0, 0), text_box)  # Clear the text box before displaying the next line
            pygame.draw.rect(self.screen, (255, 255, 255), text_box, 2)  # White border
            text_surface = self.dialog_font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (text_box.x + 10, text_box.y + 10))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before clearing the dialog

    def load_world_objects(self):
        """Load objects like trees, bushes, and houses into the world."""
        self.house = House("assets/house.png", 845, 750, 80, 94)
        
        self.greenTwin = NPC("assets/npcGreenTwin.png", 710, 331
                , 5, (50, 50), (32, 35), dialog=["hiii", "find my sister!"])
        self.pinkTwin = NPC("assets/npcPinkTwin.png", 613, 953
                , 5, (50, 50), (32, 35), dialog=["heeyyyyy!", "Have you seen my twin?"])
        self.forest_npcs.extend([self.greenTwin, self.pinkTwin])  # Add NPCs to the forest list

# Weapon Items
        fork = Item("Fork", "kind of pointy", "assets/fork.png", 822, 413)  # Provide x and y during initialization
        self.obstacles.append(fork)  # Add fork to obstacles
        print(f"Fork added at position: {fork.rect.topleft}")  # Debugging statement
        
        knife = Item("Knife", "sharp and shiny", "assets/knife.png", 714, 1095)  # Provide x and y during initialization
        self.obstacles.append(knife)  # Add knife to obstacles
        print(f"knife added at position: {knife.rect.topleft}")  # Debugging statement
        
        # Trees
        tree1 = Tree("assets/tree.png", 300, 400, 74, 94)
        tree2 = Tree("assets/tree.png", 500, 632, 74, 94)
        tree3 = Tree("assets/tree.png", 1000, 700, 74, 94)
        tree4 = Tree("assets/tree.png", 1100, 750, 74, 94)
        tree5 = Tree("assets/tree.png", 200, 700, 74, 94)
        tree6 = Tree("assets/tree.png", 1140, 540, 74, 94)
        tree7 = Tree("assets/tree.png", 228, 540, 74, 94)
        tree8 = Tree("assets/tree.png", 467, 300, 74, 94)
        tree9 = Tree("assets/tree.png", 250, 200, 74, 94)
        tree10 = Tree("assets/tree.png", 800, 100, 74, 94)
        tree11 = Tree("assets/tree.png", 900, 50, 74, 94)
        tree12 = Tree("assets/tree.png", 590, 654, 74, 94) 
        tree13 = Tree("assets/tree.png", 380, 700, 74, 94)
        tree14 = Tree("assets/tree.png", 569, 800, 74, 94)
        tree15 = Tree("assets/tree.png", 434, 900, 74, 94)
        tree16 = Tree("assets/tree.png", 73, 246, 74, 94)
        tree17 = Tree("assets/tree.png", 200, 900, 74, 94)
        tree18 = Tree("assets/tree.png", 100, 1200, 74, 94)
        tree19 = Tree("assets/tree.png", 50, 1300, 74, 94)
        tree20 = Tree("assets/tree.png", 150, 1400, 74, 94)
    #bushes (don't place at (x =700) )
        bush1 = Bush("assets/bush.png", 600, 500, 50, 50)
        bush2 = Bush("assets/bush.png", 1512, 537, 50, 50)
        bush3 = Bush("assets/bush.png", 800, 600, 50, 50)
        bush4 = Bush("assets/bush.png", 1233, 951, 50, 50)
        bush5  = Bush("assets/bush.png",200, 700, 50, 50)
        bush6 = Bush("assets/bush.png", 0, 989, 50, 50)
        bush7 = Bush("assets/bush.png", 13, 500, 50, 50)
        bush8 = Bush("assets/bush.png", 400, 400, 50, 50)
        bush9 = Bush("assets/bush.png", 429, 71, 50, 50)
        bush10 = Bush("assets/bush.png", 600, 200, 50, 50)
        bush11 = Bush("assets/bush.png", 1356, 807, 50, 50)
        bush12 = Bush("assets/bush.png", 1550, 906, 50, 50)
        bush13 = Bush("assets/bush.png", 162, 76, 50, 50)
        bush14 = Bush("assets/bush.png", 1000, -50, 50, 50)
        bush15 = Bush("assets/bush.png", 1100, -100, 50, 50)
        bush16 = Bush("assets/bush.png", 1200, -150, 50, 50)
        bush17 = Bush("assets/bush.png", 1300, -200, 50, 50)
        bush18 = Bush("assets/bush.png", 1400, -250, 50, 50)
        bush19 = Bush("assets/bush.png", 0, 0, 50, 50)
        bush20 = Bush("assets/bush.png", 1600, 350, 50, 50)
         
        # Add the house, NPCs, trees, bushes, and items to the forest obstacles list
        self.forest_obstacles.extend([self.house, self.greenTwin, self.pinkTwin, fork, knife,
                    tree1, tree2, tree3, tree4, tree5, tree6, tree7, tree8, tree9, tree10, 
                    tree11, tree12, tree13, tree14,  tree15,  tree16,  tree17, tree18, tree19, tree20,
                    bush1, bush2, bush3, bush4, bush5, bush6, bush7, bush8, bush9, bush10, 
                    bush11, bush12, bush13, bush14, bush15, bush16, bush17, bush18, bush19, bush20,])

        # Initially set obstacles to forest obstacles
        self.obstacles = self.forest_obstacles

    def setup_background_and_scaling(self, background_path, path_path):
        """Set up the background and path images with scaling."""
    #load the background image
        self.forrest = pygame.image.load(background_path).convert_alpha()
        self.path = pygame.image.load(path_path).convert_alpha()
    #calculate scaling factor based on player size
        bg_width, bg_height = self.forrest.get_size()
        scale_factor = min(self.player.scale[0] / 32, self.player.scale[1] / 32)  # player is a little taller than 32x32 pixels 
    #scale the background proportionally
        new_width = int(bg_width * scale_factor)
        new_height = int(bg_height * scale_factor)
        self.forrest = pygame.transform.scale(self.forrest, (new_width, new_height))
        self.path = pygame.transform.scale(self.path, (new_width, new_height))  # Scale the path to match the background

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.inventoryOpen:  # Close inventory if it's open
                        self.inventoryOpen = False
                    else:  # Otherwise, quit the game
                        self.running = False
                elif event.key == pygame.K_e:  # Press 'E' to pick up items
        
                    for obstacle in self.obstacles:
                        if isinstance(obstacle, Item) and obstacle.rect and self.player.rect.colliderect(obstacle.rect):
                            self.inventory.add_items(obstacle)  # Use the correct method name
                            self.obstacles.remove(obstacle)  # Remove the item from the world
                            print(f"Picked up: {obstacle.name}")
                elif event.key == pygame.K_i:  # Toggle inventory with 'I'
                    self.inventoryOpen = not self.inventoryOpen
                elif event.key == pygame.K_RETURN: 
                    for npc in self.forest_npcs:
                        if npc.rect.colliderect(self.player.rect):
                            dialog = npc.interact()
                            if dialog:
                                self.display_dialog(dialog)
                            break
                # Check if the player is within the specified range and presses Enter
                if (
                    #going to house from forrest
                    event.key == pygame.K_RETURN and
                    932 <= self.player.rect.x <= 997 and
                    937 <= self.player.rect.y <= 970
                ):
                    print("House")
                    self.load_house_setting()
                elif (
                     #going to forrest from house
                    event.key == pygame.K_RETURN and
                    285 <= self.player.rect.x <= 370 and
                    582 <= self.player.rect.y <= 612
                ):
                    print(" house to forrest")
                    self.load_forest_from_house()
                
                    
    def load_house_setting(self):
        """Logic to load the house setting."""
        print("Loading new setting...")
        self.setup_background_and_scaling("assets/Housefloors.png", "assets/Housefloors.png")
    # Only include house-specific obstacles
        self.obstacles = self.house_obstacles
    # Save NPC positions before transitioning
        for npc in self.forest_npcs:
            self.npc_positions[npc] = npc.rect.topleft
    # Hide NPCs by clearing the forest_npcs list temporarily
        self.forest_npcs.clear()
    # Set player position
        self.player.rect.topleft = (325, 612)
        print("New setting loaded!")

    def load_forest_from_house(self):
        """Logic to load the forest setting from the house."""
        print("Returning to forest...")
        self.setup_background_and_scaling("assets/forrest.png", "assets/path.png")
    # Reset obstacles to forest obstacles
        self.obstacles = self.forest_obstacles
    # Restore NPC positions
        for npc in self.npc_positions:
            npc.rect.topleft = self.npc_positions[npc]
    # Restore NPCs to the forest_npcs list
        self.forest_npcs.extend([self.greenTwin, self.pinkTwin])
    # Set player position
        self.player.rect.topleft = (942, 962)
        print("Returned to forest!")

    def update(self):
    # Use the helper function to get key presses
        keys = get_pressed_keys()

    # Create a copy of the player's current rect to calculate the proposed position
        proposed_rect = self.player.rect.copy()

    # Move the player based on input
        self.player.move(keys, self.obstacles)

    # Restrict the player's movement to the boundaries of the background
        self.player.rect.left = max(self.player.rect.left, 0)
        self.player.rect.top = max(self.player.rect.top, 0)
        self.player.rect.right = min(self.player.rect.right, self.forrest.get_width())
        self.player.rect.bottom = min(self.player.rect.bottom, self.forrest.get_height())

    # Log the player's current position in (x, y) format
        print(f"Player position: ({self.player.rect.x}, {self.player.rect.y})")

    # Update animation
        dt = self.clock.get_time()
        self.player.update_animation(dt)
        for npc in self.forest_npcs:
            npc.update_animation(dt)

    # Restrict the camera to the boundaries of the background
        self.camera_offset[0] = max(0, min(self.player.rect.centerx - self.SCREEN_WIDTH // 2, self.forrest.get_width() - self.SCREEN_WIDTH))
        self.camera_offset[1] = max(0, min(self.player.rect.centery - self.SCREEN_HEIGHT // 2, self.forrest.get_height() - self.SCREEN_HEIGHT))

    def draw(self):
        # Fill the background color
        self.screen.fill(self.DARK_RED)

        # Draw the forest background with camera offset
        self.screen.blit(self.forrest, (-self.camera_offset[0], -self.camera_offset[1]))

        # Draw the path on top of the forest background
        self.screen.blit(self.path, (-self.camera_offset[0], -self.camera_offset[1]))

        # Create a list of all sprites (player, NPCs, and other objects) for depth sorting
        sprites = self.forest_npcs + [self.player] + self.obstacles

        # Sort sprites by their y position (rect.bottom) for depth ordering
        sprites.sort(key=lambda sprite: sprite.rect.bottom)

        # Draw sprites in sorted order
        for sprite in sprites:
            if hasattr(sprite, "current_animation"):  # For NPCs and player
                self.screen.blit(sprite.current_animation[sprite.current_frame], (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1]))
            elif hasattr(sprite, "image"):  # For static objects like trees or items
                self.screen.blit(sprite.image, (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1]))
        # Ensure items are drawn properly
        for obstacle in self.obstacles:
            if isinstance(obstacle, Item) and obstacle.image:
                self.screen.blit(obstacle.image, (obstacle.rect.x - self.camera_offset[0], obstacle.rect.y - self.camera_offset[1]))
        # Draw the inventory last, as a GUI overlay
        if self.inventoryOpen:
            self.inventory.display(self.screen, self.dialog_font, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

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
