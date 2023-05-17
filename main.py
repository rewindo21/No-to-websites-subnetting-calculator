import re

def ip_check(ip):
    global ipflag
    ipfcheck = re.search("(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\."
                         "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\."
                         "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\."
                         "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])", ip)
    if ipfcheck:
        ipflag = True
    else:
        ipflag = False


def cidr_check(cidr):
    global cidrflag
    if 8 <= int(cidr) <= 30:
        cidrflag = True
    else:
        cidrflag = False


def class_recognizor(ip):
    decimal = []
    for octet in ip.split('.'):
        decimal.append(octet)

    if int(decimal[0]) == 10 :
        print("CLASS: A (PRIVATE RANGE)")
    elif 1 <= int(decimal[0]) <= 125:
        print("CLASS: A")
    elif 128 <= int(decimal[0]) <= 191 and 16 <= int(decimal[1]) <= 31 :
        print("CLASS: B (PRIVATE RANGE)")
    elif 128 <= int(decimal[0]) <= 191:
        print("CLASS: B")
    elif int(decimal[0]) == 192:
        print("CLASS: C (PRIVATE RANGE)")
    elif 192 <= int(decimal[0]) <= 222 :
        print("CLASS: C")


def host_counter(cidr):
    n = 32 - int(cidr)
    host = (2**n)-2
    print('AVALIBLE HOSTS: ' + f'2^{n} = ' + f'{host}')


def subnet(cidr):
    cidr = int(cidr)
    global mask
    mask = '00000000.00000000.00000000.00000000'
    for i in mask:
        if cidr > 0:
            mask = mask.replace('0', '1', 1)
        cidr -= 1
    

    temp = []
    for x in mask.split('.'):
        temp.append(str(int(x, 2)))
    
    subnet_mask = '.'.join(temp)
    print('SUBNET MASK: ' + subnet_mask)


def whildcard(cidr):
    cidr = int(cidr)
    mask = '11111111.11111111.11111111.11111111'
    for i in mask:
        if cidr > 0:
            mask = mask.replace('1', '0', 1)
        cidr -= 1

    temp = []
    for x in mask.split('.'):
        temp.append(str(int(x, 2)))
    
    whildcard_mask = '.'.join(temp)
    print('WHILDCARD MASK: ' + whildcard_mask)


def int2bin(ip):
    temp = []
    for x in ip.split('.'):
        temp.append(bin(int(x))[2:].rjust(8, '0'))
    
    global binary_ip
    binary_ip = '.'.join(temp)
    return binary_ip


def network_ip(binary_ip, mask):
    ip_list = []
    for i in binary_ip:
        if i.isdigit():
            ip_list.append(i)

    n = mask.count('1')
    m = []
    for i in range(32-n):
        m.append('0')

    temp = ip_list[:n]
    temp.extend(m)
    temp.insert(8, '.')
    temp.insert(17, '.')
    temp.insert(26, '.')
    global binary_net_ip
    binary_net_ip = ''.join(temp)

    temp2 = []
    for x in binary_net_ip.split('.'):
        temp2.append(str(int(x, 2)))
    
    net_ip = '.'.join(temp2)
    print('NETWORK IP: ' + net_ip)


def broadcast_ip(binary_ip, mask):
    ip_list = []
    for i in binary_ip:
        if i.isdigit():
            ip_list.append(i)

    n = mask.count('1')
    m = []
    for i in range(32-n):
        m.append('1')

    temp = ip_list[:n]
    temp.extend(m)
    temp.insert(8, '.')
    temp.insert(17, '.')
    temp.insert(26, '.')
    global binary_bc_ip
    binary_bc_ip = ''.join(temp)

    temp2 = []
    for x in binary_bc_ip.split('.'):
        temp2.append(str(int(x, 2)))
    
    bc_ip = '.'.join(temp2)
    print('BROADCAST IP: ' + bc_ip)


def first_ip(binary_net_ip):
    net_ip_list = []
    for i in binary_net_ip:
        net_ip_list.append(i)

    net_ip_list[34] = '1'
    binary_first_ip = ''.join(net_ip_list)

    temp = []
    for x in binary_first_ip.split('.'):
        temp.append(str(int(x, 2)))

    f_ip = '.'.join(temp)
    print('FIRST AVALIBLE IP: ' + f_ip)


def last_ip(binary_bc_ip):
    bc_ip_list = []
    for i in binary_bc_ip:
        bc_ip_list.append(i)

    bc_ip_list[34] = '0'
    binary_last_ip = ''.join(bc_ip_list)

    temp = []
    for x in binary_last_ip.split('.'):
        temp.append(str(int(x, 2)))

    l_ip = '.'.join(temp)
    print('LAST AVALIBLE IP: ' + l_ip)


if __name__ == "__main__":
    ip = input("ENTER IPv4 : ")
    ip_check(ip)
    cidr = input("ENTER CIDR : \\")
    cidr_check(cidr)

    if ipflag == True and cidrflag == True:
        print("-----------------------")
        class_recognizor(ip)
        host_counter(cidr)
        subnet(cidr)
        whildcard(cidr)
        int2bin(ip)
        network_ip(binary_ip, mask)
        broadcast_ip(binary_ip, mask)
        first_ip(binary_net_ip)
        last_ip(binary_bc_ip)
        print("-----------------------")
    elif ipflag != True:
        print("Invalid IP")
    elif cidrflag != True:
        print("Invalid CIDR")
