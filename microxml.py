from StringIO import StringIO

DEBUG = False


class Element(object):

    def __init__(self, tag, **attrib):
        self.tag = tag
        self.attrib = attrib


def parse_stream(stream):
    """ Pull parser that yields a succession of elements. """

    # constants
    WHITESPACE = ' \n\t'
    INDATA = 1
    LT = 2
    INENAME = 3
    INTAG = 4
    INANAME = 5
    #ANAME = 6
    EQ = 7
    #SQUOTE = 8
    DQUOTE = 9
    ATTR = 10

    if DEBUG:
        state_name = {
            1:  'INDATA',
            2:  'LT',
            3:  'INENAME',
            4:  'INTAG',
            5:  'INANAME',
            6:  'ANAME',
            7:  'EQ',
            8:  'SQUOTE',
            9:  'DQUOTE',
            10: 'ATTR',
        }

    # state of parser
    state = INDATA

    while True:
        ch = stream.read(1)
        if DEBUG:
            print repr(ch), state_name[state]

        if ch == "":
            return

        elif state == INDATA:
            if ch == '<':
                state = LT
                tag = ""

        elif state == LT:
            state = INENAME
            tag += ch

        elif state == INENAME:
            if ch == '>':
                state = INDATA
                yield Element(tag)

            elif ch in WHITESPACE:
                state = INTAG
                attrib = {}

            else:
                tag += ch

        elif state == INTAG:
            if ch in WHITESPACE:
                pass

            elif ch == '/':
                pass

            elif ch == '>':
                yield Element(tag, **attrib)

            else:
                state = INANAME
                name = ch

        elif state == INANAME:
            if ch == '=':
                state = EQ

            else:
                name += ch

#        elif state == ANAME:
#            if ch == '=':
#                state = EQ

        elif state == EQ:
            if ch == '"':
                state = DQUOTE
                value = ""

        elif state == DQUOTE:
            if ch == '"':
                state = ATTR
                attrib[name] = value

            else:
                value += ch

        elif state == ATTR:
            if ch == ' ':
                state = INTAG

            elif ch == '>':
                state = INDATA
                yield Element(tag, **attrib)


def fromstring(s):
    return parse_stream(StringIO(s))
