from github import Github

from random import randint, choice
import os
import json
import datetime

from Utils.generateGameBoard import generateGameBoard, generateEndGameBoard


def main():
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])
    issue = repo.get_issue(number=int(os.environ["ISSUE_NUMBER"]))

    issueTitle  = issue.title.lower()
    issueAuthor = "@" + issue.user.login

    issueArguments = issueTitle.split("|")
    issueType = issueArguments[1]

    # Prevent from playing twice in a row
    currentFile = open("Data/Games/current.json", "r", encoding="utf-8")
    current = json.load(currentFile)
    currentFile.close()
    if len(current["moves"]) > 0:
        if current["moves"][-1] == issueAuthor:
            # Reply and close the issue
            issue.create_comment(f"{issueAuthor} You cannot play two times in a row!")
            issue.edit(state='closed', labels=["invalid"])
            return

    if issueType == "newgame":
        newGame(issue, issueAuthor)
    elif issueType == "slideleft":
        slideLeft(issue, issueAuthor)
    elif issueType == "slideright":
        slideRight(issue, issueAuthor)
    elif issueType == "slideup":
        slideUp(issue, issueAuthor)
    elif issueType == "slidedown":
        slideDown(issue, issueAuthor)
    else:
        # Reply and close the issue
        issue.create_comment(f"{issueAuthor} This action does not exist!")
        issue.edit(state='closed', labels=["invalid"])

class createNewCurrentFile:
    def __init__(self, grid, bestScore, moves):
        self.grid = grid,
        self.score = 0,
        self.bestScore = bestScore,
        self.moves = moves

# Actions

def newGame(issue, issueAuthor):
    """Create a new 2048 game"""
    
    if checkNextActions(getGrid()):
        # Reply and close the issue
        issue.create_comment(f"{issueAuthor} The game is not ended!")
        issue.edit(state='closed', labels=["invalid"])
        return

    # Set the best score
    bestScoreFile =  open("Data/bestScore.txt", "r", encoding="utf-8")
    bestScore = int(bestScoreFile.read())
    bestScoreFile.close()

    currentFile = open("Data/Games/current.json", "r", encoding="utf-8")
    current = json.load(currentFile)
    currentFile.close()

    if bestScore < current["score"]:
        with open("Data/bestScore.txt", "w", encoding="utf-8") as _bestScoreFile:
            _bestScoreFile.write(str(current["score"]))

    # Archive the former game    
    date = datetime.datetime.now().strftime("%m-%d-%Y %H-%M")
    os.mkdir(f"Data/Games/{date}")
    os.rename("Data/Games/current.json", f"Data/Games/{date}/game.json")
    os.rename("Data/gameboard.png", f"Data/Games/{date}/gameboard.png")
    
    

    # Change the actions
    readme =  open("README.md", "r", encoding="utf-8")
    readme = readme.read()
    readme = readme.split("<!-- 2048GameActions -->", 2)

    readme[1] = "<a href=\"https://github.com/Darkempire78/readme-2048/issues/new?title=2048|slideUp&body=Just+push+'Submit+new+issue'.+You+don't+need+to+do+anything+else.\"> <img src=\"Assets/slideUp.png\"/> </a> <a href=\"https://github.com/Darkempire78/readme-2048/issues/new?title=2048|slideDown&body=Just+push+'Submit+new+issue'.+You+don't+need+to+do+anything+else.\"> <img src=\"Assets/slideDown.png\"/> </a> <a href=\"https://github.com/Darkempire78/readme-2048/issues/new?title=2048|slideLeft&body=Just+push+'Submit+new+issue'.+You+don't+need+to+do+anything+else.\"> <img src=\"Assets/slideLeft.png\"/> </a> <a href=\"https://github.com/Darkempire78/readme-2048/issues/new?title=2048|slideRight&body=Just+push+'Submit+new+issue'.+You+don't+need+to+do+anything+else.\"> <img src=\"Assets/slideRight.png\"/> </a>"

    with open("README.md", "w", encoding="utf-8") as _readme:
        _readme.write("<!-- 2048GameActions -->".join(readme))

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
    with open("Data/bestScore.txt", "r", encoding="utf-8") as _bestScore:
        bestScore = int(_bestScore.read())

    # Write the current file
    currentFile = createNewCurrentFile(grid, bestScore, [])

    with open("Data/Games/current.json", "w", encoding="utf-8") as _current:
        print(currentFile.__dict__)
        currentFile = json.dumps(currentFile.__dict__, indent=4, ensure_ascii=False) # Convert the object to json
        _current.write(currentFile)

    # End
    issueText = "New game created!"
    endAction(grid, 0, issue, issueAuthor, issueText, True)

