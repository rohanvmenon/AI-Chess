import numpy as np
import random
import math
import logging
logging.basicConfig(level=logging.INFO)

class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.board.get_legal_moves())

    def best_child(self, c_param=3.0):
        choices_weights = [
            (child.value / (child.visits + 1e-6)) + c_param * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            for child in self.children
        ]
        max_weight = max(choices_weights)
        best_children = [child for child, weight in zip(self.children, choices_weights) if weight == max_weight]
        return random.choice(best_children)  # Randomly select among the best moves

class MCTS:
    def __init__(self, neural_net):
        self.neural_net = neural_net

    def run(self, root_board, n_simulations, max_depth=3):
        root = MCTSNode(root_board)

        for _ in range(n_simulations):
            node = root
            board = root_board.copy()
            depth = 0

            # Selection
            while node.children and depth < max_depth:
                node = node.best_child()
                board.push(node.move)
                depth += 1

            # Log selected moves
            if node.move:
                logging.info(f"Selected move: {node.move}")

            # Expansion
            legal_moves = board.get_legal_moves()
            if not legal_moves:
                continue

            for move in legal_moves:
                new_board = board.copy()
                new_board.push(move)
                child_node = MCTSNode(new_board, parent=node, move=move)
                node.children.append(child_node)

            # Simulation + Evaluation
            value = self.neural_net.evaluate(board)

            # Backpropagation
            while node is not None:
                node.visits += 1
                node.value += value
                node = node.parent

        return root.best_child(c_param=0).move if root.children else None

class DummyNet:
    def evaluate(self, board_wrapper):
        try:
            fen = board_wrapper.board_to_fen()
            board = chess.Board(fen)
            info = self.engine.analyse(
                board,
                chess.engine.Limit(depth=self.depth),
                timeout=0.2
            )
            score = info["score"].white().score(mate_score=10000)
            return score if board_wrapper.color == 'white' else -score
        except Exception as e:
            print("Stockfish error:", e)
            return 0

    
import chess
import chess.engine

class StockfishNet:
    def __init__(self, stockfish_path="stockfish", depth=10):
        self.engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Rohan\Documents\machine-learning-projects\python-chess-ai-Rohan\src\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")
        self.depth = depth

    def evaluate(self, board_wrapper):
        fen = board_wrapper.board_to_fen()
        board = chess.Board(fen)
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth))
        score = info["score"].white().score(mate_score=10000)
        return score if board_wrapper.color == 'white' else -score

    def close(self):
        self.engine.quit()


class MCTSBoardWrapper:
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def copy(self):
        import copy
        return MCTSBoardWrapper(copy.deepcopy(self.board), self.color)

    def push(self, move):
        self.board.move(move.piece, move)

    def get_legal_moves(self):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                square = self.board.squares[row][col]
                if square.has_piece() and square.piece.color == self.color:
                    piece = square.piece
                    self.board.calc_moves(piece, row, col)
                    for move in piece.moves:
                        if not self.board.in_check(piece, move):  # Ensure move doesn't leave king in check
                            move.piece = piece
                            legal_moves.append(move)
        return legal_moves
    def board_to_fen(self):
        board = chess.Board()
        board.clear_board()

        for row in range(8):
            for col in range(8):
                square = self.board.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    symbol = piece.name[0].upper() if piece.color == 'white' else piece.name[0].lower()
                    if piece.name == 'knight':
                        symbol = 'N' if piece.color == 'white' else 'n'
                    board.set_piece_at(chess.square(col, 7 - row), chess.Piece.from_symbol(symbol))

        board.turn = chess.WHITE if self.color == 'white' else chess.BLACK
        return board.fen()

