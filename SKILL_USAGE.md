# OpenClaw Skill 使用说明

## 项目结构

```
gaoxiaorencai_search/
├── .trae/
│   ├── skills.json                    # Skill注册配置
│   └── skills/
│       └── gaoxiaorencai_search/      # Skill目录
│           ├── SKILL.md               # Skill元数据
│           ├── skill.json             # Skill配置
│           └── __init__.py            # Skill入口
├── config/                            # 项目配置
├── core/                              # 核心模块
├── parsers/                           # 解析模块
├── utils/                             # 工具模块
├── skill.py                           # 原Skill封装
└── main.py                            # 命令行入口
```

## 本地使用方法

### 方法一：直接Python导入

```python
# 从项目根目录导入
import sys
sys.path.insert(0, 'c:\\Users\\tchu\\PycharmProjects\\gaoxiaorencai_search')

from core import search

# 执行搜索
result = search("北京，硕士，AI方向，近1个月")
print(result)
```

### 方法二：使用Skill接口

```python
import sys
sys.path.insert(0, 'c:\\Users\\tchu\\PycharmProjects\\gaoxiaorencai_search')

from skill import run, help

# 获取帮助
print(help())

# 执行搜索
result = run("北京，硕士，AI方向，近1个月")
print(result)
```

### 方法三：命令行使用

```bash
cd c:\Users\tchu\PycharmProjects\gaoxiaorencai_search

# 单次搜索
python main.py "北京，硕士，AI方向，近1个月"

# 交互模式
python main.py -i
```

## OpenClaw集成说明

### 1. 确保OpenClaw配置正确

OpenClaw会自动检测 `.trae/skills.json` 文件中注册的Skill。

### 2. Skill自动加载

当OpenClaw启动时，会：
1. 读取 `.trae/skills.json`
2. 加载 `gaoxiaorencai_search` Skill
3. 解析 `SKILL.md` 中的元数据
4. 根据描述自动触发Skill

### 3. 触发条件

当用户输入以下类型的问题时，Skill会自动触发：
- "帮我搜索北京的高校教师职位"
- "查找AI方向的博士后岗位"
- "最近有什么硕士招聘信息"
- "高校人才网搜索..."

### 4. 在OpenClaw中使用

```
User: 帮我搜索北京硕士AI方向近1个月的招聘信息
AI: [自动调用 gaoxiaorencai_search Skill]
    
【高校人才网-实时搜索结果】（筛选条件：北京，硕士，AI方向，近1个月）

共找到 X 条招聘信息，显示前 Y 条：

1. 职位名称：...
   招聘单位：...
   ...
```

## 查询语法

### 完整格式
```
地区，学历，专业方向，时效范围
```

### 示例
```
北京，硕士，AI方向，近1个月
上海，博士，计算机，近7天
广州，本科，教育类，近3个月
深圳，硕士，近1个月
```

### 参数说明
| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 地区 | 北京、上海、广州、深圳、杭州等 | 全国 |
| 学历 | 本科、硕士、博士、博士后 | 不限 |
| 专业方向 | AI、计算机、自动化、教育、医学等 | 不限 |
| 时效范围 | 近7天、近1个月、近3个月、近半年 | 近1个月 |

## 故障排除

### 1. 导入错误

确保项目根目录在Python路径中：
```python
import sys
sys.path.insert(0, 'c:\\Users\\tchu\\PycharmProjects\\gaoxiaorencai_search')
```

### 2. 依赖缺失

安装依赖：
```bash
pip install -r requirements.txt
```

### 3. 网络问题

- 检查网络连接
- 检查是否能访问 https://www.gaoxiaojob.com
- 如有代理，配置环境变量

### 4. OpenClaw未加载Skill

检查 `.trae/skills.json` 配置：
```json
{
  "skills": [
    {
      "name": "gaoxiaorencai_search",
      "path": ".trae/skills/gaoxiaorencai_search",
      "enabled": true,
      "auto_load": true
    }
  ]
}
```

## 扩展开发

### 添加新的地区

编辑 `config/settings.py`：
```python
LOCATION_MAPPING = {
    "北京": "beijing",
    "新城市": "newcity",  # 添加新城市
    # ...
}
```

### 添加新的专业方向

编辑 `config/settings.py`：
```python
MAJOR_KEYWORDS = {
    "新专业": ["关键词1", "关键词2"],
    # ...
}
```

## 注意事项

1. **请求频率**：Skill会自动控制请求频率（10秒间隔），避免对目标网站造成压力
2. **结果时效**：默认返回近1个月的招聘信息
3. **结果数量**：最多返回50条结果
4. **错误处理**：网络异常时会自动重试2次

## 更新日志

### v1.0.0
- 实现基础搜索功能
- 支持多条件筛选
- OpenClaw Skill封装
- 实时搜索方案
