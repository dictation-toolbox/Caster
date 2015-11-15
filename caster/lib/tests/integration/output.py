import unittest

from caster.lib.tests.integration.testutils import get_playback, get_output


class TestOutput(unittest.TestCase):

    def test_formatting(self):
        get_playback(["set format laws gum bow", "format some words"]).execute()
        output = get_output()
        self.assertEqual(output, "somewords")
        
        get_playback(["snake bow some words"]).execute()
        output = get_output()
        self.assertEqual(output, "some_words")
        
        get_playback(["set format Gerrish gum bow", "format some words"]).execute()
        output = get_output()
        self.assertEqual(output, "someWords")
    
    
    
    

    