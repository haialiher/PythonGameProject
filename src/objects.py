import pygame

class Tree:
    def __init__(self, image_path, x, y, width, height, trunk_base_offset=0):
        self.image = pygame.image.load(image_path)
        # Example path: "assets/images/environment/tree.png"
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        if trunk_base_offset:
            self.rect.bottom = y + height + trunk_base_offset
        self.collision_rect = self.rect.inflate(-45, -110)  # Adjust values 

class Bush:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        # Example path: "assets/images/environment/bush.png"
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.collision_rect = self.rect.inflate(-40, -36)  # Adjust values 

class Furniture:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.collision_rect = self.rect.inflate(-40, -50)
class Bed:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.collision_rect = self.rect.inflate(-20, -40)
 
class Item: 
    def __init__(self, name, description, image_path, x=None, y=None):
        self.name = name
        self.description = description
        self.image = pygame.image.load(image_path).convert_alpha()  # Ensure transparency
        # Example path: "assets/images/items/fork.png"
        self.image = pygame.transform.scale(self.image, (32, 32))  # Scale the item image
        # Scale smaller for inventory
        self.inventory_image = pygame.transform.scale(self.image, (32, 32))  
        # Initialize rect only if x and y are provided
        if x is not None and y is not None:
            self.rect = pygame.Rect(x, y, 32, 32)
            self.collision_rect = self.rect.inflate(-10, -10)  # Add a collision rectangle
        else:
            self.rect = None  # Default to None if position is not set
            self.collision_rect = None  # Default to None if position is not set

class House:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (240, 240))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collision_rect = self.rect.inflate(-60, -60)  # Shrink collision area horizontally and vertically

    def check_interaction(self, player_rect):
        # Check if the player interacts with the house
        if self.collision_rect.colliderect(player_rect):
            self.enter_callback()  # Trigger the transition to another setting

class TwinHouse: 
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (400, 280))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collision_rect = self.rect.inflate(-60, -60)  # Shrink collision area horizontally and vertically

    def check_interaction(self, player_rect):
        # Check if the player interacts with the house
        if self.collision_rect.colliderect(player_rect):
            self.enter_callback()  # Trigger the transition to another setting   
                  
class HouseWalls:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        # Example path: "assets/images/environment/house_walls.png"
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        # Adjust collision rectangle to allow the player to appear in front
        self.collision_rect = self.rect.inflate(-20, -60)  # Shrink collision area horizontally and vertically      


def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines
class Inventory:
    def __init__(self):
        self.items = []  # List to hold items in the inventory
        self.clues = []
    def add_items(self, item):
        self.items.append(item)
    
    def add_clue(self, clue):
        self.clues.append(clue)
        
    def remove_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]
        
    # ...existing code...
    def display(self, screen, font, screenWidth, screenHeight, scroll_offset=0, max_lines=10):
        inventoryBox = pygame.Rect(50, 50, screenWidth - 100, screenHeight - 100)
        pygame.draw.rect(screen, (130, 110, 150), inventoryBox)
        pygame.draw.rect(screen, (255, 255, 255), inventoryBox, 2)
        
        max_text_width = inventoryBox.width - 80  # Adjust as needed for padding/icons
        lines = []
        for item in self.items:
            item_text = f"{item.name}: {item.description}"
            wrapped = wrap_text(item_text, font, max_text_width)
            for line in wrapped:
                lines.append(('item', line, item.inventory_image if hasattr(item, 'inventory_image') else None))
        if self.clues:
            lines.append(('title', "Clues:", None))
            for clue in self.clues:
                wrapped = wrap_text(clue, font, max_text_width)
                for line in wrapped:
                    lines.append(('clue', line, None))
        
        visible_lines = lines[scroll_offset:scroll_offset + max_lines]
        y_offset = 70
        for kind, content, img in visible_lines:
            if kind == 'item':
                if img:
                    screen.blit(img, (inventoryBox.x + 10, inventoryBox.y + y_offset - 20))
                textSurface = font.render(content, True, (255, 255, 255))
                screen.blit(textSurface, (inventoryBox.x + 60, inventoryBox.y + y_offset))
                y_offset += 30
            elif kind == 'title':
                clue_title = font.render(content, True, (255, 255, 0))
                screen.blit(clue_title, (inventoryBox.x + 10, inventoryBox.y + y_offset))
                y_offset += 30
            elif kind == 'clue':
                clueSurface = font.render(content, True, (255, 255, 255))
                screen.blit(clueSurface, (inventoryBox.x + 20, inventoryBox.y + y_offset))
                y_offset += 30

        # Draw help message at the bottom
        help_text = "Use the UP and DOWN arrows to scroll."
        help_surface = font.render(help_text, True, (255, 255, 255))
        help_x = inventoryBox.x + (inventoryBox.width - help_surface.get_width()) // 2
        help_y = inventoryBox.y + inventoryBox.height - help_surface.get_height() - 10
        screen.blit(help_surface, (help_x, help_y))