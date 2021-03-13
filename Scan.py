import json
import time
import subprocess
import re
import requests
import sys
#import http
def scan(input, output):
    dict = {}
    f = open(input, "r")
    for line in f.readlines():
        dict[line] = {"scan_time": time.time()}
        dict[line]["ipv4_addresses"] = []
        dict[line]["ipv6_addresses"] = []
    output_f = open(output, "w")
    json.dump(dict, output_f, sort_keys=True, indent=4)



def get_redirect_to(url):
    #https://stackoverflow.com/questions/33684356/how-to-capture-the-output-of-openssl-in-python
    lst = openssl_get_header(url)
    if lst != None:
        if int(lst[0][9:12]) == 301:
            print(lst)
            return True
        else:
            print("False")
            return False
    else:
        return None

def get_hst(url):
    lst = openssl_get_header(url)
    if lst != None:
        while int(lst[0][9:12]) == 301:
            location = ""
            for h in lst:
                if h.split(": ")[0] == "Location":
                    location = h.split(": ")[1]
                    break
            location = location.split("://")[1]
            if location[-1] == "/":
                location = location[0:len(location)-2]
            lst = openssl_get_header(location)
            print(lst)
        result = False
        for h in lst:
            if h.split(": ")[0] == "Strict-Transport-Security":
                print(h)
                result = True
                break
        print(result)
        return result
    else:
        return None

def get_tls_version(url):
    return []

def get_ca(url):
    print(openssl_get_ca(url))
    return openssl_get_ca(url)


def openssl_get_header(url):
    try:
        req = subprocess.Popen(["openssl", "s_client", "-quiet", "-connect", url+":443"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = req.communicate(bytes("GET / HTTP/1.0\r\nHost: " + url+"\r\n\r\n",encoding="utf-8"), timeout=2)
        output = output.decode(errors='ignore').split("\r\n\r\n")[0].split("\r\n")
        return output
    except Exception as e:
        print(e)
        return None

def openssl_get_TLSv1_3(url):
    try:
        req = subprocess.Popen(["openssl", "s_client", "-tls1_3", "-connect", url+":443"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = req.communicate(timeout=2)
        output = output.decode(errors='ignore')
        return output
    except Exception as e:
        print(e)
        return None

def openssl_get_ca(url):
    try:
        req = subprocess.Popen(["openssl", "s_client", "-connect", url+":443"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = req.communicate(timeout=2)
        output = output.decode(errors='ignore').split("\r\n")
        for line in output:
            if output[0:4] == "depth":
                result = line.split("O = ")[1].split(",")[0]
                print(result)
                return result
        return None
    except Exception as e:
        print(e)
        return None

get_hst(sys.argv[1])
#get_redirect_to(sys.argv[1])
#get_ca(sys.argv[1])
#scan(sys.argv[1], sys.argv[2]):