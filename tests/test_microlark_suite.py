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
    root_ns = None
    for element in event_iter:
        if getattr(element, 'getparent', lambda: 'x')() is None:
            nsmap = element.nsmap
            if None in nsmap:
                root_ns = nsmap[None]
        else:
            nsmap = {}

        tag = element.tag
        if root_ns is not None:
            prefix = '{%s}' % root_ns
            assert tag.startswith(prefix)
            tag = tag[len(prefix):]
        yield 'tag', tag

        attrib = dict(element.attrib)
        for ns_name in nsmap:
            attr_name = 'xmlns'
            if ns_name is not None:
                attr_name += ':' + ns_name
            attrib[attr_name] = nsmap[ns_name]
        for attr_name in sorted(attrib):
            yield 'attrib', attr_name, attrib[attr_name]


def check_well_formed(case_file):
    data = case_file.read()
    microxml_events = list(handle_events(microxml.fromstring(data)))
    etree_events = list(handle_events(lxml.etree.fromstring(data).iter("*")))
    try:
        assert microxml_events == etree_events
    except:
        print "file:", str(case_file), repr(case_file.read())
        print "microxml output:"
        pprint.pprint(microxml_events)
        print "etree output:"
        pprint.pprint(etree_events)
        raise
