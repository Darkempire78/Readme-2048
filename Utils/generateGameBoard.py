from PIL import Image, ImageDraw, ImageFont

def generateGameBoard(grid, score, bestScore):   
    
    gameboard = Image.open("Assets/background.png").convert('RGBA')
    
    # Add numbers
    for line in range(4):
        for case in range(4):
            if grid[line][case] != None:
                coordinates = gridToCoordinates(line, case)
                # Open the case image
                block = Image.open(f"Assets/{grid[line][case]}.png").convert('RGBA')
                # Past
                gameboard.paste(block, coordinates, block)
    
    # Add the score
    scoreImage = Image.open(f"Assets/score.png").convert('RGBA')
    message = str(score)
    myFont = ImageFont.truetype(font= "Utils/arial.ttf", size= 60)
    draw = ImageDraw.Draw(scoreImage)
    w, h = draw.textsize(message, font=myFont)
    W, H = scoreImage.size
    draw.text(((W-w)/2, (H-h+40)/2), message, (255,255,255), font=myFont)
    gameboard.paste(scoreImage, (599, 37), scoreImage)

    # Add the bestScore
    scoreImage = Image.open(f"Assets/best.png").convert('RGBA')
    message = str(bestScore)
    myFont = ImageFont.truetype(font= "Utils/arial.ttf", size= 60)
    draw = ImageDraw.Draw(scoreImage)
    w, h = draw.textsize(message, font=myFont)
    W, H = scoreImage.size
    draw.text(((W-w)/2, (H-h+40)/2), message, (255,255,255), font=myFont)
    gameboard.paste(scoreImage, (820, 37), scoreImage)
    
    # (599, 808), (91, 165)
    # Center => https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil

    
    gameboard.save("Data/gameboard.png")


def gridToCoordinates(line, case):
    coordinates = [
        [(58, 291), (300, 291), (544, 291), (786, 291)],
        [(58, 539), (300, 539), (544, 539), (786, 539)],
        [(58, 775), (300, 775), (544, 775), (786, 775)],
        [(58, 1023), (300, 1023), (544, 1023), (786, 1023)]
    ]

    return coordinates[line][case]   