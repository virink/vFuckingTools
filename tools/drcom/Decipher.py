def Decipher(s):
    p = ''
    key = 30137
    for i in xrange(len(s) - 1):
        ch = ord(s[i])
        if ch >= 32 and ch <= 126:
            ch -= 32
            offset = int(96.0 * (key * (i + 1) % 100537 / 100537.0))
            ch = (ch - offset) % 95
            if ch < 0:
                ch += 95
            ch += 32
            p += chr(ch)
    return p


def save(fff, txt):
    f = open(fff, 'a')
    for i in txt:
        f.write(i)
    f.close()


def fuck():
    ll = []
    f = open('x.txt')
    x = 1
    try:
        c = f.readlines()
        for i in c:
            i = i[1:-2].replace("\",\"", "####")
            t = i.split("####")
            ll.append(t[0] + "," + Decipher(t[1]) + "," + t[2] + ",\n")
    except:
        pass
    finally:
        save(ll)
        f.close()

if __name__ == '__main__':
    # fuck('pwd.txt')
    print Decipher('''Sr'J`%a''')
