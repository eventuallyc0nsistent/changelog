from unittest import TestCase
from changelog.command_line import init_argparser

class TestCmdLine(TestCase):

    def test_argparser(self):
        parser = init_argparser()
        print parser
        self.assertTrue(False)
