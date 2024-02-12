from tkinter import Tk, Button
from tkinter.font import Font
import sys
from copy import deepcopy
import time
from random import randint

"""
    Initialization of the global variables
"""
size = 4
min_util = -1000
max_util = +1000
x_player = 'X'
o_player = 'O'
empty = ' '
level = 3
moves = 0
maxDepth = 10
"""
    Variables for the statistics
"""
cutOffOccured = False
maxDepthReached = 0
totalNodes = 0
pruningMax = 0
pruningMin = 0

inf = 9999999999
neg_inf = -9999999999

computer_player = x_player
human_player = o_player

"""
    Changes the player after a move
"""


def other_player(player):
    if player == x_player:
        return o_player
    else:
        return x_player


"""
    Class state maintains the game parameters
"""


class State:
    def __init__(self, nextPlayer, other=None):
        self.nextPlayer = nextPlayer
        self.table = {}
        self.depth = 0
        self.utility = 0
        self.value = 0
        self.children = {}

        for y in range(size):
            for x in range(size):
                self.table[x, y] = empty

        # copy constructor
        if other:
            self.__dict__ = deepcopy(other.__dict__)

    def printBoard(self):
        for i in range(0, size):
            for j in range(0, size):
                if self.table[i, j] == empty:
                    sys.stdout.write(' _ ')
                elif self.table[i, j] == x_player:
                    sys.stdout.write(' X ')
                else:
                    sys.stdout.write(' O ')
            print("")

    def is_full(self):
        for i in range(0, size):
            for j in range(0, size):
                if self.table[i, j] == empty:
                    return False

        return True

    def won(self, player):
        # horizontal
        for x in range(size):
            winning = []
            for y in range(size):
                if self.table[x, y] == player:
                    winning.append((x, y))
            if len(winning) == size:
                return winning

        # vertical
        for y in range(size):
            winning = []
            for x in range(size):
                if self.table[x, y] == player:
                    winning.append((x, y))
            if len(winning) == size:
                return winning

        # diagonal \
        winning = []
        for y in range(size):
            x = y
            if self.table[x, y] == player:
                winning.append((x, y))
        if len(winning) == size:
            return winning

        # diagonal /
        winning = []
        for y in range(size):
            x = size - 1 - y
            if self.table[x, y] == player:
                winning.append((x, y))
        if len(winning) == size:
            return winning

        # default
        return None


"""
    Action function gives the next possible legal moves
"""


def ACTIONS(state):
    global maxDepthReached
    global totalNodes
    global maxDepth
    children = []
    for i in range(0, size):
        for j in range(0, size):
            if state.table[i, j] == empty and maxDepthReached<=maxDepth:
                childTable = deepcopy(state.table)
                childTable[i, j] = state.nextPlayer
                childState = State(nextPlayer=state.nextPlayer)
                childState.nextPlayer = other_player(state.nextPlayer)
                childState.table = childTable
                childState.value = state.value
                childState.depth = state.depth + 1
                maxDepthReached = max(maxDepthReached, childState.depth)
                children.append(childState)

    totalNodes += len(children)
    return children


""""
    Terminal function to check if the terminal state has been reached
"""


def TERMINAL_TEST(state):
    player = other_player(player=state.nextPlayer)
    if state.table[0, 0] == state.table[0, 1] \
            and state.table[0, 1] == state.table[0, 2] \
            and state.table[0, 2] == state.table[0, 3] \
            and state.table[0, 0] != empty:
        return True
    if state.table[1, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[1, 2] \
            and state.table[1, 2] == state.table[1, 3] \
            and state.table[1, 0] != empty:
        return True
    if state.table[2, 0] == state.table[2, 1] \
            and state.table[2, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[2, 3] \
            and state.table[2, 0] != empty:
        return True
    if state.table[3, 0] == state.table[3, 1] \
            and state.table[3, 1] == state.table[3, 2] \
            and state.table[3, 2] == state.table[3, 3] \
            and state.table[3, 0] != empty:
        return True
    if state.table[0, 0] == state.table[1, 0] \
            and state.table[1, 0] == state.table[2, 0] \
            and state.table[2, 0] == state.table[3, 0] \
            and state.table[0, 0] != empty:
        return True
    if state.table[0, 1] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 1] \
            and state.table[0, 1] != empty:
        return True
    if state.table[0, 2] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 2] \
            and state.table[0, 2] != empty:
        return True
    if state.table[0, 3] == state.table[1, 3] \
            and state.table[1, 3] == state.table[2, 3] \
            and state.table[2, 3] == state.table[3, 3] \
            and state.table[0, 3] != empty:
        return True
    if state.table[0, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 3] \
            and state.table[0, 0] != empty:
        return True
    if state.table[0, 3] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 0] \
            and state.table[0, 3] != empty:
        return True
    if state.is_full():
        return 2

    return False


