import os
import random
import sys


# Add the parent directory of 'src' to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from src.npc import NPC
from src.player import Player
from src.input import get_pressed_keys  # Import the helper function
from src.objects import Bed, Furniture, HouseWalls, Inventory, Item, Tree, Bush, House, TwinHouse  # Import Tree, Bush, and House classes

PALE_SAGE_GREEN = (152, 193, 153)
DARK_RED = (40, 0, 0)
BRIGHT_PINK = (217,83,127)    
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700  
PLAYER_START_POSITION = (714, 1000)
HOUSE_POSITION = (845, 750)

HOUSE_RECT = pygame.Rect(0, 0, 651, 612)
FOREST_RECT = pygame.Rect(0, 0, 1550, 1200)
TWIN_HOUSE_RECT = pygame.Rect(0, 0, 1050, 725)

class Game:
    def __init__(self):
        
    # pygame starts
        self.running = True
        self.show_tutorial = True
        self.showing_intro_dialog = True
        pygame.init()
       
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("idek yet")
               
        self.intro_dialog = [
            "Folks say something bad happened in the town...",
            "Help the town figure out the mystery by talking to people to get clues.",
            "Pick up the weapons and look at their descriptions.",
            "All the people in the town have seen something.",
            "Keep everything they say in mind, it might be useful later!",
            "Or not....",
            "Press ENTER to begin your investigation."
        ]
        self.intro_dialog_index = 0
    # initialize stuffs    
        self.dialog_font = pygame.font.Font( "assets/pixelFont.otf", 27)
        self.current_area = "forest" 
        self.inventory = Inventory() 
        self.inventory_scroll_offset = 0
        self.inventoryOpen = False  
        self.guessing_mode = False
        self.guess = {"npc": None, "weapon": None, "location": None}      
    # player and Camera
        self.camera_offset = [0, 0]    
        self.player = Player(
            "assets/images/characters/MC.png", 
            714,  # X position
            1000, # Y position
            5, 
            scale=(50, 50), 
            frame_size=(32, 35) 
        )
          
    # Obstacle lists
        self.obstacles = []
        self.forest_obstacles = []  # Store forest-specific obstacles
        self.house_obstacles = []   # Store house-specific obstacles
        self.twin_house_obstacles = []

        #npcs
        self.house_npcs = []  # Store house-specific NPCs
        self.forest_npcs = []  # Store forest-specific NPCs   
        self.npcList = []  
        self.npc_positions = {}  
        self.load_forest_setting()
        self.clock = pygame.time.Clock()
        self.setup_background_and_scaling("assets/backgrounds/forest/forest.png", 
                                "assets/backgrounds/forest/path.png")

#scaling background          
    def setup_background_and_scaling(self, background_path, path_path):
        self.forest = pygame.image.load(background_path).convert_alpha()
        self.path = pygame.image.load(path_path).convert_alpha()
    #calculate scaling factor based on player size
        bg_width, bg_height = self.forest.get_size()
        scale_factor = min(self.player.scale[0] / 32, self.player.scale[1] / 32)  
        new_width = int(bg_width * scale_factor)
        new_height = int(bg_height * scale_factor)
        self.forest = pygame.transform.scale(self.forest, (new_width, new_height))
        self.path = pygame.transform.scale(self.path, (new_width, new_height))  

#loading objects that will be randomized, basically            
    def load_npc(self):
        innocent_dialog = [
            "I saw {murderer} near the {location} earlier.",
            "That {weapon} looks dangerous, don’t you think?",
            "People say {murderer} has been acting strange lately.",
            "The {location} is where things got really suspicious.",
            "I heard someone talking about a {weapon} around here.",
            "Could {murderer} have been at the {location} when it happened?",
            "There’s no way the crime was done without that {weapon}.",
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
            "No one’s really sure why that {weapon} was there.",
            "The {location} has been a hotspot for trouble lately.",
            "I caught {murderer} looking nervous when the {weapon} was mentioned.",
            "Not many people know what happened at the {location}, but it wasn’t good.",
            "That {weapon} could easily have been used for something bad.",
            "You never know what {murderer} is really up to.",
            "I wouldn’t be surprised if the {weapon} was planted there.", 
            ]
        murderer_dialog = [
            "Oh sure, blame the one that was holding the {weapon}.",
            "Yeah, because *nothing* suspicious ever happens in the {location}.",
            "The {weapon}? Never seen it in my life. I just *happened* to be seen with it.",
            "Wow, a murder in the {location}? Shocking. ",
            "Honestly, if I had a dollar for every time someone asked about that {weapon}… I’d own the {location}.",
            "Please, like anyone with half a brain would leave the {weapon} just lying around in the {location}.",
            "Oh, the {weapon}? I thought it was just décor.",
            "I only go to the {location} for the vibes, not the violence—usually.",
        ]

#ginger boy
        self.gingerBoy = NPC ("Ginger Boy",
            "assets/images/characters/npcGingerBoy.png", 
                531, 391,
                3, (50, 50), (32, 35),
                dialog=[ "I like the color blue",
                        "I dont really like the forest. it has too many bugs",]
        )
        #self.house_obstacles.append(self.gingerBoy)
        self.house_npcs.append(self.gingerBoy)
