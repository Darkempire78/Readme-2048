from github import Github

from random import randint
import os
import json

from Utils.generateGameBoard import generateGameBoard


def main():
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
    issue = repo.get_issue(number=int(os.environ["ISSUE_NUMBER"]))

    issueTitle  = issue.title.lower()
    issueAuthor = "@" + issue.user.login

    issueArguments = issueTitle.split("|")
    issueType = issueArguments[1]

    if issueType == "newgame":
        newGame(issue, issueAuthor)
    elif issueType == "slideleft":
        slidLeft(issue, issueAuthor)

class createNewCurrentFile:
    def __init__(self, grid, bestScore, lastMoves):
        self.grid = grid,
        self.score = 0,
        self.bestScore = bestScore,
        self.lastMoves = lastMoves

def newGame(issue, issueAuthor):
    """Create a new 2048 game"""

    grid = [
            [None, None, None, None], 
            [None, None, None, None], 
            [None, None, None, None],
            [None, None, None, None]
        ]
    
    # Add random number
    gridLine = randint(0, 3)
    gridCase = randint(0, 3)
    grid[gridLine][gridCase] = 2

    # Read the bestScore
    bestScore = 0
    with open("Data/bestScore.txt", "r") as _bestScore:
        bestScore = int(_bestScore.read())

    # Write the current file
    currentFile = createNewCurrentFile(grid, bestScore, [])

    with open("Data/Games/current.json", "w") as _current:
        currentFile = json.dumps(currentFile.__dict__, indent=4, ensure_ascii=False) # Convert the object to json
        _current.write(currentFile)

    # End
    issueText = "New game created!"
    endAction(grid, 0, issue, issueAuthor, issueText)

def slidLeft(issue, issueAuthor):
    """Slide up the grid"""
    grid = getGrid()

    score = 0
    lastCase = False
    for line in range(4):
        for case in range(4):
            if grid[line][case] is None:
                lastCase = None
            elif (lastCase is None) and (grid[line][case]):
                grid[line][case-1] = grid[line][case]
                grid[line][case] = None
            elif (lastCase) and (grid[line][case]) and (lastCase == grid[line][case]):
                score += grid[line][case]
                grid[line][case-1] = grid[line][case] * 2
                grid[line][case] = None
                
    issueText = "You slided to left!"
    endAction(grid, score, issue, issueAuthor, issueText)


def getGrid():
    with open("Data/Games/current.json", "r") as _grid:
        grid = _grid.read()
        grid = json.load(grid)
    return grid["grid"]

def endAction(grid, score, issue, issueAuthor, issueText):
    """End the bot action"""
    generateGameBoard(grid)

    # Update current.json
    with open("Data/Games/current.json", "r") as _current:
        current = json.load(_current)
        print("current[score] : ", current["score"])
        print("score : ", score)
        current["score"] += score
        current["grid"] = grid
    with open("Data/Games/current.json", "w") as _current:
        currentFile = json.dumps(current.__dict__, indent=4, ensure_ascii=False) # Convert the object to json
        _current.write(currentFile)

    # Reply and close the issue
    issue.create_comment(f"{issueAuthor} {issueText}")
    issue.edit(state='closed')



if __name__ == "__main__":
	main() 