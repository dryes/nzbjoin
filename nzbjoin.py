#!/usr/bin/python2

# Author: Joseph Wiseman <joswiseman@cock.li>
# URL: https://github.com/d2yes/nzbjoin/

import argparse,cgi,os,sys
from datetime import date
from pynzb import nzb_parser


def init_argparse():
    parser = argparse.ArgumentParser(
        description='join multiple nzb files together.',
        usage=os.path.basename(sys.argv[0]) + ' [--opts] file1.nzb file2.nzb ...'
    )

    parser.add_argument(
        'input',
        nargs='*',
        help='nzb files',
        default=''
    )
    parser.add_argument(
        '--output', '-o',
        help='output to specific file -- default behaviour overwrites first input nzb',
        default=None
    )
    parser.add_argument(
        '--delete', '-d',
        action='store_true',
        help='delete input nzb files',
        default=False
    )

    args = parser.parse_args()

    return vars(args)

def main(nzbfile):
    try:
        nzb = open(nzbfile, 'r').read()
        nzbparse = nzb_parser.parse(nzb)
    except:
        return False

    content = ''
    for f in nzbparse:
        unixdate = str(((f.date.toordinal() - date(1970, 1, 1).toordinal()) * 24*60*60))
        content += '<file poster="%s" date="%s" subject="%s">\n' % \
            (cgi.escape(f.poster, True), unixdate, cgi.escape(f.subject, True))

        content += '\t<groups>\n'
        for g in f.groups:
            content += '\t\t<group>%s</group>\n' % (g)
        content += '\t</groups>\n'

        content += '\t<segments>\n'
        for s in f.segments:
            content += '\t\t<segment bytes="%s" number="%s">%s</segment>\n' % \
                (str(s.bytes), str(s.number), s.message_id)
        content += '\t</segments>\n'

        content += '</file>\n'

    return content

if __name__ == '__main__':
    content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    content += '<!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 1.1//EN" "http://www.newzbin.com/DTD/nzb/nzb-1.1.dtd">\n'
    content += '<nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">\n'

    args = init_argparse()

    if len(args['input']) == 0:
        sys.exit(0)

    for f in args['input']:
        nzbcontent = main(f)
        if nzbcontent == False:
            print('error processing: %s.' % f)
            continue
        content += nzbcontent

    content += '</nzb>'

    if args['output'] is not None:
        output = args['output']
    else:
        output = args['input'][0]

    outputdir = os.path.dirname(output)
    if not os.path.isdir(outputdir) and len(outputdir) > 0:
        try:
            os.makedirs(outputdir)
        except:
            print('error creating output directory: %s' % outputdir)

    with open(output, 'w') as f:
        try:
            f.write(content)
        except:
            print('error writing nzb: %s' % output)
            sys.exit(1)

    print('successfully wrote nzb file to: %s' % output)

    if not args['delete']:
        sys.exit(0)

    for f in args['input']:
        if not os.path.isfile(f) or f == output:
            continue

        try:
            os.unlink(f)
        except:
            print('error deleting input nzb: %s' % f)
