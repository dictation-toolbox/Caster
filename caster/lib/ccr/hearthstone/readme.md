A caster module which allows Hearthstone (the PC game) to be played entirely by voice. It has two elements:
* A screen overlay linking the positions of the cards in game to the commands which need to be spoken to click on them.
* A CCR module with the grammar and functions in.

An overlay PNG (from this project: https://github.com/wujerry573/TwitchPlaysHearthstone) is included, but only for 1080p resolution. I'm using this utility to lay it over my screen: http://customdesktoplogo.wikidot.com/download.

It's pretty hacky at the moment, but seems to be working in the few tests I've done. Long-term, ideally it would detect the size and position of the Hearthstone window, calculate (or recall) the positions, render and display the overlay, and update the commands all from within python.

![hs](https://user-images.githubusercontent.com/42875462/45365694-ff8e2500-b5d4-11e8-8fa9-ac04b3075231.jpg)