#green Twin
        self.greenTwin = NPC( "Green Twin",
            "assets/images/characters/npcGreenTwin.png", 
                710, 331, 
                3, (50, 50), (32, 35), 
                 dialog=[ "I'm trying to find my sister",
                         "My favorite color is actually pink but my sister said it could be.",
                         "I sorry I dont really have that much information.", 
                ] 
        )
        #self.forest_obstacles.append(self.greenTwin)
        self.forest_npcs.append(self.greenTwin)
#pink Twin
        self.pinkTwin = NPC( "Pink Twin",
            "assets/images/characters/npcPinkTwin.png", 
                613, 953, 
                3, (50, 50), (32, 35), 
                dialog= ["Ew go away.",
                        "Why are you speaking to me ?", 
                        ]
        )
        #self.forest_obstacles.append(self.pinkTwin)
        self.forest_npcs.append(self.pinkTwin)
        
        if self.greenTwin not in self.forest_npcs:
            self.forest_npcs.append(self.greenTwin)
        if self.pinkTwin not in self.forest_npcs:
            self.forest_npcs.append(self.pinkTwin)   
        if self.gingerBoy not in self.house_npcs:
            self.house_npcs.append(self.gingerBoy)

        
        self.npcList_names = [self.greenTwin.name, self.pinkTwin.name,self.gingerBoy.name]  # Store NPC names for dialo
        self.murderer = random.choice(self.npcList_names)
        print(f"Random murderer: {self.murderer}")
         
        if self.murderer != self.greenTwin.name: 
            self.greenTwin.dialog.extend(innocent_dialog)
        else:  
            self.greenTwin.dialog.extend(murderer_dialog)
            
        if self.murderer != self.pinkTwin.name: 
            self.pinkTwin.dialog.extend(innocent_dialog)
        else:  
            self.pinkTwin.dialog.extend(murderer_dialog)
               
        if self.murderer != self.gingerBoy.name: 
            self.gingerBoy.dialog.extend(innocent_dialog)
        else:  
            self.gingerBoy.dialog.extend(murderer_dialog)   
    def load_items(self):

        self.item_names = ["Fork", "Knife", "Bat","Brick","Mug", ]
        self.weapon = random.choice(self.item_names)
        self.location_names = ["house", "forest","twin's house"]
        self.weapon_location = random.choice(self.location_names)
        print(f" Random Weapon: {self.weapon} \nRandom Location: {self.weapon_location}") 
#where weapons are located 
    #Fork
        if self.weapon == "Fork":
            if self.weapon_location == "forest":
                self.fork = Item("Fork", "kind of pointy, looks like it was hidden. ", "assets/images/items/fork.png", 1316, 718)
                self.forest_obstacles.append(self.fork)
            elif self.weapon_location == "house":
                self.fork = Item("Fork", "kinda of pointy, looks used.", "assets/images/items/fork.png", 300, 400)
                self.house_obstacles.append(self.fork)
            elif self.weapon_location == "twin's house":
                self.fork = Item("Fork", "dull but is very used. ", "assets/images/items/fork.png", 231, 220)
                self.twin_house_obstacles.append(self.fork)
    #Knife
        elif self.weapon == "Knife":
            if self.weapon_location == "forest":
                self.knife = Item("Knife", "it was tossed into the grass", "assets/images/items/knife.png", 435, 955)
                self.forest_obstacles.append(self.knife)
            elif self.weapon_location == "house":
                self.knife = Item("Knife", "it was used to cut things recently", "assets/images/items/knife.png", 360, 195)
                self.house_obstacles.append(self.knife)
            elif self.weapon_location == "twin's house":
                self.knife = Item("Knife", "it was used to cut things recently", "assets/images/items/knife.png", 900, 487)
                self.twin_house_obstacles.append(self.knife)
    #bat
        elif self.weapon == "Bat":
            if self.weapon_location == "forest":
                self.bat = Item("Bat", "looks lost or purposely placed", "assets/images/items/bat.png", 1095, 110)
                self.forest_obstacles.append(self.bat)
            elif self.weapon_location == "house":
                self.bat = Item("Bat", "Possibly used for Baseball or other things.", "assets/images/items/bat.png", 120, 422)
                self.house_obstacles.append(self.bat)
            elif self.weapon_location == "twin's house":
                self.bat = Item("Bat", "Used for baseball but the twins don't play.", "assets/images/items/bat.png", 841, 208)
                self.twin_house_obstacles.append(self.bat)
    #brick
        elif self.weapon == "Brick":
            if self.weapon_location == "forest":
                self.brick = Item("Brick", "Heavy, the contruction site is 16 miles away", "assets/images/items/brick.png", 1480, 349)
                self.forest_obstacles.append(self.brick) 
            elif self.weapon_location == "house":
                self.brick = Item("Brick", "Heavy, why would it be in the house", "assets/images/items/brick.png", 582, 534)
                self.house_obstacles.append(self.brick)
            elif self.weapon_location == "twin's house":
                self.brick = Item("Brick", "Heavy, twins don't do construction", "assets/images/items/brick.png", 311, 474)
                self.twin_house_obstacles.append(self.brick)
    #mug
        elif self.weapon == "Mug":
            if self.weapon_location == "forest":
                self.mug = Item("Mug", "Chipped, looks like it hasn't been used for drinks", "assets/images/items/mug.png", 1510, 466) 
                self.forest_obstacles.append(self.mug) 
            elif self.weapon_location == "house":
                self.mug = Item("Mug", "Old and Chipped, has dust on the inside ", "assets/images/items/mug.png", 191, 533) 
                self.house_obstacles.append(self.mug) 
            elif self.weapon_location == "twin's house":
                self.mug = Item("Mug", "Chipped, Twins HATE coffee why did they have this ", "assets/images/items/mug.png", 900, 487) 
                self.twin_house_obstacles.append(self.mug)
    #pipe  
        elif self.weapon == "Pipe":
            if self.weapon_location == "forest":
                self.pipe = Item("Pipe", "Has a large dent and hairs on it ", "assets/images/items/pipe.png", 615, 15) 
                self.forest_obstacles.append(self.pipe) 
            elif self.weapon_location == "house":
                self.pipe = Item("Pipe", "No one has done construction in house recently ", "assets/images/items/pipe].png", 191, 533) 
                self.house_obstacles.append(self.pipe) 
            elif self.weapon_location == "twin's house":
                self.pipe = Item("Pipe", " The Twins just cleaned after construction was done ", "assets/images/items/pipe.png", 391, 410) 
                self.twin_house_obstacles.append(self.pipe)
