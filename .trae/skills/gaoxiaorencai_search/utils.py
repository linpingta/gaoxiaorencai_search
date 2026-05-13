"""
工具模块 - 日志和辅助功能
"""
import logging
import sys
from datetime import datetime


def setup_logger(name: str = "gaoxiaorencai_search") -> logging.Logger:
    """设置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


logger = setup_logger()


def normalize_date(date_str: str) -> str:
    """标准化日期格式"""
    if not date_str:
        return ""
    
    date_str = date_str.strip()
    current_year = datetime.now().year
    
    # 匹配 MM-DD 格式
    import re
    match = re.match(r"(\d{1,2})-(\d{1,2})", date_str)
    if match:
        month, day = match.groups()
        return f"{current_year}-{int(month):02d}-{int(day):02d}"
    
    # 匹配 YYYY-MM-DD 格式
    match = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", date_str)
    if match:
        year, month, day = match.groups()
        return f"{year}-{int(month):02d}-{int(day):02d}"
    
    # 匹配今天/昨天/前天
    from datetime import timedelta
    today = datetime.now()
    if "今天" in date_str:
        return today.strftime("%Y-%m-%d")
    elif "昨天" in date_str:
        yesterday = today - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")
    elif "前天" in date_str:
        before_yesterday = today - timedelta(days=2)
        return before_yesterday.strftime("%Y-%m-%d")
    
    return date_str


# 配置数据
LOCATION_MAPPING = {
    "北京": "beijing", "上海": "shanghai", "广州": "guangzhou",
    "深圳": "shenzhen", "杭州": "hangzhou", "南京": "nanjing",
    "武汉": "wuhan", "成都": "chengdu", "西安": "xian",
    "重庆": "chongqing", "天津": "tianjin", "苏州": "suzhou",
    "长沙": "changsha", "郑州": "zhengzhou", "青岛": "qingdao",
}

EDUCATION_MAPPING = {
    "本科": "bachelor", "学士": "bachelor",
    "硕士": "master", "研究生": "master",
    "博士": "doctor", "博士后": "postdoctor",
}

MAJOR_KEYWORDS = {
    "ai": ["人工智能", "AI", "机器学习", "深度学习"],
    "计算机": ["计算机", "软件工程", "信息技术", "大数据"],
    "自动化": ["自动化", "控制科学", "电气工程", "机器人"],
    "教育": ["教育", "教育学", "心理学", "师范"],
}

TIME_RANGE_CONFIG = {
    "近7天": 7, "近一周": 7,
    "近1个月": 30, "近一个月": 30,
    "近3个月": 90, "近三个月": 90,
    "近半年": 180,
}

SEARCH_CONFIG = {
    "timeout": 10,
    "max_retries": 2,
    "retry_delay": 3,
    "request_delay": 10,
    "max_results": 50,
}
