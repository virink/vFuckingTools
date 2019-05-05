#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

// flag{xxtea_1s_1nterest1ng_ha-_-ha}

#define DELTA 0x9e3779b9 // 2654435769
#define MX (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((sum ^ y) + (key[(p & 3) ^ e] ^ z)))


void btea(uint32_t *, int, uint32_t const key[4]);
void pack(uint64_t *, uint32_t, uint32_t);
void unpack(uint64_t , uint32_t *, uint32_t *);

char crypt[300]="\x56\x95\xd7\xfb\x7b\xd5\xb4\x8b\xe6\xd2\xba\xa4\x4c\x71\x52\xa4\x34\x2d\xfd\xf9\x46\xdb\x89\x7a\xba\xcb\xc5\x6d\xa2\x07\x9a\x78\x3b\x62\x5f\x64\xfd\x5e\x02\x03\x3a\x7a\x4c\x9f\x14\xee\xf6\xeb\x3a\x7a\x4c\x9f\x14\xee\xf6\xeb\xcc\x28\x37\x81\xe9\x24\xa6\x8f\xb1\x79\xb6\x74\x2b\xd6\x4b\xce\x34\x2d\xfd\xf9\x46\xdb\x89\x7a\x08\x7a\xbd\x54\x6b\x82\xb3\x2f\xbb\x9b\x6c\x63\x7d\xc2\xfe\x13\x0d\xc8\xb3\x93\x3b\x34\x01\x25\x08\x7a\xbd\x54\x6b\x82\xb3\x2f\xbb\x9b\x6c\x63\x7d\xc2\xfe\x13\x5b\xc0\x36\xe1\x62\xa1\x59\xe1\xcc\x28\x37\x81\xe9\x24\xa6\x8f\xb1\x79\xb6\x74\x2b\xd6\x4b\xce\x18\xb7\x12\xac\x14\x40\x5c\xca\xb1\x79\xb6\x74\x2b\xd6\x4b\xce\x0d\xc8\xb3\x93\x3b\x34\x01\x25\xcc\x28\x37\x81\xe9\x24\xa6\x8f\xbb\x9b\x6c\x63\x7d\xc2\xfe\x13\x5b\xc0\x36\xe1\x62\xa1\x59\xe1\xba\xcb\xc5\x6d\xa2\x07\x9a\x78\x08\x7a\xbd\x54\x6b\x82\xb3\x2f\x16\x31\x4b\x54\xef\x95\xa5\x49\x34\x2d\xfd\xf9\x46\xdb\x89\x7a\x1f\x27\x75\xa5\x94\x46\x27\xe3\x08\x7a\xbd\x54\x6b\x82\xb3\x2f\x1f\x27\x75\xa5\x94\x46\x27\xe3\x16\x31\x4b\x54\xef\x95\xa5\x49\x34\x2d\xfd\xf9\x46\xdb\x89\x7a\xd8\xf3\x37\x26\x1f\x46\xff\x17\x5d\x88\x2e\x70\xef\xd7\x12\xb3";


int main(int argc, char *argv[])
{
    uint32_t key[4] = {0x342d3221, 0x4320fa22, 0x46257a42, 0x9002bf22};
    uint64_t b64;
    uint32_t b64_split[2];
    int ji=0;

    while (1) {
        if (ji>=35) {
            return 0;
        }
        memcpy(&b64,&crypt[8*ji],8);
        //fread(&b64, sizeof(uint64_t), 1, stdin);
        if (b64 == 0x00000000ffffffff)
            break;
        unpack(b64, &b64_split[0], &b64_split[1]);

        btea(b64_split, -2, key);

        pack(&b64, b64_split[0], b64_split[1]);

        putc(b64, stdout);

        ji+=1;
    }

    return 0;
}


void btea(uint32_t *v, int n, uint32_t const key[4])
{
    uint32_t y, z, sum;
    unsigned p, rounds, e;
    n = -n;
    rounds = 6 + 52/n;
    sum = rounds * DELTA;
    y = v[0];
    do {
        e = (sum >> 2) & 3;
        for (p = n - 1; p > 0; p--) {
            z = v[p - 1];
            y = v[p] -= MX;
        }
        z = v[n - 1];
        y = v[0] -= MX;
        sum -= DELTA;
    } while (--rounds);
}


void pack(uint64_t *b64, uint32_t b32_0, uint32_t b32_1)
{
    *b64 = ((uint64_t) b32_0) << 32 | b32_1;
}


void unpack(uint64_t b64, uint32_t *b32_0, uint32_t *b32_1)
{
    *b32_0 = (uint32_t)((b64 & 0xFFFFFFFF00000000) >> 32);
    *b32_1 = (uint32_t)(b64 & 0xFFFFFFFF);
}
