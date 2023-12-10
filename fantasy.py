from espn_api.football import League
from numpy import std, mean
import matplotlib.pyplot as plt

class Fantasy:
    """
    Class that contains all of the fantasy football data and methods.

    Attributes:
        league (League)
            - the league
        rosters (list)
            - the rosters of the league
        all_boxscores (list)
            - all of the boxscores for each week up until the current week
        scores (dict)
            - the scores of each team
        startingLineups (dict)
            - the starting lineups of each team
        wholeLineups (dict)
            - the whole lineups of each team
        avgPosRanks (dict)
            - the average position ranks of each team's starting lineup
        posRanksStdDev (dict)
            - the standard deviation of the position ranks of each team's starting lineup
        avgScores (dict)
            - the average scores of each team
        scoreStdDev (dict)
            - the standard deviation of the scores of each team


    Methods:
        allBoxScores()
        getStartingLineups()
        getWholeLineup()
        getAvgPosRanks()
        getPosRanksStdDev()
        getScores()
        getTeamsScoreStdDev()
        getTeamsAverageScore()
        plotAvgPosRanks()
        plotPosRanksStdDev()
        plotAvgScores()
        plotScoreStdDev()
        plotScoresOverTime()
        showPlots()
        debug()
    """

    def __init__(self):

        self.league = League(
            league_id=1341300474,
            year=2023, espn_s2='AEAIFqzKEKeftvMMu5%2F5MetKk1VGKU5rOISKN%2BJwEu8BKMxVzP%2FOm8AGrI%2FMvGVuV%2FmQJtUIaIaL1zDnI9V%2B3liyixzfXy1YaEKqoWEt5XJUiNsnh%2B%2BZC%2Ftem3B6ggHYxyDa%2B4Gf6vyLpGuAW4u75nyfW7WfVvFmCk0P6DA25Zrpsif12SEjWhydWZkE4vJt7Bd1%2BmE86GbPmGuEJvf7VeBw%2B0hRqJ%2BAF2OauDWlviY2HhkhoyR%2Ftmer7luqA7kDYd9INo%2BuZYHq2AGpnTBHhfdV',
            swid='{4C0FA7AD-3853-46D2-BAE7-556390C16C1A}',
            debug=False
        )

        self.rosters = self.league.teams
        
        self.all_boxscores = self.allBoxScores()

        self.scores = self.getScores()
        self.lineups = self.getLineups()
        self.startingLineups = self.getStartingLineups()
        self.wholeLineups = self.getWholeLineup()

        self.avgPosRanks = self.getAvgPosRanks()
        self.avgPosRanksEntireTeam = self.getAvgPosRanksEntireTeam()
        self.posRanksStdDev = self.getPosRanksStdDev()

        self.avgScores = self.getTeamsAverageScore()
        self.scoreStdDev = self.getTeamsScoreStdDev()

    
    def allBoxScores(self):
        """
        Returns a list of all of the boxscores for each week up until the current week.

        Parameters: none

        Returns:
            all_boxscores (list): list of all of the boxscores for each week up until the current week
        """

        all_boxscores = []
        for i in range(1, self.league.current_week + 1):
            all_boxscores.append(self.league.box_scores(i))
        return all_boxscores

    def getStartingLineups(self):
        """
        Returns a dictionary with the team abbrev as the key and the starting lineup as the value.
        A player is considered to be in the starting lineup if their slot position is not 'BE' or 'IR'.

        Parameters: none

        Returns:
            startingLineups (dict): dictionary with the team abbrev as the key and the starting lineup as the value
        """

        startingLineups = {}

        for matchup in self.all_boxscores[self.league.current_week - 1]:
            homeLineup = []
            awayLineup = []
            for player in matchup.home_lineup:
                if player.slot_position != 'BE' and player.slot_position != 'IR':
                    homeLineup.append(player)
            for player in matchup.away_lineup:
                if player.slot_position != 'BE' and player.slot_position != 'IR':
                    awayLineup.append(player)
            startingLineups[matchup.home_team.team_abbrev] = homeLineup
            startingLineups[matchup.away_team.team_abbrev] = awayLineup

        return startingLineups


    def getWholeLineup(self):
        """
        Returns a dictionary with the team abbrev as the key and the whole lineup as the value.
        A player is considered to be in the whole lineup if they are on the roster.

        Parameters: none

        Returns:
            wholeLineups (dict): dictionary with the team abbrev as the key and the whole lineup as the value
        """
            
        wholeLineups = {}

        for matchup in self.all_boxscores[self.league.current_week - 1]:
            homeLineup = []
            awayLineup = []
            for player in matchup.home_lineup:
                homeLineup.append(player)
            for player in matchup.away_lineup:
                awayLineup.append(player)
            wholeLineups[matchup.home_team.team_abbrev] = homeLineup
            wholeLineups[matchup.away_team.team_abbrev] = awayLineup

        return wholeLineups
    

    def getLineups(self):
        """
        Returns a dictionary with the team abbrev as the key and an array containging two arrays as the value. The first array contains the starting lineup and the second array contains the whole lineup.

        Parameters: none

        Returns:
        
        """

        lineups = {}

        for matchup in self.all_boxscores[self.league.current_week - 1]:
            homeStartingLineup = []
            homeWholeLineup = []
            awayStartingLineup = []
            awayWholeLineup = []
            for player in matchup.home_lineup:
                if player.slot_position != 'BE' and player.slot_position != 'IR':
                    homeStartingLineup.append(player)
                homeWholeLineup.append(player)
            for player in matchup.away_lineup:
                if player.slot_position != 'BE' and player.slot_position != 'IR':
                    awayStartingLineup.append(player)
                awayWholeLineup.append(player)
            lineups[matchup.home_team.team_abbrev] = [homeStartingLineup, homeWholeLineup]
            lineups[matchup.away_team.team_abbrev] = [awayStartingLineup, awayWholeLineup]

        return lineups


    def getAvgPosRanks(self):
        """
        Returns a dictionary with the team abbrev as the key and the average position rank as the value.

        Parameters:
            startingLineups (dict): dictionary with the team abbrev as the key and the starting lineup as the value

        Returns:
            avgPosRanks (dict): dictionary with the team abbrev as the key and the average position rank as the value
        """

        posRanks = {}
        avgPosRanks = {}

        for team in self.rosters:
            posRanks[team.team_abbrev] = []
            for player in team.roster:
                for startingPlayer in self.startingLineups[team.team_abbrev]:
                    if player.name == startingPlayer.name:
                        posRanks[team.team_abbrev].append(player.posRank)
            avgPosRanks[team.team_abbrev] = mean(posRanks[team.team_abbrev])

        return avgPosRanks
    
    def getAvgPosRanksEntireTeam(self):
        """
        Returns a dictionary with the team abbrev as the key and the average position rank as the value.

        Parameters: none

        Returns:
            avgPosRanks (dict): dictionary with the team abbrev as the key and the average position rank as the value
        """

        posRanks = {}
        avgPosRanks = {}

        for team in self.rosters:
            posRanks[team.team_abbrev] = []
            for player in team.roster:
                for startingPlayer in self.wholeLineups[team.team_abbrev]:
                    if player.name == startingPlayer.name:
                        posRanks[team.team_abbrev].append(player.posRank)
            avgPosRanks[team.team_abbrev] = mean(posRanks[team.team_abbrev])

        return avgPosRanks



    def getPosRanksStdDev(self):
        """
        Returns a dictionary with the team abbrev as the key and the standard deviation of the position ranks as the value.

        Parameters:
            startingLineups (dict): dictionary with the team abbrev as the key and the starting lineup as the value

        Returns:
            posRanksStdDev (dict): dictionary with the team abbrev as the key and the standard deviation of the position ranks as the value
        """

        posRanksStdDev = {}

        for team in self.rosters:
            posRanks = []
            for player in team.roster:
                for startingPlayer in self.startingLineups[team.team_abbrev]:
                    if player.name == startingPlayer.name:
                        posRanks.append(player.posRank)
                        
            posRanksStdDev[team.team_abbrev] = std(posRanks)

        return posRanksStdDev


    def getScores(self):
        """
        Returns a dictionary with the team abbrev as the key and an array of scores as the value.

        Parameters: none

        Returns:
            scores (dict): dictionary with the team abbrev as the key and an array of scores as the value
        """


        scores = {}

        for team in self.league.teams:
            scores[team.team_abbrev] = []

        for week in self.all_boxscores:
            for boxscore in week:
                scores[boxscore.home_team.team_abbrev].append(boxscore.home_score)
                scores[boxscore.away_team.team_abbrev].append(boxscore.away_score)

        for team in scores:
            scores[team] = scores[team][:-1]

        return scores


    def getTeamsScoreStdDev(self):
        """
        Returns a dictionary with the team abbrev as the key and the standard deviation of the scores as the value.

        Parameters: none

        Returns:
            scoreStdDev (dict): dictionary with the team abbrev as the key and the standard deviation of the scores as the value
        """

        scoreStdDev = {}

        for team in self.scores:
            scoreStdDev[team] = std(self.scores[team])

        return scoreStdDev


    def getTeamsAverageScore(self):
        """
        Returns a dictionary with the team abbrev as the key and the average score as the value.

        Parameters:
            numWeeks (int): the number of weeks to average the scores over

        Returns:
            avgScores (dict): dictionary with the team abbrev as the key and the average score as the value
        """

        avgScores = {}

        for team in self.scores:
            avgScores[team] = mean(self.scores[team])

        return avgScores
    

    def playoffClinchers(self):
        """
        Calculates playoff clinching scenarios for each team.

        Parameters: none

        Returns: none
        """
    

    def plotAvgPosRanks(self):
        """
        Creates and plots a scatter plot of the avgPosRanks.

        Parameters: none

        Returns: none
        """

        # create and plot a scatter plot of the avgPosRanks
        plt.figure()
        plt.scatter(self.avgPosRanks.keys(), self.avgPosRanks.values())
        plt.title("Average Position Rank of Each Team's Starting Lineups (Week " + str(self.league.current_week) + ")")
        plt.xlabel("Team")
        plt.ylabel("Average Position Rank")

        # Label the points with the values (truncate to 1 decimal place)
        for team in self.avgPosRanks:
            plt.annotate(str(round(self.avgPosRanks[team], 1)), (team, self.avgPosRanks[team]))


    def plotAvgPosRanksEntireTeam(self):
        """
        Creates and plots a scatter plot of the avgPosRanks.

        Parameters: none

        Returns: none
        """

        # create and plot a scatter plot of the avgPosRanks
        plt.figure()
        plt.scatter(self.avgPosRanksEntireTeam.keys(), self.avgPosRanksEntireTeam.values())
        plt.title("Average Position Rank of Each Team (Week " + str(self.league.current_week) + ")")
        plt.xlabel("Team")
        plt.ylabel("Average Position Rank")

        # Label the points with the values (truncate to 1 decimal place)
        for team in self.avgPosRanksEntireTeam:
            plt.annotate(str(round(self.avgPosRanksEntireTeam[team], 1)), (team, self.avgPosRanksEntireTeam[team]))

    
    def plotPosRanksStdDev(self):
        """
        Creates and plots a scatter plot of the posRanksStdDev.

        Parameters: none

        Returns: none
        """

        plt.figure()
        plt.scatter(self.posRanksStdDev.keys(), self.posRanksStdDev.values())
        plt.title("Standard Deviation of Position Ranks of Each Team (Week " + str(self.league.current_week) + ")")
        plt.xlabel("Team")
        plt.ylabel("Standard Deviation of Position Ranks")

        # Label the points with the values (truncate to 1 decimal place)
        for team in self.posRanksStdDev:
            plt.annotate(str(round(self.posRanksStdDev[team], 1)), (team, self.posRanksStdDev[team]))


    def plotAvgScores(self):
        """
        Plot box and whisker plot of each team's scores. Gets scores from self.scores[teamAbbrev]
        where each key is a self.rosters.team_abbrev and each value is an array of scores.

        Parameters: none

        Returns: none
        """
        
        plt.figure()
        plt.boxplot(self.scores.values(), labels=self.scores.keys())
        plt.title("Scores of Each Team (Week " + str(self.league.current_week) + ")")
        plt.xlabel("Team")
        plt.ylabel("Score")


    def plotAvgScoresOnAllScores(self):
        """
        Plot each team's average score on top of their other scores in a scatter plot.
        A given team's average score is held in self.avgScores[teamAbbrev]. A given
        team's scores are held in an array in self.scores[teamAbbrev].

        Parameters: none

        Returns: none
        """
        
        plt.figure()
        for team in self.scores:
            plt.scatter([team] * len(self.scores[team]), self.scores[team], label=team, color='gray')
            plt.scatter(team, self.avgScores[team], label=team + " Average", color='red')
        plt.title("Scores of Each Team (Week " + str(self.league.current_week) + ")")
        plt.xlabel("Team")
        plt.ylabel("Score")


    def plotScoreStdDev(self):
        """
        Creates and plots a scatter plot of the scoreStdDev.

        Parameters: none

        Returns: none
        """

        plt.figure()
        plt.scatter(self.scoreStdDev.keys(), self.scoreStdDev.values())
        plt.title("Standard Deviation of Scores of Each Team (Week " + str(self.league.current_week) + ")")
        plt.xlabel("Team")
        plt.ylabel("Standard Deviation of Scores")

        # Label the points with the values (truncate to 1 decimal place)
        for team in self.scoreStdDev:
            plt.annotate(str(round(self.scoreStdDev[team], 1)), (team, self.scoreStdDev[team]))


    def plotScoresOverTime(self, teamAbbrev):
        """
        Plots the scores of a team over time. Gets scores from self.scores[teamAbbrev]

        Parameters:
            teamAbbrev (str): the team abbreviation

        Returns: none
        """

        # plot the scores
        plt.figure()
        plt.plot(self.scores[teamAbbrev])
        plt.title("Scores of " + teamAbbrev + " Over Time")
        plt.xlabel("Week")
        plt.ylabel("Score")

    
    def plotAllScoresOverTime(self):
        """
        Plots the scores of all teams over time in the same plot. There are many lines
        and they are on top of each other. To make the lines more readable we will spread them out
        top to bottom by adding a constant to each score. The constant will be the team's average score.
        
        Parameters: none

        Returns: none
        """

        # plot the scores
        plt.figure()
        for team in self.scores:
            plt.plot(self.scores[team], label=team)
        plt.title("Scores of Each Team Over Time")
        plt.xlabel("Week")
        plt.ylabel("Score")
        plt.legend()


    def showPlots(self):
        """
        Shows all of the plots.
        """

        plt.show()


    def debug(self):
        """
        Prints all of the data.
        """

        print("Rosters:")
        for team in self.rosters:
            print(team.team_abbrev)
            for player in team.roster:
                print(player.name)
            print()
        
        print("Boxscores:")
        for boxscore in self.boxscores:
            print(boxscore.home_team.team_abbrev, boxscore.home_score)
            print(boxscore.away_team.team_abbrev, boxscore.away_score)
            print()

        print("Starting Lineups:")
        for team in self.startingLineups:
            print(team)
            for player in self.startingLineups[team]:
                print(player.name)
            print()

        print("Average Position Ranks:")
        for team in self.avgPosRanks:
            print(team, self.avgPosRanks[team])
        print()

        print("Position Ranks Standard Deviation:")
        for team in self.posRanksStdDev:
            print(team, self.posRanksStdDev[team])
        print()

        print("Average Scores:")
        for team in self.avgScores:
            print(team, self.avgScores[team])
        print()

        print("Score Standard Deviation:")
        for team in self.scoreStdDev:
            print(team, self.scoreStdDev[team])
        print()