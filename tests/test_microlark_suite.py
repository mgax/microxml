from StringIO import StringIO
import pprint
import py.path
import lxml.etree
import microxml

data_path = py.path.local(__file__).dirpath()

def test_well_formed():
    microxml.DEBUG = True
    for case_file in data_path.join('wf').listdir():
        yield check_well_formed, case_file


def handle_events(event_iter):
    for element in event_iter:
        yield 'tag', element.tag
        for name, value in element.attrib.iteritems():
            yield 'attrib', name, value


def check_well_formed(case_file):
    data = case_file.read()
    etree_events = list(handle_events(lxml.etree.fromstring(data).iter("*")))
    microxml_events = list(handle_events(microxml.fromstring(data)))
    try:
        assert etree_events == microxml_events
    except:
        print "file:", str(case_file), repr(case_file.read())
        print "etree output:"
        pprint.pprint(etree_events)
        print "microxml output:"
        pprint.pprint(microxml_events)
        raise
