# coding: utf-8
"""
xunit pocha reporter
"""

import time
import traceback

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

from pocha.reporters.base import Reporter


# taken from https://gist.github.com/zlalanne/5711847
def CDATA(text=None):
    element = ElementTree.Element('![CDATA[')
    element.text = text
    return element

ElementTree._original_serialize_xml = ElementTree._serialize_xml

def _serialize_xml(write, elem, encoding, qnames, namespaces):
    if elem.tag == '![CDATA[':
        write('<%s%s]]>' % (elem.tag, elem.text))
        return

    return ElementTree._original_serialize_xml(write, elem, encoding, qnames, namespaces)

ElementTree._serialize_xml = ElementTree._serialize['xml'] = _serialize_xml

# taken from https://pymotw.com/2/xml/etree/ElementTree/create.html
def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')

class XUnitReporter(Reporter):

    def __init__(self):
        self.start = None
        self.passing = 0
        self.failing = 0
        self.skipping = 0
        self.total = 0
        self.testsuite = Element('testsuite')
        self.test_start = 0
        self.suite_stack = []

    def afterTests(self, stdout):
        self.testsuite.set('name', 'Pocha Tests')
        self.testsuite.set('tests', str(self.total))
        self.testsuite.set('errors', '0')
        self.testsuite.set('failures', str(self.failing))
        self.testsuite.set('skip', str(self.skipping))
        stdout.write(prettify(self.testsuite))

    def beforeSuite(self, stdout, suite):
        self.suite_stack.append(suite.name)

    def afterSuite(self, stdout, suite):
        self.suite_stack.pop(-1)

    def beforeTest(self, stdout, test):
        self.test_start = time.time()

    def afterTest(self, stdout, test):
        duration = time.time() - self.test_start
        self.total += 1

        testcase = SubElement(self.testsuite, 'testcase', {
            'classname': ' '.join(self.suite_stack),
            'name': test.name,
            'time': '%.3f' % duration
        })

        if test.status == 'pass':
            self.passing += 1

        if test.status == 'skip':
            skipped = SubElement(testcase, 'skipped')
            self.skipping += 1

        elif test.status == 'fail':
            error = SubElement(testcase, 'error')
            error.append(CDATA('\n'.join(traceback.format_exception(*test.exc_info))))
            self.failing += 1

        stdout.flush()
