# BFS, DFS, and A* Pathfinding Visualizer

## Description

This project is a simple Python application that demonstrates three pathfinding algorithms: Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search.

The program allows the user to select an algorithm and visualize how it searches for a path from the starting point to the goal.

## Algorithms

### BFS (Breadth-First Search)

BFS explores the grid level by level. It can find the shortest path when all movements have the same cost.

### DFS (Depth-First Search)

DFS explores one path as deeply as possible before going back and trying another path.

### A* (A-Star)

A* uses the distance traveled and an estimated distance to the goal to determine which cell to explore next.

## Features

- BFS pathfinding
- DFS pathfinding
- A* pathfinding
- Interactive grid
- Visual representation of the search process
- Displays the path from start to goal

## Requirements

- Python 3.x
- Tkinter

## How to Run

1. Open the `bfs_dfs_astar` folder in VS Code.
2. Open the terminal.
3. Run:

```bash
python pathfinder.py