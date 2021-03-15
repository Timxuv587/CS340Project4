import json
import time
import subprocess
import re
import requests
import maxminddb
from texttable import Texttable

import sys
#import http

def report(input, output):
    f = open(input, "r")
    dict = json.load(f)
    #for line in f.readlines():
        #get_ipv4_addresses(url)
        #get_ipv6_addresses(url)
        #get_http_server(url)
        #check_insecure_http(url)
        #get_redirect_to(url)
        #get_hst(url)
        #get_tls_version(url)
        #get_ca(url)
    output_f = open(output, "w")
    output_f.write(information(dict))
    output_f.close()
    #output_f = open(output, "w")
    #json.dump(dict, output_f, sort_keys=True, indent=4)


def information(dict):
    table = Texttable()
    align = ["l"]
    valign = ["t"]
    first_row = []
    domains = list(dict.keys())
    headers = list(dict[domains[0]].keys())
    for i in headers:
        align.append("l")
        valign.append("t")
    table.set_cols_align(align)
    table.set_cols_valign(valign)
    rows = []
    frist_line = copy(headers)
    first_line.append("")
    rows.append(headers)
    for d in domains:
        row = []
        row.append(d)
        for h in headers:
            row.append(str(dict[d][h]))
        rows.append(row)
        print(row)
    table.add_rows(rows)
    return table.draw() + "\n"


report(sys.argv[1], sys.argv[2])

