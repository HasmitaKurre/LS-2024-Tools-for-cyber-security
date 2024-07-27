import subprocess
import re
import os

# Function to solve a Sudoku puzzle using backtracking
def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True  # Puzzle solved
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

# Function to find an empty cell (represented by 0)
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

# Function to check if placing a number in a cell is valid
def is_valid(board, num, row, col):
    for i in range(len(board)):
        if board[row][i] == num or board[i][col] == num:
            return False

    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True

# Function to convert board to string format required by the executable
def board_to_string(board):
    return "\n".join(" ".join(str(cell) for cell in row) for row in board) + "\n"

# Function to parse the board from the string format provided by the executable
def parse_board(board_str):
    lines = board_str.strip().split('\n')
    board = []
    for line in lines:
        board.append([int(num) for num in line.split()])
    return board

def main():
    # Ensure the 'sudoku' executable has the correct permissions
    os.chmod('/content/sudoku', 0o755)

    # Initialize the subprocess
    process = subprocess.Popen('/content/sudoku', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    puzzle_count = 0

    try:
        while True:
            # Read the output from the executable
            output = ""
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                output += line
                if "Enter the solution for the above puzzle" in line:
                    break

            if not output.strip():
                print("No more output from the executable.")
                break

            print("Output from sudoku executable:")
            print(output)

            # Extract the board from the output
            match = re.search(r'(?s)((\d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+\n){9})', output)
            if not match:
                print("No puzzle found in the output.")
                break

            board_str = match.group(1)
            print("Puzzle received:")
            print(board_str)

            board = parse_board(board_str)

            # Solve the Sudoku puzzle
            if solve_sudoku(board):
                solution_str = board_to_string(board)
                print("Solution to be sent:")
                print(solution_str)

                process.stdin.write(solution_str + '\n')
                process.stdin.flush()
                puzzle_count += 1

                # Adding a small delay to ensure output is processed
                time.sleep(0.1)
            else:
                print("Failed to solve puzzle")
                break

            # Read additional output after sending the solution
            additional_output = process.stdout.read()
            print("Additional output:")
            print(additional_output)
    finally:
        # Ensure the subprocess is closed properly
        process.stdin.close()
        process.stdout.close()
        process.stderr.close()
        process.wait()

if __name__ == "__main__":
    # Add your flag in the first line as a comment after you obtain it
    # Example: # FLAG{example_flag}
    main()
