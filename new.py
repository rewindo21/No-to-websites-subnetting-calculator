import sys
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def class_recognizor(ipv4_addr:int):
    n = int(ipv4_addr)
    if n == 10 :
        return "A (PRIVATE RANGE)"
    elif 1 <= n <= 125:
        return "A"
    elif 128 <= n <= 191 and 16 <= n <= 31 :
        return "B (PRIVATE RANGE)"
    elif 128 <= n <= 191:
        return "B"
    elif n == 192:
        return "C (PRIVATE RANGE)"
    elif 192 <= n <= 222 :
        return "C"

def test_ip(ipv4_addr:str):
    return bool(re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ipv4_addr))

if not all([test_ip(ip) for ip in sys.argv[1:3]]):
    print(f"${sys.argv[0]} <ipv4 addr> <subnet mask>")
    exit()


ip_ints = [int(i) for i in sys.argv[1].split('.')]
mask_ints = [int(i) for i in sys.argv[2].split('.')]
network_ints = [ip_ints[i] & mask_ints[i] for i in range(4)]
host_ints = [ip_ints[i] &~ mask_ints[i] for i in range(4)]

ip_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*ip_ints)
mask_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*mask_ints)
network_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*network_ints)
host_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*host_ints)
empty_b = "00000000.00000000.00000000.00000000"
full_b = "11111111.11111111.11111111.11111111"

ip_first_octet = "{0}".format(*ip_ints)

cidr = mask_b.count('1')
color_line = cidr
if cidr > 8: color_line += 1
if cidr > 16: color_line += 1
if cidr > 24: color_line += 1

print(f"IPv4 Address b10: {sys.argv[1]}")
print(f"IPv4 SubMask b10: {sys.argv[2]}" + f"\tCIDR: /{cidr}")
print(f"IPv4 Class: {class_recognizor(ip_first_octet)}")
print(f"Available hosts: {(2 ** (32 - cidr)) - 2}\n")


print(f"Mask Split")
print(f"IPv4 Address b2: {ip_b}")
print(f"IPv4 SubMask b2: {mask_b}")
print(f"IPv4 Network b2: {bcolors.OKBLUE + network_b[:color_line] + bcolors.ENDC}\
{bcolors.OKGREEN + network_b[color_line:] + bcolors.ENDC}")
print(f"IPv4 Hosts   b2: {bcolors.OKBLUE + host_b[:color_line] + bcolors.ENDC}\
{bcolors.OKGREEN + host_b[color_line:] + bcolors.ENDC}\n")

print("First and Last Addresses in Range")
print("IPv4 First b10: {0}.{1}.{2}.{3}".format(*[int(octet,2) for octet in f"{network_b[:color_line]}{empty_b[color_line:]}".split('.')]))
print("IPv4 Last  b10: {0}.{1}.{2}.{3}".format(*[int(octet,2) for octet in f"{network_b[:color_line]}{full_b[color_line:]}".split('.')]))

print(f"IPv4 First b2: {bcolors.OKBLUE + network_b[:color_line] + bcolors.ENDC}\
{bcolors.OKGREEN + empty_b[color_line:] + bcolors.ENDC}")
print(f"IPv4 Last  b2: {bcolors.OKBLUE + network_b[:color_line] + bcolors.ENDC}\
{bcolors.OKGREEN + full_b[color_line:] + bcolors.ENDC}")
