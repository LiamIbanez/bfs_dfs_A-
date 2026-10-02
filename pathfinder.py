import tkinter as tk
from collections import deque
import heapq
import random


ROWS = 12
COLS = 18
CELL = 40

START = (5, 0)
GOAL = (10, 14)

algorithm = "BFS"

walls = set()
visited = []
final_path = []

visit_index = 0
path_index = 0
running = False




def get_neighbors(node):
    row, col = node

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for dr, dc in directions:
        new_node = (row + dr, col + dc)

        if 0 <= new_node[0] < ROWS and 0 <= new_node[1] < COLS:
            if new_node not in walls:
                neighbors.append(new_node)

    return neighbors


def make_path(parent):
    if GOAL not in parent:
        return []

    path = []
    current = GOAL

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def bfs():
    queue = deque([START])
    parent = {START: None}
    order = []

    while queue:
        current = queue.popleft()

        if current in order:
            continue

        order.append(current)

        if current == GOAL:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    return order, make_path(parent)


def dfs():
    stack = [START]
    parent = {START: None}
    order = []

    while stack:
        current = stack.pop()

        if current in order:
            continue

        order.append(current)

        if current == GOAL:
            break

        for neighbor in reversed(get_neighbors(current)):
            if neighbor not in parent:
                parent[neighbor] = current
                stack.append(neighbor)

    return order, make_path(parent)


def heuristic(node):
    r1, c1 = node
    r2, c2 = GOAL

    return abs(r1 - r2) + abs(c1 - c2)


def astar():
    queue = [(0, START)]
    parent = {START: None}
    cost = {START: 0}
    order = []

    while queue:
        _, current = heapq.heappop(queue)

        if current in order:
            continue

        order.append(current)

        if current == GOAL:
            break

        for neighbor in get_neighbors(current):
            new_cost = cost[current] + 1

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current

                priority = new_cost + heuristic(neighbor)

                heapq.heappush(
                    queue,
                    (priority, neighbor)
                )

    return order, make_path(parent)




root = tk.Tk()
root.title("BFS, DFS and A* Pathfinding Visualizer")
root.configure(bg="#111827")




def reset_search():
    global visited, final_path
    global visit_index, path_index, running

    visited = []
    final_path = []
    visit_index = 0
    path_index = 0
    running = False

    status.config(
        text=f"{algorithm} | Start: S | Goal: G"
    )

    draw_grid()


def select_algorithm(name):
    global algorithm

    algorithm = name

    reset_search()

    bfs_button.config(bg="#26334a")
    dfs_button.config(bg="#26334a")
    astar_button.config(bg="#26334a")

    if name == "BFS":
        bfs_button.config(bg="#9b8cff")

    elif name == "DFS":
        dfs_button.config(bg="#9b8cff")

    else:
        astar_button.config(bg="#9b8cff")


def run_search():
    global visited, final_path
    global visit_index, path_index, running

    if running:
        return

    reset_search()

    if algorithm == "BFS":
        visited, final_path = bfs()

    elif algorithm == "DFS":
        visited, final_path = dfs()

    else:
        visited, final_path = astar()

    running = True
    animate()


def animate():
    global visit_index, path_index, running

    # Show search quickly
    if visit_index < len(visited):

        visit_index = min(
            visit_index + 10,
            len(visited)
        )

        draw_grid()

        root.after(10, animate)

        return

    # Show final path quickly
    if path_index < len(final_path):

        path_index = min(
            path_index + 5,
            len(final_path)
        )

        draw_grid()

        root.after(10, animate)

        return

    running = False

    status.config(
        text=f"{algorithm} Complete | Path: {len(final_path)} cells"
    )


def step_search():
    global visited, final_path
    global visit_index, path_index

    if not visited:

        if algorithm == "BFS":
            visited, final_path = bfs()

        elif algorithm == "DFS":
            visited, final_path = dfs()

        else:
            visited, final_path = astar()

    if visit_index < len(visited):
        visit_index = min(
            visit_index + 5,
            len(visited)
        )

    elif path_index < len(final_path):
        path_index = min(
            path_index + 2,
            len(final_path)
        )

    draw_grid()


