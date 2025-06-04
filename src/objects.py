import pygame

class Tree:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        # Example path: "assets/images/environment/tree.png"
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        # Shrink the collision rectangle to allow closer walking
        self.collision_rect = self.rect.inflate(-45, -110)  # Adjust values as needed

class Bush:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        # Example path: "assets/images/environment/bush.png"
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        # Shrink the collision rectangle to allow closer walking
        self.collision_rect = self.rect.inflate(-40, -36)  # Adjust values as needed
        
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
            
class HouseWalls:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        # Example path: "assets/images/environment/house_walls.png"
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        # Adjust collision rectangle to allow the player to appear in front
        self.collision_rect = self.rect.inflate(-20, -60)  # Shrink collision area horizontally and vertically      
class Inventory:
    def __init__(self):
        self.items = []  # List to hold items in the inventory
    def add_items(self, item):
        """Add an item to the inventory."""
        self.items.append(item)
    def remove_item(self, item_name):
        """Remove an item from the inventory."""
        self.items = [item for item in self.items if item.name != item_name]
    def display(self, screen, font, screenWidth, screenHeight):
        """Display the inventory items on the screen."""
        inventoryBox = pygame.Rect(50, 50, screenWidth - 100, screenHeight - 100)
        pygame.draw.rect(screen, (130, 110, 150), inventoryBox)
        pygame.draw.rect(screen, (255, 255, 255), inventoryBox, 2)
        
        y_offset = 70
        for item in self.items:
            if item.inventory_image:
                # Position the inventory image to the left of the text
                screen.blit(item.inventory_image, (inventoryBox.x + 10, inventoryBox.y + y_offset - 20))  # Adjust for larger image
            textSurface = font.render(f"{item.name}: {item.description}", True, (255, 255, 255))
            screen.blit(textSurface, (inventoryBox.x + 60, inventoryBox.y + y_offset))  # Adjust text position
            y_offset += 50  # Increase spacing for larger image
        