"""
    Utility function to calculate the utility of a state
"""


def UTILITY(state):
    if state.table[0, 0] == state.table[0, 1] \
            and state.table[0, 1] == state.table[0, 2] \
            and state.table[0, 2] == state.table[0, 3] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[1, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[1, 2] \
            and state.table[1, 2] == state.table[1, 3] \
            and state.table[1, 0] != empty:
        return PLAYER_UTIL(state.table[1, 0])
    if state.table[2, 0] == state.table[2, 1] \
            and state.table[2, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[2, 3] \
            and state.table[2, 0] != empty:
        return PLAYER_UTIL(state.table[2, 0])
    if state.table[3, 0] == state.table[3, 1] \
            and state.table[3, 1] == state.table[3, 2] \
            and state.table[3, 2] == state.table[3, 3] \
            and state.table[3, 0] != empty:
        return PLAYER_UTIL(state.table[3, 0])
    if state.table[0, 0] == state.table[1, 0] \
            and state.table[1, 0] == state.table[2, 0] \
            and state.table[2, 0] == state.table[3, 0] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[0, 1] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 1] \
            and state.table[0, 1] != empty:
        return PLAYER_UTIL(state.table[0, 1])
    if state.table[0, 2] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 2] \
            and state.table[0, 2] != empty:
        return PLAYER_UTIL(state.table[0, 2])
    if state.table[0, 3] == state.table[1, 3] \
            and state.table[1, 3] == state.table[2, 3] \
            and state.table[2, 3] == state.table[3, 3] \
            and state.table[0, 3] != empty:
        return PLAYER_UTIL(state.table[0, 3])
    if state.table[0, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 3] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[0, 3] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 0] \
            and state.table[0, 3] != empty:
        return PLAYER_UTIL(state.table[0, 3])

    return 0


def PLAYER_UTIL(player):
    if player == computer_player:
        return max_util
    elif player == human_player:
        return min_util
    return 0


"""
    RANDOM PLAY
"""


def RANDOM_PLAY(state):
    state.children = ACTIONS(state)
    retVal = randint(0, len(state.children) - 1)
    return state.children[retVal]


"""
    ALPHA BETA SEARCH ALGORITHM
"""


def ALPHA_BETA_SEARCH(state, start):
    v = MAX_VALUE(state=state, alpha=min_util, beta=max_util, start=start)
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    return retVal


def MAX_VALUE(state, alpha, beta, start):
    global cutOffOccured
    global pruningMax
    global pruningMin
    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

    duration = time.time() - start
    if duration >= 10:
        cutOffOccured = True
        return HEURISTIC(state)

    v = neg_inf
    new_alpha = alpha
    state.children = ACTIONS(state)
    for a in state.children:
        v = max(v, MIN_VALUE(state=a, alpha=new_alpha, beta=beta, start=start))
        a.value = v
        if v >= beta:
            pruningMax += 1
            return v
        new_alpha = max(new_alpha, v)
    return v


def MIN_VALUE(state, alpha, beta, start):
    global cutOffOccured
    global pruningMax
    global pruningMin
    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

    duration = time.time() - start
    if duration >= 10:
        cutOffOccured = True
        return HEURISTIC(state)

    v = inf
    new_beta = beta
    state.children = ACTIONS(state)
    for a in state.children:
        v = min(v, MAX_VALUE(state=a, alpha=alpha, beta=new_beta, start=start))
        a.value = v
        if v <= alpha:
            pruningMin += 1
            return v
        new_beta = min(new_beta, v)
    return v


