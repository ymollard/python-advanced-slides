import asyncio, time


def log(*args):
    if not hasattr(log, "t0"):
        log.t0 = time.time()
    print("t+" + str(int(time.time()-log.t0)) + "\t: ", end="")
    print(*args)


class ChessMaster:
    def __init__(self):
        self.is_busy = asyncio.Lock()

    async def think_and_play(self, round: int, opponent: "Player"):
        async with self.is_busy:
            await opponent.player_is_done.wait()
            opponent.player_is_done.clear()
            log(f"Master is thinking for round {round} with opponent {opponent.id}...")
            await asyncio.sleep(1)
            opponent.master_is_done.set()


class Round:
    def __init__(self, round: int, master: "ChessMaster", players: list["Player"]):
        self.players = players
        self.round = round
        self.master = master
        self.tasks = []  # All async tasks of this round go there

    async def play(self, opponent_id: int):
        master_task = asyncio.create_task(self.master.think_and_play(self.round, self.players[opponent_id]))
        opponent_task = asyncio.create_task(self.players[opponent_id].think_and_play(self.round))
        self.tasks += [master_task, opponent_task]


class Player:
    def __init__(self, id: int):
        self.id = id
        self.is_busy = asyncio.Lock()           # Prevents the player to play with someone else
        self.player_is_done = asyncio.Event()   # Tells if the player has finished his turn
        self.master_is_done = asyncio.Event()   # Tells if the master has finished his turn with this player

    async def think_and_play(self, round: int):
        await self.master_is_done.wait()
        self.master_is_done.clear()
        async with self.is_busy:
            log("Player {} is thinking for round {}...".format(self.id, round))
            await asyncio.sleep(5)
            self.player_is_done.set()

class Simulator:
    def __init__(self):
        self.num_players = 3
        self.num_rounds = 2
        self.master = ChessMaster()
        self.players = [Player(i) for i in range(self.num_players)]
        self.rounds = [Round(i, self.master, self.players) for i in range(self.num_rounds)]

    async def simulate(self):
        # Playing all rounds with all players
        for round_id, round in enumerate(self.rounds):
            for player_id, player in enumerate(self.players):
                if round_id == 0:
                    log("Authorizing player {} to start the first for the first round".format(player_id))
                    player.master_is_done.set()
                await round.play(player_id)

        log("Simulating all moves...")
        for round in self.rounds:
            await asyncio.wait(round.tasks)
        log("Simulation is over")


async def main():
    await Simulator().simulate()

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
