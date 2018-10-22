#!/usr/bin/env python3

_v4_len = 32
_v6_len = 128

def eng_exponent(n):
    return len(("{:,d}".format(n)).split(",")) - 1

def num_addresses(prefix_length, address_length):
    return 2 ** (address_length - prefix_length)

if __name__ == "__main__":
    prefix = int(input("Network prefix length: "), 10)
    network = input("IP version (4 or 6): ")

    v = _v4_len if network == "4" else _v6_len
    t = num_addresses(prefix, v)

    print("Number of addresses: {:,d} ({:g})".format(t,t))
    p = eng_exponent(t)
    print("1000^{:d}".format(p))