#if they arent a weapon,                
        if self.weapon != "Fork":
                self.fork = Item("Fork", "Brand new but might be misplaced", "assets/images/items/fork.png", 400, 613)
                self.forest_obstacles.append(self.fork)
        if self.weapon != "Knife":
                self.knife = Item("Knife", "so shiny you can see your reflection", "assets/images/items/knife.png", 500, 305)
                self.twin_house_obstacles.append(self.knife)
        if self.weapon != "Bat":
            self.bat = Item("Bat", "Lost baseball bat hopefully owner comes by", "assets/images/items/bat.png", 189, 828)
            self.forest_obstacles.append(self.bat)
        if self.weapon != "Brick":
            self.brick = Item("Brick", "Heavy, truck must've dropped it", "assets/images/items/brick.png", 74, 62)
            self.forest_obstacles.append(self.brick)
        if self.weapon != "Mug":
            self.mug = Item("Mug", "Still has some coffee in it", "assets/images/items/mug.png" , 548,60)
            self.house_obstacles.append(self.mug)
        if self.weapon != "Pipe":
            self.pipe = Item("Pipe", " The Twins just had construction done ", "assets/images/items/pipe.png", 391, 410) 
            self.twin_house_obstacles.append(self.pipe)

    #forest loading
    def load_forest_setting(self):
        self.load_npc()  # Load NPCs
        self.load_items()  # Load items
        self.draw_trees_and_bushes()  # Load trees and bushes
        self.house = House("assets/images/environment/house.png", *HOUSE_POSITION, 80, 94)
        self.twinHouse = TwinHouse("assets/images/environment/twinHouse.png", 170, 190, 400, 280)
        self.npcList.clear()  # Remove house NPCs
        self.npcList.extend(self.forest_npcs)  # Add forest NPCs dynamically
        self.forest_obstacles.extend(self.trees + self.bushes + [self.house] + [self.twinHouse])
        self.obstacles = self.forest_obstacles
    def load_forest_from_house(self):
        print("Returning to forest...")
        self.setup_background_and_scaling("assets/backgrounds/forest/forest.png", "assets/backgrounds/forest/path.png")
        self.obstacles = self.forest_obstacles
        self.npcList.clear()
        self.npcList.extend(self.forest_npcs)
        for npc in self.npc_positions:
            npc.rect.topleft = self.npc_positions[npc]
        #self.npcList.extend([self.greenTwin, self.pinkTwin])
        self.player.rect.topleft = (942, 962)        
    def load_forest_from_twin_house(self):
        print("Returning to forest...")
        self.setup_background_and_scaling("assets/backgrounds/forest/forest.png", "assets/backgrounds/forest/path.png")
        self.obstacles = self.forest_obstacles
        self.npcList.clear()
        self.npcList.extend(self.forest_npcs)
        for npc in self.npc_positions:
            npc.rect.topleft = self.npc_positions[npc]
        #self.npcList.extend([self.greenTwin, self.pinkTwin])
        self.player.rect.topleft = (347, 442)     
    #house             
    def load_house_setting(self):
        self.setup_background_and_scaling("assets/backgrounds/house/Housefloors.png", "assets/backgrounds/house/Housefloors.png")
        self.obstacles = self.house_obstacles
        self.draw_housewalls()  # Load house walls
        self.draw_house_furn()   #furniture
        self.npcList.clear()
        self.npcList.extend(self.house_npcs)
        
        self.player.rect.topleft = (325, 612)
        for npc in self.npcList:
            self.npc_positions[npc] = npc.rect.topleft
         #removing ig they are in forest    
    #twin's house
    def load_twinHouse_setting(self):
        print("Loading new setting...")
        self.setup_background_and_scaling("assets/backgrounds/twinHouse/twinHouseInside.png", "assets/backgrounds/twinHouse/twinHouseInside.png")
        self.npcList.clear()
        self.draw_twinhousewalls()
        self.draw_twin_house_furn()
        self.obstacles = self.twin_house_obstacles 
        self.player.rect.topleft = (466, 654)
        for npc in self.npcList:
            self.npc_positions[npc] = npc.rect.topleft
    
