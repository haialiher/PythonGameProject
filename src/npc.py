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
        self.collision_rect = self.rect.inflate(-40, -40)  # Adjust values as needed
        self.speed = speed
        self.dialog = dialog or []  # Add dialog attribute to NPC
        #self.dialog_templete = dialog_templete or []  # Default to an empty list if not provided
        self.last_direction = "down"  # Track the last movement direction
        self.current_frame = 0
        self.animation_timer = 0
        if x is not None and y is not None:
            self.rect = pygame.Rect(x, y, 32, 32)
            self.collision_rect = self.rect.inflate(-10, -10)  # Add a collision rectangle
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
    

 #new random dialog for NPC