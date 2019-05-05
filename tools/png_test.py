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
    return str(data, encoding="utf-8")

_im = 0


class PngChunk:

    def __init__(self, length, typecode, data, crc):
        print(str(typecode))
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
            print("%s CRC Error : %s" %
                  (b2s(self.ChunkTypeCode), bin2hex(self.CRC)))
            print("Current CRC : %x" % (crc32result))
            # sys.exit(0)

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


class PngtEXt:

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

# class PngiCCP:
#     def __init__(self):
#         self.len


class PngIDAT:

    def __init__(self, data):
        self.data = data
        # print(data)
        self.info = data[:2]  # 0x78,0xda,0x01
        self.len = struct.unpack('h', data[2:4])[0]
        self.nlen = struct.unpack('h', data[4:6])[0]
        self.cdata = data[6:-4]  # 6 + self.len * 5
        self.adler32 = data[-4:]
        self.show()

    def show(self):
        # print(self.len, self.nlen, self.adler32)
        # self.check()
        print(self.data[:20])
        print("")

    def check(self):
        global _im
        print(self.cdata[:8])
        _len = self.len ^ 0xFFFF
        if _len != self.nlen:
            print("ERROR : 压缩块LEN和NLEN信息错误")
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
            self.analyzing(png_data)

    def analyzing(self, png_data):
        _header = hex2bin("89504E470D0A1A0A")
        self.header = png_data[:8]
        print("File Header : %s " % b2s(bin2hex(self.header)))
        if self.header != _header:
            print("Header Error")
            sys.exit(1)
        pos = 8
        # IHDR ===============================
        if b'IHDR' in png_data[pos:]:
            _p = pos
            length = bin2dec(png_data[_p:_p + 4])
            pos = _p + length + 12
            self.IHDR = PngChunk(length, b'IHDR', PngIHDR(
                png_data[_p + 8:_p + 8 + length]), png_data[pos - 4:pos])
        # IHDR ===============================
        # if b'iCCP' in png_data[pos:]:
        #     _p = pos
        #     length = bin2dec(png_data[_p:_p + 4])
        #     pos = _p + length + 12
        #     self.iCCP = PngChunk(length, b'iCCP', PngIHDR(
        #         png_data[_p + 8:_p + 8 + length]), png_data[pos - 4:pos])
        # cHRM gAMA sBIT ===============================
        _pos_plte = png_data.find(b'PLTE')
        while (b'cHRM' in png_data[pos:] or b'gAMA' in png_data[pos:] or b'sBIT' in png_data[pos:]) and _pos_plte > (pos + 4):
            if b'cHRM' in png_data[pos:]:
                _p = pos
                length = bin2dec(png_data[_p:_p + 4])
                pos = _p + length + 12
                self.cHRM = PngChunk(length, b'cHRM', png_data[
                                     _p + 8:_p + 8 + length], png_data[pos - 4:pos])
            elif b'gAMA' in png_data[pos:]:
                _p = pos
                length = bin2dec(png_data[_p:_p + 4])
                pos = _p + length + 12
                self.gAMA = PngChunk(length, b'gAMA', png_data[
                                     _p + 8:_p + 8 + length], png_data[pos - 4:pos])
            elif b'sBIT' in png_data[pos:]:
                _p = pos
                length = bin2dec(png_data[_p:_p + 4])
                pos = _p + length + 12
                self.sBIT = PngChunk(length, b'sBIT', png_data[
                                     _p + 8:_p + 8 + length], png_data[pos - 4:pos])
        # PLTE ===============================
        if b'PLTE' in png_data[pos:]:
            if self.IHDR.ChunkData.ct != 3:
                print(
                    "This png should be a Index color image, Please repair the Color Type")
            _p = pos
            length = bin2dec(png_data[_p:_p + 4])
            pos = _p + length + 12
            self.PLTE = PngChunk(length, b'PLTE', PngPLTE(png_data[
                                 _p + 8:_p + 8 + length]), png_data[pos - 4:pos])
        elif self.IHDR.ChunkData.ct == 3:
            print("This is a Index color image, but PLTE is not found")
            sys.exit(0)
        # IDAT ===============================
        self.IDAT = {}
        i = 1
        while png_data[pos:].find(b'IDAT') < png_data[pos:].find(b'IEND') and png_data[pos:].find(b'IDAT') > 0:
            _p = pos
            length = bin2dec(png_data[_p:_p + 4])
            pos = _p + length + 12
            self.IDAT.update({i: PngChunk(length, b'IDAT', PngIDAT(png_data[
                _p + 8:_p + 8 + length]), png_data[pos - 4:pos])})
            i += 1
        _idat_data = bytearray(b'')
        for i in self.IDAT:
            _idat_data += self.IDAT[i].ChunkData.toBytes()
        # tEXt ===============================
        if b'tEXt' in png_data[pos:]:
            _p = png_data.find(b'tEXt')
            length = bin2dec(png_data[_p:_p + 4])
            pos = _p + length + 12
            self.tEXt = PngChunk(length, b'tEXt', PngtEXt(
                png_data[_p + 8:_p + 8 + length]), png_data[pos - 4:pos])
        # IEND ===============================
        self._IEND = hex2bin("00000000" + "49454E44" + "AE426082")
        if b'IEND' in png_data[pos:]:
            _p = pos
            length = bin2dec(png_data[_p:_p + 4])
            if length == 0:
                end_chunk = b''
            else:
                end_chunk = png_data[_p + 8:_p + 8 + length]
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
