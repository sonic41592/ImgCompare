import pygame
import os
import sys
import send2trash
import winshell
import pythoncom

# Initialize Pygame
pygame.init()

# Set up display with resizable flag
screen_width = 1200  # Initial width of the display window
screen_height = 700  # Initial height of the display window (including space for text)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Image Viewer')

# Folder paths
folder1 = sys.argv[1]
folder2 = sys.argv[2]

# Get list of images in each folder
images1 = sorted([img for img in os.listdir(folder1) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
images2 = sorted([img for img in os.listdir(folder2) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])

# Initialize indices and deleted files lists
index1 = 0
index2 = 0
deleted_files = []

# Load and scale images
def load_image(folder, filename, width, height):
    image = pygame.image.load(os.path.join(folder, filename))
    return pygame.transform.scale(image, (width, height))

def display_images():
    screen.fill((0, 0, 0))
    
    image1 = load_image(folder1, images1[index1], screen_width // 2, screen_height - 50)
    image2 = load_image(folder2, images2[index2], screen_width // 2, screen_height - 50)
    screen.blit(image1, (0, 0))
    screen.blit(image2, (screen_width // 2, 0))

    # Display image index and total count
    font = pygame.font.Font(None, 36)
    text1 = font.render(f'{index1 + 1} / {len(images1)}', True, (255, 255, 255))
    text2 = font.render(f'{index2 + 1} / {len(images2)}', True, (255, 255, 255))
    
    screen.blit(text1, (screen_width // 4 - text1.get_width() // 2, screen_height - 40))
    screen.blit(text2, (3 * screen_width // 4 - text2.get_width() // 2, screen_height - 40))
    
    pygame.display.flip()

def send_to_recycle_bin(folder, images, index):
    file_path = os.path.join(folder, images[index])
    send2trash.send2trash(file_path)
    deleted_files.append(file_path)
    del images[index]
    return min(index, len(images) - 1)

def restore_from_recycle_bin():
    if not deleted_files:
        return

    last_deleted_file = deleted_files.pop()
    file_name = os.path.basename(last_deleted_file)
    pythoncom.CoInitialize()
    winshell.undelete(last_deleted_file)
    pythoncom.CoUninitialize()
    
    folder = os.path.dirname(last_deleted_file)
    if folder == folder1:
        images1.append(file_name)
        images1.sort()
    elif folder == folder2:
        images2.append(file_name)
        images2.sort()
    return

# Display the first images
display_images()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                index1 = (index1 + 1) % len(images1)
                index2 = (index2 + 1) % len(images2)
            elif event.key == pygame.K_LEFT:
                index1 = (index1 - 1) % len(images1)
                index2 = (index2 - 1) % len(images2)
            elif event.key == pygame.K_z:
                index1 = (index1 - 1) % len(images1)
            elif event.key == pygame.K_x:
                index1 = (index1 + 1) % len(images1)
            elif event.key == pygame.K_PERIOD:
                index2 = (index2 - 1) % len(images2)
            elif event.key == pygame.K_SLASH:
                index2 = (index2 + 1) % len(images2)
            elif event.key == pygame.K_q:
                if images1:
                    index1 = send_to_recycle_bin(folder1, images1, index1)
            elif event.key == pygame.K_p:
                if images2:
                    index2 = send_to_recycle_bin(folder2, images2, index2)
            elif event.key == pygame.K_u:
                restore_from_recycle_bin()
            display_images()
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            display_images()

# Quit Pygame
pygame.quit()
sys.exit()
