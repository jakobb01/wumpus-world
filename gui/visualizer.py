import tkinter as tk
import os
from PIL import Image, ImageTk

class Visualizer:
    def __init__(self, world, agent):
        self.world = world
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("Wumpus World")
        self.canvas = tk.Canvas(self.root, width=440, height=450)
        self.canvas.pack()

    # todo: M44 means map is 4 cells wide and 4 cells high


    def load_images(self):
        # load all images and store them in a dictionary and resize to fit into cells
        self.images = {}
        image_files = {
            'B': 'breeze.png',
            'P': 'pit.png',
            'S': 'stench.png',
            'W': 'wumpus.png',
            'G': 'gold.png'
        }
        cell_img_size = 40  # < 100 (cell)
        for key, filename in image_files.items():
            path = os.path.join('images', filename)
            img = Image.open(path)
            img = img.resize((cell_img_size, cell_img_size), Image.LANCZOS)
            self.images[key] = ImageTk.PhotoImage(img)

    def run(self):
        self.load_images()
        self.draw_grid()
        self.draw_world()
        self.root.mainloop()

    def draw_grid(self):
        cell_size = 100
        grid_size = 4
        margin_top = 10
        margin_left = 40

        # grid cells
        for x in range(grid_size):
            for y in range(grid_size):
                self.canvas.create_rectangle(
                    margin_left+x * cell_size, margin_top+y * cell_size,
                    margin_left+(x+1) * cell_size, margin_top+(y+1) * cell_size,
                    fill="white"
                )

        # write row numbers on the left
        for y in range(grid_size):
            self.canvas.create_text(
                10, margin_top+y * cell_size + cell_size // 2,
                text=str(grid_size - y),
                font=("Arial", 14, "bold"),
                anchor="w"
            )

        # write column numbers below the grid
        for x in range(grid_size):
            self.canvas.create_text(
                margin_left+x * cell_size + cell_size // 2, margin_top+grid_size * cell_size + 20,
                text=str(x + 1),
                font=("Arial", 14, "bold"),
                anchor="center"
            )

    # draw world objects (breeze, pit, stench, wumpus, gold) on the grid
    def draw_world(self):
        cell_size = 100
        margin_top = 10
        margin_left = 40

        # get all items for each cell
        cell_contents = {}
        for tag, coordinates in self.world.items():
            for (x, y) in coordinates:
                cell = (x, y)
                if cell not in cell_contents:
                    cell_contents[cell] = []
                # add only valid keys (those present in self.images)
                for char in tag:
                    if char in self.images:
                        cell_contents[cell].append(char)

        # for each cell, draw up to 4 images in quadrants
        for (x, y), keys in cell_contents.items():
            # calc top left corner of the cell
            cell_left = margin_left + (x - 1) * cell_size
            cell_top = margin_top + (4 - y) * cell_size

            # for more images in one cell we split into quadrants
            if len(keys) > 1:
                offsets = [
                    (cell_size // 4, cell_size // 4),           # top left
                    (3 * cell_size // 4, cell_size // 4),       # top right
                    (cell_size // 4, 3 * cell_size // 4),       # bottom left
                    (3 * cell_size // 4, 3 * cell_size // 4),   # bottom right
                ]
                for i, key in enumerate(keys[:4]):
                    # get position of each image with offsets
                    dx, dy = offsets[i]
                    canvas_x = cell_left + dx
                    canvas_y = cell_top + dy
                    self.canvas.create_image(canvas_x, canvas_y, image=self.images[key])
            # center single image
            else:
                key = keys[0]
                # position of the picture
                canvas_x = cell_left + cell_size // 2
                canvas_y = cell_top + cell_size // 2
                self.canvas.create_image(canvas_x, canvas_y, image=self.images[key])