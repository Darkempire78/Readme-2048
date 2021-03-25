from PIL import Image, ImageDraw, ImageFont

def generateGameBoard(grid):   
    
    gameboard = Image.open("Assets/background.png")
    
    # Add numbers
    for line in range(4):
        for case in range(4):
            if grid[line][case] != None:
                coordinates = gridToCoordinates(line, case)
                # Open the case image
                block = Image.open(f"Assets/{grid[line][case]}.png").convert('RGBA')
                # Past
                gameboard.paste(block, coordinates, block)
    
    # Add score
    font = ImageFont.truetype(font= "Utils/arial.ttf", size= 15)
    draw = ImageDraw.Draw(gameboard)
    draw.text((599, 808), (91, 165), "123456789", (255,255,255), font=font, align="center")

    
    gameboard.save("Data/gameboard.png")


def gridToCoordinates(line, case):
    coordinates = [
        [(58, 291), (300, 291), (544, 291), (786, 291)],
        [(58, 539), (300, 539), (544, 539), (786, 539)],
        [(58, 775), (300, 775), (544, 775), (786, 775)],
        [(58, 1023), (300, 1023), (544, 1023), (786, 1023)]
    ]

    return coordinates[line][case]   