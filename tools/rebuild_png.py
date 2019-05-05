#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import struct
import os
import sys
import binascii
import zlib


def hex2bin(data):
    return binascii.a2b_hex(data)


def bin2hex(data):
    return binascii.b2a_hex(data)


def bin2dec(data):
    return int(bin2hex(data), 16)


def b2s(data):
    return str(data)

_im = 0


class _logger:

    def error(self, data):
        print("\033[1;31;40m")
        print(data)
        print("\033[0m")

logger = _logger()


class PngChunk:

    def __init__(self, length, typecode, data, crc):
        self.Length = length
        self.ChunkTypeCode = typecode
        self.ChunkData = data
        self.CRC = crc
        self._ChunkData = self._ChunkData_bytes()
        self.crc32()

    def _ChunkData_bytes(self):
        if isinstance(self.ChunkData, PngIHDR):
            _ChunkData = self.ChunkData.toBytes()
        elif isinstance(self.ChunkData, PngIDAT):
            _ChunkData = self.ChunkData.toBytes()
        elif isinstance(self.ChunkData, PngPLTE):
            _ChunkData = self.ChunkData.toBytes()
        else:
            _ChunkData = self.ChunkData
        return _ChunkData

    def crc32(self):
        crc32result = binascii.crc32(self.ChunkTypeCode + self._ChunkData)
        if crc32result != bin2dec(self.CRC):
            logger.error("%s CRC Error : %s" %
                         (b2s(self.ChunkTypeCode), bin2hex(self.CRC)))
            self.CRC = hex2bin(hex(crc32result)[2:])
            print("Repair crc32 : %s\n" % hex(crc32result)[2:])
            # self.crc32()

    def toBytes(self):
        return struct.pack(">i", self.Length) + self.ChunkTypeCode + self._ChunkData + self.CRC


class PngIHDR:

    BITDEPTH_TABLE = {
        0: [1, 2, 4, 8, 16],
        3: [1, 2, 4, 8],
        2: [8, 16],
    }
    COLORTYPE_TABLE = {
        0: "灰度图像",
        2: "真彩色图像",
        3: "索引彩色图像",
        4: "带α通道数据的灰度图像",
        6: "带α通道数据的真彩色图像",
    }

    INTERLACE_TABLE = {
        0: "非隔行扫描",
        1: "Adam7(由Adam M. Costello开发的7遍隔行扫描方法)"
    }

    COMPRESSION_TABLE = {
        0: "deflate"
    }

    def __init__(self, data):
        global _im
        self.data = data
        print("PngIHDR: %s" % b2s(bin2hex(data)))
        self.width = bin2dec(data[:4])
        self.height = bin2dec(data[4:8])
        self.bitdepth = int(data[8])
        self.ct = int(data[9])
        if self.ct in self.BITDEPTH_TABLE.keys() and self.bitdepth not in self.BITDEPTH_TABLE[self.ct]:
            print("颜色类型与图像深度不匹配")
        self.cm = int(data[10])
        self.fm = int(data[11])
        self.im = int(data[12])
        _im = self.im
        self.show()

    def show(self):
        _ct = self.COLORTYPE_TABLE[
            self.ct] if self.ct in self.COLORTYPE_TABLE.keys() else "ColorType Error"
        _cm = self.COMPRESSION_TABLE[self.cm] if self.cm in self.COMPRESSION_TABLE.keys(
        ) else "Compression Method Error"
        _im = self.INTERLACE_TABLE[
            self.im] if self.im in self.INTERLACE_TABLE.keys() else "Interlace Method Error"
        print("\t 图像宽度 : %s px" % self.width)
        print("\t 图像高度 : %s px" % self.height)
        print("\t 颜色类型 : %s" % _ct)
        print("\t 图像深度 : %d" % self.bitdepth)
        print("\t 压缩方法 : %s" % _cm)
        print("\t 滤波器方法 : %s" % self.fm)
        print("\t 隔行扫描方法 : %s" % _im)

    def toBytes(self):
        return self.data


class PngPLTE:

    def __init__(self, data):
        self.data = data
        self.PLTE = {}
        if len(data) % 3:
            print('Error PLTE : %s' % data)
            sys.exit(0)
        _p = len(data) // 3
        i = 0
        print("PLTE List:")
        while i < _p:
            _rgb = {'r': data[i + 1], 'g': data[i + 2], 'b': data[i + 3]}
            print("\t", i, " : ", _rgb, " : ", data[i:i + 3])
            self.PLTE.update({i: _rgb})
            i += 1

    def toBytes(self):
        return self.data


class PngIDAT:

    def __init__(self, data):
        try:
            data = zlib.decompress(data, -zlib.MAX_WBITS)
        except zlib.error:
            data = zlib.decompress(data)
        self.data = data
        self.info = data[:3]  # 0x78,0xda,0x01
        self.len = struct.unpack('h', data[3:5])[0]
        self.nlen = struct.unpack('h', data[5:7])[0]
        self.cdata = data[7:-4]  # 6 + self.len * 5
        self.adler32 = data[-4:]
        self.show()

    def show(self):
        print("压缩信息 : %s" % self.info)
        print("LEN : %s \t LEN^0xFFFF : %s \t NLEN : %s" %
              (self.len, self.len ^ 0xFFFF, self.nlen))
        print("Adler32 : %s" % self.adler32)

    def check(self):
        global _im
        _len = self.len ^ 0xFFFF
        if _len != self.nlen:
            logger.error("ERROR : 压缩块LEN和NLEN信息错误")
            print("LEN : %s \t LEN^0xFFFF : %s \t NLEN : %s" %
                  (self.len, _len, self.nlen))
        if _im == 0 and len(self.cdata) != self.len * 5:
            print("数据长度不匹配")

    def toBytes(self):
        return self.data


