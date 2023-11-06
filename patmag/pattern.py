import os, glob
from PIL import Image, ImageDraw


class Pattern:
    def __init__(self, height, width):
        assert height > 0, "height must be positive"
        assert width > 0, "width must be positive"
        self.height = height
        self.width = width
        self.contents = []
        for i in range(height):
            self.contents.append(["-" for j in range(width)].copy())
            
    def __repr__(self):
        return "\n".join([str(row) for row in self.contents])
    
    @property
    def sigilcount(self):
        sigil_sum = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.contents[i][j] != "-":
                    sigil_sum += 1
        return sigil_sum
    
    def set_contents(self, contents_string:str):
        assert len(contents_string) == (self.width * self.height), "length of contents_string must equal width times height"
        nested_contents_lists = []
        for i in range(self.height):
            contents_row = []
            for j in range(self.width):
                contents_row.append(contents_string[j + (i*self.width)])
            nested_contents_lists.append(contents_row.copy())
        self.contents = nested_contents_lists
        return
    
    def get_contents(self):
        contents_string = ""
        for i in range(self.height):
            for j in range(self.width):
                contents_string += self.contents[i][j]
        return contents_string
    
    def read(self, row_min:int=0, row_max:int=None, col_min:int=0, col_max:int=None) -> "Pattern":
        """Reads portion of self to new Pattern object
        
        Parameters
        ----------
        row_min:int=0
        row_max:int=self.height-1
        col_min:int=0
        col_max:int=self.width-1
        
        Returns
        -------
        subset_pattern:Pattern
        """
        if row_max is None:
            row_max = self.height-1
        if col_max is None:
            col_max = self.width-1
        assert row_min >=0, "row_min cannot be negative"
        assert row_max >= row_min, "row_max must be greater than row_min"
        assert col_min >= 0, "col_min cannot be negative"
        assert col_max >= col_min, "col_max must be greater than col_min"
        assert row_max < self.height, "row_max cannot exceed pattern height"
        assert col_max < self.width, "col_max cannot exceed pattern width"
        
        out_list = []
        for i in range(row_min, row_max+1):
            for j in range(col_min, col_max+1):
                out_list.append(self.contents[i][j])
        subset_pattern = Pattern((row_max-row_min)+1, (col_max-col_min)+1)
        subset_pattern.set_contents("".join(out_list))
        return subset_pattern
        
        
    def write(self, other, offset_row:int=0, offset_col:int=0) -> None:
        """Writes other pattern onto self at given offsets
        
        ***
        
        Parameters 
        ----------
        other: Pattern
            pattern to be written onto self
        offset_row:int=0
            Number of rows to shift other pattern down
        offset_col:int=0
            Number of columns to shift other pattern right
            
        Returns 
        -------
        None
        """
        assert offset_row >= 0, "offset_row cannot be negative"
        assert offset_col >= 0, "offset_col cannot be negative"
        assert (other.height + offset_row) <= self.height, "can't write pattern with height {0} to pattern with height {1} with offset {2}".format(other.height, self.height, offset_row)
        assert (other.width + offset_col) <= self.width, "can't write pattern with width {0} to pattern with width {1} with offset {2}".format(other.width, self.width, offset_col)
        for i in range(other.height):
            for j in range(other.width):
                self.contents[i+offset_row][j+offset_col] = other.contents[i][j]
        return
    
    def compare(self, other, offset_row:int=0, offset_col:int=0) -> int:
        assert offset_row >= 0, "offset_row cannot be negative"
        assert offset_col >= 0, "offset_col cannot be negative"
        assert (other.height + offset_row) <= self.height, "can't compare pattern with height {0} to pattern with height {1} with offset {2}".format(other.height, self.height, offset_row)
        assert (other.width + offset_col) <= self.width, "can't compare pattern with width {0} to pattern with width {1} with offset {2}".format(other.width, self.width, offset_col)
        similarity = 0
        for i in range(other.height):
            for j in range(other.width):
                if self.contents[i+offset_row][j+offset_col] == other.contents[i][j]:
                    if other.contents[i][j]=="-":
                        continue
                    similarity += 1
        return similarity
    
    def contains(self, other) -> bool:
        assert other.height <= self.height, "contained pattern cannot be larger"
        assert other.width <= self.width, "contained pattern cannot be larger"
        for i in range((self.height - other.height)+1):
            for j in range((self.width - other.width)+1):
                similarity = self.compare(other, i, j)
                if similarity == other.sigilcount:
                    return True
        return False
    
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
            create_dashed_line(draw, start_h, end_h, dash_length, space_length)

        for i in range(1, self.width):
            start_v = (i * symbol_size, 0)
            end_v = (i * symbol_size, mosaic_height)
            create_dashed_line(draw, start_v, end_v, dash_length, space_length)

        # Save or display the mosaic
        mosaic.save(out_path)
        return
    
    def save(self, out_path:str):
        """Saves pattern to .ptn file"""
        contents_string = self.get_contents()
        save_string = "{} {}\n".format(self.height, self.width) + contents_string
        base, ext = os.path.splitext(out_path)
        assert ext == ".ptn", "can only save to .ptn file"
        with open(out_path, 'w') as wf:
            wf.write(save_string)
            
    @classmethod
    def load(cls, saved_path:str):
        assert os.path.splitext(saved_path)[1] == ".ptn", "can only load Pattern from .ptn file"
        with open(saved_path, 'r') as rf:
            save_string = rf.read()
        dimensions, contents_string = save_string.split("\n")
        height, width = (int(dim) for dim in dimensions.split())
        loaded_pattern = Pattern(height, width)
        loaded_pattern.set_contents(contents_string)
        return loaded_pattern

    
def load(saved_path:str):
    return Pattern.load(saved_path)
    

def create_dashed_line(draw, start, end, dash_length=5, space_length=3):
    """Helper function for creating dashed line within Pattern.visualize()"""
    x1, y1 = start
    x2, y2 = end
    total_length = ((x2-x1)**2 + (y2-y1)**2) ** 0.5
    num_dashes = int(total_length / (dash_length + space_length))
    x_displacement = (x2-x1)/num_dashes
    y_displacement = (y2-y1)/num_dashes

    for i in range(num_dashes):
        start_pos = (x1 + i*x_displacement, y1 + i*y_displacement)
        end_pos = (start_pos[0] + (x_displacement * (dash_length / (dash_length + space_length))), start_pos[1] + (y_displacement * (dash_length / (dash_length + space_length))))
        draw.line([start_pos, end_pos], fill="black", width=1)