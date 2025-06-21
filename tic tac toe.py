import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.full((3, 3), ' ')
        self.current_player = 'X'  # Human is X, AI is O
        self.game_over = False
        self.winner = None
        
    def print_board(self):
        print("\nCurrent Board:")
        for i, row in enumerate(self.board):
            print(" " + " | ".join(row))
            if i < 2:
                print("-----------")
        print()
    
    def check_winner(self, board=None):
        if board is None:
            board = self.board
        # Check rows
        for row in board:
            if row[0] != ' ' and row[0] == row[1] == row[2]:
                return row[0]
        
        # Check columns
        for col in range(3):
            if board[0][col] != ' ' and board[0][col] == board[1][col] == board[2][col]:
                return board[0][col]
        
        # Check diagonals
        if board[0][0] != ' ' and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] != ' ' and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        
        # Check for tie
        if ' ' not in board.flatten():
            return 'Tie'
        
        return None
    
    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.winner = self.check_winner()
            
            if self.winner:
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
    
    def minimax(self, board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        # Evaluate board state
        result = self.check_winner(board)
        if result == 'O': return 10 - depth
        if result == 'X': return depth - 10
        if result == 'Tie': return 0
        
        if is_maximizing:  # AI's turn (maximizing player)
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:  # Human's turn (minimizing player)
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score
    
    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ' '
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            self.make_move(best_move[0], best_move[1])
            print(f"AI plays at position ({best_move[0]+1}, {best_move[1]+1})")

def main():
    game = TicTacToe()
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'X', AI is 'O'")
    print("Enter moves as row and column numbers (1-3)\n")
 
    
    while not game.game_over:
        game.print_board()
        
        if game.current_player == 'X':  # Human's turn
            valid_move = False
            while not valid_move:
                try:
                    row = int(input("Enter row (1-3): ")) - 1
                    col = int(input("Enter column (1-3): ")) - 1
                    if 0 <= row <= 2 and 0 <= col <= 2:
                        if game.make_move(row, col):
                            valid_move = True
                        else:
                            print("Cell already occupied! Try again.")
                    else:
                        print("Invalid input! Numbers must be between 1-3.")
                except ValueError:
                    print("Invalid input! Please enter numbers only.")
        else:  # AI's turn
            print("AI is thinking...")
            game.ai_move()
    
    game.print_board()
    if game.winner == 'Tie':
        print("It's a tie!")
    else:
        print(f"{game.winner} wins!")

if __name__ == "__main__":
    main()