#include <stdio.h>
#include <string.h>

// const char * base64Table = "BADCFEHGIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

const char * base64Table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

char * base64_encode(const unsigned char * bindata, char * base64, int binlength)
{
    int i, j;
    unsigned char current;

    for (i = 0, j = 0; i < binlength; i += 3)
    {
        current = (bindata[i] >> 2);
        current &= (unsigned char)0x3F;
        base64[j++] = base64Table[(int)current];

        current = ((unsigned char)(bindata[i] << 4)) & ((unsigned char)0x30);
        if (i + 1 >= binlength)
        {
            base64[j++] = base64Table[(int)current];
            base64[j++] = '=';
            base64[j++] = '=';
            break;
        }
        current |= ((unsigned char)(bindata[i + 1] >> 4)) & ((unsigned char)0x0F);
        base64[j++] = base64Table[(int)current];

        current = ((unsigned char)(bindata[i + 1] << 2)) & ((unsigned char)0x3C);
        if (i + 2 >= binlength)
        {
            base64[j++] = base64Table[(int)current];
            base64[j++] = '=';
            break;
        }
        current |= ((unsigned char)(bindata[i + 2] >> 6)) & ((unsigned char)0x03);
        base64[j++] = base64Table[(int)current];

        current = ((unsigned char)bindata[i + 2]) & ((unsigned char)0x3F);
        base64[j++] = base64Table[(int)current];
    }
    base64[j] = '\0';
    return base64;
}

int main(int argc, char ** argv){
    unsigned char bindata[2048];
    char base64[4096];
    if(argc > 1){
        // sprintf(bindata, argv[1]);
        printf("%s\n", base64_encode(bindata, base64, 2048));
    }else{
        printf("Error : argc=%d < 2\n", argc);
    }
}