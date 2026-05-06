# 高校人才网实时搜索

基于实时搜索方案的高校人才网(gaoxiaojob.com)招聘信息获取工具，支持按地区、学历、专业方向等多条件筛选。

## 功能特性

- **实时搜索**：按需触发搜索，无需长期爬虫运行
- **多条件筛选**：支持地区、学历、专业方向、时效范围组合筛选
- **智能解析**：自动解析用户输入，支持模糊匹配
- **结果格式化**：支持文本、Markdown、JSON等多种输出格式
- **OpenClaw Skill**：提供标准化Skill接口，便于集成

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd gaoxiaorencai_search

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 命令行使用

```bash
# 单次搜索
python main.py "北京，硕士，AI方向，近1个月"

# 交互模式
python main.py -i

# 显示详细日志
python main.py "北京，硕士，AI方向" -v
```

### Python API

```python
from gaoxiaorencai_search import search

# 执行搜索
result = search("北京，硕士，AI方向，近1个月")
print(result)
```

### OpenClaw Skill

```python
from gaoxiaorencai_search import skill

# 执行搜索
result = skill.run("北京，硕士，AI方向，近1个月")
print(result)

# 获取帮助
help_text = skill.help()
print(help_text)
```

## 查询语法

输入格式：`地区，学历，专业方向，时效范围`

### 参数说明

| 参数 | 示例 | 说明 |
|------|------|------|
| 地区 | 北京、上海、广州、深圳 | 支持主要城市 |
| 学历 | 本科、硕士、博士、博士后 | 学历要求 |
| 专业方向 | AI、计算机、自动化、教育 | 专业关键词 |
| 时效范围 | 近7天、近1个月、近3个月 | 发布时间范围 |

### 示例

```
北京，硕士，AI方向，近1个月
上海，博士，计算机，近7天
广州，本科，教育类，近3个月
深圳，硕士，近1个月
```

## 项目结构

```
gaoxiaorencai_search/
├── config/             # 配置文件
│   ├── __init__.py
│   └── settings.py     # 配置参数
├── core/               # 核心模块
│   ├── __init__.py
│   ├── search_engine.py    # 搜索引擎
│   ├── query_parser.py     # 查询解析
│   ├── formatter.py        # 结果格式化
│   └── search_service.py   # 搜索服务
├── parsers/            # 解析模块
│   ├── __init__.py
│   └── job_parser.py   # 职位解析
├── utils/              # 工具模块
│   ├── __init__.py
│   └── logger.py       # 日志工具
├── tests/              # 测试模块
│   ├── __init__.py
│   ├── test_query_parser.py
│   └── test_job_parser.py
├── skill.py            # OpenClaw Skill封装
├── main.py             # 命令行入口
├── requirements.txt    # 依赖列表
└── README.md           # 项目说明
```

## 配置说明

在 `config/settings.py` 中可以修改以下配置：

- `SEARCH_CONFIG`: 搜索参数（超时时间、重试次数等）
- `LOCATION_MAPPING`: 地区映射
- `EDUCATION_MAPPING`: 学历映射
- `MAJOR_KEYWORDS`: 专业方向关键词
- `TIME_RANGE_CONFIG`: 时效范围配置
- `LOG_CONFIG`: 日志配置

## 注意事项

1. 请合理控制搜索频率，避免对目标网站造成压力
2. 搜索结果仅供参考，请以高校人才网官网信息为准
3. 如遇验证码或访问限制，请稍后重试

## 许可证

MIT License
