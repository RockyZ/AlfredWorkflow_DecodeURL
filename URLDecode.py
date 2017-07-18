#!/usr/bin/python
# encoding: utf-8

import json
import os
import sys

from urlparse import urlparse, parse_qsl

from workflow import Workflow

def main(wf):
    comps = wf.args[0].split(' ')
    url = comps[0]
    filter = None
    if len(comps) > 1:
        filter = comps[1]

    if "http" not in url:
        url = "http://" + url

    parse_result = urlparse(url)

    if parse_result:
        qs = parse_result.query
        if qs:
            qs_result = parse_qsl(qs)

            if qs_result and filter:
                qs_result = wf.filter(filter, qs_result, key=lambda x: x[0], min_score=20)

            for key, value in qs_result:
                wf.add_item(title=key,
                            subtitle=value,
                            arg=value,
                            valid=True)

    # wf.add_item(title="%s" % wf.args,
    #             subtitle="%s" % len(wf.args),
    #             arg="%s" % wf.args,
    #             valid=True)
    # Send the results to Alfred as XML
    wf.send_feedback()
    return 0

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
