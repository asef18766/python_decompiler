from pyinstxtractor.pyinstxtractor import PyInstArchive
import uncompyle6
import sys
import os
import shutil

def unpack_pyc(filename:str):
    arch = PyInstArchive(filename)
    if arch.open():
        if arch.checkFile():
            if arch.getCArchiveInfo():
                arch.parseTOC()
                arch.extractFiles()
                arch.close()
                print('[+] Successfully extracted pyinstaller archive: {0}'.format(filename))
                return
        arch.close()

def patch_pyc(filename:str):
    src_path = f"{filename[:-4]}.pyc"
    magic_path = f"struct.pyc"
    with open(magic_path, "rb") as fp:
        magic_num = fp.read(16)
        fp = open(src_path, "rb")
        new_pyc = magic_num + fp.read()[16:]
        fp.close()
        with open("tmp.pyc", "wb") as fp:
            fp.write(new_pyc)

def main():
    if len(sys.argv) < 2:
        print("usage: python3 main.py <target.exe> <optional export filename>")
        return
    bin_name = sys.argv[1]
    # unpack exe
    unpack_pyc(bin_name)
    # patch binary
    patch_pyc(bin_name)
    os.chdir("..")
    uncompyle6.decompile_file(f"{bin_name}_extracted/tmp.pyc", sys.stdout if len(sys.argv) < 3 else open(sys.argv[2], "w"))
    shutil.rmtree(f"{bin_name}_extracted")

if __name__ == "__main__":
    main()