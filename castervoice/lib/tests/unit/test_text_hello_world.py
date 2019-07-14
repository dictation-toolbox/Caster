import unittest

import os, time
from pywinauto.application import Application
from dragonfly import Key, Text

class TestHelloWord(unittest.TestCase):
    def setUp(self):
        x = 1

    def test_hw(self):
        test_out_path = os.path.abspath(os.path.join(os.getcwd(), "test_out.txt"))
        if os.path.exists(test_out_path):
            os.remove(test_out_path)
        open(test_out_path, 'a').close()

        app = Application().start("notepad.exe " + test_out_path)

        Text("Hello world").execute()
        time.sleep(0.1)
        app.Notepad.type_keys("^S")
        while not os.path.exists(os.path.abspath(test_out_path)):
            time.sleep(0.1)
        with open(test_out_path, "r") as file:
            self.assertEqual(file.read(), "Hello world")
        app.kill()
        if os.path.exists(test_out_path):
            os.remove(test_out_path)

if __name__ == '__main__':
    unittest.main()