"""
    Heuristic function called if timeout occurs
"""


def HEURISTIC(state):
    x3 = 0
    x2 = 0
    x1 = 0
    o3 = 0
    o2 = 0
    o1 = 0

    # check row wise
    for r in range(0, size):
        os = 0
        xs = 0
        for c in range(0, size):
            if state.table[r, c] == x_player:
                xs += 1
            elif state.table[r, c] == o_player:
                os += 1

        if xs == 0:
            if os == 1:
                o1 += 1
            elif os == 2:
                o2 += 1
            elif os == 3:
                o3 += 1

        if os == 0:
            if xs == 1:
                x1 += 1
            elif xs == 2:
                x2 += 1
            elif xs == 3:
                x3 += 1

    # check column wise
    for c in range(0, size):
        os = 0
        xs = 0
        for r in range(0, size):
            if state.table[r, c] == x_player:
                xs += 1
            elif state.table[r, c] == o_player:
                os += 1

        if xs == 0:
            if os == 1:
                o1 += 1
            elif os == 2:
                o2 += 1
            elif os == 3:
                o3 += 1

        if os == 0:
            if xs == 1:
                x1 += 1
            elif xs == 2:
                x2 += 1
            elif xs == 3:
                x3 += 1

    # check main diagonal
    os = 0
    xs = 0
    for i in range(0, size):
        if state.table[i, i] == x_player:
            xs += 1
        elif state.table[i, i] == o_player:
            os += 1

    if xs == 0:
        if os == 1:
            o1 += 1
        elif os == 2:
            o2 += 1
        elif os == 3:
            o3 += 1

    if os == 0:
        if xs == 1:
            x1 += 1
        elif xs == 2:
            x2 += 1
        elif xs == 3:
            x3 += 1

            # check main diagonal
    os = 0
    xs = 0
    for i in range(0, size):
        if state.table[size - i - 1, i] == x_player:
            xs += 1
        elif state.table[size - i - 1, i] == o_player:
            os += 1

    if xs == 0:
        if os == 1:
            o1 += 1
        elif os == 2:
            o2 += 1
        elif os == 3:
            o3 += 1

    if os == 0:
        if xs == 1:
            x1 += 1
        elif xs == 2:
            x2 += 1
        elif xs == 3:
            x3 += 1

    return (6 * x3 + 3 * x2 + x1) - (6 * o3 + 3 * o2 + o1)


start = time.time()

first = "h"

"""
    Code for the GUI of the game using Tkinter library
"""