#checking where player    
    def check_location(self):
    # Transition from forest to house
        if 932 <= self.player.rect.x <= 997 and 937 <= self.player.rect.y <= 970:
            if self.current_area == "forest":
                print("to the house...")
                self.load_house_setting()
                self.current_area = "house"
                return True
    # Transition from house to forest
        elif 285 <= self.player.rect.x <= 370 and 582 <= self.player.rect.y <= 612:
            if self.current_area == "house":
                print("to the forest...")
                self.load_forest_from_house()
                self.current_area = "forest"
                return True
    #transition from forest to Twin House 
        elif 326 <= self.player.rect.x <= 400 and 440 <= self.player.rect.y <= 470:
            if self.current_area == "forest": 
                print("to the Twin's house...")
                self.load_twinHouse_setting() 
                self.current_area = "twin house"
                return True
    #Twin House to Forest
        elif 390 <= self.player.rect.x <= 560 and 630 <= self.player.rect.y <= 670:
            if self.current_area == "twin house":
                print("to the forest...")
                self.load_forest_from_twin_house()
                self.current_area = "forest"
                return True            
    def check_near_npc(self, player_rect, npc_rect, proximity_range=50):
        distance = ((player_rect.centerx - npc_rect.centerx) ** 2 + (player_rect.centery - npc_rect.centery) ** 2) ** 0.5
        return distance <= proximity_range    
    def check_near_item(self, player_rect, item_rect, proximity_range=50):
        distance = ((player_rect.centerx - item_rect.centerx) ** 2 + (player_rect.centery - item_rect.centery) ** 2) ** 0.5
        return distance <= proximity_range
    
#Handle key events                               
    def handle_item_pickup(self):
        for obstacle in self.obstacles:
            if isinstance(obstacle, Item) and obstacle.rect and self.player.rect.colliderect(obstacle.rect):
                self.inventory.add_items(obstacle)  # Add the item to the inventory
                self.obstacles.remove(obstacle)  # Remove the item from the world
                print(f"Picked up: {obstacle.name}")                
    def handle_dialog(self):
        for npc in self.npcList:
            if self.player.rect.colliderect(npc.rect):  
                if npc.interaction_count >= 4:  
                    self.display_dialog("I have nothing else to say.", npc_name=npc.name)
                    #print(f"{npc.name} has no dialog left.") 
                    return
                
                dialog = random.choice(npc.dialog)  
                if dialog:  # Ensure dialog is not None
                    try:
                        # Format the dialog with the correct keys
                        formatted_dialog = dialog.format(murderer=self.murderer, weapon=self.weapon, location=self.weapon_location)
                        self.display_dialog(formatted_dialog, npc_name=npc.name)
                        npc.dialog.remove(dialog)
                        self.inventory.add_clue(f"{npc.name}: {formatted_dialog}")
                    except KeyError as e:
                        print(f"Error formatting dialog: {e}")
                        self.display_dialog("Something seems off with the dialog.", npc_name=npc.name)
                
                npc.interaction_count += 1  # Increment interaction count for this NPC
                #print(f"{npc.name} interaction count: {npc.interaction_count}")                  
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

            # Inventory open: handle scrolling and closing
            if self.inventoryOpen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.inventory_scroll_offset += 1
                    elif event.key == pygame.K_UP:
                        self.inventory_scroll_offset = max(0, self.inventory_scroll_offset - 1)
                    elif event.key == pygame.K_ESCAPE:
                        self.inventoryOpen = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Mouse wheel up
                        self.inventory_scroll_offset = max(0, self.inventory_scroll_offset - 1)
                    elif event.button == 5:  # Mouse wheel down
                        self.inventory_scroll_offset += 1
                continue  # Skip further event handling if inventory is open

            # Tutorial and intro dialog handling
            if event.type == pygame.KEYDOWN:
                if self.show_tutorial:
                    if event.key == pygame.K_RETURN:
                        self.show_tutorial = False
                elif self.showing_intro_dialog and event.key == pygame.K_RETURN:
                    self.intro_dialog_index += 1
                    if self.intro_dialog_index >= len(self.intro_dialog):
                        self.showing_intro_dialog = False
                else:
                    if event.key == pygame.K_TAB:
                        self.handle_dialog()
                    elif event.key == pygame.K_RETURN:
                        if self.check_location():
                            return
                    elif event.key == pygame.K_ESCAPE:
                        self.show_tutorial = True
                    elif event.key == pygame.K_e:
                        self.handle_item_pickup()
                    elif event.key == pygame.K_c:
                        self.inventoryOpen = not self.inventoryOpen
                    elif event.key == pygame.K_g:
                        self.guessing_mode = not self.guessing_mode
    def handle_guess(self):
        print(f"Player's guess: NPC={self.guess['npc']}, Weapon={self.guess['weapon']}, Location={self.guess['location']}")
        print(f"Correct values: NPC={self.murderer}, Weapon={self.weapon}, Location={self.weapon_location}")

        if (self.guess["npc"] == self.murderer and
            self.guess["weapon"] == self.weapon and
            self.guess["location"]== self.weapon_location):
                self.draw_display_message("yayyyy you are correct", color=(157, 193, 131))
                print("wooooo! you solved it")
                self.guessing_mode = False   
                self.running = False 
        elif (self.guess["npc"] == None or
            self.guess["weapon"] == None or
            self.guess["location"]== None):
            self.draw_display_message("Guess can't be blank.", color=(224, 33, 138))
        else:
            print("hmm something seems wrong. try again")
            self.draw_display_message("Hmm, something seems wrong. Try again.", color=(224, 33, 138))

