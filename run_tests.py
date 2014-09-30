#!/usr/bin/env python3
import unittest
from tests import *

testsuite = unittest.TestLoader().discover('tests/')
unittest.TextTestRunner(verbosity=1).run(testsuite)