class GUI:
    def __init__(self):
        self.game = State(nextPlayer=human_player)
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=32)
        self.buttons = {}

        for x, y in self.game.table:
            handler = lambda x=x, y=y: self.move(x, y)
            button = Button(self.app, command=handler, font=self.font, width=2, height=1)
            button.grid(row=x, column=y)
            self.buttons[x, y] = button

        # handler = lambda: self.reset()
        # button = Button(self.app, text='Reset', command=handler)
        # button.grid(row=size + 1, column=0, columnspan=size, sticky='WE')

        """
        Code for selecting the levels
        """
        # buttonE = Button(self.app, text='Easy', command=lambda: self.selectdifficulty(1))
        # buttonE.grid(row=size + 2, column=0, columnspan=size, sticky='WE')
        # buttonM = Button(self.app, text='Medium', command=lambda: self.selectdifficulty(2))
        # buttonM.grid(row=size + 3, column=0, columnspan=size, sticky='WE')
        # buttonH = Button(self.app, text='Hard', command=lambda: self.selectdifficulty(3))
        # buttonH.grid(row=size + 4, column=0, columnspan=size, sticky='WE')
        # self.update()
        if first == "c":
            self.game.nextPlayer = computer_player
            self.computer_move()

    def selectdifficulty(self, value):
        global level
        level = value
        self.reset()

    def reset(self):
        self.resetStats()
        self.game = State(nextPlayer=human_player)
        self.update()
        self.app.destroy()
        Select().mainloop()

    def move(self, x, y):
        global level
        self.app.config(cursor="watch")
        self.app.update()
        self.game.table[x, y] = human_player
        self.game.nextPlayer = computer_player
        self.update()
        if TERMINAL_TEST(self.game):
            return
        self.computer_move()

    def computer_move(self):
        if level == 3:
            self.game.depth = 0
            self.game = ALPHA_BETA_SEARCH(self.game, time.time())
            self.printStats()
            self.resetStats()
        elif level == 2:
            global moves
            if moves % 2 == 0:
                self.game = RANDOM_PLAY(self.game)
            else:
                self.game = ALPHA_BETA_SEARCH(self.game, time.time())
                self.printStats()
                self.resetStats()
            moves += 1
        elif level == 1:
            self.game = RANDOM_PLAY(self.game)
        self.update()
        self.app.config(cursor="")

    def update(self):
        for (x, y) in self.game.table:
            text = self.game.table[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'green'
            if text == empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                self.buttons[x, y]['state'] = 'disabled'
        winning = TERMINAL_TEST(self.game)
        if winning==True:
            winner2 = self.game.won(player=other_player(self.game.nextPlayer))
            if winner2:
                for x, y in winner2:
                    self.buttons[x, y]['disabledforeground'] = 'red'
                print(other_player(self.game.nextPlayer) + " wins!")
                if other_player(self.game.nextPlayer) != 'X':
                    temp=Tk()
                    temp.title("Win :)")
                    def comm():
                        temp.destroy()
                        self.reset()
                    bwin=Button(temp,text="You Win!",command=comm)
                    bwin.grid(row=0, column=0, rowspan=20, columnspan=20, sticky='WE')
                else:
                    temp=Tk()
                    temp.title("Loss :(")
                    def comm():
                        temp.destroy()
                        self.reset()
                    bwin=Button(temp,text="You Lost!",command=comm)
                    bwin.grid(row=0, column=0, rowspan=20, columnspan=20, sticky='WE')
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
        elif winning==2:
            temp=Tk()
            temp.title("Tie")
            def comm():
                temp.destroy()
                self.reset()
            b=Button(temp,text="Tied GG",command=comm)
            b.grid(row=0, column=0, rowspan=20, columnspan=20, sticky='WE')
        for (x, y) in self.game.table:
            self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()

    ## Function to reset the stats of the game
    def resetStats(self):
        global cutOffOccured
        global maxDepthReached
        global totalNodes
        global pruningMax
        global pruningMin

        cutOffOccured = False
        maxDepthReached = 0
        totalNodes = 0
        pruningMax = 0
        pruningMin = 0

    ## Funtion to print the stats of the game
    def printStats(self):
        global cutOffOccured
        global maxDepthReached
        global totalNodes
        global pruningMax
        global pruningMin

        print("-----------------------")
        print("Statistics of the Move")
        print("Cutoff Occured:" + str(cutOffOccured))
        print("Maximum Depth Reached:" + str(maxDepthReached))
        print("Total number of nodes generated:" + str(totalNodes))
        print("Number of times pruning occured within Max-Value:" + str(pruningMax))
        print("Number of times pruning occured within Min-Value:" + str(pruningMin))


"""
    Code for a dialog box to select who goes first: human or the computer
"""


class Select:
    def __init__(self):
        self.app = Tk()
        self.app.title('Select Who Goes First')
        self.app.geometry("400x100")
        self.font = Font(family="Helvetica", size=32)

        computer_handle = lambda: self.choose("c")
        human_handle = lambda: self.choose("h")
        b1 = Button(self.app, text='Computer', command=computer_handle)
        b1.grid(row=0, column=0, columnspan=20, sticky='WE')

        b2 = Button(self.app, text='Human', command=human_handle)
        b2.grid(row=1, column=0, columnspan=20, sticky='WE')

    def choose(self, option):
        global first
        first = option
        self.app.destroy()
        GUI().mainloop()

    def mainloop(self):
        self.app.mainloop()


"""
    main function starts from here
"""
Select().mainloop()