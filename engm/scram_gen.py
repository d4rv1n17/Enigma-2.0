import random


def generate_scramble(cube_type, lenght):
    
    if cube_type == "2x2x2":
        moves = ["U", "D", "F", "B", "R", "L"]
        dir = ["", "'", "2"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    if cube_type == "3x3x3":
        moves = ["U", "D", "F", "B", "R", "L"]
        dir = ["", "'", "2"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    if cube_type == "4x4x4":
        moves = ["U", "D", "F", "B", "R", "L"]
        dir = ["", "'", "2", "w", "w2", "w'"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    if cube_type == "5x5x5":
        moves = ["U", "D", "F", "B", "R", "L"]
        dir = ["", "'", "2", "w", "w2", "w'"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    if cube_type == "6x6x6":
        moves = ["U", "D", "F", "B", "R", "L", "3U", "3D", "3F", "3B", "3R", "3L"]
        dir = ["", "'", "2", "w", "w2", "w'"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    if cube_type == "7x7x7":
        moves = ["U", "D", "F", "B", "R", "L", "3U", "3D", "3F", "3B", "3R", "3L"]
        dir = ["", "'", "2", "w", "w2", "w'"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    if cube_type == "pyraminx":
        moves = ["U", "B", "R", "L", "u", "b", "r", "l"]
        dir = ["", "'"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    if cube_type == "skewb":
        moves = ["U", "B", "R", "L"]
        dir = ["", "'"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    if cube_type == "megaminx":
        moves = ["R", "D", "U"]
        dir = ["--", "'", "++"]

        s = valid([[random.choice(moves), random.choice(dir)] for x in range(lenght)])

    
    return ''.join(str(s[x][0]) + str(s[x][1]) + ' ' for x in range(len(s)))


def valid(ar):
    moves = ["U", "D", "F", "B", "R", "L"]
    dir = ["", "'", "2"]
    for x in range(1, len(ar)):
         while ar[x][0] == ar[x-1][0]:
             ar[x][0] = random.choice(moves)
    for x in range(2, len(ar)):
        while ar[x][0] == ar[x-2][0] or ar[x][0] == ar[x-1][0]:
             ar[x][0] = random.choice(moves)
    return ar
