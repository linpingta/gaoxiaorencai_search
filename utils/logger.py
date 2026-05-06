"""
日志工具模块
"""
import os
import logging
import datetime
from pathlib import Path

from config import LOG_CONFIG


def setup_logger(name: str = "gaoxiaorencai_search") -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_CONFIG["level"]))
    
    # 清除已有处理器
    logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_CONFIG["format"])
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    log_file = LOG_CONFIG["file"]
    log_dir = os.path.dirname(log_file)
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # 按日期分割日志文件
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_with_date = log_file.replace(".log", f"_{today}.log")
    
    file_handler = logging.FileHandler(log_file_with_date, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def clean_old_logs(log_dir: str = "logs", max_days: int = 30):
    """
    清理过期日志文件
    
    Args:
        log_dir: 日志目录
        max_days: 最大保留天数
    """
    if not os.path.exists(log_dir):
        return
    
    now = datetime.datetime.now()
    for filename in os.listdir(log_dir):
        if not filename.endswith(".log"):
            continue
        
        file_path = os.path.join(log_dir, filename)
        file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        
        if (now - file_mtime).days > max_days:
            try:
                os.remove(file_path)
            except OSError:
                pass


# 默认日志记录器
logger = setup_logger()
