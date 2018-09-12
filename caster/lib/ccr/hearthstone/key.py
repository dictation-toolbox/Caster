import pyautogui
import time
import sys

keyMap = {
  "face": [962, 204],
  "hero": [959, 817],
  "tap": [1133, 817],
  "end turn": [1561, 489],
  "hand 1": [623, 1057],
  "hand 2": [693, 1057],
  "hand 3": [756, 1057],
  "hand 4": [807, 1057],
  "hand 5": [862, 1057],
  "hand 6": [918, 1057],
  "hand 7": [971, 1057],
  "hand 8": [1031, 1057],
  "hand 9": [1090, 1057],
  "hand 10": [1162, 1057],
  "my 1": [541, 583],
  "my 2": [611, 583],
  "my 3": [680, 583],
  "my 4": [746, 583],
  "my 5": [811, 583],
  "my 6": [885, 583],
  "my 7": [955, 583],
  "my 8": [1022, 583],
  "my 9": [1094, 583],
  "my 10": [1162, 583],
  "my 11": [1239, 583],
  "my 12": [1310, 583],
  "my 13": [1400, 583],
  "his 1": [545, 390],
  "his 2": [613, 390],
  "his 3": [682, 390],
  "his 4": [743, 390],
  "his 5": [818, 390],
  "his 6": [884, 390],
  "his 7": [952, 390],
  "his 8": [1017, 390],
  "his 9": [1087, 390],
  "his 10": [1159, 390],
  "his 11": [1232, 390],
  "his 12": [1300, 390],
  "his 13": [1381, 390]
}

def my_minions(boardn):
    phrase = "my " + str(boardn)
    coords = keyMap[phrase]
    pyautogui.moveTo(coords[0], coords[1], 0.1)
    pyautogui.click(clicks=1, button='left')
    time.sleep(0.15)

def click_board():
    pyautogui.moveTo(keyMap["my 7"][0],keyMap["my 7"][1], 0.1)
    pyautogui.click(clicks=1, button='left')
    time.sleep(0.15)

def his_minions(boardn):
    phrase = "his " + str(boardn)
    coords = keyMap[phrase]
    pyautogui.moveTo(coords[0], coords[1], 0.1)
    pyautogui.click(clicks=1, button='left')
    time.sleep(0.15)

def hand(handn):
    phrase = "hand " + str(handn)
    coords = keyMap[phrase]
    pyautogui.moveTo(coords[0], coords[1], 0.1)
    pyautogui.click(clicks=1, button='left')
    time.sleep(0.15)

def face():
    phrase = "face"
    coords = keyMap[phrase]
    pyautogui.moveTo(coords[0], coords[1], 0.1)
    pyautogui.click(clicks=1, button='left')
    time.sleep(0.15)

def tap():
    phrase = "tap"
    coords = keyMap[phrase]
    pyautogui.moveTo(coords[0], coords[1], 0.1)
    pyautogui.click(clicks=1, button='left')
    time.sleep(0.15)

def hero():
    phrase = "hero"
    coords = keyMap[phrase]
    pyautogui.moveTo(coords[0], coords[1], 0.1)
    pyautogui.click(clicks=1, button='left')
    time.sleep(0.15)

def end_turn():
    phrase = "end turn"
    coords = keyMap[phrase]
    pyautogui.moveTo(coords[0], coords[1], 0.1)
    pyautogui.click(clicks=1, button='left')
    time.sleep(0.15)

def get_mouse_position():
    file = open("saved_mouse_positions.txt", "a+")
    pos = pyautogui.position()
    file.write("[" + str(pos[0]) + ", " + str(pos[1]) + "] \n")
