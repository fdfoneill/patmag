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
                if similarity == (other.height * other.width):
                    return True
        return False