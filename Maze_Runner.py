#This was my side project, i worked on it in the sandbox and not in creative task section so it allowed me to write extra functions
#but then when i switched it to my main project i forgot that it wouldn't work and i just realized.
#Sorry please give me another chance


app.background = 'black'

# Initialize app properties
app.keys_pressed = []  # A list to track currently pressed keys
app.game_active = True  # Boolean to control the game state (True = game is running)

# MAZE DEFINITION:v rows of maze layout using # as walls because it's easier to convert it rather than drawing it
define_maze = [
    '####################',
    '#                 ##',
    '# ####### ######  ##',
    '#            #     #',
    '###  ##### #########',
    '#    #             #',
    '################ ###',
    '#                 ##',
    '##  #######  ###  ##',
    '#        #         #',
    '#######  ###########',
    '#                  #',
    '###############  ###',
    '##############  ####',
    '#############  #####',
    '############  ######',
    '###########  #######',
    '##########  ########',
    '########## #########',
    '##########          '
]

# WALL CREATION: Create white rectangles where '#' is found in define_maze
walls = []
for y, row in enumerate(define_maze):
    for x, char in enumerate(row):
        if char == '#':
            walls.append(Rect(x*20, y*20, 20, 20, fill='white'))

# PLAYER SETUP: Blue square starting near the top-left
player = Rect(23, 23, 15, 15, fill='blue')

# GOAL SETUP: Green square near the bottom-right
finish = Rect(380, 380, 20, 20, fill='green')

# ENEMY (Ghost) SETUP: Red square that chases the player
ghost = Rect(23, 100, 15, 15, fill='red')
ghost_speed = 0.5  # Speed for ghost

# COIN SETUP: Gold coins to collect and slow down ghost
coins = [
    Rect(260, 25, 10, 10, fill='gold'),
    Rect(300, 185, 10, 10, fill='gold'),
    Rect(60, 225, 10, 10, fill='gold')
]

# When a key is pressed, add it to keys_pressed if it's not already there
def onKeyPress(key):
    if key not in app.keys_pressed:
        app.keys_pressed.append(key)

# When a key is released, remove it from keys_pressed
def onKeyRelease(key):
    if key in app.keys_pressed:
        app.keys_pressed.remove(key)

# Check if the ghost is is hitting any wall
def check_wall_collision(rect):
    for wall in walls:
        if rect.hitsShape(wall):
            return True
    return False

# GHOST MOVEMENT: Move ghost toward player using Breadth-First Search. Link: https://www.hackerrank.com/challenges/bfsshortreach/problem
# Converts maze to a grid and finds shortest path from ghost to player
# Moves ghost one step along that path

def move_ghost_toward_player():
    maze_grid = [list(row) for row in define_maze]  # Convert each row into a list of characters
    start = (int(ghost.centerY / 20), int(ghost.centerX / 20))  # Ghost's position in grid coordinates
    goal = (int(player.centerY / 20), int(player.centerX / 20))  # Player's position in grid coordinates

    if start == goal:
        return

    queue = [start]  # Queue for BFS
    came_from = {start: None}  # Tracks path

    while queue:
        current = queue.pop(0)

        if current == goal:
            break

        # Try moving in four directions
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if (0 <= neighbor[0] < len(maze_grid) and
                0 <= neighbor[1] < len(maze_grid[0]) and
                maze_grid[neighbor[0]][neighbor[1]] == ' ' and
                neighbor not in came_from):
                queue.append(neighbor)
                came_from[neighbor] = current

    path = []
    current = goal
    while current and current != start:
        path.append(current)
        current = came_from[current]

    path.reverse()  # Reverse to get path from start to goal

    if path:
        next_step = path[0]
        # Move ghost toward the center of the next grid cell
        dx = (next_step[1] * 20 + 10) - ghost.centerX
        dy = (next_step[0] * 20 + 10) - ghost.centerY

        ghost.centerX += ghost_speed * dx / abs(dx) if dx != 0 else 0
        ghost.centerY += ghost_speed * dy / abs(dy) if dy != 0 else 0

# MAIN LOOP FUNCTION: Runs every frame
speed = 1  # Player speed

def onStep():
    global ghost_speed
    if not app.game_active:
        return

    dx = 0
    dy = 0

    # PLAYER MOVEMENT BASED ON KEY PRESS
    if 'up' in app.keys_pressed:
        dy -= speed
    if 'down' in app.keys_pressed:
        dy += speed
    if 'left' in app.keys_pressed:
        dx -= speed
    if 'right' in app.keys_pressed:
        dx += speed

    # MOVE PLAYER ALONG X AND CHECK COLLISION
    player.centerX += dx
    player.centerY += dy
    if check_wall_collision(player):
        app.game_active = False
        Label('Game Over! You hit a wall.', 200, 200, size=30, fill='red', bold=True)
        return

    # MOVE PLAYER ALONG Y AND CHECK COLLISION
    
  

    # CHECK IF PLAYER REACHED FINISH
    if player.hitsShape(finish):
        app.game_active = False
        Label('You Win!', 200, 200, size=50, fill='yellow', bold=True)
        return

    # MOVE THE GHOST
    move_ghost_toward_player()

    # CHECK IF GHOST CAUGHT PLAYER
    if ghost.hitsShape(player):
        app.game_active = False
        Label('Game Over! The ghost got you.', 200, 200, size=30, fill='red', bold=True)
        return

    for coin in coins[:]:  # Iterate over a copy to avoid modifying while iterating
        if player.hitsShape(coin):
            coins.remove(coin)
            coin.visible = False
            ghost_speed = max(ghost_speed - 0.1, 0.1)  # Reduce ghost speed, but not below 0.1
            