from github import Github

from random import randint, choice
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
        slideLeft(issue, issueAuthor)
    elif issueType == "slideright":
        slideRight(issue, issueAuthor)

class createNewCurrentFile:
    def __init__(self, grid, bestScore, lastMoves):
        self.grid = grid,
        self.score = 0,
        self.bestScore = bestScore,
        self.lastMoves = lastMoves

# Actions

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
        print(currentFile.__dict__)
        currentFile = json.dumps(currentFile.__dict__, indent=4, ensure_ascii=False) # Convert the object to json
        _current.write(currentFile)

    # End
    issueText = "New game created!"
    endAction(grid, 0, issue, issueAuthor, issueText)


def slideLeft(issue, issueAuthor):
    """Slide left the grid"""
    grid = getGrid()

    changes = True
    score = 0
    lastCase = False

    while changes:
        changes = False
        for line in range(4):
            for case in range(4):

                if (lastCase is None) and (grid[line][case]) and (case != 0):
                    grid[line][case-1] = grid[line][case]
                    grid[line][case] = None
                    changes = True

                elif (lastCase) and (grid[line][case]) and (lastCase == grid[line][case]):
                    score += grid[line][case]
                    grid[line][case-1] = grid[line][case] * 2
                    grid[line][case] = None
                    changes = True
                
                lastCase = grid[line][case]
                
    issueText = "You slided to left!"
    endAction(grid, score, issue, issueAuthor, issueText)


def slideRight(issue, issueAuthor):
    """Slide right the grid"""
    grid = getGrid()

    changes = True
    score = 0
    lastCase = False

    while changes:
        changes = False
        for line in range(3,-1, -1):
            for case in range(3,-1, -1):

                if (lastCase is None) and (grid[line][case]) and (case != 3):
                    grid[line][case+1] = grid[line][case]
                    grid[line][case] = None
                    changes = True

                elif (lastCase) and (grid[line][case]) and (lastCase == grid[line][case]):
                    score += grid[line][case]
                    grid[line][case+1] = grid[line][case] * 2
                    grid[line][case] = None
                    changes = True
                
                lastCase = grid[line][case]
                
    issueText = "You slided to right!"
    endAction(grid, score, issue, issueAuthor, issueText)

# Utils

def getGrid():
    with open("Data/Games/current.json", "r") as _grid:
        grid = json.load(_grid)
    return grid["grid"]

def addRandomNumber(grid):

    availableCases = []

    for line in range(4):
        for case in range(4):
            if grid[line][case] is None:
                availableCases.append((line, case))

    if availableCases:
        line, case = choice(availableCases)
        newCase = randint(1, 10)
        newCase = 4 if newCase == 1 else 2
        grid[line][case] = newCase
    else:
        print("You lost!")


def endAction(grid, score, issue, issueAuthor, issueText):
    """End the bot action"""

    # Update current.json
    with open("Data/Games/current.json", "r") as _current:
        current = json.load(_current)
        try:
            current["score"] = int(current["score"][0])
        except:
            pass
        current["score"] += score
        try:
            current["bestScore"] = int(current["bestScore"][0])
        except:
            pass
        current["grid"] = grid
    with open("Data/Games/current.json", "w") as _current:
        currentFile = json.dumps(current, indent=4, ensure_ascii=False) # Convert the object to json
        _current.write(currentFile)
    
    # Add a number in the grid
    addRandomNumber(grid)
    # Generate the new game board
    generateGameBoard(grid)
    

    # Reply and close the issue
    issue.create_comment(f"{issueAuthor} {issueText}")
    issue.edit(state='closed')



if __name__ == "__main__":
	main()