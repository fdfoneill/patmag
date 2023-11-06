import os, glob
from PIL import Image, ImageDraw

from .pattern import Pattern, create_dashed_line

class Board(Pattern):
    def __init__(self, *args, **kwargs):
        super().__init__(height=9, width=9, *args, **kwargs)
        
    @property
    def houses(self):
        houses = []
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                houses.append(self.read(i, i+2, j, j+2))
        return houses
    
    def visualize(self, out_path:str, symbol_size:int=150) -> None:
        """Save pattern to a PNG"""
        asset_dir = os.path.join(os.path.dirname(__file__), "assets")
        mosaic_width = self.width * symbol_size
        mosaic_height = self.height * symbol_size
        mosaic = Image.new('RGB', (mosaic_width, mosaic_height), "white")
        draw = ImageDraw.Draw(mosaic)
        for row_index, row in enumerate(self.contents):
            for col_index, letter in enumerate(row):
                # Construct the file path for the current letter
                file_path = os.path.join(asset_dir, f'{letter}.png')
                assert os.path.exists(file_path), "Failed to find symbol asset for character '{}'".format(letter)

                # Open the image file
                with Image.open(file_path) as img:
                    # Make sure the image is of the correct size
                    img = img.resize((symbol_size, symbol_size))

                    # Calculate the position where the image should be pasted
                    position = (col_index * symbol_size, row_index * symbol_size)

                    # Paste the image into the mosaic
                    mosaic.paste(img, position)
        # Draw the dashed grid lines
        dash_length = symbol_size * 0.08
        space_length = symbol_size * 0.05
        for i in range(1, self.height):
            start_h = (0, i * symbol_size)
            end_h = (mosaic_width, i * symbol_size)
            if i%3 == 0:
                draw.line([start_h, end_h], fill="black", width=1)
            else:
                create_dashed_line(draw, start_h, end_h, dash_length, space_length)

        for i in range(1, self.width):
            start_v = (i * symbol_size, 0)
            end_v = (i * symbol_size, mosaic_height)
            if i%3 == 0:
                draw.line([start_v, end_v], fill="black", width=1)
            else:
                create_dashed_line(draw, start_v, end_v, dash_length, space_length)

        # Save or display the mosaic
        mosaic.save(out_path)
        return