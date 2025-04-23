import chess
import chess.engine

class LeelaInterface:
    def __init__(self, path_to_lc0=r"C:\Users\Rohan\Documents\machine-learning-projects\python-chess-ai-Rohan\lc0.exe", depth=10):
        self.engine = chess.engine.SimpleEngine.popen_uci(path_to_lc0)
        self.depth = depth  # Or time-based search, e.g., {'movetime': 1000}

    def get_best_move(self, fen):
        board = chess.Board(fen)
        result = self.engine.play(board, chess.engine.Limit(depth=self.depth))
        return result.move  # Returns a python-chess Move object

    def evaluate(self, fen):
        board = chess.Board(fen)
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth))
        score = info["score"].white().score(mate_score=10000)
        return score

    def close(self):
        self.engine.quit()
