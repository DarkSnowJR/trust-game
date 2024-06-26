from bots import *
import matplotlib.pyplot as plt


class Tournament:
    def __init__(self, players, number_of_rounds=10, top_players_to_reproduce=5, new_game=True):
        self.players = players
        self.number_of_rounds = number_of_rounds
        self.top_players_to_reproduce = top_players_to_reproduce
        self.new_game = new_game

        if self.new_game:
            self.scores = {player: 0 for player in self.players}
        self.payout = {
            ("C", "C"): (2, 2),
            ("C", "N"): (-1, 3),
            ("N", "C"): (3, -1),
            ("N", "N"): (0, 0)
        }

    def add_new_players(self, new_players):
        self.players = new_players

    def clear_history(self):
        for player in self.players:
            player.clear_history()

    def run_tournament(self):
        print("Starting tournament...")
        # print("Scores:", scores)
        for player1_index, player1 in enumerate(self.players):
            for player2_index in range(player1_index + 1, len(self.players)):
                player2 = self.players[player2_index]
                for _ in range(self.number_of_rounds):
                    move1 = player1.move()
                    move2 = player2.move()
                    payoff = self.payout[(move1, move2)]
                    self.scores[player1] += payoff[0]
                    self.scores[player2] += payoff[1]
        self.players.sort(key=lambda x: self.scores[x], reverse=True)
        top_players = self.players[:self.top_players_to_reproduce]

        print("Tournament finished!")
        print("Final standings:")
        for player in self.players:
            print(
                f"{player.__class__.__name__} - Score: {self.scores[player]}")

        self.new_game = False


def create_players():
    players = [
        AlwaysCooperate(), AlwaysCooperate(), AlwaysCooperate(),
        AlwaysBetray(), AlwaysBetray(), AlwaysBetray(),
        Copycat(), Copycat(), Copycat(),
        Copykitten(), Copykitten(), Copykitten(),
        Simpleton(), Simpleton(), Simpleton(),
        Random(), Random(), Random(), Random(),
        Grudger(), Grudger(), Grudger(),
        Detective(), Detective(), Detective(),
    ]
    return players


def add_player(name):
    if name == "AlwaysCooperate":
        return AlwaysCooperate()
    elif name == "AlwaysBetray":
        return AlwaysBetray()
    elif name == "Copycat":
        return Copycat()
    elif name == "Copykitten":
        return Copykitten()
    elif name == "Simpleton":
        return Simpleton()
    elif name == "Random":
        return Random()
    elif name == "Grudger":
        return Grudger()
    elif name == "Detective":
        return Detective()


def main():
    new_game = True
    # Define tournament parameters
    number_of_rounds = 10
    number_of_top_players_to_reproduce = 5

    while True:
        if new_game:
            # Create initial set of players
            players = create_players()
            for player in players:
                print(f"{player.__class__.__name__}")

            print("__________________________________________________")

            # Create tournament instance and run the tournament
            tournament = Tournament(
                players, number_of_rounds, number_of_top_players_to_reproduce)
            tournament.run_tournament()
            new_game = False

        else:
            for player in new_players:
                print(
                    f"{player.__class__.__name__} - Score: {tournament.scores[player]}")

            print("__________________________________________________")
            tournament.add_new_players(new_players)
            tournament.run_tournament()

        # print("Number of tournament players: ", len(tournament.players))
        # Get top 20 players from the previous tournament
        top_players_previous = tournament.players[:int(len(
            tournament.players)) - number_of_top_players_to_reproduce]

        # Get the top 5 players to reproduce
        get_top_players_to_reproduce = tournament.players[:
                                                          number_of_top_players_to_reproduce]

        get_last_players = tournament.players[-number_of_top_players_to_reproduce:]

        # Reset scores of top 5 players to reproduce
        top_players_to_reproduce = []
        for player in get_top_players_to_reproduce:
            new_player = add_player(player.__class__.__name__)
            top_players_to_reproduce.append(new_player)
            tournament.scores[new_player] = tournament.scores[player]

        for last_player in get_last_players:
            tournament.scores.pop(last_player)

        # Add top 5 players to the new tournament with reset scores
        new_players = top_players_previous + top_players_to_reproduce
        random.shuffle(new_players)

        chartLabel = []
        chartData = []
        for player in new_players:
            chartLabel.append(player.__class__.__name__)

        labels = list(dict.fromkeys(chartLabel))

        for p in labels:
            chartData.append(chartLabel.count(p))

        fig, ax = plt.subplots()
        ax.pie(chartData, labels=labels, autopct='%1.1f%%', startangle=120)
        plt.title('Pie Chart with Aggregated Labels')
        plt.axis('equal')
        plt.show()

        # Ask user if they want to run another tournament
        prompt = input(
            "Do you want to run another tournament? (y/n): ").lower()
        if prompt == 'n':
            print("Exiting the program.")
            break
        elif prompt != 'y':
            print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()
