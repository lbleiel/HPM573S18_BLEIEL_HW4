from enum import Enum
import numpy as np
import random as random


class CoinFlip(Enum):
    HEAD = 1
    TAIL = 0


class Game(object):
    def __init__(self, id):
        self._id = id
        self._coinState = CoinFlip.HEAD
        self._countTails = 0
        self._countWin = 0
        self._totalFlips = 20
        self._flipNum = 1
        self._rnd = np.random
        self._rnd.seed(self._id * self._flipNum)

    def nextFlip(self):
        if self._coinState == CoinFlip.HEAD:
            if self._rnd.random_sample() > 0.5:
                self._coinState = CoinFlip.HEAD

            if self._rnd.random_sample() < 0.5:
                self._coinState = CoinFlip.TAIL
                self._countTails = 1

        elif self._coinState == CoinFlip.TAIL:
            if self._rnd.random_sample() <0.5:
                self._coinState = CoinFlip.TAIL
                self._countTails += 1

            if self._rnd.random_sample() > 0.5:
                self._coinState = CoinFlip.HEAD
                if self._countTails >=2:
                    self._countWin += 1
                self._countTails = 0
        self._flipNum += 1

    def play(self):
        for i in range(1, self._totalFlips+1):
            self._rnd = np.random
            self._rnd.seed(self._id * self._flipNum)
            self.nextFlip()

    def get_reward(self):
        self.play()
        self.reward = (100*self._countWin) - 250
        return self.reward


class Cohort:
    def __init__(self, id, pop_size):
        self._players = []
        n = 1

        while n <= pop_size:
            player = Game(id=id*pop_size + n)
            self._players.append(player)
            n += 1

    def simulate(self):
        game_reward = []
        for player in self._players:
            game_reward.append(player.get_reward())
        return sum(game_reward)/len(game_reward)


trial1 = Cohort(id=1, pop_size=1000)
print(trial1.simulate())
