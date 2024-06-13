
class RuleSetInterface:
    def is_valid_move(self, start_pos, end_pos, board):
        """Check if a move is valid according to the specific rules."""
        pass

    def check_win_condition(self, board):
        """Check if the current board state satisfies any win condition."""
        pass

    def special_rules(self, board):
        """Implement any special rules for the chess variant."""
        pass
