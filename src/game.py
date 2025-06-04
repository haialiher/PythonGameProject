import os
import random
import sys


# Add the parent directory of 'src' to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from src.npc import NPC
from src.player import Player
from src.input import get_pressed_keys  # Import the helper function
from src.objects import HouseWalls, Inventory, Item, Tree, Bush, House  # Import Tree, Bush, and House classes

PALE_SAGE_GREEN = (152, 193, 153)
DARK_RED = (40, 0, 0)    
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700  
PLAYER_START_POSITION = (714, 1000)
HOUSE_POSITION = (845, 750)

HOUSE_RECT = pygame.Rect(0, 0, 651, 612)
FOREST_RECT = pygame.Rect(0, 0, 1550, 1200)

class Game:
    def __init__(self):
    # Pygame
        
        pygame.init()
        pygame.display.set_caption("idek yet")

    # Set up the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Initialize the inventory
        self.inventory = Inventory() 
        self.inventoryOpen = False  
        self.dialog_font = pygame.font.Font(None, 36)
        self.guessing_mode = False
        self.guess = {"npc": None, "weapon": None, "location": None}
    # player pixels
        self.player = Player(
            "assets/images/characters/MC.png", 
            714,  # X position
            1000, # Y position
            5, 
            scale=(50, 50), 
            frame_size=(32, 35)  #32x35 for characters pixels slicing
        )

        self.camera_offset = [0, 0]    # Camera
        self.clock = pygame.time.Clock()
        self.running = True
    # Obstacles (trees, bushes, house)
        self.obstacles = []
        self.main_obstacles = []  # Store forest-specific obstacles
        self.house_obstacles = []   # Store house-specific obstacles
    # NPCs
        self.npcList = []  
        self.npc_positions = {}  
    # Call load_world_objects to initialize world objects
        self.locations = {
            "House": HOUSE_RECT,
            "Forest": FOREST_RECT
        }
        self.load_world_objects()
        self.setup_background_and_scaling("assets/backgrounds/forrest/forrest.png", "assets/backgrounds/forrest/path.png")
    # Initialize font for dialog
        self.dialog_font = pygame.font.Font(None, 36)
        
    def render_areas(self):
        pygame.draw.rect(self.screen, (255, 0, 0), HOUSE_RECT, 2)  # Red outline for the house
        pygame.draw.rect(self.screen, (0, 255, 0), FOREST_RECT, 2)  # Green outline for the forest


    def display_dialog(self, dialog, npc_name=None):
        if not dialog or len(dialog) == 0:
            print("No dialog to display!")
            return
        
        print(f"Displaying dialog: {dialog}")  # Debugging statement
        text_box = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 50)
        self.screen.fill(DARK_RED, text_box)  # Clear the text box
        pygame.draw.rect(self.screen, (255, 255, 255), text_box, 2)
        text_surface = self.dialog_font.render(dialog, True, (255, 255, 255))
        self.screen.blit(text_surface, (text_box.x + 10, text_box.y + 10))

        # Render NPC name in the bottom-left corner
        if npc_name:
            name_surface = self.dialog_font.render(npc_name, True, (255, 255, 255))
            self.screen.blit(name_surface, (10, SCREEN_HEIGHT - 40))  # Adjust position as needed

        pygame.display.flip()

        # Wait for 2 seconds or until Tab is pressed
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 3000:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    return  # Exit the dialog early if Tab is pressed

    def load_npcs(self):
        innocent_dialog = [
            "I saw {murderer} near the {location} earlier.",
            "That {weapon} looks dangerous, don’t you think?",
            "People say {murderer} has been acting strange lately.",
            "The {location} is where things got really suspicious.",
            "I heard someone talking about a {weapon} around here.",
            "Could {murderer} have been at the {location} when it happened?",
            "There’s no way the crime was done without that {weapon}.",
            "I saw {murderer} holding something shiny the other day.",
            "The {location} has always been quiet, until now.",
            "Do you think the {weapon} was left behind intentionally?",
            "{murderer} was nervous when asked about the {weapon}.",
            "The {location} seemed deserted when I passed by.",
            "Some say {murderer} has a grudge against someone here.",
            "That {weapon} belongs to someone from around here.",
            "Who else would bring a {weapon} to the {location}?",
            "I’m not sure if {murderer} was even near the {location}.",
            "I don’t trust {murderer}—there’s something off about them.",
            "That {weapon}... it’s not the kind you see every day.",
            "Why would {murderer} be hanging around the {location} so late?",
            "I heard whispers about {murderer} and that {weapon}.",
            "Something about the {location} doesn’t add up.",
            "If I were you, I’d keep an eye on {murderer}.",
            "No one’s really sure why that {weapon} was there.",
            "People say strange things happen when {murderer} is near.",
            "The {location} has been a hotspot for trouble lately.",
            "I caught {murderer} looking nervous when the {weapon} was mentioned.",
            "Not many people know what happened at the {location}, but it wasn’t good.",
            "That {weapon} could easily have been used for something bad.",
            "You never know what {murderer} is really up to.",
            "The {location} has a dark past, just like {murderer}.",
            "I wouldn’t be surprised if the {weapon} was planted there.",
    ]
        murderer_dialog = [
            "Funny how everyone’s so quick to jump to conclusions these days.",
            "Sometimes, the quietest places hide the loudest secrets.",
            "I’ve seen things happen in the {location} that would surprise you.",
            "People always talk about the {weapon}, but what about the person who holds it?",
            "It’s strange how memories can play tricks on you, isn’t it?",
            "Not everything is as straightforward as it seems.",
            "Sometimes the truth is hidden in the smallest details.",
            "I was just passing through when it all happened—didn’t see much.",
            "You never really know what someone is capable of.",
            "Rumors spread faster than facts, especially in places like {location}.",
        ]
        self.greenTwin = NPC( "Green Twin",
            "assets/images/characters/npcGreenTwin.png", 
                710, 331, 
                5, (50, 50), (32, 35), 
                 dialog=[ None 
                ] 
        )
        self.pinkTwin = NPC( "Pink Twin",
            "assets/images/characters/npcPinkTwin.png", 
                613, 953, 
                5, (50, 50), (32, 35), 
                dialog= None 
        )
        
        self.npcList = [self.greenTwin, self.pinkTwin]
        self.npcList_names = [self.greenTwin.name, self.pinkTwin.name]  # Store NPC names for dialo
        self.murderer = random.choice(self.npcList_names)
        print(f"Random murderer selected: {self.murderer}")
        
        
        if self.murderer != self.greenTwin.name: 
            self.greenTwin.dialog = innocent_dialog
        else:  
            self.greenTwin.dialog = murderer_dialog
            
        if self.murderer != self.pinkTwin.name: 
            self.pinkTwin.dialog = innocent_dialog
        else:  
            self.pinkTwin.dialog = murderer_dialog

          
    def load_items(self):
        # loading fork and knife into locations

        # Randomly select weapon and location
        self.item_names = ["Fork", "Knife"]
        self.weapon = random.choice(self.item_names)
        location_names = ["house", "forest"]
        self.weapon_location = random.choice(location_names)
        print(f"Random Weapon selected: {self.weapon} location: {self.weapon_location}")   
        if self.weapon == "Fork":
            if self.weapon_location == "forest":
                self.fork = Item("Fork", "kind of pointy, looks like it was hidden", "assets/images/items/fork.png", 822, 413)
                self.main_obstacles.append(self.fork)
            elif self.weapon_location == "house":
                self.fork = Item("Fork", "kinda of pointy, looks used.", "assets/images/items/fork.png", 300, 400)
                self.house_obstacles.append(self.fork)
            else:     
                self.fork = Item("Fork", "Brand new", "assets/images/items/fork.png", 400, 413)
        elif self.weapon == "Knife":
            if self.weapon_location == "forest":
                self.knife = Item("Knife", "it was tossed into the grass", "assets/images/items/knife.png", 714, 1095)
            elif self.weapon_location == "house":
                self.knife = Item("Knife", "it was used to cut things recently", "assets/images/items/knife.png", 360, 195)
                self.house_obstacles.append(self.knife)
            else:
                self.knife = Item("Knife", "sharp and shiny almost brand new", "assets/images/items/knife.png", 714, 1095)
            
    def load_housewalls(self):
        self.HouseWallsLeft = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsLeft.png", 0, 0, 48, 700)
        self.HouseWallsRight = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsRight.png", 651, 0, 48, 700)
        self.HouseWallsTop = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsTop.png", 0, 0, 700, 56)

        self.HouseWallsBotLeft = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsBotLeft.png", 0, 605, 300, 120)
        self.HouseWallsBotRight = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsBotRight.png", 400, 605, 300, 120)
        self.HousewallsMidLeft = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsMidLeft.png", 0, 290, 300, 70)
        self.HousewallsMidRight = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsMidRight.png", 400, 290, 300, 70)
        self.HousewallsMid = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsMid.png", 400, 190, 48, 120)
        
        self.house_obstacles.extend([
            self.HouseWallsLeft,
            self.HouseWallsRight,
            self.HouseWallsTop,
            self.HouseWallsBotLeft,
            self.HouseWallsBotRight,
            self.HousewallsMidLeft,
            self.HousewallsMidRight,
            self.HousewallsMid,
            
        ])
          
    def load_trees_and_bushes(self):
        self.trees = [
            Tree("assets/images/environment/tree.png", 300, 400, 74, 94),
            Tree("assets/images/environment/tree.png", 500, 632, 74, 94),
            Tree("assets/images/environment/tree.png", 1000, 700, 74, 94),
            Tree("assets/images/environment/tree.png", 1100, 750, 74, 94),
            Tree("assets/images/environment/tree.png", 200, 700, 74, 94),
            Tree("assets/images/environment/tree.png", 1140, 540, 74, 94),
            Tree("assets/images/environment/tree.png", 228, 540, 74, 94),
            Tree("assets/images/environment/tree.png", 467, 300, 74, 94),
            Tree("assets/images/environment/tree.png", 250, 200, 74, 94),
            Tree("assets/images/environment/tree.png", 800, 100, 74, 94),
            Tree("assets/images/environment/tree.png", 900, 50, 74, 94),
            Tree("assets/images/environment/tree.png", 590, 654, 74, 94),
            Tree("assets/images/environment/tree.png", 380, 700, 74, 94),
            Tree("assets/images/environment/tree.png", 569, 800, 74, 94),
            Tree("assets/images/environment/tree.png", 434, 900, 74, 94),
            Tree("assets/images/environment/tree.png", 73, 246, 74, 94),
            Tree("assets/images/environment/tree.png", 200, 900, 74, 94),
            Tree("assets/images/environment/tree.png", 100, 1200, 74, 94),
            Tree("assets/images/environment/tree.png", 50, 1300, 74, 94),
            Tree("assets/images/environment/tree.png", 150, 1400, 74, 94),
        ]
    #bushes (don't place at (x =700) )
        self.bushes = [
            Bush("assets/images/environment/bush.png", 600, 500, 50, 50),
            Bush("assets/images/environment/bush.png", 1512, 537, 50, 50),
            Bush("assets/images/environment/bush.png", 800, 600, 50, 50),
            Bush("assets/images/environment/bush.png", 1233, 951, 50, 50),
            Bush("assets/images/environment/bush.png", 200, 700, 50, 50),
            Bush("assets/images/environment/bush.png", 0, 989, 50, 50),
            Bush("assets/images/environment/bush.png", 13, 500, 50, 50),
            Bush("assets/images/environment/bush.png", 400, 400, 50, 50),
            Bush("assets/images/environment/bush.png", 429, 71, 50, 50),
            Bush("assets/images/environment/bush.png", 600, 200, 50, 50),
            Bush("assets/images/environment/bush.png", 1356, 807, 50, 50),
            Bush("assets/images/environment/bush.png", 1550, 906, 50, 50),
            Bush("assets/images/environment/bush.png", 162, 76, 50, 50),
            Bush("assets/images/environment/bush.png", 1000, -50, 50, 50),
            Bush("assets/images/environment/bush.png", 1100, -100, 50, 50),
            Bush("assets/images/environment/bush.png", 1200, -150, 50, 50),
            Bush("assets/images/environment/bush.png", 1300, -200, 50, 50),
            Bush("assets/images/environment/bush.png", 1400, -250, 50, 50),
            Bush("assets/images/environment/bush.png", 0, 0, 50, 50),
            Bush("assets/images/environment/bush.png", 1600, 350, 50, 50),
        ]
        
    def load_world_objects(self):
        """Load objects like trees, bushes, house, items, and NPCs into the world."""
        self.load_npcs()  # Load NPCs
        self.load_items()  # Load items
        self.load_trees_and_bushes()  # Load trees and bushes
        self.house = House("assets/images/environment/house.png", *HOUSE_POSITION, 80, 94)
        # Initially set obstacles to forest obstacles
        self.main_obstacles.extend(self.trees + self.bushes + [self.house] + self.npcList)
        self.obstacles = self.main_obstacles

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
        
    def load_house_setting(self):
        """Logic to load the house setting."""
        print("Loading new setting...")
        self.setup_background_and_scaling("assets/backgrounds/house/Housefloors.png", "assets/backgrounds/house/Housefloors.png")
        self.obstacles = self.house_obstacles
        self.load_housewalls()  # Load house walls
        # Add house walls to house_obstacles so they are drawn and used for collision

        self.player.rect.topleft = (325, 612)
        for npc in self.npcList:
            self.npc_positions[npc] = npc.rect.topleft
        self.npcList.clear() #removing ig they are in forrest
    # Set player position
        
        print("New setting loaded!")

    def load_forest_from_house(self):
        print("Returning to forest...")
        self.setup_background_and_scaling("assets/backgrounds/forrest/forrest.png", "assets/backgrounds/forrest/path.png")
        self.obstacles = self.main_obstacles
        for npc in self.npc_positions:
            npc.rect.topleft = self.npc_positions[npc]
        self.npcList.extend([self.greenTwin, self.pinkTwin])
        self.player.rect.topleft = (942, 962)

    def check_area(self, player_rect):
        for location_name, location_rect in self.locations.items():
            if location_rect.colliderect(player_rect):
                #print(f"Player is in the {location_name} area.")
                return
        print("Player is outside defined areas.")
        return None
    
    def check_transition(self):
    # Transition from forest to house
        if 932 <= self.player.rect.x <= 997 and 937 <= self.player.rect.y <= 970:
            print("Transitioning to house...")
            self.load_house_setting()
            return True
    # Transition from house to forest
        elif 285 <= self.player.rect.x <= 370 and 582 <= self.player.rect.y <= 612:
            print("Transitioning to forest...")
            self.load_forest_from_house()
            return True
  
