#아래의 코드에서 많은 도움을 받았습니다.
# - 모두의 연구소: 이영무님 TicTacToe with MCTS : http://www.modulabs.co.kr/RL_library/7984
# - MCTS python Implementation : http://mcts.ai/code/python.html

from gomoku import *

class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent_node = parent
        self.child_nodes = []

        self.n_wins = 0
        self.n_visits = 0
        self.untried_actions = state.get_possible_actions()
        self.player = state.player

    def select_child_with_UCT(self):
        childs = sorted(self.child_nodes, key = lambda c: c.n_wins/c.n_visits + sqrt(2 * log(self.n_visits) / c.n_visits)) # UCT 수식
        return childs[-1]

    def add_child(self, state, action):
        n = Node(action = action, parent = self, state = copy.deepcopy(state))
        self.untried_actions.remove(action)
        self.child_nodes.append(n)
        return n

    def update(self, result):
        self.n_wins += result
        self.n_visits += 1

    def __repr__(self):
        return 'Action : %s W/V : %s \n'%(self.action, round(self.n_wins/self.n_visits, 3))


def MCTS_UCT(root_state, n_simulation, tree_policy=random.choice, default_policy=random.choice):
    # 현재는 tree_policy와 default_policy는 random.choice로 세팅
    # 추후에 critic과 actor로 대체

    root_node = Node(state = root_state)

    for i in range(n_simulation):
        if (i+1)%100 == 0:
            print('%s-th simulation on process'%(i+1), end='\r')
        node = root_node
        state = copy.deepcopy(root_state)

        #selection
        # root node에서 시작해서 현재까지 펼쳐진 child node 중 하나로 내려간다
        while node.untried_actions == [] and node.child_nodes != []:
            node = node.select_child_with_UCT()
            state.do_action(node.action)

        #Expansion
        # 아직 선택해보지 않은 action이 남았다면 (not-fully expanded), 해당 action을 선택하고 새로운 child node를 생성함
        if node.untried_actions != []:
            random_a = tree_policy(node.untried_actions)
            state.do_action(random_a)
            node = node.add_child(state, random_a) # add child and descent tree

        #simulation
        # 선택된(selected) 혹은 확장된(expanded) node에서부터 게임이 끝날때까지 play
        while state.get_possible_actions() != []:
            random_a = default_policy(state.get_possible_actions())
            state.do_action(random_a)

        #BackPropagation
        while node != None:
            node.update(state.get_result(node.player))
            node = node.parent_node

    childs = sorted(root_node.child_nodes, key = lambda c: c.n_wins/c.n_visits)
    print('\n %s'%childs[-5:])

    best_child = sorted(childs, key = lambda c: c.n_visits)[-1]
    return best_child, best_child.action
