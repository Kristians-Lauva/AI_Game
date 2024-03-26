import random

class GameContent:
    def __init__(self):
        pass
    
    @staticmethod
    def generate_sequence(length):
        return [0,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1]

    @staticmethod
    def score(pair):
        if pair == [0, 0] or pair == [1, 1]:
            return (1, 0)
        elif pair == [0, 1] or pair == [1, 0]:
            return (-1, 0)  # Subtract 1 from the score if the pair is [0, 1] or [1, 0]
        else:
            return (0, 0)
        
    @staticmethod
    def make_move(state, move):
        index1, index2 = move
        new_state = state[:]  

        if index1 > index2:
            index1, index2 = index2, index1  # Ensure index1 is less than index2

        if state[index1] == 0 and state[index2] == 1:  # Check if the selected pair is [0, 1]
            new_state.pop(index2)  # Remove the second index
        elif state[index1] == 1 and state[index2] == 0:  # Check if the selected pair is [1, 0]
            new_state.pop(index2)  # Remove the second index
        elif state[index1] == state[index2]:  # If the pair is [0, 0] or [1, 1]
            new_state.pop(index2)  # Remove the second index
            new_state[index1] = 1 if state[index1] == 0 else 0  # Change the value at index1
        return new_state
    
    @staticmethod
    def game_over(state):
        return len(state) == 1
    
    @staticmethod
    def play_game():
        length = int(input("Enter the length of the sequence (15-25): "))
        if length < 15 or length > 25:
            print("Invalid length. Please enter a number between 15 and 25.")
            return

        sequence = GameContent.generate_sequence(length)  # Use base class method for sequence generation
        print("Initial sequence:", sequence)

        player_score = 0
        ai_score = 0

        while not GameContent.game_over(sequence):  # Use base class method for game over condition
            print("Player's turn:")
            player_move_input = input("Enter two adjacent indices to swap separated by space (0-indexed): ")
            if player_move_input.lower() == 'kill':
                print("Game terminated.")
                return
            player_move = tuple(map(int, player_move_input.split()))
            
            # Check if the indices are adjacent
            if len(player_move) != 2 or not (0 <= player_move[0] < len(sequence) - 1 and player_move[1] == player_move[0] + 1):
                print("Invalid move. Please enter two adjacent indices.")
                continue
            
            pair = sequence[player_move[0]:player_move[1]+1]
            player_score += GameContent_min.score(pair)[0]
            sequence = GameContent.make_move(sequence, player_move)  # Use base class method for making moves
            print("Sequence after player's move:", sequence)
            print("Player's score:", player_score)

            if GameContent.game_over(sequence):  # Use base class method for game over condition
                print("Game Over!")
                break

            print("AI's turn:")
            ai_move = GameContent_min.get_best_move(sequence)
            print("AI changes indices:", ai_move)
            pair = sequence[ai_move[0]:ai_move[1]+1]
            ai_score += GameContent_min.score(pair)[0]
            sequence = GameContent.make_move(sequence, ai_move)  # Use base class method for making moves
            print("Sequence after AI's move:", sequence)
            print("AI's score:", ai_score)

            if GameContent.game_over(sequence):  # Use base class method for game over condition
                print("Game Over!")
                break

        print("Player's final score:", player_score)
        print("AI's final score:", ai_score)

        if player_score > ai_score:
            print("Player wins!")
        elif player_score < ai_score:
            print("AI wins!")
        else:
            print("It's a tie!")

# Subclass specific to the original game logic
class GameContent_min(GameContent):
    @staticmethod
    def score(pair):
        if pair == [0, 0] or pair == [1, 1]:
            return (1, 0)
        elif pair == [0, 1] or pair == [1, 0]:
            return (-1, 0)
        else:
            return (0, 0) 
    
    @staticmethod
    def minimax(state, depth, maximizing_player):
        if depth == 0 or GameContent_min.game_over(state):
            return GameContent_min.evaluate(state)

        if maximizing_player:
            max_eval = float('-inf')
            for move in GameContent_min.get_possible_moves(state):
                new_state = GameContent_min.make_move(state, move)
                eval = GameContent_min.score(new_state[move[0]:move[1]+1])[0]
                if eval == 1:
                    eval += GameContent_min.minimax(new_state, depth-1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in GameContent_min.get_possible_moves(state):
                new_state = GameContent_min.make_move(state, move)
                eval = GameContent_min.score(new_state[move[0]:move[1]+1])[0]
                if eval == -1:
                    eval += GameContent_min.minimax(new_state, depth-1, True)
                min_eval = min(min_eval, eval)
            return min_eval


    @staticmethod
    def get_best_move(state, maximizing_player=True, depth=4, indent=0):
        best_moves = []
        max_eval = float('-inf') if maximizing_player else float('inf')

        # Get all possible moves
        possible_moves = GameContent_min.get_possible_moves(state)

        print("AI is thinking about its moves...")

        # Print the sequence generated by the AI before evaluating the moves
        print("Sequence after AI's move:", state)

        for move in possible_moves:
            new_state = GameContent_min.make_move(state, move)
            eval = GameContent_min.minimax(new_state, depth, not maximizing_player)
            if (maximizing_player and eval > max_eval) or (not maximizing_player and eval < max_eval):
                max_eval = eval
                best_moves = [move]
            elif eval == max_eval:
                best_moves.append(move)

        print(f"{' ' * indent}AI decides on moves {best_moves} with score {max_eval}")

        if depth > 1:
            for move in best_moves:
                new_state = GameContent_min.make_move(state, move)
                print(f"{' ' * indent}Move {move}:")
                GameContent_min.get_best_move(new_state, not maximizing_player, depth - 1, indent + 4)
            if indent == 0:  # Print horizontal bars only once at the top level of recursion
                print(f"{' ' * indent}{'|' * 100}")  # Print horizontal bars to indicate the end of each branch

        return random.choice(best_moves) if best_moves else None
    @staticmethod
    def get_possible_moves(state):
        moves = []
        # First, find all moves that form pairs [0, 0] or [1, 1]
        for i in range(len(state) - 1):
            if state[i] == state[i + 1]:
                moves.append((i, i + 1))

        # Then, find all adjacent indices pairs
        for i in range(len(state) - 1):
            moves.append((i, i + 1))

        return moves
    
    @staticmethod
    def evaluate(state):
        ai_score = 0
        for i in range(len(state) - 1):
            if state[i] == state[i + 1]:
                ai_score += 1  # Increment score for each pair of adjacent elements
        return ai_score

if __name__ == "__main__":
    GameContent_min.play_game()


    #def evaluate(state):
        #ai_score = 0
        #for i in range(len(state) - 1):
       #     if state[i] == state[i + 1]:
        #        ai_score += 1  # Increment score for each pair of adjacent elements
       # return ai_score