#Handle key events                  
    def handle_keydown(self,event):
        if event.key == pygame.K_RETURN:
            self.handle_dialog()
        elif event.key == pygame.K_e:
            self.handle_item_pickup()
        elif event.key == pygame.K_i:
            self.inventoryOpen = not self.inventoryOpen
        elif event.key == pygame.K_ESCAPE:
            self.running = False if not self.inventoryOpen else self.close_inventory()
             
    def handle_item_pickup(self):
        for obstacle in self.obstacles:
            if isinstance(obstacle, Item) and obstacle.rect and self.player.rect.colliderect(obstacle.rect):
                self.inventory.add_items(obstacle)  # Add the item to the inventory
                self.obstacles.remove(obstacle)  # Remove the item from the world
                print(f"Picked up: {obstacle.name}")
                
    def handle_dialog(self):
        for npc in self.npcList:
            if self.player.rect.colliderect(npc.rect):  # Check if player is near an NPC
                dialog = random.choice(npc.dialog)  # Select a random dialog from the NPC's dialog list
                if dialog:  # Ensure dialog is not None
                    try:
                        # Format the dialog with the correct keys
                        formatted_dialog = dialog.format(murderer=self.murderer, weapon=self.weapon, location=self.weapon_location)
                        self.display_dialog(formatted_dialog, npc_name=npc.name)
                    except KeyError as e:
                        print(f"Error formatting dialog: {e}")
                        self.display_dialog("Something seems off with the dialog.", npc_name=npc.name)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.handle_dialog()
                    # Advance dialog on Enter key
                    if self.check_transition():  # Check for forest/house transitions
                        return  # Exit early if transitioning
                elif event.key == pygame.K_ESCAPE:
                    if self.inventoryOpen:  # Close inventory if it's open
                        self.inventoryOpen = False
                    else:  # Otherwise, quit the game
                        self.running = False
                elif event.key == pygame.K_e:  # Press e to pick up items
                    self.handle_item_pickup()
                elif event.key == pygame.K_i:  # Toggle inventory with 'I'
                    self.inventoryOpen = not self.inventoryOpen
                  
    def handle_keydown(self,event):
        if event.key == pygame.K_RETURN:
            self.handle_dialog()
        elif event.key == pygame.K_e:
            self.handle_item_pickup()
        elif event.key == pygame.K_i:
            self.inventoryOpen = not self.inventoryOpen
        elif event.key == pygame.K_g:
            self.guessing_mode = not self.guessing_mode
            if self.guessing_mode:
                print("Guessing mode enabled. Press G again to disable.")
            else:
                print("Guessing mode disabled.")
        elif event.key == pygame.K_ESCAPE:
            self.running = False if not self.inventoryOpen else self.close_inventory()
            
    def draw_guessing_ui(self):
        guessingBox = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
        pygame.draw.rect(self.screen, (130, 110, 150), guessingBox)  # Background color
        pygame.draw.rect(self.screen, (255, 255, 255), guessingBox, 2)  # Border color

    # Display instructions
        instructions = self.dialog_font.render("Press keys to guess: NPC (1/2), Weapon (3/4), Location (5/6)", True, (255, 255, 255))
        self.screen.blit(instructions, (guessingBox.x + 10, guessingBox.y + 10))

    # Display current guess
        current_guess = f"NPC: {self.guess['npc']}, Weapon: {self.guess['weapon']}, Location: {self.guess['location']}"
        guess_text = self.dialog_font.render(current_guess, True, (255, 255, 255))
        self.screen.blit(guess_text, (guessingBox.x + 10, guessingBox.y + 50))    
        
    def handle_guess(self, events):
        if not self.guessing_mode:
            return
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.guess['npc'] = self.npcList_names[0]
                elif event.key == pygame.K_2:
                    self.guess['npc'] = self.npcList_names[1]
                elif event.key == pygame.K_3:
                    self.guess['weapon'] = "Fork"
                elif event.key == pygame.K_4:
                    self.guess['weapon'] = "Knife"
                elif event.key == pygame.K_5:
                    self.guess['location'] = "House"
                elif event.key == pygame.K_6:
                    self.guess['location'] = "Forest"
                elif event.key == pygame.K_RETURN:
                    self.check_guess()
                    
    def display_message(self, message, color=(255, 255, 255)):
        """Display a message on the screen."""
        message_font = pygame.font.Font(None, 50)  # Create a font object
        message_surface = message_font.render(message, True, color)  # Render the message
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Center the message
        self.screen.blit(message_surface, message_rect)  # Draw the message on the screen
        pygame.display.update()  # Update the display
        pygame.time.delay(2000)  # Pause for 2 seconds to show the message
        
    def check_guess(self):
        print(f"Player's guess: NPC={self.guess['npc']}, Weapon={self.guess['weapon']}, Location={self.guess['location']}")
        print(f"Correct values: NPC={self.murderer}, Weapon={self.weapon}, Location={self.weapon_location}")

        if (self.guess["npc"].lower() == self.murderer.lower() and
            self.guess["weapon"].lower() == self.weapon.lower() and
            self.guess["location"].lower() == self.weapon_location.lower()):
                self.display_message("yayyyy you are correct", color=(DARK_RED))
                print("wooooo! you solved it")
                self.guessing_mode = False    
        else:
            print("hmm something seems wrong. try again")
            self.display_message("Hmm, something seems wrong. Try again.", color=(DARK_RED))
        
            
    def handle_item_pickup(self):
        for obstacle in self.obstacles:
            if isinstance(obstacle, Item) and obstacle.rect and self.player.rect.colliderect(obstacle.rect):
                self.inventory.add_items(obstacle)  # Add the item to the inventory
                self.obstacles.remove(obstacle)  # Remove the item from the world
                print(f"Picked up: {obstacle.name}")
                          
    def handle_events(self,events):
         for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.handle_dialog()  # Advance dialog on Tab key
                elif event.key == pygame.K_RETURN:
                    if self.check_transition():
                        return
                elif event.key == pygame.K_ESCAPE:
                    if self.inventoryOpen:  # Close inventory if it's open
                        self.inventoryOpen = False
                    else:  # Otherwise, quit the game
                        self.running = False
                elif event.key == pygame.K_e:  # Press e to pick up items
                    self.handle_item_pickup()
                elif event.key == pygame.K_i:  # Toggle inventory with 'I'
                    self.inventoryOpen = not self.inventoryOpen
                elif event.key == pygame.K_g:
                    self.guessing_mode = not self.guessing_mode
                    if self.guessing_mode:
                        print("Guessing mode enabled. Press G again to disable.")
                    else:
                        print("Guessing mode disabled.")
