/**
 *  base64编码、解码实现
 *       C语言源代码
 *
 *   注意：请使用gcc编译
 *
 *             叶剑飞
 *
 * 
 *
 *  使用说明：
 *      命令行参数说明：若有“-d”参数，则为base64解码，否则为base64编码。
 *                      若有“-o”参数，后接文件名，则输出到标准输出文件。
 *      输入来自标准输入stdin，输出为标准输出stdout。可重定向输入输出流。
 *
 *        base64编码：输入任意二进制流，读取到文件读完了为止（键盘输入则遇到文件结尾符为止）。
 *                    输出纯文本的base64编码。
 *
 *        base64解码：输入纯文本的base64编码，读取到文件读完了为止（键盘输入则遇到文件结尾符为止）。
 *                    输出原来的二进制流。
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <io.h>
#include <fcntl.h>
#include <stdbool.h>

#ifndef MAX_PATH
#define MAX_PATH 256
#endif

const char * base64char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

char * base64_encode( const unsigned char * bindata, char * base64, int binlength )
{
    int i, j;
    unsigned char current;

    for ( i = 0, j = 0 ; i < binlength ; i += 3 )
    {
        current = (bindata[i] >> 2) ;
        current &= (unsigned char)0x3F;
        base64[j++] = base64char[(int)current];

        current = ( (unsigned char)(bindata[i] << 4 ) ) & ( (unsigned char)0x30 ) ;
        if ( i + 1 >= binlength )
        {
            base64[j++] = base64char[(int)current];
            base64[j++] = '=';
            base64[j++] = '=';
            break;
        }
        current |= ( (unsigned char)(bindata[i+1] >> 4) ) & ( (unsigned char) 0x0F );
        base64[j++] = base64char[(int)current];

        current = ( (unsigned char)(bindata[i+1] << 2) ) & ( (unsigned char)0x3C ) ;
        if ( i + 2 >= binlength )
        {
            base64[j++] = base64char[(int)current];
            base64[j++] = '=';
            break;
        }
        current |= ( (unsigned char)(bindata[i+2] >> 6) ) & ( (unsigned char) 0x03 );
        base64[j++] = base64char[(int)current];

        current = ( (unsigned char)bindata[i+2] ) & ( (unsigned char)0x3F ) ;
        base64[j++] = base64char[(int)current];
    }
    base64[j] = '\0';
    return base64;
}

int base64_decode( const char * base64, unsigned char * bindata )
{
    int i, j;
    unsigned char k;
    unsigned char temp[4];
    for ( i = 0, j = 0; base64[i] != '\0' ; i += 4 )
    {
        memset( temp, 0xFF, sizeof(temp) );
        for ( k = 0 ; k < 64 ; k ++ )
        {
            if ( base64char[k] == base64[i] )
                temp[0]= k;
        }
        for ( k = 0 ; k < 64 ; k ++ )
        {
            if ( base64char[k] == base64[i+1] )
                temp[1]= k;
        }
        for ( k = 0 ; k < 64 ; k ++ )
        {
            if ( base64char[k] == base64[i+2] )
                temp[2]= k;
        }
        for ( k = 0 ; k < 64 ; k ++ )
        {
            if ( base64char[k] == base64[i+3] )
                temp[3]= k;
        }

        bindata[j++] = ((unsigned char)(((unsigned char)(temp[0] << 2))&0xFC)) |
                ((unsigned char)((unsigned char)(temp[1]>>4)&0x03));
        if ( base64[i+2] == '=' )
            break;

        bindata[j++] = ((unsigned char)(((unsigned char)(temp[1] << 4))&0xF0)) |
                ((unsigned char)((unsigned char)(temp[2]>>2)&0x0F));
        if ( base64[i+3] == '=' )
            break;

        bindata[j++] = ((unsigned char)(((unsigned char)(temp[2] << 6))&0xF0)) |
                ((unsigned char)(temp[3]&0x3F));
    }
    return j;
}

void encode(FILE * fp_in, FILE * fp_out)
{
    unsigned char bindata[2050];
    char base64[4096];
    size_t bytes;
    while ( !feof( fp_in ) )
    {
        bytes = fread( bindata, 1, 2049, fp_in );
        base64_encode( bindata, base64, bytes );
        fprintf( fp_out, "%s", base64 );
    }
}

void decode(FILE * fp_in, FILE * fp_out)
{
    int i;
    unsigned char bindata[2050];
    char base64[4096];
    size_t bytes;
    while ( !feof( fp_in ) )
    {
        for ( i = 0 ; i < 2048 ; i ++ )
        {
            base64[i] = fgetc(fp_in);
            if ( base64[i] == EOF )
                break;
            else if ( base64[i] == '\n' || base64[i] == '\r' )
                i --;
        }
        bytes = base64_decode( base64, bindata );
        fwrite( bindata, bytes, 1, fp_out );
    }
}

void help(const char * filepath)
{
    fprintf( stderr, "Usage: %s [-d] [input_filename] [-o output_filepath]\n", filepath );
    fprintf( stderr, "\t-d\tdecode data\n" );
    fprintf( stderr, "\t-o\toutput filepath\n\n" );
}

int main(int argc, char * argv[])
{
    FILE * fp_input = NULL;
    FILE * fp_output = NULL;
    bool isencode = true;
    bool needHelp = false;
    int opt = 0;
    char input_filename[MAX_PATH] = "";
    char output_filename[MAX_PATH] = "";

    opterr = 0;
    while ( (opt = getopt(argc, argv, "hdo:")) != -1 )
    {
        switch(opt)
        {
        case 'd':
            isencode = false;
            break;
        case 'o':
            strncpy(output_filename, optarg, sizeof(output_filename));
            output_filename[sizeof(output_filename)-1] = '\0';
            break;
        case 'h':
            needHelp = true;
            break;
        default:
            fprintf(stderr, "%s: invalid option -- %c\n", argv[0], optopt);
            needHelp = true;
            break;
        }
    }
    if ( optind < argc )
    {
        strncpy(input_filename, argv[optind], sizeof(input_filename));
        input_filename[sizeof(input_filename)-1] = '\0';
    }

    if (needHelp)
    {
        help(argv[0]);
        return EXIT_FAILURE;
    }

    if ( !strcmp(input_filename, "") )
    {
        fp_input = stdin;
        if (isencode)
            _setmode( _fileno(stdin), _O_BINARY );
    }
    else
    {
        if (isencode)
            fp_input = fopen(input_filename, "rb");
        else
            fp_input = fopen(input_filename, "r");
    }
    if ( fp_input == NULL )
    {
        fprintf(stderr, "Input file open error\n");
        return EXIT_FAILURE;
    }

    if ( !strcmp(output_filename, "") )
    {
        fp_output = stdout;
        if (!isencode)
            _setmode( _fileno(stdout), _O_BINARY );
    }
    else
    {
        if (isencode)
            fp_output = fopen(output_filename, "w");
        else
            fp_output = fopen(output_filename, "wb");
    }
    if ( fp_output == NULL )
    {
        fclose(fp_input);
        fp_input = NULL;
        fprintf(stderr, "Output file open error\n");
        return EXIT_FAILURE;
    }

    if (isencode)
        encode(fp_input, fp_output);
    else
        decode(fp_input, fp_output);
    fclose(fp_input);
    fclose(fp_output);
    fp_input = fp_output = NULL;
    return EXIT_SUCCESS;
}