from tkinter import Tk, Label, Button, X
from fantasy import Fantasy


fantasy = Fantasy()


def plot_graph(number):

    if number == 1:
        fantasy.plotAvgPosRanks()
    elif number == 2:
        fantasy.plotPosRanksStdDev()
    elif number == 3:
        fantasy.plotAvgScores()
    elif number == 4:
        fantasy.plotScoreStdDev()
    elif number == 5:
        fantasy.plotAvgPosRanks()
        fantasy.plotPosRanksStdDev()
        fantasy.plotAvgScores()
        fantasy.plotScoreStdDev()
    elif number == 6:
        fantasy.debug()
        return
    elif number == 7:
        fantasy.plotAvgPosRanksEntireTeam()

    fantasy.showPlots()


def scoresOverTime(choice):
    if choice == 1:
        fantasy.plotAllScoresOverTime()
    # if choice is a string
    elif type(choice) == str:
        fantasy.plotScoresOverTime(choice)
    else:
        fantasy.plotScoresOverTime('')
        fantasy.plotScoresOverTime('')
        fantasy.plotScoresOverTime('')
        fantasy.plotScoresOverTime('')
        fantasy.plotScoresOverTime('')
        fantasy.plotScoresOverTime('')
        fantasy.plotScoresOverTime('')
        fantasy.plotScoresOverTime('')
    
    fantasy.showPlots()


root = Tk()


root.title("Fantasy Football Data Analysis")
Label(root, text="Fantasy Football Data Analysis", font=("Helvetica", 16)).pack(pady=10)

Button(root, text="Plot Avg. Position Ranks of Starters", command=lambda: plot_graph(1)).pack(fill=X)
Button(root, text="Plot Avg. Position Ranks of Entire Team", command=lambda: plot_graph(7)).pack(fill=X)
Button(root, text="Plot Std. Dev. of Position Ranks", command=lambda: plot_graph(2)).pack(fill=X)
Button(root, text="Plot Avg. Scores", command=lambda: plot_graph(3)).pack(fill=X)
Button(root, text="Plot Std. Dev. of Scores", command=lambda: plot_graph(4)).pack(fill=X)
Button(root, text="Plot All", command=lambda: plot_graph(5)).pack(fill=X)
Button(root, text="Debug", command=lambda: plot_graph(14)).pack(fill=X)
Button(root, text="Quit", command=root.quit).pack(fill=X)

Label(root, text="Plot Scores Over Time", font=("Helvetica", 16)).pack(pady=10)
Button(root, text="", command=lambda: scoresOverTime('')).pack(fill=X)
Button(root, text="", command=lambda: scoresOverTime('')).pack(fill=X)
Button(root, text="", command=lambda: scoresOverTime('')).pack(fill=X)
Button(root, text="", command=lambda: scoresOverTime('')).pack(fill=X)
Button(root, text="", command=lambda: scoresOverTime('')).pack(fill=X)
Button(root, text="", command=lambda: scoresOverTime('')).pack(fill=X)
Button(root, text="", command=lambda: scoresOverTime('')).pack(fill=X)
Button(root, text="", command=lambda: scoresOverTime('')).pack(fill=X)
Button(root, text="Plot All Separately", command=lambda: scoresOverTime(None)).pack(fill=X)
Button(root, text="Plot All Together", command=lambda: scoresOverTime(1)).pack(fill=X)


root.mainloop()