#Update and Drawing
    def update(self):
        keys = get_pressed_keys()
        proposed_rect = self.player.rect.copy()
            # Move the player based on input
        self.player.move(keys, self.obstacles)
            # cannot exite our the bondaries of map.
        self.player.rect.left = max(self.player.rect.left, 0)
        self.player.rect.top = max(self.player.rect.top, 0)
        self.player.rect.right = min(self.player.rect.right, self.forrest.get_width())
        self.player.rect.bottom = min(self.player.rect.bottom, self.forrest.get_height())

#PLAYER POSITION
        print(f"Player position: ({self.player.rect.x}, {self.player.rect.y})")

    # Update animation
        dt = self.clock.get_time()
        self.player.update_animation(dt)
        for npc in self.npcList:
            npc.update_animation(dt)

    # Restrict the camera to the boundaries of the background
        self.camera_offset[0] = max(0, min(self.player.rect.centerx - SCREEN_WIDTH // 2, self.forrest.get_width() - SCREEN_WIDTH))
        self.camera_offset[1] = max(0, min(self.player.rect.centery - SCREEN_HEIGHT // 2, self.forrest.get_height() - SCREEN_HEIGHT))

    def draw_background(self):
        self.screen.fill(DARK_RED)
        self.screen.blit(self.forrest, (-self.camera_offset[0], -self.camera_offset[1]))
        self.screen.blit(self.path, (-self.camera_offset[0], -self.camera_offset[1])) 
              
    def draw_sprites(self):
    # Create a list of all sprites (player, NPCs, and other objects) for depth sorting
        sprites = self.npcList + [self.player] + self.obstacles
    # Sort sprites by their y position (rect.bottom) for depth ordering
        sprites.sort(key=lambda sprite: sprite.rect.bottom)
        for sprite in sprites:
            if hasattr(sprite, "current_animation"):  # For NPCs and player
                self.screen.blit(sprite.current_animation[sprite.current_frame], (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1]))
            elif hasattr(sprite, "image"):  # For static objects like trees or items
                self.screen.blit(sprite.image, (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1]))
     # Ensure items are drawn properly
        for obstacle in self.obstacles:
            if isinstance(obstacle, Item) and obstacle.image:
                self.screen.blit(obstacle.image, (obstacle.rect.x - self.camera_offset[0], obstacle.rect.y - self.camera_offset[1]))
                
    def draw_gui(self):
        if self.inventoryOpen:
            self.inventory.display(self.screen, self.dialog_font, SCREEN_WIDTH, SCREEN_HEIGHT)
        
    def draw(self):
        self.draw_background()
        self.draw_sprites()
        self.draw_gui()
        pygame.display.flip()
        
     #checking the area
   

    def run(self):
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)

            if self.guessing_mode:
            # Draw only the guessing UI
                self.screen.fill((0, 0, 0))  # Clear the screen (black background)
                self.draw_guessing_ui()
                self.handle_guess(events)
            else:
            # Normal game updates and rendering
                self.update()
                self.draw()

            self.clock.tick(60)  # Limit frame rate
            pygame.display.update()  # Update the display

    # Quit Pygame
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    game = Game()
    game.run()