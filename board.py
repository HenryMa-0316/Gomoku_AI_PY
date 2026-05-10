from constant import BOARD_SIZE

class GomokuBoard:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.move_history = []
        self.game_over = False
        self.winner = 0

    def make_move(self, row, col):
        if self.game_over:
            return False
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return False
        if self.board[row][col] != 0:
            return False
        
        self.board[row][col] = self.current_player
        self.move_history.append((row, col))
        
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True
        if len(self.move_history) == BOARD_SIZE * BOARD_SIZE:
            self.game_over = True
            return True
        self.current_player *= -1
        return True

    def check_win(self, row, col):
        if self.board[row][col] == 0:
            return False
        player = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dc, dr in directions:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
                
            if count >= 5:
                return True
            
        return False

    def undo_move(self):
        if not self.move_history or self.game_over:
            return False
        row, col = self.move_history.pop()
        self.board[row][col] = 0
        self.current_player *= -1
        self.game_over = False
        self.winner = 0
        return True

    def reset(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.move_history.clear()
        self.game_over = False
        self.winner = 0
