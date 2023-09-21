import sys
import re

class bcolors:
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'

def class_recognizor(first_octet):
    n = int(first_octet)
    if n == 10: return "A (PRIVATE RANGE)"
    elif 1 <= n <= 125: return "A"
    elif 128 <= n <= 191 and 16 <= n <= 31: return "B (PRIVATE RANGE)"
    elif 128 <= n <= 191: return "B"
    elif n == 192: return "C (PRIVATE RANGE)"
    elif 192 <= n <= 222: return "C"

def int2b(integer_octetcs):
    return "{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(*integer_octetcs)

def test_ip(ipv4_addr:str):
    return bool(re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ipv4_addr))


if not all([test_ip(ip) for ip in sys.argv[1:3]]):
    print(f"${sys.argv[0]} <ipv4 addr> <subnet mask>")
    exit()

ip_int = [int(i) for i in sys.argv[1].split('.')]
mask_int = [int(i) for i in sys.argv[2].split('.')]
wildcard_int = [(~mask_int[i] & 0xff) for i in range(4)]
network_int = [ip_int[i] & mask_int[i] for i in range(4)]
broadcast_int = [ip_int[i] | (~mask_int[i] & 0xff) for i in range(4)]
first_host_int = [network_int[i] for i in range(4)]
first_host_int[3] += 1
last_host_int = [broadcast_int[i] for i in range(4)]
last_host_int[3] -= 1

ip_first_octet = "{0}".format(*ip_int)

cidr = int2b(mask_int).count('1')
color_line = cidr
if cidr > 8: color_line += 1
if cidr > 16: color_line += 1
if cidr > 24: color_line += 1


print("\n")

print(f"IPv4 Class: {class_recognizor(ip_first_octet)}")
print(f"CIDR Notation: /{cidr}")
print(f"Number of Usable Hosts: {(2 ** (32 - cidr)) - 2}")

print("\n")

print(f"IPv4 Address        b10: {sys.argv[1]}")
print(f"IPv4 SubMask        b10: {sys.argv[2]}")
print(f"IPv4 Whildcard      b10: {wildcard_int[0]}.{wildcard_int[1]}.{wildcard_int[2]}.{wildcard_int[3]}")
print(f"Network Address     b10: {network_int[0]}.{network_int[1]}.{network_int[2]}.{network_int[3]}")
print(f"Broadcast Address   b10: {broadcast_int[0]}.{broadcast_int[1]}.{broadcast_int[2]}.{broadcast_int[3]}")
print(f"First Avalible Host b10: {first_host_int[0]}.{first_host_int[1]}.{first_host_int[2]}.{first_host_int[3]}")
print(f"Last Avalible Host  b10: {last_host_int[0]}.{last_host_int[1]}.{last_host_int[2]}.{last_host_int[3]}")

print("\n")

print(f"IPv4 Address        b2: {int2b(ip_int)}")
print(f"IPv4 SubMask        b2: {bcolors.OKBLUE + int2b(mask_int)[:color_line] + bcolors.ENDC}{int2b(mask_int)[color_line:]}")
print(f"IPv4 Whildcard      b2: {int2b(wildcard_int)[:color_line]}{bcolors.OKBLUE + int2b(wildcard_int)[color_line:] + bcolors.ENDC}")
print(f"Network Address     b2: {bcolors.OKBLUE + int2b(network_int)[:color_line] + bcolors.ENDC}{int2b(network_int)[color_line:]}")
print(f"Broadcast Address   b2: {bcolors.OKBLUE + int2b(broadcast_int)[:color_line] + bcolors.ENDC}{int2b(broadcast_int)[color_line:]}")
print(f"First Avalible Host b2: {int2b(first_host_int)[:color_line]}{bcolors.OKBLUE + int2b(first_host_int)[color_line:] + bcolors.ENDC}")
print(f"Last Avalible Host  b2: {int2b(last_host_int)[:color_line]}{bcolors.OKBLUE +int2b(last_host_int)[color_line:] + bcolors.ENDC}")


