import pygame
import sys
import ctypes

# Initialize pygame
pygame.init()

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

# Circle (pet) settings
circle_radius = 20
pet_window_height = circle_radius * 2 + 20  # Height of the pet window

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

# Colors
background_color = (0, 0, 0, 0)  # Fully transparent background
grass_color = (50, 200, 50)  # Green grass
circle_color = (200, 50, 50)  # Red circle (pet)

# Clock for controlling FPS
clock = pygame.time.Clock()

# Circle (pet) position
circle_x = screen_width // 2
circle_y = circle_radius + 10

# Animation direction (left or right)
direction = 1  # 1 for right, -1 for left

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

    # Draw grass
    pygame.draw.rect(screen, grass_color, (0, pet_window_height - 20, screen_width, 20))

    # Move the circle (pet)
    circle_x += direction * 2
    if circle_x + circle_radius >= screen_width or circle_x - circle_radius <= 0:
        direction *= -1  # Reverse direction

    # Draw the circle (pet)
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()