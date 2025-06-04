import pygame

sprites = []
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
            "down": self.extract_frames(0, 7),
            "up": self.extract_frames(1, 7),
            "left": self.extract_frames(2, 7),
            "right": self.extract_frames(3, 7),
            "idle_down": self.extract_frames(4, 7),
            "idle_up": self.extract_frames(5, 7),  # Use the first frame of "up" as idle
            "idle_left": self.extract_frames(7, 7),  # Use the first frame of "left" as idle
            "idle_right": self.extract_frames(6, 7),  # Use the first frame of "right" as idle
        }
        self.current_animation = self.animations["idle_down"]
        self.last_direction = "down"  # Track the last movement direction
        self.current_frame = 0
        self.animation_timer = 0
        self.rect = pygame.Rect(x, y, scale[0], scale[1])
        self.collision_rect = self.rect.inflate(-10, -20)  # Adjust values as needed
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
        #print(f"Extracted {len(frames)} frames for row {row}")
        return frames

    def move(self, keys, obstacles):
        previous_animation = self.current_animation  # Track the current animation before changes

        # Create a copy of the player's current rect to calculate the proposed position
        proposed_rect = self.rect.copy()

        if keys[pygame.K_w] and keys[pygame.K_d]:
            proposed_rect.y -= self.speed / 1.44
            proposed_rect.x += self.speed / 1.44
            self.current_animation = self.animations["right"]
            self.last_direction = "right"
            #print("rightup diagonal")
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            proposed_rect.y -= self.speed / 1.44
            proposed_rect.x -= self.speed / 1.44
            self.current_animation = self.animations["left"]
            self.last_direction = "left"
            #print("left up diagonal")
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            proposed_rect.y += self.speed / 1.44
            proposed_rect.x -= self.speed / 1.44
            self.current_animation = self.animations["left"]
            self.last_direction = "left"
            #print("left down diagonal")
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            proposed_rect.y += self.speed / 1.44
            proposed_rect.x += self.speed / 1.44
            self.current_animation = self.animations["right"]
            self.last_direction = "right"
            #print("right down diagonal")
        elif keys[pygame.K_a]:
            proposed_rect.x -= self.speed
            self.current_animation = self.animations["left"]
            self.last_direction = "left"
            #print("Moving left")
        elif keys[pygame.K_d]:
            proposed_rect.x += self.speed
            self.current_animation = self.animations["right"]
            self.last_direction = "right"
            #print("Moving right")
        elif keys[pygame.K_w]:
            proposed_rect.y -= self.speed
            self.current_animation = self.animations["up"]
            self.last_direction = "up"
            #print("Moving up")
        elif keys[pygame.K_s]:
            proposed_rect.y += self.speed
            self.current_animation = self.animations["down"]
            self.last_direction = "down"
            #print("Moving down")
        else:
            # Set idle animation based on the last direction
            self.current_animation = self.animations[f"idle_{self.last_direction}"]
            #print("Idle")

        # Check for collisions with obstacles using their collision_rect
        if not any(proposed_rect.colliderect(obstacle.collision_rect) for obstacle in obstacles if hasattr(obstacle, 'collision_rect')):
            # If no collision, update the player's position
            self.rect = proposed_rect
        self.collision_rect.topleft = self.rect.topleft  # Ensure collision_rect is updated
        if self.current_animation != previous_animation:
            self.current_frame = 0

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer > 275:  # Adjust this value to control animation speed
            self.animation_timer = 1
            if len(self.current_animation) > 0:  # Ensure the animation is not empty
                self.current_frame = (self.current_frame + 1) % len(self.current_animation)
                #print(f"Current animation: {self.current_animation}, Current frame: {self.current_frame}")
           # else:
               # print("Warning: current_animation is empty!")

    def draw(self, screen):
        try:
            screen.blit(self.current_animation[self.current_frame], self.rect.topleft)
        except IndexError as e:
            print(f"Error drawing frame: {e}")
           # print(f"Current animation: {self.current_animation}, Current frame: {self.current_frame}")
