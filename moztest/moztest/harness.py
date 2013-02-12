import mozrunner

class MozTest(object):
    """abstract base class for test harnesses"""
    runner = mozrunner.FirefoxRunner

    def __init__(self):
        pass

    def run(self, *tests):
        pass

