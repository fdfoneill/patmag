import tkinter as tk

from .board import Board

# Constants representing the size of the grid and the symbols
GRID_SIZE = 9
SYMBOLS = [' ', 'f', 'w', 'e', 'a', 's']  # ASCII characters for now

class GridGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("9x9 Grid GUI")
        self.current_symbol = ' '
        self.current_symbol_button = None  # To keep track of the currently selected button
        self.symbol_buttons = []  # List to keep references to the sidebar buttons
        self.grid_widgets = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.create_sidebar()
        self.create_grid()
    
    def create_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                frame = tk.Frame(self, width=40, height=40)
                frame.grid(row=i, column=j, padx=1, pady=1)
                frame.pack_propagate(False)  # Don't shrink

                button = tk.Button(frame, text=' ', command=lambda x=i, y=j: self.set_symbol(x, y))
                button.pack(expand=True, fill='both')

                self.grid_widgets[i][j] = button

    def create_sidebar(self):
        sidebar = tk.Frame(self, width=200, height=40 * GRID_SIZE)
        sidebar.grid(row=0, column=GRID_SIZE, rowspan=GRID_SIZE, padx=1, pady=1, sticky='ns')

        for i, symbol in enumerate(SYMBOLS):
            button = tk.Button(sidebar, text=symbol, command=lambda s=symbol, b=i: self.select_symbol(s, b))
            button.pack(fill='both')
            self.symbol_buttons.append(button)

    def select_symbol(self, symbol, button_index):
        self.current_symbol = symbol
        
        for btn in self.symbol_buttons:
            btn.config(highlightthickness=0)

        # Set a border on the selected button
        self.symbol_buttons[button_index].config(highlightthickness=2, highlightbackground='black')
        
        self.current_symbol_button = button_index

    def set_symbol(self, x, y):
        self.grid_widgets[x][y].config(text=self.current_symbol)

    def export_grid(self):
        grid_values = []
        for row in self.grid_widgets:
            for button in row:
                grid_values.append(button.cget('text'))
        grid_text = "".join(grid_values)
        board = Board()
        board.set_contents(grid_text.replace(" ", "-"))
        return board

