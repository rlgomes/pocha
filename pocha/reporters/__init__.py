"""
"""

from dot import DotReporter
from spec import SpecReporter
from xunit import XUnitReporter

_REPORTERS = {
    'dot': DotReporter,
    'spec': SpecReporter,
    'xunit': XUnitReporter
}

def get_reporter(name):

    if name not in _REPORTERS.keys():
        raise Exception('reporter "%s" not found' % name)

    return _REPORTERS[name]
