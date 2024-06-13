import pygame
import sys

pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
RECT_WIDTH, RECT_HEIGHT = 400, 300
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Scrollable Text in Pygame")

# Font
font = pygame.font.SysFont(None, 36)

# Sample long text
long_text = ("This is a very long text that will be used to demonstrate "
             "scrollable text functionality in a Pygame window. " * 10)

# Create a surface for the text area
text_surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT * 10))  # Ensure large enough to hold the text
text_surface.fill(WHITE)

# Render the text onto the text_surface
def render_text(text, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.size(line + words[0])[0] <= max_width:
            line += words.pop(0) + ' '
        lines.append(line)
    return lines

text_lines = render_text(long_text, font, RECT_WIDTH)

y_offset = 0
for line in text_lines:
    line_surface = font.render(line, True, BLACK)
    text_surface.blit(line_surface, (0, y_offset))
    y_offset += line_surface.get_height()

# Define the scrollable area
scrollable_area = pygame.Rect((WINDOW_WIDTH - RECT_WIDTH) // 2, (WINDOW_HEIGHT - RECT_HEIGHT) // 2, RECT_WIDTH, RECT_HEIGHT)

# Scrolling variables
scroll_y = 0
scroll_speed = 5
max_scroll = max(0, text_surface.get_height() - RECT_HEIGHT)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_y = max(scroll_y - scroll_speed, 0)
            elif event.button == 5:  # Scroll down
                scroll_y = min(scroll_y + scroll_speed, max_scroll)

    screen.fill(WHITE)

    # Draw the text surface within the scrollable area
    screen.blit(text_surface, scrollable_area.topleft, (0, scroll_y, RECT_WIDTH, RECT_HEIGHT))
    pygame.draw.rect(screen, BLACK, scrollable_area, 2)  # Draw the border of the scrollable area

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
