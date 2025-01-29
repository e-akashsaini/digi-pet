import pygame
import sys
import ctypes
import win32gui
import win32con
import random
import time

# Initialize pygame
pygame.init()

# Load and play background music
pygame.mixer.music.load("assets//music-lowpoli.mp3")  # Replace with your music file path
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play on a loop (-1 for infinite)

# Enable DPI awareness for accurate scaling on high-DPI screens
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# Get screen dimensions using Windows API
user32 = ctypes.windll.user32
screen_width = int(user32.GetSystemMetrics(0))
screen_height = int(user32.GetSystemMetrics(1))

# Use SystemParametersInfo to get the working area (excluding taskbar)
class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

work_area = RECT()
ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(work_area), 0)

# Calculate taskbar height
taskbar_height = screen_height - (work_area.bottom - work_area.top)

# Debugging output: Print screen dimensions and taskbar height
print(f"Screen Width: {screen_width}")
print(f"Screen Height: {screen_height}")
print(f"Taskbar Height: {taskbar_height}")

# Pet settings
pet_image_size_height = 130  # Fixed dimensions for the pet image height
pet_image_size_width = 60  # Fixed dimensions for the pet image width
pet_window_height = 60  # Fixed height for the pet window

# Calculate window position (just above the taskbar)
window_x = 0
window_y = screen_height - taskbar_height - pet_window_height

# Debugging output: Print calculated window position
print(f"Window Position: X={window_x}, Y={window_y}")
print(f"Pet Window Height: {pet_window_height}")

# Create screen
screen = pygame.display.set_mode((screen_width, pet_window_height), pygame.NOFRAME)
pygame.display.set_caption("Digital Pet")

# Force window position using `ctypes`
window_handle = pygame.display.get_wm_info()['window']
ctypes.windll.user32.MoveWindow(
    window_handle,  # Window handle
    int(window_x), int(window_y),  # X and Y position
    int(screen_width), int(pet_window_height),  # Width and height
    True  # Repaint the window
)

# Ensure the window is always on top using `win32gui`
win32gui.SetWindowPos(
    window_handle,  # Window handle
    win32con.HWND_TOPMOST,  # Always on top
    0, 0, 0, 0,
    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
)

# Load the static grass field image
grass_image = pygame.image.load("assets\\gs-01.png")
grass_image = pygame.transform.scale(grass_image, (screen_width, pet_window_height))  # Scale to match window height

# Load animation frames for the pet moving
pet_frames = [
    pygame.transform.scale(pygame.image.load(f"assets\\trial-png\\001.png"), (pet_image_size_height, pet_image_size_width)),
    pygame.transform.scale(pygame.image.load(f"assets\\trial-png\\002.png"), (pet_image_size_height, pet_image_size_width)),
    pygame.transform.scale(pygame.image.load(f"assets\\trial-png\\003.png"), (pet_image_size_height, pet_image_size_width)),
    pygame.transform.scale(pygame.image.load(f"assets\\trial-png\\004.png"), (pet_image_size_height, pet_image_size_width)),
    pygame.transform.scale(pygame.image.load(f"assets\\trial-png\\005.png"), (pet_image_size_height, pet_image_size_width)),
    pygame.transform.scale(pygame.image.load(f"assets\\trial-png\\006.png"), (pet_image_size_height, pet_image_size_width)),
    pygame.transform.scale(pygame.image.load(f"assets\\trial-png\\007.png"), (pet_image_size_height, pet_image_size_width)),
    pygame.transform.scale(pygame.image.load(f"assets\\trial-png\\008.png"), (pet_image_size_height, pet_image_size_width)),
]

# Load the static pet image for when the pet is idle
idle_pet_image = pygame.transform.scale(pygame.image.load("assets\\trial-png\\001.png"), (pet_image_size_height, pet_image_size_width))

# Animation settings
current_frame = 0
frame_update_time = 0.1  # Time (in seconds) between frame updates
last_frame_time = time.time()
facing_left = False  # Track direction of the pet

# Clock for controlling FPS
clock = pygame.time.Clock()

# Pet position and movement
pet_x = screen_width // 2  # Start position
pet_y = (pet_window_height - pet_image_size_width) // 2  # Centered vertically
target_x = random.randint(0, screen_width - pet_image_size_width)  # Initial random target position
movement_speed = 0.6  # Fractional speed for smoother and slower movement
last_movement_time = time.time()  # Track the last time the target was updated
movement_delay = random.randint(5, 7)  # Initial random delay (5 to 7 seconds)
waiting = False  # Track whether the pet is waiting

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear screen with transparency
    screen.fill((0, 0, 0, 0))

    # Draw the grass field image
    screen.blit(grass_image, (0, 0))

    # Check if the pet is waiting
    if waiting:
        # Wait for the delay time before moving to a new target
        if time.time() - last_movement_time >= movement_delay:
            target_x = random.randint(0, screen_width - pet_image_size_width)  # New random target position
            last_movement_time = time.time()  # Reset the timer
            movement_delay = random.randint(5, 7)  # New random delay (5 to 7 seconds)
            waiting = False  # Exit waiting state
            print("Next movement delay:", movement_delay)

        if facing_left:
            flipped_idle_image = pygame.transform.flip(idle_pet_image, True, False)
            screen.blit(flipped_idle_image, (pet_x, pet_y))
        else:
            screen.blit(idle_pet_image, (pet_x, pet_y))
        # Draw the idle pet image
        # screen.blit(idle_pet_image, (pet_x, pet_y))
    else:
        # Update animation frame if enough time has passed
        if time.time() - last_frame_time >= frame_update_time:
            current_frame = (current_frame + 1) % len(pet_frames)  # Cycle through frames
            last_frame_time = time.time()

        # Determine the pet's direction and flip frames if needed
        if pet_x < target_x:
            facing_left = False  # Moving right
        elif pet_x > target_x:
            facing_left = True  # Moving left

        # Get the current frame, flipped if facing left
        frame_to_draw = pet_frames[current_frame]
        if facing_left:
            frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)

        # Draw the current frame of the pet animation
        screen.blit(frame_to_draw, (pet_x, pet_y))

        # Move the pet toward the target position
        if abs(pet_x - target_x) <= movement_speed:  # Close enough to the target
            pet_x = target_x  # Snap to the target position
            waiting = True  # Enter waiting state
            last_movement_time = time.time()  # Start the wait timer
        elif pet_x < target_x:
            pet_x += movement_speed
        elif pet_x > target_x:
            pet_x -= movement_speed

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()

