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
    def __init__(self, sprite_sheet_path, x, y, speed, scale, frame_size, dialog=None):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width, self.frame_height = frame_size
        self.scale = scale
        self.animations = {
            "idle_down": self.extract_frames(4, 7),
            "idle_up": self.extract_frames(5, 7),  # Use the first frame of "up" as idle
            "idle_left": self.extract_frames(7, 7),  # Use the first frame of "left" as idle
            "idle_right": self.extract_frames(6, 7),  # Use the first frame of "right" as idle
        }
        self.current_animation = self.animations["idle_down"]
        self.current_frame = 0
        self.animation_timer = 0
        self.rect = pygame.Rect(x, y, scale[0], scale[1])
        self.collision_rect = self.rect.inflate(-30, -40)  # Adjust values as needed
        self.speed = speed
        self.dialog = dialog or []  # Add dialog attribute to NPC

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
                raise  # Raise the exception after logging it for better debugging
        #print(f"Extracted {len(frames)} frames for row {row}")
        return frames

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer > 275:  # Adjust this value to control animation speed
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)

    def draw(self, screen, camera_offset):
        screen.blit(self.current_animation[self.current_frame], (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))

    def interact(self):
        """Return the dialog for interaction."""
        return self.dialog