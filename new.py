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

def class_recognizor(first_octet:int):
    n = int(first_octet)
    if n == 10: return "A (PRIVATE RANGE)"
    elif 1 <= n <= 125: return "A"
    elif 128 <= n <= 191 and 16 <= n <= 31: return "B (PRIVATE RANGE)"
    elif 128 <= n <= 191: return "B"
    elif n == 192: return "C (PRIVATE RANGE)"
    elif 192 <= n <= 222: return "C"

def test_ip(ipv4_addr:str):
    return bool(re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ipv4_addr))

if not all([test_ip(ip) for ip in sys.argv[1:3]]):
    print(f"${sys.argv[0]} <ipv4 addr> <subnet mask>")
    exit()


ip_ints = [int(i) for i in sys.argv[1].split('.')]
mask_ints = [int(i) for i in sys.argv[2].split('.')]
wildcard_ints = [(~mask_ints[i] & 0xff) for i in range(4)]
network_ints = [ip_ints[i] & mask_ints[i] for i in range(4)]
broadcast_ints = [ip_ints[i] | (~mask_ints[i] & 0xff) for i in range(4)]
first_host_ints = [network_ints[i] for i in range(4)]
first_host_ints[3] += 1
last_host_ints = [broadcast_ints[i] for i in range(4)]
last_host_ints[3] -= 1
# host_ints = [ip_ints[i] &~ mask_ints[i] for i in range(4)]

ip_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*ip_ints)
mask_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*mask_ints)
whildcard_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*wildcard_ints)
network_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*network_ints)
broadcast_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*broadcast_ints)
first_host_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*first_host_ints)
last_host_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*last_host_ints)
# host_b = "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*host_ints)
# empty_b = "00000000.00000000.00000000.00000000"
# full_b = "11111111.11111111.11111111.11111111"

ip_first_octet = "{0}".format(*ip_ints)

cidr = mask_b.count('1')
color_line = cidr
if cidr > 8: color_line += 1
if cidr > 16: color_line += 1
if cidr > 24: color_line += 1


print("\n")

print(f"CIDR: /{cidr}")
print(f"IPv4 Class: {class_recognizor(ip_first_octet)}")
print(f"Available hosts: {(2 ** (32 - cidr)) - 2}")

print("\n")

print(f"IPv4 Address    b10: {sys.argv[1]}")
print(f"IPv4 SubMask    b10: {sys.argv[2]}")
print(f"IPv4 Whildcard  b10: {wildcard_ints[0]}.{wildcard_ints[1]}.{wildcard_ints[2]}.{wildcard_ints[3]}")
print(f"IPv4 Network    b10: {network_ints[0]}.{network_ints[1]}.{network_ints[2]}.{network_ints[3]}")
print(f"IPv4 Broadcast  b10: {broadcast_ints[0]}.{broadcast_ints[1]}.{broadcast_ints[2]}.{broadcast_ints[3]}")
print(f"IPv4 First Host b10: {first_host_ints[0]}.{first_host_ints[1]}.{first_host_ints[2]}.{first_host_ints[3]}")
print(f"IPv4 Last Last  b10: {last_host_ints[0]}.{last_host_ints[1]}.{last_host_ints[2]}.{last_host_ints[3]}")

print("\n")

print(f"IPv4 Address    b2: {ip_b}")
print(f"IPv4 SubMask    b2: {mask_b}")
print(f"IPv4 Whildcard  b2: {whildcard_b}")
print(f"IPv4 Network    b2: {bcolors.OKBLUE + network_b[:color_line] + bcolors.ENDC}{network_b[color_line:]}")
print(f"IPv4 Broadcast  b2: {bcolors.OKBLUE + broadcast_b[:color_line] + bcolors.ENDC}{broadcast_b[color_line:]}")
print(f"IPv4 First Host b2: {first_host_b[:color_line]}{bcolors.OKBLUE + first_host_b[color_line:] + bcolors.ENDC}")
print(f"IPv4 Last Host  b2: {last_host_b[:color_line]}{bcolors.OKBLUE +last_host_b[color_line:] + bcolors.ENDC}")
# print(f"IPv4 Hosts     b2: {host_b[:color_line]}{bcolors.OKBLUE + host_b[color_line:] + bcolors.ENDC}")
# print(f"IPv4 First     b2: {bcolors.OKBLUE + network_b[:color_line] + bcolors.ENDC}{bcolors.OKGREEN + empty_b[color_line:] + bcolors.ENDC}")
# print(f"IPv4 Last      b2: {bcolors.OKBLUE + network_b[:color_line] + bcolors.ENDC}{bcolors.OKGREEN + full_b[color_line:] + bcolors.ENDC}")


