import os
import requests
import re
import argparse
import ipaddress



def get_as_path(ip):

    stream = os.popen(f"tracert {ip}")
    z = stream.read()
    rr = re.compile("Request timed out")
    ips = []
    for i in z.split("\n")[3:-2]:
        if not i: continue
        if not re.search("Request timed out", i):
            ips.append(list(filter(lambda x: x != "", i.split(" ")))[-1].strip("[]"))
    c:int=1
    for i in ips:
        r = requests.post("http://ip-api.com/json/" + i + "?fields = regionName, city, as, asname, query")

        data = r.json()
        if data.get("status", None)=="success":
            print(f"{c}  |  {data.get('query')}  |  {data.get('as').split(' ')[0]}  |  {data.get('country')}  |  {data.get('regionName')}  |  {data.get('city')}  |  {data.get('isp')}")
        else:
            print(f"{c}  |  {i}  |  no information about as found")
        c+=1


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="as tracer")
    parser.add_argument("target_ip", type=str, help="ip address to trace")
    args = parser.parse_args()
    try:
        ipaddress.ip_address(args.target_ip)
        get_as_path(args.target_ip)

    except ValueError:
        print("wrong ip address")
