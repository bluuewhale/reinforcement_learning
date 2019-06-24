#아래의 코드에서 많은 도움을 받았습니다.
# - 모두의 연구소: 이영무님 TicTacToe with MCTS : http://www.modulabs.co.kr/RL_library/7984
# - MCTS python Implementation : http://mcts.ai/code/python.html
from math import *
import random
import copy
import ast

class Gomoku:
    def __init__(self, state=None, turn=0, k=5):
        self.state = state
        self.turn = turn
        self.k = k

        if self.state == None:
            self.state = [[0 for _ in range(self.k)] for _ in range(self.k)]

    @property
    def player(self):
        return (self.turn)%2 + 1

    def do_action(self, grid, print_information=False):
        self.turn += 1

        x, y = grid
        assert x >= 0 and x < self.k and y >= 0 and y < self.k # 게임판 밖을 벗어나면 assert
        assert self.state[x][y] == 0 # 해당 위치에 이미 누가 돌을 놨으면 assert

        self.state[x][y] = self.player # 바둑 판 위에 돌을 얹음
        winner = self.check_state() # 0=게임 중, 1=1번 player 승리, 2=2번 player 승리

        if print_information:
            if self.player == 1:
                player = 'Player'
            else :
                player = 'Agent'
            print('\n %s has put GoStone on %s'%(player, grid))
            print(self) # 현재 바둑판 출력

            if winner == 1 :
                print('You Won!')
            if winner == 2:
                print('Agent Won!, You Lost!')
        return

    def get_possible_actions(self):
        if self.check_state() != 0:
            return []
        else:
            actions = [(x, y) for x in range(self.k) for y in range(self.k) if self.state[x][y] == 0]
            return actions

    def get_result(self, player):
        result = self.check_state()

        if result == player: # player 승리
            return 1.0
        else:
            return 0.0 # draw

    def check_state(self):
        winning_cases = [[(x, y), (x+1, y), (x+2, y), (x+3, y), (x+4, y)] for x in range(self.k-4) for y in range(self.k)] # 세로로 5개를 채워서 이기는 경우
        winning_cases += [[(x, y), (x, y+1), (x, y+2), (x, y+3), (x, y+4)] for x in range(self.k) for y in range(self.k-4)] # 가로로 5개를 채워서 이기는 경우
        winning_cases += [[(x, y), (x-1, y+1), (x-2, y+2), (x-3, y+3), (x-4, y+4)] for x in range(4, self.k) for y in range(0, self.k-4)] # 우상향 대각선으로 5개를 채워서 이기는 경우
        winning_cases += [[(x, y), (x+1, y+1), (x+2, y+2), (x+3, y+3), (x+4, y+4)] for x in range(0, self.k-4) for y in range(0, self.k-4)] # 좌상향 대각선으로 5개를 채워서 이기는 경우

        for grids in winning_cases:
            (x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5) = grids

            if self.state[x1][y1] == self.state[x2][y2] == self.state[x3][y3] == self.state[x4][y4] == self.state[x5][y5]: # 3줄을 완성한 경우
                if self.state[x1][y1] == 1:
                    return 1 # 1번 플레이어가 승리

                elif self.state[x1][y1] == 2:
                    return 2 # 2번 플레이어가 승리

        return 0 # 경기 진행 중

    def convert_state_to_str(self, state):
        s = ''
        sign = '.OX'

        for x in range(self.k):
            s += '%s '%x # x축 표시

            for y in range(self.k):
                s += ' %s'%(sign[state[x][y]])

            s+= '\n'
        # 맨 밑줄에 y축 표시
        s += '\n   '
        for y in range(self.k):
            s += '%s '%y
        s += '\n   '

        return s

    def __repr__(self):
        return self.convert_state_to_str(self.state)