#drawing objects and stuffs
    def draw_tutorial(self):
        """Render the tutorial screen with instructions."""
        self.screen.fill((DARK_RED))  # Fill the screen with black

    # Display tutorial text
        font = pygame.font.Font("assets/pixelFont.otf", 40)
        instructions = [
            "There's clues hidden in item descriptions and npc text",
            "",
            "Controls:",
            "'WASD' to move.",
            "'TAB' to talk to NPCs", 
            "'E' to pick up items.",
            "'C' to open your clues.", 
            "'ESC' to open control menu.",
            "",
            "Use the 'G' key to enter guessing mode when ready.",
            "",
            "Press ENTER."
        ]
        total_height = len(instructions) * 45  
        start_y = (SCREEN_HEIGHT - total_height) // 2

        # Render each line of text
        for i, line in enumerate(instructions):
            text_surface = font.render(line, True, (255, 255, 255))  # White text
            text_width = text_surface.get_width()
            x = (SCREEN_WIDTH - text_width) // 2  # Center horizontally
            y = start_y + i * 40  # Position each line with spacing
            self.screen.blit(text_surface, (x, y))

        pygame.display.flip()  # Update the display    
    
    def draw_intro_dialog(self, screen):
        if self.showing_intro_dialog:
            font = pygame.font.Font("assets/pixelFont.otf", 32)
            dialog = self.intro_dialog[self.intro_dialog_index]
            text_surface = font.render(dialog, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surface, text_rect)
    #forest
    def draw_trees_and_bushes(self):
        self.trees = [
            Tree("assets/images/environment/tree.png", 1039, 332, 74, 94),
            Tree("assets/images/environment/tree.png", 1341, 539, 74, 94),
            Tree("assets/images/environment/tree.png", 1463, 267, 74, 94),
            Tree("assets/images/environment/tree.png", 920, 400, 74, 94),
            Tree("assets/images/environment/tree.png", 500, 632, 74, 94),
            Tree("assets/images/environment/tree.png", 1000, 700, 74, 94),
            Tree("assets/images/environment/tree.png", 1100, 750, 74, 94),
            Tree("assets/images/environment/tree.png", 200, 700, 74, 94),
            Tree("assets/images/environment/tree.png", 1140, 540, 74, 94),
            #Tree("assets/images/environment/tree.png", 228, 540, 74, 94),
            Tree("assets/images/environment/tree.png", 467, 300, 74, 94),
            Tree("assets/images/environment/tree.png", 150, 200, 74, 94),
            Tree("assets/images/environment/tree.png", 800, 100, 74, 94),
            Tree("assets/images/environment/tree.png", 900, 50, 74, 94),
            Tree("assets/images/environment/tree.png", 590, 780, 74, 94),
            Tree("assets/images/environment/tree.png", 52, 826, 74, 94),
            Tree("assets/images/environment/tree.png", 85, 619, 74, 94),
            Tree("assets/images/environment/tree.png", 434, 900, 74, 94),
            Tree("assets/images/environment/tree.png", 73, 246, 74, 94),
            Tree("assets/images/environment/tree.png", 200, 900, 74, 94),
            Tree("assets/images/environment/tree.png", 100, 1200, 74, 94),
            Tree("assets/images/environment/tree.png", 50, 1300, 74, 94),
            Tree("assets/images/environment/tree.png", 150, 1400, 74, 94),
        ]
    #bushes (don't place at (x =700) )
        self.bushes = [
            Bush("assets/images/environment/bush.png", 600, 400, 50, 50),
            Bush("assets/images/environment/bush.png", 1242, 331, 50, 50),
            Bush("assets/images/environment/bush.png", 1512, 537, 50, 50),
            Bush("assets/images/environment/bush.png", 861, 260, 50, 50),
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
    #house                     
    def draw_house_furn(self):
        self.pinkBed = Bed("assets/images/furniture/pinkBed.png",150,20,80,150)
        self.PinkbedsideTable = Furniture("assets/images/furniture/PinkbedsideTable.png",50,20,64,64)
        self.pinkDresser = Furniture("assets/images/furniture/dresser.png",250,0, 64,90 )
        
        self.fridge = Furniture("assets/images/furniture/fridge.png", 405, 0 , 60, 100)
        self.stove = Furniture("assets/images/furniture/stove.png", 465, 20, 64,74 )
        self.counter = Furniture("assets/images/furniture/counter.png", 530, 20, 70,64 )
        self.counter2 = Furniture("assets/images/furniture/counter.png", 580, 20, 70,64 )
        self.house_obstacles.extend([
            self.pinkBed, self.PinkbedsideTable,self.pinkDresser,
            self.fridge, self.stove, self.counter, self.counter2,
        ])
    def draw_housewalls(self):
        self.HouseWallsLeft = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsLeft.png", 0, 0, 48, 700)
        self.HouseWallsRight = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsRight.png", 651, 0, 48, 700)
        self.HouseWallsTop = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsTop.png", 0, 0, 700, 56)

        self.HouseWallsBotLeft = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsBotLeft.png", 0, 605, 300, 120)
        self.HouseWallsBotRight = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsBotRight.png", 400, 605, 300, 120)
        self.HousewallsMidLeft = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsMidLeft.png", 0, 290, 300, 70)
        self.HousewallsMidRight = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsMidRight.png", 400, 290, 300, 70)
        self.HousewallsMid = HouseWalls("assets/backgrounds/house/HouseWalls/HouseWallsMid.png", 400, 190, 50, 120)
        
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
        #twin's house
    #twin's house
    def draw_twin_house_furn(self):
    #bedrooms
        self.greenBed = Bed("assets/images/furniture/greenBed.png",150,20,80,150)
        self.greenBedTable = Furniture("assets/images/furniture/greenBedTable.png", 80,30,64,64)
        self.greenDresser = Furniture("assets/images/furniture/greenDresser.png",250,10, 64,90 )
        self.pinkBed = Bed("assets/images/furniture/pinkBed.png",830,20,80,150)
        self.PinkbedsideTable = Furniture("assets/images/furniture/PinkbedsideTable.png",930,30,64,64)
        self.pinkDresser = Furniture("assets/images/furniture/dresser.png",750, 10, 64,90 )
    #kitchen
        self.fridge = Furniture("assets/images/furniture/fridge.png", 715, 360 , 60, 100)
        self.stove = Furniture("assets/images/furniture/stove.png", 775, 385, 64,74 )
        self.counter = Furniture("assets/images/furniture/counter.png", 840, 390, 70,64 )
        self.counter2 = Furniture("assets/images/furniture/counter.png", 900, 390, 70,64 )
        
        
        self.twin_house_obstacles.extend([
           self.pinkBed, self.PinkbedsideTable, self.pinkDresser,
           self.greenBed, self.greenBedTable, self.greenDresser,
           self.fridge, self.stove, self.counter, self.counter2,
        ])
    def draw_twinhousewalls(self):
        self.THLeftBotWall = HouseWalls("assets/backgrounds/twinHouse/thWalls/THLeftBotWall.png",-2, 660, 400, 56) 
        self.THLeftWall = HouseWalls("assets/backgrounds/twinHouse/thWalls/THLeftWall.png", -2 , -2 , 56 ,725)
        self.THtopWall = HouseWalls("assets/backgrounds/twinHouse/thWalls/THtopWall.png", 0 , 0 , 1050 ,56)
        self.THRightWall = HouseWalls("assets/backgrounds/twinHouse/thWalls/THRightWall.png", 1000 , -20 , 56 ,725)
        self.THRightBotWall = HouseWalls("assets/backgrounds/twinHouse/thWalls/THRightBotWall.png", 600 , 660 , 400 ,56)
        self.THMidRightWall = HouseWalls("assets/backgrounds/twinHouse/thWalls/THMidRightWall.png", 620 , 340 , 380 ,90)
        self.THLeftMidWall = HouseWalls("assets/backgrounds/twinHouse/thWalls/THLeftMidWall.png", -2 , 360 , 400 ,80)
        self.THMidWall =  HouseWalls("assets/backgrounds/twinHouse/thWalls/THMidWall.png", 620 , 200 , 56 ,150)
        
        self.twin_house_obstacles.extend ([
            self.THLeftBotWall,
            self.THLeftWall,
            self.THtopWall,
            self.THRightWall,
            self.THRightBotWall,
            self.THMidRightWall,
            self.THLeftMidWall,
            self.THMidWall,
        ])
    #guessing stuffs     
    def draw_guessing_ui(self):
        guessingBox = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
        pygame.draw.rect(self.screen, (178, 156, 162), guessingBox)  # Background color for the guessing box
        pygame.draw.rect(self.screen, (255, 255, 255), guessingBox, 2)  # Border color
        # Render multi-line instructions
        instructions_lines = [
            "Choose category then use left and right arrows to choose",
            "Suspect (1), Weapon (2), Location (3)",
            "Click enter when ready to guess :p"
        ]
        line_height = self.dialog_font.get_height()
        for i, line in enumerate(instructions_lines):
            instructions = self.dialog_font.render(line, True, (255, 255, 255))
            instructions_width = instructions.get_width()
            instructions_x = guessingBox.x + (guessingBox.width - instructions_width) // 2
            instructions_y = guessingBox.y + 10 + i * line_height
            self.screen.blit(instructions, (instructions_x, instructions_y))


        current_guess = f"NPC: {self.guess['npc']}, Weapon: {self.guess['weapon']}, Location: {self.guess['location']}"
        guess_text = self.dialog_font.render(current_guess, True, (255, 255, 255))

        text_width, text_height = guess_text.get_size()
        text_x = guessingBox.x + (guessingBox.width - text_width) // 2
        text_y = guessingBox.y + (guessingBox.height - text_height) // 2
        self.screen.blit(guess_text, (text_x, text_y))
    def draw_guess_logic(self, events):
        if 'npc_index' not in self.__dict__:
            self.npc_index = 0  
        if 'weapon_index' not in self.__dict__:
            self.weapon_index = 0
        if 'location_index' not in self.__dict__:
            self.location_index = 0
    
        if not self.guessing_mode:
            return
    
        # Track the current category being guessed
        if 'current_category' not in self.__dict__:
            self.current_category = None   
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_category = "npc"
                elif event.key == pygame.K_2:
                    self.current_category = "weapon"
                elif event.key == pygame.K_3:
                    self.current_category = "location"

                elif event.key == pygame.K_LEFT:
                    if self.current_category == "npc":
                        self.npc_index = (self.npc_index - 1) % len(self.npcList_names)
                        self.guess['npc'] = self.npcList_names[self.npc_index]
                    elif self.current_category == "weapon":
                        self.weapon_index = (self.weapon_index - 1) % len(self.item_names)
                        self.guess['weapon'] = self.item_names[self.weapon_index]
                    elif self.current_category == "location":
                        self.location_index = (self.location_index - 1) % len(self.location_names)
                        self.guess['location'] = self.location_names[self.location_index]
                elif event.key == pygame.K_RIGHT:
                    if self.current_category == "npc":
                        self.npc_index = (self.npc_index + 1) % len(self.npcList_names)
                        self.guess['npc'] = self.npcList_names[self.npc_index]
                    elif self.current_category == "weapon":
                        self.weapon_index = (self.weapon_index + 1) % len(self.item_names)
                        self.guess['weapon'] = self.item_names[self.weapon_index]
                    elif self.current_category == "location":
                        self.location_index = (self.location_index + 1) % len(self.location_names)
                        self.guess['location'] = self.location_names[self.location_index]
    
                # Confirm guess
                elif event.key == pygame.K_RETURN:
                    self.handle_guess()                    
    def draw_display_message(self, message, color=None):
        """Display a message on the screen."""
        message_font = pygame.font.Font("assets/pixelFont.otf", 50)
        message_surface = message_font.render(message, True, color)
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        box_width = message_rect.width + 40  # Add padding to the box width
        box_height = message_rect.height + 20  # Add padding to the box height
        box_x = message_rect.x - 20  # Adjust box position for padding
        box_y = message_rect.y - 10  # Adjust box position for padding
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        pygame.draw.rect(self.screen, (0, 0, 0), box_rect)  # Black fill
        pygame.draw.rect(self.screen, (178, 156, 162), box_rect, 2)  # White border
 
        self.screen.blit(message_surface, message_rect)
        pygame.display.update()
        pygame.time.delay(2000)
    #player can click (shows them)
    def draw_interaction_message(self):
        message = "TAB to talk"
        font = pygame.font.Font("assets/pixelFont.otf", 24)
        text_surface = font.render(message, True, (BRIGHT_PINK))  
        
        background_surface = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 10), pygame.SRCALPHA)
        background_surface.fill((0, 0, 0, 128))
        
        self.screen.blit(background_surface, (5, 5))
        self.screen.blit(text_surface, (10, 10))        
    def draw_pickup_message(self):
        message = "Press E to pick up"
        font = pygame.font.Font("assets/pixelFont.otf", 24)
        text_surface = font.render(message, True, (BRIGHT_PINK))
        
        background_surface = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 10), pygame.SRCALPHA)
        background_surface.fill((0, 0, 0, 128))
        
        self.screen.blit(background_surface, (5, 5))
        self.screen.blit(text_surface, (10, 10))         
    def draw_transition_check(self):
        # Show "Enter" prompt if player is in any transition area
        if self.current_area == "forest" and 932 <= self.player.rect.x <= 997 and 937 <= self.player.rect.y <= 970:
            self.draw_transition_message("Enter")
        elif self.current_area == "house" and 285 <= self.player.rect.x <= 370 and 582 <= self.player.rect.y <= 612:
            self.draw_transition_message("Enter")
        elif self.current_area == "forest" and 326 <= self.player.rect.x <= 400 and 440 <= self.player.rect.y <= 470:
            self.draw_transition_message("Enter")
        elif self.current_area == "twin house" and 390 <= self.player.rect.x <= 560 and 630 <= self.player.rect.y <= 670:
            self.draw_transition_message("Enter")     
    def draw_transition_message(self, message):
        message = "ENTER"
        font = pygame.font.Font("assets/pixelFont.otf", 24)
        text_surface = font.render(message, True, (BRIGHT_PINK)) 
        
        background_surface = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 10), pygame.SRCALPHA)
        background_surface.fill((0, 0, 0, 128)) 

        self.screen.blit(background_surface, (5, 5))
        self.screen.blit(text_surface, (10, 10)) 
   
