# coding: utf-8
import unittest

import main
import paths


class Test(unittest.TestCase):

    def test(self):
        for ps, sp in zip(main.main(), paths.paths):
            self.assertEqual(ps, sp)
