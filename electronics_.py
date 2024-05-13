import pygame
import sqlite3

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Product Management System")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Create font
font = pygame.font.SysFont(None, 24)

# Create input fields
input_fields = [
    {"label": "Product Name", "value": "", "rect": pygame.Rect(50, 50, 200, 30)},
    {"label": "Price", "value": "", "rect": pygame.Rect(50, 100, 200, 30)},
    {"label": "Quantity", "value": "", "rect": pygame.Rect(50, 150, 200, 30)},
    {"label": "Category", "value": "", "rect": pygame.Rect(50, 200, 200, 30)}
]

# Create buttons
buttons = [
    {"label": "Add", "rect": pygame.Rect(50, 250, 100, 30)},
    {"label": "Update", "rect": pygame.Rect(175, 250, 100, 30)},
    {"label": "Delete", "rect": pygame.Rect(300, 250, 100, 30)},
    {"label": "Clear", "rect": pygame.Rect(425, 250, 100, 30)}
]

# Create search input field and button
search_input = {"label": "Search", "value": "", "rect": pygame.Rect(50, 350, 200, 30)}
search_button = {"label": "Search", "rect": pygame.Rect(50, 400, 100, 30)}

# Create a connection to the SQLite database
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Create the products table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        quantity INTEGER,
        category TEXT
    )
""")
conn.commit()

# Function to render text
def render_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

# Function to handle button clicks
def handle_button_click(button_label):
    if button_label == "Add":
        # Insert a new product into the database
        name = input_fields[0]["value"]
        price = float(input_fields[1]["value"])
        quantity = int(input_fields[2]["value"])
        category = input_fields[3]["value"]
        cursor.execute("INSERT INTO products (name, price, quantity, category) VALUES (?, ?, ?, ?)",
                       (name, price, quantity, category))
        conn.commit()
        print("Product added successfully!")
    elif button_label == "Update":
        # Update an existing product in the database
        name = input_fields[0]["value"]
        price = float(input_fields[1]["value"])
        quantity = int(input_fields[2]["value"])
        category = input_fields[3]["value"]
        cursor.execute("UPDATE products SET price=?, quantity=?, category=? WHERE name=?",
                       (price, quantity, category, name))
        conn.commit()
        print("Product updated successfully!")
    elif button_label == "Delete":
        # Delete a product from the database
        name = input_fields[0]["value"]
        cursor.execute("DELETE FROM products WHERE name=?", (name,))
        conn.commit()
        print("Product deleted successfully!")
    elif button_label == "Clear":
        # Clear all input fields
        for field in input_fields:
            field["value"] = ""
        search_input["value"] = ""

# Function to handle search button click
def handle_search_click():
    search_term = search_input["value"]
    cursor.execute("SELECT * FROM products WHERE name LIKE ? OR category LIKE ?",
                   ('%' + search_term + '%', '%' + search_term + '%'))
    products = cursor.fetchall()
    if products:
        product = products[0]  # Display the first matching product
        input_fields[0]["value"] = product[1]
        input_fields[1]["value"] = str(product[2])
        input_fields[2]["value"] = str(product[3])
        input_fields[3]["value"] = product[4]
    else:
        print("No matching products found!")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any button is clicked
            for button in buttons:
                if button["rect"].collidepoint(event.pos):
                    handle_button_click(button["label"])
            # Check if the search button is clicked
            if search_button["rect"].collidepoint(event.pos):
                handle_search_click()
        elif event.type == pygame.KEYDOWN:
            # Update the value of the focused input field
            for field in input_fields:
                if field["rect"].collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        field["value"] = field["value"][:-1]
                    else:
                        field["value"] += event.unicode
            # Update the value of the search input field
            if search_input["rect"].collidepoint(pygame.mouse.get_pos()):
                if event.key == pygame.K_BACKSPACE:
                    search_input["value"] = search_input["value"][:-1]
                else:
                    search_input["value"] += event.unicode

    # Clear the screen
    screen.fill(WHITE)

    # Render input fields
    for field in input_fields:
        pygame.draw.rect(screen, LIGHT_GRAY, field["rect"])
        render_text(field["label"], field["rect"].x, field["rect"].y - 20)
        render_text(field["value"], field["rect"].x + 5, field["rect"].y + 5)
        # Show cursor on the selected input field
        if field["rect"].collidepoint(pygame.mouse.get_pos()):
            pygame.draw.line(screen, BLACK, (field["rect"].x + 5 + font.size(field["value"])[0], field["rect"].y + 5),
                             (field["rect"].x + 5 + font.size(field["value"])[0], field["rect"].y + 25), 2)

    # Render buttons
    for button in buttons:
        pygame.draw.rect(screen, GRAY, button["rect"])
        render_text(button["label"], button["rect"].x + 10, button["rect"].y + 5)

    # Render search input field and button
    pygame.draw.rect(screen, LIGHT_GRAY, search_input["rect"])
    render_text(search_input["label"], search_input["rect"].x, search_input["rect"].y - 20)
    render_text(search_input["value"], search_input["rect"].x + 5, search_input["rect"].y + 5)
    # Show cursor on the search input field
    if search_input["rect"].collidepoint(pygame.mouse.get_pos()):
        pygame.draw.line(screen, BLACK, (search_input["rect"].x + 5 + font.size(search_input["value"])[0], search_input["rect"].y + 5),
                         (search_input["rect"].x + 5 + font.size(search_input["value"])[0], search_input["rect"].y + 25), 2)
    pygame.draw.rect(screen, GRAY, search_button["rect"])
    render_text(search_button["label"], search_button["rect"].x + 10, search_button["rect"].y + 5)

    # Update the display
    pygame.display.flip()

# Close the database connection
conn.close()

# Quit Pygame
pygame.quit()