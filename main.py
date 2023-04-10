import os
import requests
import re
import argparse


def align_and_print(t: list[list[str]]) -> None:
    widths = [0 for i in range(len(max(t, key=lambda x: len(x))))]
    for i in t:
        for j in range(len(i)):
            widths[j] = max(widths[j], len(i[j]))
    for i in t:
        form = ""
        for j in range(len(i)):
            form += " {: <" + str(widths[j]) + "} |"
        print(form.format(*i))


# "{: < 8} | {: < 3} | {: < 16} | {: < 9} | {: < 6} | {: < 8} | "


def get_as_path(ip):
    stream = os.popen(f"tracert {ip}")
    z = stream.read()
    if z.split(" ")[0:6] == ['Unable', 'to', 'resolve', 'target', 'system', 'name']:
        print("Invalid ip address or domain name")
        exit(0)
    ips = []
    for i in z.split("\n")[3:-2]:
        if not i:
            continue
        if not re.search("Request timed out", i):
            ips.append(list(filter(lambda x: x != "", i.split(" ")))[-1].strip("[]"))
    c: int = 1
    output = []
    for i in ips:
        r = requests.post("http://ip-api.com/json/" + i)

        data = r.json()
        if data.get("status", None) == "success":
            output.append(
                list(map(str, [c, data.get("query"), data.get("as").split(" ")[0], data.get("country"),
                               data.get("regionName"),
                               data.get('city'), data.get('isp')])))
        else:
            output.append([str(c), str(i), "No info found"])
        c += 1
    align_and_print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="as tracer")
    parser.add_argument("target_ip", type=str, help="ip address to trace")
    args = parser.parse_args()
    get_as_path(args.target_ip)
    exit(0)
