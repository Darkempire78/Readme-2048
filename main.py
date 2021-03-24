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

class createNewCurrentFile:
    def __init__(self, grid, score, bestScore, lastMoves):
        self.grid = grid,
        self.score = score,
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
    currentFile = createNewCurrentFile(grid, 0, bestScore, [])

    with open("Data/Games/current.json", "w") as _current:
        currentFile = json.dumps(currentFile.__dict__, indent=4, ensure_ascii=False) # Convert the object to json
        _current.write(currentFile)

    # End
    issueText = "New game created!"
    endAction(grid, issue, issueAuthor, issueText)


def endAction(grid, issue, issueAuthor, issueText):
    """End the bot action"""
    generateGameBoard(grid)      
    issue.create_comment(f"{issueAuthor} {issueText}")
    issue.edit(state='closed')

def test():
    print(':(')

if __name__ == "__main__":
	main() 