import time


def log(*args):
    if not hasattr(log, "t0"):
        log.t0 = time.time()
    print("t+" + str(int(time.time()-log.t0)) + "\t: ", end="")
    print(*args)


class ChessMaster:
    def think_and_play(self, round: int, opponent: "Player"):
        log(f"Master is thinking for round {round} with opponent {opponent.id}...")
        time.sleep(1)


class Round:
    def __init__(self, round: int, master: "ChessMaster", players: list["Player"]):
        self.players = players
        self.round = round
        self.master = master

    def play(self, opponent_id: int):
        self.players[opponent_id].think_and_play(self.round)
        self.master.think_and_play(self.round, self.players[opponent_id])


class Player:
    def __init__(self, id: int):
        self.id = id

    def think_and_play(self, round: int):
        log(f"Player {self.id} is thinking for round {round}...")
        time.sleep(5)


class Simulator:
    def __init__(self):
        self.num_players = 3
        self.num_rounds = 2
        self.master = ChessMaster()
        self.players = [Player(i) for i in range(self.num_players)]
        self.rounds = [Round(i, self.master, self.players) for i in range(self.num_rounds)]

    def simulate(self):
        log("Simulating all moves...")
        for round_id, round in enumerate(self.rounds):
            for player_id, player in enumerate(self.players):
                round.play(player_id)

        log("Simulation is over")


if __name__ == "__main__":
    Simulator().simulate()