class Png:

    def __init__(self, _argv=None):
        png_data = None
        if _argv:
            if os.path.exists(_argv) and os.path.isfile(_argv):
                with open(_argv, 'rb') as f:
                    png_data = f.read()
            else:
                png_data = _argv
            print("File siez : %s" % len(png_data))
            self.analyzing(png_data)

    def analyzing(self, png_data):
        self._header = hex2bin("89504E470D0A1A0A")
        pos = 8
        # IHDR ===============================
        if b'IHDR' in png_data[pos:]:
            pos = png_data[pos:].find(b'IHDR') - 4 + pos
            _p = pos
            length = bin2dec(png_data[_p:_p + 4])
            pos = _p + length + 12
            self.IHDR = PngChunk(length, b'IHDR', PngIHDR(
                png_data[_p + 8:_p + 8 + length]), png_data[pos - 4:pos])
        # PLTE ===============================
        if b'PLTE' in png_data[pos:]:
            if self.IHDR.ChunkData.ct != 3:
                print(
                    "This png should be a Index color image, Please repair the Color Type")
            else:
                _p = pos
                length = bin2dec(png_data[_p:_p + 4])
                pos = _p + length + 12
                self.IHDR = PngChunk(length, b'PLTE', PngPLTE(png_data[
                    _p + 8:_p + 8 + length]), png_data[pos - 4:pos])
        elif self.IHDR.ChunkData.ct == 3:
            print("This is a Index color image, but PLTE is not found")
            sys.exit(0)
        # IDAT ===============================
        self.IDAT = {}
        _idat_count = 1
        _first_idat_pos = png_data.find(b'IDAT')
        pos = _first_idat_pos
        print("_p : %s" % _p)
        while png_data[pos:].find(b'IDAT') < png_data[pos:].find(b'IEND') and png_data[pos:].find(b'IDAT') != -1:
            print("IDAT %s" % _idat_count)
            try:
                _p = pos
                length = bin2dec(png_data[_p - 4:_p])
                print("length : %s" % length)
                pos = _p + length + 12
                _png_chunk_tmp = PngChunk(length, b'IDAT', PngIDAT(png_data[
                    _p + 4:_p + 4 + length]), png_data[pos - 8:pos - 4])
                if _png_chunk_tmp:
                    self.IDAT.update({_idat_count: _png_chunk_tmp})
            except Exception as e:
                print("Exception : %s" % e)
                pos = _p = png_data[pos:].find(b'IDAT')
                _tags = [b'IDAT', b'tIME', b'tEXt', b'zTXt',
                         b'fRAc', b'gIFg', b'gIFt', b'gIFx', b'IEND']
                _tags_test = [png_data[pos + 8:].find(i) for i in _tags]
                print(_tags_test)
                _tags_min = min([j for j in _tags_test if j > 0])
                print("_tags_min : %s" % _tags_min)
                _next_chunk_pos = 0
                if _tags_min > 0:
                    _next_chunk_pos = _p + _tags_min + 8
                length = _next_chunk_pos - pos - 12
                pos = _next_chunk_pos
                print("_next_chunk_pos : %s" % _next_chunk_pos)
                print("length : %s" % length)
                print("pos : %s" % pos)
                print("test : %s" % png_data[_p - 10: _p + 12])
                _png_chunk = PngChunk(length, b'IDAT', PngIDAT(
                    png_data[_p + 8: _p + 8 + length]), png_data[pos - 4: pos])
                self.IDAT.update({_idat_count: _png_chunk})
            _idat_count += 1
        _idat_data = bytearray(b'')
        for i in self.IDAT:
            print(i)
            _idat_data += self.IDAT[i].ChunkData.toBytes()
        print("pos : %s" % pos)
        print("test : %s" % png_data[pos: pos + 4])
        # IEND ===============================
        self._IEND = hex2bin("00000000" + "49454E44" + "AE426082")
        if b'IEND' in png_data[pos:]:
            _p = pos
            length = bin2dec(png_data[_p: _p + 4])
            if length == 0:
                end_chunk = b''
            else:
                end_chunk = png_data[_p + 8: _p + 8 + length]
            pos = _p + length + 12
            self.IEND = PngChunk(
                length, b'IEND', end_chunk, png_data[pos - 4:pos])
        else:
            print("IEND is not found")
        if self._IEND != self.IEND.toBytes():
            print("IEND Error:")
            print("Should:\t")
            print(bin2hex(self._IEND))
            print("Error:\t")
            print(bin2hex(self.IEND.toBytes()))
            sys.exit(0)
        png_data_len = len(png_data)
        if png_data_len > pos:
            print("There are some other data(%s->%s) in the end of this png" %
                  (pos, png_data_len))
            print(bin2hex(png_data[pos:]))
            sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) > 0:
        p = Png(sys.argv[1])
        # print(p)
    else:
        print("Usage: ./%s [filepath|filedata]" % sys.argv[0])
