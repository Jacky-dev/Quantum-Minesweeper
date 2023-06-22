import random
from qiskit import *
from qiskit.visualization import plot_histogram
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import math
import numpy as np
import random
import json
import requests

def send_to_the_quokka(circuit):
  req_str_qasm = 'http://quokka1.quokkacomputing.com/qsim/qasm' # the URL listening for qasm files
  qasmFile = circuit.qasm() # create a qasm file from our circuit

  print(qasmFile)

  data = {
    'script': qasmFile,
    'count': 1
    }
  result = requests.post(req_str_qasm, json=data)
  json_obj = json.loads(result.content)

  return ''.join(map(str, json_obj['result']['c'][0])) # convert to a string of binary values
class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.visible_board = [["-" for _ in range(width)] for _ in range(height)]
        self.mines = set()
        self.is_game_over = False

    def place_mines(self, start_x, start_y):
        num_placed = 0
        while num_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) != (start_x, start_y) and (x, y) not in self.mines:
                self.mines.add((x, y))
                num_placed += 1

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) in self.mines:
                        count += 1
        return count

    def reveal(self, x, y):
        if (x, y) in self.mines:
            self.is_game_over = True
            self.visible_board[x][y] = "X"
        else:
            count = self.count_adjacent_mines(x, y)
            self.visible_board[x][y] = str(count)
            if count == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.visible_board[nx][ny] == "-":
                                self.reveal(nx, ny)

    def handle_click(self, x, y):
        if not self.is_game_over:
            self.reveal(x, y)
            self.update_board()

            if self.is_game_over:
                messagebox.showinfo("Game Over", "You hit a mine! Game Over.")

    def update_board(self):
        for i in range(self.height):
            for j in range(self.width):
                self.buttons[i][j].configure(text=self.visible_board[i][j])

    def create_buttons(self):
        self.buttons = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                button = tk.Button(
                    self.root,
                    text="-",
                    width=4,
                    command=lambda x=i, y=j: self.handle_click(x, y)
                )
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.create_buttons()

    def play(self):
        self.create_window()
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)
        self.place_mines(start_x, start_y)
        tk.mainloop()

# Usage example
width = 12
height = 12
num_mines = 10

game = Minesweeper(width, height, num_mines)
game.play()
