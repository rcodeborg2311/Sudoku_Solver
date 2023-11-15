import random
import tkinter as tk
from tkinter import messagebox

# Function to create sudoku board
def display_board(bord):
    for i in range(len(bord)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(bord[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(bord[i][j])
            else:
                print(str(bord[i][j]) + " ", end="")


# Function to cheak if a number is at the right place according to rules of sudoku
def sudoku_valid(bord, num, pos):
    # Check row
    for i in range(len(bord[0])):
        if bord[pos[0]][i] == num and pos[1] != i:
            return False
    # Check column
    for i in range(len(bord)):
        if bord[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bord[i][j] == num and (i,j) != pos:
                return False
    return True

# Function to remove numbers from the true solution to create a set of a game
def remove_clues(bord, num_clues):
    clues_removed = 0
    size = len(bord)
    while clues_removed < (size * size - num_clues):
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if bord[row][col] != 0:
            bord[row][col] = 0
            clues_removed += 1

# Function to check for empty spots on the sudoku grid
def find_empty(bord):
    for i in range(len(bord)):
        for j in range(len(bord[0])):
            if bord[i][j] == 0:
                return (i, j)  # row, col

    return None

def solve(bord):
    find = find_empty(bord)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if sudoku_valid(bord, i, (row, col)):
            bord[row][col] = i

            if solve(bord):
                return True

            bord[row][col] = 0

    return False

# MAIN_FUNCTION
def main():
    # Ask user for difficulty level
    global difficulty;
    difficulty = input("Enter difficulty level (easy, medium, hard): ").lower()
    if difficulty == "easy":
        num_clues = 40 
    elif difficulty == "medium":
        num_clues = 30
    elif difficulty=="hard" :
        num_clues = 20

    # Initialize an empty board
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Solve the board first to get a complete solution
    solve(board)

    # Save the solution for later checking
    solved_board = [row[:] for row in board]

    # Remove clues to create a puzzle
    remove_clues(board, num_clues)

if __name__ == "__main__":
    main()


# Function used by show_solution button to display solution on the GUI
def show_solution():
    global solved_board, entries
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, solved_board[i][j])
            entries[i][j].config(state='readonly', readonlybackground='light grey', fg='blue')
            
# MAIN_FUNCTION_GUI
def main_gui():
    global entries, puzzle_board, solved_board

    colors = ["#FF0000", "#008000", "#0000FF", "#FFFF00", "#FFA500", "#800080", "#00FFFF", "#FF00FF", "#808080"]

    # Initialize the main window
    window = tk.Tk()
    window.title("Sudoku Game")

    # Create a 9x9 grid of Entry widgets
    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            # Determine the color based on the 3x3 grid
            grid_index = (i // 3) * 3 + (j // 3)
            bg_color = colors[grid_index]

            # Create a frame for each cell without additional border
            cell_frame = tk.Frame(window, bg=bg_color)
            cell_frame.grid(row=i, column=j)

            entry = tk.Entry(cell_frame, width=2, font=('Arial', 18), justify='center', bg=bg_color)
            entry.pack(padx=1, pady=1)  # Padding for the internal Entry widget
            row_entries.append(entry)
        entries.append(row_entries)

    # Function to check the user's solution
    def check_solution():
        for i in range(9):
            for j in range(9):
                if entries[i][j].get() != str(solved_board[i][j]):
                    messagebox.showinfo("Result", "Incorrect Solution!")
                    return
        messagebox.showinfo("Result", "Correct Solution!")

    # Function to start a new game
    def new_game(difficulty_level):
        global puzzle_board, solved_board

        # Initialize an empty board
        puzzle_board = [[0 for _ in range(9)] for _ in range(9)]

        # Solve the board first to get a complete solution
        solve(puzzle_board)

        # Save the solution for later checking
        solved_board = [row[:] for row in puzzle_board]

        # Remove clues to create a puzzle
        num_clues = 40 if difficulty_level == "easy" else 30 if difficulty_level == "medium" else 20
        remove_clues(puzzle_board, num_clues)



        # Update GUI with the puzzle board
        for i in range(9):
            for j in range(9):
                entries[i][j].config(state='normal', bg='white', fg='black')  # Reset color and state
                entries[i][j].delete(0, tk.END)
                if puzzle_board[i][j] != 0:
                    entries[i][j].insert(0, puzzle_board[i][j])
                    entries[i][j].config(state='readonly', readonlybackground='light grey')
                else:
                    entries[i][j].config(state='normal', bg='white')

    # Add control buttons
    check_button = tk.Button(window, text="Check Solution", command=check_solution)
    check_button.grid(row=10, column=0, columnspan=4)

    # Start a new game with chosen difficulty
    # You can replace this with a method to select difficulty, for now, using 'easy'
    new_game_button = tk.Button(window, text="New Game", command=lambda: new_game(difficulty))
    new_game_button.grid(row=10, column=5, columnspan=4)
    
    show_solution_button = tk.Button(window, text="Show Solution", command=show_solution)
    show_solution_button.grid(row=11, column=0, columnspan=9)
    # Start a new game when the application launches
    new_game(difficulty)

    # Run the application
    window.mainloop()

if __name__ == "__main__":
    main_gui()