from tkinter import Tk, Label, Frame
from PIL import Image, ImageTk

def create_chessboard(parent):
    board_color_1 = "white"
    board_color_2 = "gray"
    squares = []

    for row in range(8):
        row_of_squares = []
        for col in range(8):
            color = board_color_1 if (row + col) % 2 == 0 else board_color_2
            square = tk.Label(parent, bg=color, width=2, height=1)
            square.grid(row=row, column=col, sticky='nsew')
            row_of_squares.append(square)
        squares.append(row_of_squares)
    
    for i in range(8):
        parent.grid_rowconfigure(i, weight=1)
        parent.grid_columnconfigure(i, weight=1)

    return squares

def main():
    root = tk.Tk()
    root.geometry('800x600')  

    chessboard_frame = tk.Frame(root)
    chessboard_frame.pack(expand=True, fill='both')

    create_chessboard(chessboard_frame)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()