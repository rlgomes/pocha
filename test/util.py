"""
unit testing utilities
"""

from lxml import etree

from robber.matchers.base import Base
from robber import expect

def init():
    class XPath(Base):

        def matches(self):
            root = etree.fromstring(self.actual)
            return root.xpath(self.expected) is not None

        def failure_message(self):
            return 'Expected "%s" to match xpath "%s"' % (self.actual, self.expected)

    expect.register('xpath', XPath)
