"""
配置文件 - 高校人才网实时搜索配置
"""

# 基础URL配置
BASE_URL = "https://www.gaoxiaojob.com"
JOB_LIST_URL = f"{BASE_URL}/job"

# 搜索配置
SEARCH_CONFIG = {
    "timeout": 10,  # 请求超时时间（秒）
    "max_retries": 2,  # 最大重试次数
    "retry_delay": 3,  # 重试间隔（秒）
    "request_delay": 10,  # 请求间隔（秒）
    "max_results": 50,  # 最大返回结果数
}

# 请求头配置
DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# 地区映射
LOCATION_MAPPING = {
    "北京": "beijing",
    "上海": "shanghai",
    "广州": "guangzhou",
    "深圳": "shenzhen",
    "杭州": "hangzhou",
    "南京": "nanjing",
    "武汉": "wuhan",
    "成都": "chengdu",
    "西安": "xian",
    "重庆": "chongqing",
    "天津": "tianjin",
    "苏州": "suzhou",
    "长沙": "changsha",
    "郑州": "zhengzhou",
    "青岛": "qingdao",
    "大连": "dalian",
    "厦门": "xiamen",
    "宁波": "ningbo",
    "无锡": "wuxi",
    "济南": "jinan",
    "合肥": "hefei",
    "福州": "fuzhou",
    "东莞": "dongguan",
    "佛山": "foshan",
    "石家庄": "shijiazhuang",
    "沈阳": "shenyang",
    "哈尔滨": "haerbin",
    "长春": "changchun",
    "昆明": "kunming",
    "南昌": "nanchang",
    "贵阳": "guiyang",
    "南宁": "nanning",
    "兰州": "lanzhou",
    "海口": "haikou",
    "乌鲁木齐": "wulumuqi",
    "银川": "yinchuan",
    "西宁": "xining",
    "拉萨": "lasa",
    "呼和浩特": "huhehaote",
    "太原": "taiyuan",
}

# 学历映射
EDUCATION_MAPPING = {
    "本科": "bachelor",
    "学士": "bachelor",
    "硕士": "master",
    "研究生": "master",
    "博士": "doctor",
    "博士后": "postdoctor",
}

# 专业方向关键词映射
MAJOR_KEYWORDS = {
    "ai": ["人工智能", "AI", "机器学习", "深度学习", "计算机视觉", "自然语言处理", "智能科学"],
    "计算机": ["计算机", "软件工程", "信息技术", "大数据", "云计算", "网络安全", "物联网"],
    "自动化": ["自动化", "控制科学", "电气工程", "机器人", "智能制造"],
    "电子": ["电子", "通信工程", "微电子", "集成电路", "电子信息"],
    "机械": ["机械", "机械工程", "车辆工程", "航空航天", "船舶工程"],
    "材料": ["材料", "材料科学", "纳米材料", "高分子", "金属材料"],
    "化学": ["化学", "化工", "应用化学", "化学工程", "制药"],
    "生物": ["生物", "生命科学", "生物技术", "生物医学", "生物工程"],
    "医学": ["医学", "临床医学", "基础医学", "药学", "公共卫生"],
    "数学": ["数学", "应用数学", "统计学", "数据科学"],
    "物理": ["物理", "应用物理", "光学", "凝聚态物理"],
    "经济": ["经济", "金融", "会计", "财务管理", "国际贸易"],
    "管理": ["管理", "工商管理", "公共管理", "人力资源管理", "行政管理"],
    "教育": ["教育", "教育学", "心理学", "体育", "师范"],
    "文学": ["文学", "中文", "外语", "翻译", "新闻传播"],
    "法学": ["法学", "法律", "政治学", "社会学", "马克思主义"],
    "历史": ["历史", "考古", "哲学", "宗教学"],
    "艺术": ["艺术", "美术", "音乐", "舞蹈", "设计"],
    "建筑": ["建筑", "土木工程", "城市规划", "景观设计"],
    "环境": ["环境", "环境科学", "环境工程", "生态学", "资源科学"],
    "农业": ["农业", "农学", "林学", "畜牧", "兽医", "水产"],
}

# 时效配置（天数）
TIME_RANGE_CONFIG = {
    "近7天": 7,
    "近一周": 7,
    "近1个月": 30,
    "近一个月": 30,
    "近3个月": 90,
    "近三个月": 90,
    "近半年": 180,
    "近1年": 365,
    "近一年": 365,
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/gaoxiaorencai_search.log",
    "max_days": 30,
}

# 职位类型映射
JOB_TYPE_MAPPING = {
    "教师": "teacher",
    "教学": "teacher",
    "科研": "research",
    "博士后": "postdoctor",
    "辅导员": "counselor",
    "行政": "admin",
    "管理": "management",
    "实验": "experiment",
    "技术": "technology",
}