# Slide

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
                    score += grid[line][case] * 2
                    grid[line][case-1] = grid[line][case] * 2
                    grid[line][case] = None
                    changes = True
                
                lastCase = grid[line][case]
                
    issueText = "You slided left!"
    endAction(grid, score, issue, issueAuthor, issueText, False)

def slideRight(issue, issueAuthor):
    """Slide right the grid"""
    grid = getGrid()

    changes = True
    score = 0
    lastCase = False

    while changes:
        changes = False
        for line in range(4):
            for case in range(3,-1, -1):

                if (lastCase is None) and (grid[line][case]) and (case != 3):
                    grid[line][case+1] = grid[line][case]
                    grid[line][case] = None
                    changes = True

                elif (lastCase) and (grid[line][case]) and (lastCase == grid[line][case]) and (case != 3):
                    score += grid[line][case] * 2
                    grid[line][case+1] = grid[line][case] * 2
                    grid[line][case] = None
                    changes = True
                
                lastCase = grid[line][case]
                
    issueText = "You slided right!"
    endAction(grid, score, issue, issueAuthor, issueText, False)

def slideUp(issue, issueAuthor):
    """Slide up the grid"""
    grid = getGrid()

    changes = True
    score = 0
    lastCase = False

    while changes:
        changes = False
        for case in range(4):
            for line in range(4):

                if (lastCase is None) and (grid[line][case]) and (line != 0):
                    grid[line-1][case] = grid[line][case]
                    grid[line][case] = None
                    changes = True

                elif (lastCase) and (grid[line][case]) and (lastCase == grid[line][case]):
                    score += grid[line][case] * 2
                    grid[line-1][case] = grid[line][case] * 2
                    grid[line][case] = None
                    changes = True
                
                lastCase = grid[line][case]
                
    issueText = "You slided up!"
    endAction(grid, score, issue, issueAuthor, issueText, False)

def slideDown(issue, issueAuthor):
    """Slide down the grid"""
    grid = getGrid()

    changes = True
    score = 0
    lastCase = False

    while changes:
        changes = False
        for case in range(4):
            for line in range(3, -1, -1):

                if (lastCase is None) and (grid[line][case]) and (line != 3):
                    grid[line+1][case] = grid[line][case]
                    grid[line][case] = None
                    changes = True

                elif (lastCase) and (grid[line][case]) and (lastCase == grid[line][case]):
                    score += grid[line][case] * 2
                    grid[line+1][case] = grid[line][case] * 2
                    grid[line][case] = None
                    changes = True
                
                lastCase = grid[line][case]
                
    issueText = "You slided down!"
    endAction(grid, score, issue, issueAuthor, issueText, False)

# Utils

def getGrid():
    with open("Data/Games/current.json", "r", encoding="utf-8") as _grid:
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

def checkNextActions(grid):
    """
    return True : if there is one/+ possible action 
    return False : if there is no possible action
    """
    if any(None in line for line in grid): 
        return True

    # Check lines
    lastCase = False
    for line in range(4):
        for case in range(4):

            if case == 0:
                pass
            elif lastCase == grid[line][case]:
                return True
            lastCase = grid[line][case]
    
    # Check columns
    lastCase = False
    for case in range(4):
        for column in range(4):

            if case == 0:
                pass
            elif lastCase == grid[column][case]:
                return True
            lastCase = grid[column][case]
    
    return False

