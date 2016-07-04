"""
base pocha reporter
"""


class Reporter(object):

    def beforeTests(self, stdout):
        pass

    def beforeSuite(self, stdout, suite):
        pass

    def beforeTest(self, stdout, test):
        pass

    def afterTests(self, stdout):
        pass

    def afterSuite(self, stdout, suite):
        pass

    def afterTest(self, stdout, test):
        pass
