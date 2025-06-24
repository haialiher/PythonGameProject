import random
import pygame

# Dictionary to cache loaded images
loaded = {}
sprites = []
class Sprite:
    def __init__(self, image, x, y, scale=None):
        if image in loaded:
            self.image = loaded[image]
        else:
            original_image = pygame.image.load(image)
            if scale:  # Ensure scale is a tuple (width, height)
                self.image = pygame.transform.scale(original_image, scale)
            else:
                self.image = original_image
            loaded[image] = self.image
        self.x = x
        self.y = y
        sprites.append(self)
        
    def delete(self):
        sprites.remove(self)
        
class NPC:
    def __init__(self, name, sprite_sheet_path, x, y, speed, scale, frame_size, dialog = None):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width, self.frame_height = frame_size
        self.name = name
        self.scale = scale
        self.interaction_count = 0
        self.animations = {
            "down": self.extract_frames(0, 7),
            "up": self.extract_frames(1, 7),
            "left": self.extract_frames(2, 7),
            "right": self.extract_frames(3, 7),
            "idle_down": self.extract_frames(4, 7),
            "idle_up": self.extract_frames(5, 7), 
            "idle_left": self.extract_frames(7, 7), 
            "idle_right": self.extract_frames(6, 7),  
        }
        self.current_animation = self.animations["idle_down"]
        self.rect = pygame.Rect(x, y, scale[0], scale[1])
        self.collision_rect = self.rect.inflate(-10, -20)  # Adjust values as needed
        self.speed = 3
        self.dialog = dialog or []  
        self.last_direction = "down"  
        self.current_frame = 0
        self.animation_timer = 0
        self.direction = "idle_down"
        self.move_timer = 0 
        self.current_area = "forest"
        
        if x is not None and y is not None:
            self.rect = pygame.Rect(x, y, 32, 32)
            self.collision_rect = self.rect.inflate(-10, -20)  # Add a collision rectangle
        else:
            self.rect = None  # Default to None if position is not set
            self.collision_rect = None  # Default to None if position is not set
        
    def interact(self):
        if self.dialog:
            return random.choice(self.dialog)
        else: 
            return "I have nothing to say....to you."
      
# in the interact I can give the NPC self dialogs but I can just make the clues
# in this so it will be a randomizer that picks between 0-2 
# if 0 or 1 = self dialog if 2 = clue dialog the game will add the clue dialog 67%
    
    def extract_frames(self, row, num_frames):
        frames = []
        for i in range(num_frames):
            try:
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(i * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
                )
                if self.scale:
                    frame = pygame.transform.scale(frame, self.scale)
                frames.append(frame)
            except Exception as e:
               print(f"Error extracting frame {i} from row {row}: {e}")
        #print(f"Extracted {len(frames)} frames for row {row}")
        return frames
    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer > 275:  # Adjust this value to control animation speed
            self.animation_timer = 1
            if len(self.current_animation) > 0:  # Ensure the animation is not empty
                self.current_frame = (self.current_frame + 1) % len(self.current_animation)
                #print(f"Current animation: {self.current_animation}, Current frame: {self.current_frame}")
           # else:
               # print("Warning: current_animation is empty!")
    

    def choose_random_direction(self):
        directions = ["up", "down", "left", "right", "idle", "up_right", "up_left", "down_right", "down_left"]
        self.direction = random.choice(directions)
        self.move_timer =  random.randint(1000,3000)
        #print(f"{self.name} chose direction {self.direction} for {self.move_timer}ms")
    
    def move(self, dt, boundaries, obstacles):
        # Determine dx, dy based on direction and speed
        dx, dy = 0, 0
        if self.direction == "up" and self.direction == "right":
            dy -= self.speed / 1.44
            dx += self.speed / 1.44
            self.current_animation = self.animations["right"]
            self.last_direction = "right"
        elif self.direction == "up" and self.direction == "left":
            dy -= self.speed / 1.44
            dx -= self.speed / 1.44
            self.current_animation = self.animations["left"]
            self.last_direction = "left"
        elif self.direction == "down" and self.direction == "left":
            dy += self.speed / 1.44
            dx -= self.speed / 1.44
            self.current_animation = self.animations["left"]
            self.last_direction = "left"
        elif self.direction == "down" and self.direction == "right":
            dy += self.speed / 1.44
            dx += self.speed / 1.44
            self.current_animation = self.animations["right"]
            self.last_direction = "right"
        elif self.direction == "left":
            dx -= self.speed
            self.current_animation = self.animations["left"]
            self.last_direction = "left"
        elif self.direction == "right":
            dx += self.speed
            self.current_animation = self.animations["right"]
            self.last_direction = "right"
        elif self.direction == "up":
            dy -= self.speed
            self.current_animation = self.animations["up"]
            self.last_direction = "up"
        elif self.direction == "down":
            dy += self.speed
            self.current_animation = self.animations["down"]
            self.last_direction = "down"
        else:
            self.current_animation = self.animations[f"idle_{self.last_direction}"]

        proposed_rect = self.rect.move(dx, dy)

        # Check for collision with obstacles
        for obs in obstacles:
            obs_rect = getattr(obs, 'collision_rect', getattr(obs, 'rect', None))
            if obs_rect and proposed_rect.colliderect(obs_rect):
                return  # Don't move if colliding

        # Optionally, check boundaries
        if boundaries and not boundaries.contains(proposed_rect):
            return

        # If no collision, move NPC
        self.rect = proposed_rect
        self.collision_rect.topleft = self.rect.topleft  # Ensure collision_rect is updated
        print(f"{self.name} moved to {self.rect.topleft}")  # Debugging
    
        # Reset animation frame if the animation has changed
            
    """def check_area_transition(self):
        FOREST_TO_HOUSE_TRANSITION = pygame.Rect(932, 937, 65, 33)
        HOUSE_TO_FOREST_TRANSITION = pygame.Rect(285, 582, 85, 30)
        FOREST_TO_TWIN_HOUSE_TRANSITION = pygame.Rect(326, 440, 74, 30)
        TWIN_HOUSE_TO_FOREST_TRANSITION = pygame.Rect(390, 630, 170, 40)
        if self.current_area == "forest" and FOREST_TO_HOUSE_TRANSITION.colliderect(self.rect):
            self.current_area = "house"
            self.rect.topleft = (325, 612)  
        elif self.current_area == "house" and HOUSE_TO_FOREST_TRANSITION.colliderect(self.rect):
            self.current_area = "forest"
            self.rect.topleft = (942, 962)  # New position in the forest
        elif self.current_area == "forest" and FOREST_TO_TWIN_HOUSE_TRANSITION.colliderect(self.rect):
            self.current_area = "twin house"
            self.rect.topleft = (466, 654)  # New position in the twin house
        elif self.current_area == "twin house" and TWIN_HOUSE_TO_FOREST_TRANSITION.colliderect(self.rect):
            self.current_area = "forest"
            self.rect.topleft = (347, 442)  # New position in the forest""" 
    
    def update(self, dt, boundaries, obstacles):
        self.move_timer -= dt
        #print(f"{self.name} move_timer: {self.move_timer}")  # Debugging
        if self.move_timer <=0 : 
            self.choose_random_direction()
        
        self.move(dt, boundaries, obstacles)
        self.update_animation(dt)
        #self.check_area_transition()