def random_walls():
    walls.clear()

    for row in range(ROWS):
        for col in range(COLS):

            position = (row, col)

            if position == START or position == GOAL:
                continue

            if random.random() < 0.20:
                walls.add(position)

    reset_search()


def clear_walls():
    walls.clear()
    reset_search()


def click_grid(event):
    row = event.y // CELL
    col = event.x // CELL

    position = (row, col)

    if position == START or position == GOAL:
        return

    if position in walls:
        walls.remove(position)
    else:
        walls.add(position)

    reset_search()




def draw_grid():

    canvas.delete("all")

    for row in range(ROWS):
        for col in range(COLS):

            position = (row, col)

            x1 = col * CELL
            y1 = row * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            if position == START:
                color = "#22c99a"

            elif position == GOAL:
                color = "#9b8cff"

            elif position in final_path[:path_index]:
                color = "#f2b01e"

            elif position in visited[:visit_index]:
                color = "#ff6685"

            elif position in walls:
                color = "#182235"

            else:
                color = "#315f78"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="#263c4d"
            )

    # START
    sr, sc = START

    canvas.create_text(
        sc * CELL + CELL / 2,
        sr * CELL + CELL / 2,
        text="S",
        fill="white",
        font=("Arial", 20, "bold")
    )

    # GOAL
    gr, gc = GOAL

    canvas.create_text(
        gc * CELL + CELL / 2,
        gr * CELL + CELL / 2,
        text="G",
        fill="white",
        font=("Arial", 20, "bold")
    )




title = tk.Label(
    root,
    text="BFS / DFS / A* PATHFINDING",
    font=("Arial", 20, "bold"),
    bg="#111827",
    fg="white"
)

title.pack(pady=10)


# Algorithm buttons
top = tk.Frame(root, bg="#111827")
top.pack(pady=5)


bfs_button = tk.Button(
    top,
    text="BFS",
    width=8,
    font=("Arial", 11, "bold"),
    bg="#9b8cff",
    command=lambda: select_algorithm("BFS")
)

bfs_button.pack(side="left", padx=3)


dfs_button = tk.Button(
    top,
    text="DFS",
    width=8,
    font=("Arial", 11, "bold"),
    bg="#26334a",
    fg="white",
    command=lambda: select_algorithm("DFS")
)

dfs_button.pack(side="left", padx=3)


astar_button = tk.Button(
    top,
    text="A*",
    width=8,
    font=("Arial", 11, "bold"),
    bg="#26334a",
    fg="white",
    command=lambda: select_algorithm("A*")
)

astar_button.pack(side="left", padx=3)


# Control buttons
controls = tk.Frame(root, bg="#111827")
controls.pack(pady=8)


tk.Button(
    controls,
    text="Run",
    width=10,
    command=lambda: run_search()
).pack(side="left", padx=4)


tk.Button(
    controls,
    text="Step",
    width=10,
    command=lambda: step_search()
).pack(side="left", padx=4)


tk.Button(
    controls,
    text="Reset Search",
    width=12,
    command=lambda: reset_search()
).pack(side="left", padx=4)


tk.Button(
    controls,
    text="Random Walls",
    width=12,
    command=lambda: random_walls()
).pack(side="left", padx=4)


tk.Button(
    controls,
    text="Clear Walls",
    width=12,
    command=lambda: clear_walls()
).pack(side="left", padx=4)


# Canvas
canvas = tk.Canvas(
    root,
    width=COLS * CELL,
    height=ROWS * CELL,
    bg="#315f78",
    highlightthickness=0
)

canvas.pack(pady=12)

canvas.bind(
    "<Button-1>",
    click_grid
)


# Status
status = tk.Label(
    root,
    text="BFS | Start: S | Goal: G",
    font=("Arial", 11, "bold"),
    bg="#111827",
    fg="white"
)

status.pack(pady=5)


# Start
draw_grid()

root.mainloop()