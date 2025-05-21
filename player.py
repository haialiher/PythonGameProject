import pygame

sprites = []
# Dictionary for caching loaded images
loaded = {}

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
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Player:
    def __init__(self, sprite_sheet_path, x, y, speed, scale, frame_size):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width, self.frame_height = frame_size
        self.scale = scale
        self.animations = {
            "down": self.extract_frames(0, 4),
            "up": self.extract_frames(1, 3),
            "left": self.extract_frames(2, 6),
            "idle": self.extract_frames(3, 4),
            "right": self.extract_frames(4, 6),
        }
        self.current_animation = self.animations["idle"]
        self.current_frame = 0
        self.animation_timer = 0
        self.rect = pygame.Rect(x, y, scale[0], scale[1])
        self.speed = speed

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
        print(f"Extracted {len(frames)} frames for row {row}")
        return frames

    def move(self, keys):
        if keys[pygame.K_w] and keys[pygame.K_d]:
             self.rect.y -= self.speed / 1.44
             self.rect.x += self.speed/ 1.44
             self.current_animation = self.animations["right"]
             print("rightup diagonal")
        elif keys[pygame.K_w] and keys[pygame.K_a]:
             self.rect.y -= self.speed / 1.44
             self.rect.x -= self.speed / 1.44
             self.current_animation = self.animations["left"]
             print("left up diagonal")
        elif keys[pygame.K_s] and keys[pygame.K_a]:
             self.rect.y += self.speed / 1.44
             self.rect.x -= self.speed / 1.44
             self.current_animation = self.animations["left"]
             print("left down diagonal")
        elif keys[pygame.K_s] and keys[pygame.K_d]:
             self.rect.y += self.speed / 1.44
             self.rect.x += self.speed / 1.44
             self.current_animation = self.animations["right"]
             print("right down diagonal")
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.current_animation = self.animations["left"]
            print("Moving left")
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.current_animation = self.animations["right"]
            print("Moving right")
        elif keys[pygame.K_w]:
            self.rect.y -= self.speed 
            self.current_animation = self.animations["up"]
            print("Moving up")
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
            self.current_animation = self.animations["down"]
            print("Moving down")
        # Set to idle animation when no movement keys are pressed
        else:
            self.current_animation = self.animations["idle"]
            print("Idle")

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer > 250:  # Change frame every 100ms
            self.animation_timer = 1
            self.current_frame = (self.current_frame + 1) % len(self.current_animation)
            print(f"Current animation: {self.current_animation}, Current frame: {self.current_frame}")

    def draw(self, screen):
        try:
            screen.blit(self.current_animation[self.current_frame], self.rect.topleft)
        except IndexError as e:
            print(f"Error drawing frame: {e}")
            print(f"Current animation: {self.current_animation}, Current frame: {self.current_frame}")