def updateRanking(issueAuthor):
    # Increase the player ranking
    with open("Data/topMoves.json", "r", encoding="utf-8") as _topMovesRead:
        topMovesRead = json.load(_topMovesRead)
        
        if issueAuthor in topMovesRead["topMoves"]:
            topMovesRead["topMoves"][f"{issueAuthor}"] += 1
        else:
            topMovesRead["topMoves"][f"{issueAuthor}"] = 1
    
    with open("Data/topMoves.json", "w", encoding="utf-8") as _topMovesWrite:
        topMovesRead2 = json.dumps(topMovesRead, indent=4, ensure_ascii=False) # Convert the object to json
        _topMovesWrite.write(topMovesRead2)

    # Update the ranking (makdown)
    # Change the actions
    readme =  open("README.md", "r", encoding="utf-8")
    readme = readme.read()
    readme = readme.split("<!-- 2048Ranking -->", 2)

    # Sort the ranking
    topMovesRead = topMovesRead["topMoves"]
    ranking = sorted(topMovesRead.items(), key=lambda t: t[1], reverse=True)

    readme[1] = "\n| Players | Actions |\n|---------------|:---------:|\n"
    for players in ranking[:10]:
        readme[1] += f"| [{players[0]}](https://github.com/{players[0][1:]}) | {players[1]} |\n"

    with open("README.md", "w", encoding="utf-8") as _readme:
        _readme.write("<!-- 2048Ranking -->".join(readme))

# End

def endAction(grid, score, issue, issueAuthor, issueText, isNewGame):
    """End the bot action"""

    if any(None in line for line in grid): 
        # Add a number in the grid
        if not isNewGame:
            addRandomNumber(grid)

    # Read current.json
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
        current["moves"].append(issueAuthor)

    # Check if the game is ended
    if checkNextActions(grid):
        # Generate the new game board
        generateGameBoard(grid, current["score"], current["bestScore"])
        
        # Update current.json
        with open("Data/Games/current.json", "w") as _current:
            currentFile = json.dumps(current, indent=4, ensure_ascii=False) # Convert the object to json
            _current.write(currentFile)

        updateRanking(issueAuthor)

        # Reply and close the issue
        issue.create_comment(f"{issueAuthor} {issueText}\nThe gameboard may take a few moments to refresh.\n\nAsk a friend to do the next action: [Share on Twitter...](https://twitter.com/intent/tweet?text=I%27m%20playing%202048%20on%20a%20GitHub%20Profile%20Readme!%20I%20just%20played.%20You%20have%20the%20action%20at%20https%3A%2F%2Fgithub.com%2FDarkempire78%2FDarkempire78)")
        issue.edit(state='closed', labels=["done"])

    # Game ended
    else:
        # Update current.json
        with open("Data/Games/current.json", "w") as _current:
            currentFile = json.dumps(current, indent=4, ensure_ascii=False) # Convert the object to json
            _current.write(currentFile)

        # Generate end gameboard
        generateEndGameBoard(grid, current["score"], current["bestScore"])

        # Change the actions
        readme =  open("README.md", "r")
        readme = readme.read()
        readme = readme.split("<!-- 2048GameActions -->", 2)

        readme[1] = "<a  href=\"https://github.com/Darkempire78/readme-2048/issues/new?title=2048|newGame&body=Just+push+'Submit+new+issue'.+You+don't+need+to+do+anything+else.\"><img src=\"Assets/newGame.png\"/></a>"

        with open("README.md", "w") as _readme:
            _readme.write("<!-- 2048GameActions -->".join(readme))

        updateRanking(issueAuthor)

        # Reply and close the issue
        players = list(set(current["moves"])) # Remove duplicates
        issue.create_comment(f"The game is over, well done! {players}")
        issue.edit(state='closed', labels=["done"])



if __name__ == "__main__":
	main()