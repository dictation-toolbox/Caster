from dragonfly import Mouse
import time
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
    time.sleep(0.15)
    phrase = "my " + str(boardn)
    Mouse("[" + str(keyMap[phrase][0]) + ", " + str(keyMap[phrase][1]) + "], left").execute()
    time.sleep(0.15)

def click_board():
    time.sleep(0.15)
    phrase = "my 7"
    Mouse("[" + str(keyMap[phrase][0]) + ", " + str(keyMap[phrase][1]) + "], left").execute()
    time.sleep(0.15)

def his_minions(boardn):
    time.sleep(0.15)
    phrase = "his " + str(boardn)
    Mouse("[" + str(keyMap[phrase][0]) + ", " + str(keyMap[phrase][1]) + "], left").execute()
    time.sleep(0.15)

def hand(handn):
    time.sleep(0.15)
    phrase = "hand " + str(handn)
    Mouse("[" + str(keyMap[phrase][0]) + ", " + str(keyMap[phrase][1]) + "], left").execute()
    time.sleep(0.15)

def face():
    time.sleep(0.15)
    phrase = "face"
    Mouse("[" + str(keyMap[phrase][0]) + ", " + str(keyMap[phrase][1]) + "], left").execute()
    time.sleep(0.15)

def tap():
    time.sleep(0.15)
    phrase = "tap"
    Mouse("[" + str(keyMap[phrase][0]) + ", " + str(keyMap[phrase][1]) + "], left").execute()
    time.sleep(0.15)

def hero():
    time.sleep(0.15)
    phrase = "hero"
    Mouse("[" + str(keyMap[phrase][0]) + ", " + str(keyMap[phrase][1]) + "], left").execute()
    time.sleep(0.15)

def end_turn():
    time.sleep(0.15)
    phrase = "end turn"
    Mouse("[" + str(keyMap[phrase][0]) + ", " + str(keyMap[phrase][1]) + "], left").execute()
    time.sleep(0.15)