#Update/drawing everything
    def update(self):
        keys = get_pressed_keys()
        proposed_rect = self.player.rect.copy()
            # Move the player based on input
        self.player.move(keys, self.obstacles)
            #bondaries of map.
        self.player.rect.left = max(self.player.rect.left, 0)
        self.player.rect.top = max(self.player.rect.top, 0)
        self.player.rect.right = min(self.player.rect.right, self.forest.get_width())
        self.player.rect.bottom = min(self.player.rect.bottom, self.forest.get_height())#PLAYER POSITION

    # Update animation
        #dt = self.clock.get_time()
        dt = self.clock.tick(60)  #
        self.player.update_animation(dt)
        for npc in self.npcList:
            npc.update_animation(dt)
        for npc in self.house_npcs:
            npc.update_animation(dt)
            
        for npc in self.npcList:
            if npc.current_area == "forest":
                npc.update(dt, FOREST_RECT, self.obstacles)
            elif npc.current_area == "house":
                npc.update(dt, HOUSE_RECT, self.obstacles)
            elif npc.current_area == "twin house":
                npc.update(dt, TWIN_HOUSE_RECT, self.obstacles) 

    # Restrict the camera to the boundaries of the background
        self.camera_offset[0] = max(0, min(self.player.rect.centerx - SCREEN_WIDTH // 2, self.forest.get_width() - SCREEN_WIDTH))
        self.camera_offset[1] = max(0, min(self.player.rect.centery - SCREEN_HEIGHT // 2, self.forest.get_height() - SCREEN_HEIGHT))
    def display_dialog(self, dialog, npc_name=None):
        if not dialog or len(dialog) == 0:
            print("No dialog to display!")
            return
        pink = (222, 93, 131)  # Define the pink color for the text box
        print(f"Displaying dialog: {dialog}")  # Debugging statement
        text_box = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 50)
        self.screen.fill(pink, text_box)  # Clear the text box
        pygame.draw.rect(self.screen, (255, 255, 255), text_box, 2)
        text_surface = self.dialog_font.render(dialog, True, (255, 255, 255))
        self.screen.blit(text_surface, (text_box.x + 10, text_box.y + 10))
    # Display NPC name if provided
        if npc_name:
            name_surface = self.dialog_font.render(npc_name, True, (255, 255, 255))
            self.screen.blit(name_surface, (10, SCREEN_HEIGHT - 40))  # Adjust position as needed

        pygame.display.flip()

        tab_pressed = False
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 3000:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    tab_pressed = True
                    break
            if tab_pressed:
                break
    def draw_forest_background(self):
        self.screen.blit(self.forest, (-self.camera_offset[0], -self.camera_offset[1]))
        self.screen.blit(self.path, (-self.camera_offset[0], -self.camera_offset[1]))              
    def draw_sprites(self):
        # Only include objects with a rect attribute
        sprites = [sprite for sprite in (self.npcList + [self.player] + self.obstacles) if hasattr(sprite, "rect")]
        sprites.sort(key=lambda sprite: sprite.rect.bottom)
        for sprite in sprites:
            if hasattr(sprite, "current_animation"):  # NPCs and player
                self.screen.blit(sprite.current_animation[sprite.current_frame], (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1]))
            elif hasattr(sprite, "image"):  # Static objects like trees, bushes, items, houses
                self.screen.blit(sprite.image, (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1]))             
    def draw_gui(self):
        if self.inventoryOpen:
            self.inventory.display(
                self.screen, self.dialog_font, SCREEN_WIDTH, SCREEN_HEIGHT,
                scroll_offset=self.inventory_scroll_offset, max_lines=10
            )
        
        for npc in self.npcList:
            if self.check_near_npc(self.player.rect, npc.rect):
                self.draw_interaction_message()
                break
             
        for obstacle in self.obstacles:
            if isinstance(obstacle, Item) and self.check_near_item(self.player.rect, obstacle.rect):
                self.draw_pickup_message()
                break 
        self.draw_transition_check()        
    def draw(self):
        self.screen.fill(DARK_RED) 
        
        if self.showing_intro_dialog == True :
            self.draw_intro_dialog(self.screen)
        else:
            self.draw_forest_background()
            self.draw_sprites()
            self.draw_gui()
        pygame.display.flip()
    def run(self):
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)
            #print(f"Player position: ({self.player.rect.x}, {self.player.rect.y})")
            #print(self.current_area)
            if self.show_tutorial:
                self.draw_tutorial()
            elif self.guessing_mode:
            # Draw only the guessing UI
                #self.screen.fill((0, 0, 0))  # Clear the screen (black background)
                self.draw_guessing_ui()
                self.draw_guess_logic(events)
            else:
            # Normal game updates and rendering
                self.update()
                self.draw()
            pygame.display.update()  # Update the display

    # Quit Pygame
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    game = Game()
    game.run()