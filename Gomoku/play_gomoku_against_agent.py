from gomoku import *
from MCTS import *

def play_game():
    state = Gomoku(k=7)
    print(state)

    # 게임이 끝날 때까지
    while state.get_possible_actions() != []:
        # player1은 컴퓨터, player2는 사람
        if state.player == 1:
            root_state = copy.deepcopy(state)
            best_child, a = MCTS_UCT(root_state, n_simulation = 5000)
            print('\n Best Action suggested after simulation: \n%s'%(best_child))
        else:
            print('\n Your Turn!')
            done = False

            while not done:
                try:
                    a = ast.literal_eval(input('Enter the grid (x,y) where you want to put your stone on : '))
                    done = True
                except:
                    pass


        state.do_action(a, print_information=True)

if __name__ == "__main__":
    play_game()
