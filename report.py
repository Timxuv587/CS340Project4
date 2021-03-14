import json
import time
import subprocess
import re
import requests
import maxminddb
from texttable import Texttable

import sys
#import http

def report(json, output):
    f = open(json, "r")
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
    print(dict)
    output_f = open(output, "w")
    output_f.write(information())
    output_f.close()
    #output_f = open(output, "w")
    #json.dump(dict, output_f, sort_keys=True, indent=4)


def information():
    table = Texttable()
    table.set_cols_align(["l", "r", "c"])
    table.set_cols_valign(["t", "m", "b"])
    table.add_rows([["Name", "Age", "Nickname"],
                    ["Mr\nXavier\nHuon", 32, "Xav'"],
                    ["Mr\nBaptiste\nClement", 1, "Baby"],
                    ["Mme\nLouise\nBourgeau", 28, "Lou\n\nLoue"]])
    return table.draw() + "\n"


report(sys.argv[1], sys.argv[2])

