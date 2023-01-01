from datetime import datetime

def format_datetime(time)->str:
    """
        将时间转为新格式: 2022/12/18 16:07:04
    """
    return datetime.strftime(time,"%Y/%m/%d %H:%M:%S")