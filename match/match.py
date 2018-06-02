from collections import namedtuple

# Mapping of pts to strings.
POINTS = {
    0: '0',
    1: '15',
    2: '30',
    3: '40',
}


class Match:
    """Represents a match of tennis."""

    def __init__(self, player_a, player_b):
        self.player_a = player_a
        self.player_b = player_b

        self.tiebreaker = False # Indicates the game is in a tiebreaker.

        self.player_scores = {
            self.player_a: {
                'tiebreak_points': 0,
                'points': 0,
                'games': 0,
            },
            self.player_b: {
                'tiebreak_points': 0,
                'points': 0,
                'games': 0,
            },
        }

    def reset_scores(self):
        """Reset the score to zero."""
        self.tiebreaker = False

        self.player_scores = {
            self.player_a: {
                'tiebreak_points': 0,
                'points': 0,
                'games': 0,
            },
            self.player_b: {
                'tiebreak_points': 0,
                'points': 0,
                'games': 0,
            },
        }

    def point_won_by(self, winner):
        if self.tiebreaker:
            self.player_scores[winner]['tiebreak_points'] += 1
        else:
            self.player_scores[winner]['points'] += 1

        # Get the other player
        for player in self.player_scores.keys():
            if player != winner:
                other_player = player

        # If the player is two points ahead then the game is won
        if self.player_scores[winner]['points'] > 3 and \
                self.player_scores[winner]['points'] > \
                self.player_scores[other_player]['points'] + 1:

            self.player_scores[winner]['points'] = 0
            self.player_scores[winner]['games'] += 1

            self.player_scores[other_player]['points'] = 0

        # Check if the tiebreaker has been won.
        # If the winning player is above 7 and two points ahead.
        if self.player_scores[winner]['tiebreak_points'] >= 7 and \
                self.player_scores[winner]['tiebreak_points'] > \
                self.player_scores[other_player]['tiebreak_points'] + 1:

            self.reset_scores()

        # If the player is two games ahead then the set is over
        # Since we don't keep track of sets this will just wrap around
        if self.player_scores[winner]['games'] >= 6 and \
                self.player_scores[winner]['games'] > \
                self.player_scores[other_player]['games'] + 1:

            self.reset_scores()

        # Check if the game is on tiebreaker
        if self.player_scores[winner]['games'] == 6 and \
                self.player_scores[other_player]['games'] == 6:

            self.tiebreaker = True

    def score(self):
        """Generate a string of the current match score.

        String is returned in the from 0-0, 15, 40
        """
        player_a_games = self.player_scores[self.player_a]['games']
        player_b_games = self.player_scores[self.player_b]['games']

        if self.tiebreaker:
            return "{}-{}, Tiebreaker {}-{}".format(
                player_a_games,
                player_b_games,
                self.player_scores[self.player_a]['tiebreak_points'],
                self.player_scores[self.player_b]['tiebreak_points'],
            )

        player_a_pts = self.player_scores[self.player_a]['points']
        player_b_pts = self.player_scores[self.player_b]['points']

        # The game is in a special state
        if player_a_pts >= 3 and player_b_pts >= 3:
            if player_a_pts == player_b_pts:
                return "{}-{}, Deuce".format(
                    player_a_games,
                    player_b_games,
                )

            leading_player = self.player_a
            if player_a_pts < player_b_pts:
                leading_player = self.player_b

            return "{}-{}, Advantage {}".format(
                player_a_games,
                player_b_games,
                leading_player
            )

        return "{}-{}, {}-{}".format(
            player_a_games,
            player_b_games,
            POINTS[player_a_pts],
            POINTS[player_b_pts],
        )
