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
            return True
        else:
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
                location = location[0:len(location)-1]
            lst = openssl_get_header(location)
        result = False
        for h in lst:
            if h.split(": ")[0] == "Strict-Transport-Security":
                result = True
                break
        return result
    else:
        return None

def get_tls_version(url):
    result = []
    nmap_get_TLS(url)
    return result

def get_ca(url):
    return openssl_get_ca(url)


def openssl_get_header(url):
    try:
        req = subprocess.Popen(["openssl", "s_client", "-quiet", "-connect", url+":443"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = req.communicate(bytes("GET / HTTP/1.0\r\nHost: " + url+"\r\n\r\n",encoding="utf-8"), timeout=2)
        output = output.decode(errors='ignore').split("\r\n\r\n")[0].split("\r\n")
        return output
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(e)
        return None

def nmap_get_TLS(url):
    try:
        TLS_lst = ["SSLv2", "SSLv3", "TLSv1.0", "TLSv1.1", "TLSv1.2"]
        req = subprocess.Popen(["nmap", "--script", "ssl-enum-ciphers", "-p", "443", url],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = req.communicate(timeout=2)
        output = output.decode()
        lst = output.split('\n|')
        result = []
        for h in lst:
            if h.strip().split(":")[0] in TLS_lst:
                result.append(h)
        return output
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(e)
        return None

def openssl_get_TLSv1_3(url):
    try:
        req = subprocess.Popen(["openssl", "s_client", "-tls1_3", "-connect", url+":443"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = req.communicate(timeout=2)
        output = output.decode(errors='ignore')
        return output
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(e)
        return None

def openssl_get_ca(url):
    try:
        req = subprocess.Popen(["openssl", "s_client", "-connect", url+":443"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = req.communicate(timeout=2)
        output = output.decode(errors='ignore').split("---\n")
        for line in output:
            if line[0:17] == "Certificate chain":
                result = line.split("O = ")[-1].split(",")[0]
                return result
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(e)
        return None

print("hst")
print(get_hst(sys.argv[1]))
print("redirect")
print(get_redirect_to(sys.argv[1]))
print("ca")
print(get_ca(sys.argv[1]))
print("tls")
print(get_tls_version(sys.argv[1]))
#scan(sys.argv[1], sys.argv[2]):