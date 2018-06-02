import unittest
import unittest

from match.match import Match

POINTS_TO_WIN_GAME = 4
POINTS_TO_WIN_SET = 24

class TestMatch(unittest.TestCase):
    def setUp(self):
        self.players = ("player 1", "player 2")
        self.match = Match(*self.players)

    def test_point_scored(self):
        """Test a point being added to a player a."""
        # Initial score should be 0-0 all
        self.assertEqual(
            self.match.score(),
            "0-0, 0-0",
        )

        self.match.point_won_by("player 1")
        self.assertEqual(
            self.match.score(),
            "0-0, 15-0",
        )

    def test_winning_game(self):
        """Tests a single player winning 4 points in a row to win a game.

        Tests both player_a and player_b
        """
        EXPECTED_SCORES = {
            self.players[0]: [
                "0-0, 0-0",
                "0-0, 15-0",
                "0-0, 30-0",
                "0-0, 40-0",
                "1-0, 0-0",
            ],
            self.players[1]: [
                "0-0, 0-0",
                "0-0, 0-15",
                "0-0, 0-30",
                "0-0, 0-40",
                "0-1, 0-0",
            ],
        }

        for player in self.players:
            for expected_score in EXPECTED_SCORES[player]:
                self.assertEqual(
                    self.match.score(),
                    expected_score,
                )
                self.match.point_won_by(player)

            self.match.reset_scores()

    def set_deuce(self):
        """Helper function to set a match to the state of deuce."""
        self.match.reset_scores()
        for i in range(3):
            self.match.point_won_by(self.players[0])
            self.match.point_won_by(self.players[1])

    def test_deuce(self):
        """Sets up the situation where the players are in deuce."""
        self.set_deuce()
        self.assertEqual(
            self.match.score(),
            '0-0, Deuce',
        )

    def test_advantage(self):
        """Test both players can reach the state of advantage."""
        self.set_deuce()

        # advantage player 1
        self.match.point_won_by(self.players[0])
        self.assertEqual(
            self.match.score(),
            '0-0, Advantage {}'.format(self.players[0])
        )

        self.set_deuce()
        # advantage player 2
        self.match.point_won_by(self.players[1])
        self.assertEqual(
            self.match.score(),
            '0-0, Advantage {}'.format(self.players[1])
        )

    def test_set_win(self):
        """Checks that a set can be won by each player."""
        # Player 1
        for i in range(POINTS_TO_WIN_SET - 1):
            self.match.point_won_by(self.players[0])
        self.assertEqual(
            self.match.score(),
            '5-0, 40-0',
        )

        self.match.point_won_by(self.players[0])
        self.assertEqual(
            self.match.score(),
            '0-0, 0-0',
        )

        # Player 2
        for i in range(POINTS_TO_WIN_SET - 1):
            self.match.point_won_by(self.players[1])
        self.assertEqual(
            self.match.score(),
            '0-5, 0-40',
        )

        self.match.point_won_by(self.players[1])
        self.assertEqual(
            self.match.score(),
            '0-0, 0-0',
        )

    def test_close_set_win(self):
        """Checks that the set continues to a seventh game when close."""
        # Adds five games to both players scores
        for i in range(5 * POINTS_TO_WIN_GAME):
            self.match.point_won_by(self.players[0])

        for i in range(5 * POINTS_TO_WIN_GAME + 3):
            self.match.point_won_by(self.players[1])

        self.assertEqual(
            self.match.score(),
            '5-5, 0-40',
        )

        self.match.point_won_by(self.players[1])
        self.assertEqual(
            self.match.score(),
            '5-6, 0-0',
        )
        for i in range(POINTS_TO_WIN_GAME):
            self.match.point_won_by(self.players[1])

        self.assertEqual(
            self.match.score(),
            '0-0, 0-0',
        )

    def test_tiebreaker(self):
        # Adds 6 games to both players scores
        for i in range(5 * POINTS_TO_WIN_GAME):
            self.match.point_won_by(self.players[0])

        for i in range(6 * POINTS_TO_WIN_GAME):
            self.match.point_won_by(self.players[1])

        for i in range(POINTS_TO_WIN_GAME):
            self.match.point_won_by(self.players[0])

        self.assertEqual(
            self.match.score(),
            "6-6, Tiebreaker 0-0",
        )

        for i in range(5):
            self.match.point_won_by(self.players[0])
            self.match.point_won_by(self.players[1])

        self.assertEqual(
            self.match.score(),
            "6-6, Tiebreaker 5-5",
        )

        self.match.point_won_by(self.players[0])
        self.assertEqual(
            self.match.score(),
            "6-6, Tiebreaker 6-5",
        )
        self.match.point_won_by(self.players[0])
        self.assertEqual(
            self.match.score(),
            "0-0, 0-0",
        )
