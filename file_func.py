import os
import struct
from psutil import disk_partitions
from enum import Enum


MaxDepth = 5 # 显示的最大深度
RootPath = "d:/" # 根路径/起始位置
size_unit_map = {
    0:'B',
    1:'KB',
    2:"MB",
    3:"GB"
}

def size_unit_int_to_str(size:int)->str:
    """
        对小数部分采取向下取整
    """
    unit = 0
    while True:
        if size < 1024 or unit == 3:
            break
        else:
            unit += 1
            size = size / 1024
    unit = size_unit_map[unit]
    return f"{round(size,2)}{unit}"

def get_size(path):
    """
        获取某个文件或文件夹或快捷方式的大小(非占用空间大小)
        对于文件, 返回文件大小
        对于文件夹, 返回文件夹本身、下面所有文件与文件夹的大小
        对于快捷方式, 返回实际指向位置的大小
    """
    size = 0
    while True:
        file_type = get_file_type(path)
        if file_type == FileType.File:
            size += os.path.getsize(path)
            break
        elif file_type == FileType.Link:
            path = get_lnk_file_abs_path(path)
        else:
            # 文件夹本身大小
            size += os.path.getsize(path)
            # 下面所有文件与文件夹的大小
            for dirpath, dirnames, filenames in os.walk(path):
                for dirname in dirnames:
                    path = os.path.join(dirpath,dirname)
                    size += os.path.getsize(path)

                for filename in filenames:
                    path = os.path.join(dirpath,filename)
                    size += os.path.getsize(path)
            break

    return size_unit_int_to_str(size)

class FileType(Enum):
    File = 0
    Link = 1
    Dir = 2

def get_file_type(abs_path:str):
    """
        判断文件类型
        返回枚举值
    """
    
    if os.path.isfile(abs_path):
        if abs_path.endswith('.lnk'):
            return FileType.Link
        else:
            return FileType.File
    elif os.path.isdir(abs_path):
        return FileType.Dir

def get_all_drive_letters():
    """
    返回主机上所有盘符名

    Returns:
        list[str]: 盘符名
    """
    return [ i.device for i in disk_partitions()]

def dir_tree(path):
    """
    _summary_

    Args:
        path (_type_): _description_

    Yields:
        _type_: _description_
    """
    for dirpath, dirnames, filenames in os.walk(top=path):
        yield dirpath, dirnames, filenames


def get_lnk_file_abs_path(path:str):
    """
        get the target path of the file or directory that the link file points to,
        result is encoded by gbk
    Args:
        path (str): the link file's absolute path

    Returns:
        the target path
    """
    with open(path, 'rb') as stream:
        content = stream.read()
        # skip first 20 bytes (HeaderSize and LinkCLSID)
        # read the LinkFlags structure (4 bytes)
        lflags = struct.unpack('I', content[0x14:0x18])[0]
        position = 0x18
        # if the HasLinkTargetIDList bit is set then skip the stored IDList 
        # structure and header
        if (lflags & 0x01) == 1:
            position = struct.unpack('H', content[0x4C:0x4E])[0] + 0x4E
        last_pos = position
        position += 0x04
        # get how long the file information is (LinkInfoSize)
        length = struct.unpack('I', content[last_pos:position])[0]
        # skip 12 bytes (LinkInfoHeaderSize, LinkInfoFlags, and VolumeIDOffset)
        position += 0x0C
        # go to the LocalBasePath position
        lbpos = struct.unpack('I', content[position:position+0x04])[0]
        position = last_pos + lbpos
        # read the string at the given position of the determined length
        size= (length + last_pos) - position - 0x02
        temp = struct.unpack('c' * size, content[position:position+size])
        res = bytes()
        for i in temp:
            res += i
    return res.decode('gbk')

def list_dir(path:str):
    """
        遍历path目录, 按照[dirs], [files]的格式返回文件名
    Args:
        path (str): 绝对路径

    Returns:
        [str],[str]: 目录名与文件名
    """
    os.chdir(path)
    
    files,dirs = [], []
    for item in os.listdir(path):
        if os.path.isfile(item):
            files.append(item)
        else:
            dirs.append(item)
    return dirs, files

def path_join(path_list):
    """
        将list中的path连接起来

    Args:
        path_list (list[str]): 

    Returns:
        str: 连接后形成的路径
    """
    res = ""
    for path in path_list:
        res = os.path.join(res,path)
    return res
if __name__ == "__main__":
    res = dir_tree()
    print()
    print(get_lnk_file_abs_path("d:/word模板 - 快捷方式.lnk"))

    