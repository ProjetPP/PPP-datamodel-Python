#!/usr/bin/env python3
import unittest

testsuite = unittest.TestLoader().discover('tests/')
unittest.TextTestRunner(verbosity=1).run(testsuite)
