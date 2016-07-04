"""
reporters register module
"""

from pocha.reporters.dot import DotReporter
from pocha.reporters.spec import SpecReporter
from pocha.reporters.xunit import XUnitReporter

_REPORTERS = {
    'dot': DotReporter,
    'spec': SpecReporter,
    'xunit': XUnitReporter
}

def get_reporter(name):

    if name not in _REPORTERS.keys():
        raise Exception('reporter "%s" not found' % name)

    return _REPORTERS[name]
