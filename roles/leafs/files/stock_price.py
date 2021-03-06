#/usr/bin/env python2.7

'''
  requires yahoo-finance module
  pip install yahoo-finance
  https://pypi.python.org/pypi/yahoo-finance
'''
from yahoo_finance import Share
import json
import subprocess


def get_asn():
    command = "show ip bgp summary json"
    try:
        output = subprocess.check_output(["sudo", "vtysh", "-c", command])
    except OSError as e:
        print "problem executing vtysh %s " % (e)
        exit(3)

    if len(output) == 0:
        print "No BGP neighbor output. Is BGP configured?"
        exit(3)

    json_summary = json.loads(output)

    if "as" in json_summary:
        return json_summary["as"]
    else:
        print "ASN not found in output."
        exit(3)


def use_both_spines():
    try:
        subprocess.check_output(["sudo", "vtysh", "-c", "conf t", "-c", "router bgp 64601", "-c", "no neighbor swp2 route-map prepend in"])
    except OSError as e:
        print "problem executing vtysh %s " % (e)
        exit(3)


def use_spine1():
    try:
        subprocess.check_output(["sudo", "vtysh", "-c", "conf t", "-c", "router bgp 64601", "-c", "neighbor swp2 route-map prepend in"])
    except OSError as e:
        print "problem executing vtysh %s " % (e)
        exit(3)


if __name__ == "__main__":
    low_date = "2015-09-28"
    high_date = "2016-07-19"
    route_map_name = "prepend"

    stock = Share("GE")
    asn = get_asn()

    TARGET_PRICE = 25.00

    # 32.93
    high_price = stock.get_historical(high_date, high_date)[0]["Close"]

    # 24.30
    low_price = stock.get_historical(low_date, low_date)[0]["Close"]

    # print "Current price: " + str(stock.get_price())
    current_price = high_price

    print "Reference stock price is: " + str(current_price)
    print "Target price is: " + str(TARGET_PRICE)

    if float(current_price) > float(TARGET_PRICE):
        print "Modifying routing to single path"
        use_spine1()

    if float(current_price) < float(TARGET_PRICE):
        print "Modifying routing to both paths"
        use_both_spines()

    exit(0)
