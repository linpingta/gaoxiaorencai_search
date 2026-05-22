# 高校人才网实时搜索 Skill

基于实时API搜索方案的高校人才网(gaoxiaojob.com)招聘信息获取工具，支持按地区、学历、专业方向等多条件筛选。

## 功能特性

- **实时搜索**：通过官方API实时获取最新招聘信息
- **多条件筛选**：支持地区、学历、专业方向、时效范围组合筛选
- **智能解析**：自动解析用户输入，支持模糊匹配
- **结果格式化**：结构化的职位信息输出
- **OpenClaw Skill**：提供标准化Skill接口，便于集成到AI助手

## 项目结构

```
gaoxiaorencai_search/
├── .trae/
│   └── skills/
│       └── gaoxiaorencai_search/   # Skill核心代码
│           ├── __init__.py         # Skill入口
│           ├── core.py             # 搜索引擎和查询解析
│           ├── parsers.py          # 数据解析
│           ├── utils.py            # 工具函数
│           ├── skill.json          # Skill配置
│           └── SKILL.md            # Skill说明文档
├── install_skill.ps1               # Skill安装脚本
├── test_skill_local.py             # 本地测试脚本
├── requirements.txt                # 依赖列表
└── README.md                       # 项目说明
```

## 安装到 OpenClaw/Trae

### 方法一：使用 PowerShell 安装脚本（推荐）

1. 打开 PowerShell，切换到项目目录
2. 运行安装脚本：

```powershell
cd c:\Users\tchu\PycharmProjects\gaoxiaorencai_search
.\install_skill.ps1
```

安装脚本会自动：
- 将skill文件复制到 `~\.trae\skills\gaoxiaorencai_search`
- 创建/更新 `~\.trae\skills.json` 配置文件
- 验证安装是否成功

### 方法二：手动安装

如果脚本无法运行，可以手动复制：

```powershell
# 1. 创建目标目录
mkdir -Force ~\.trae\skills

# 2. 复制skill文件
Copy-Item -Path ".trae\skills\gaoxiaorencai_search" -Destination "~\.trae\skills\" -Recurse -Force

# 3. 创建 skills.json 配置文件
$config = @{
    skills = @(
        @{
            name = "gaoxiaorencai_search"
            path = ".trae/skills/gaoxiaorencai_search"
            enabled = $true
            auto_load = $true
        }
    )
}
$config | ConvertTo-Json -Depth 10 | Set-Content -Path "~\.trae\skills.json" -Encoding UTF8
```

### 安装后使用

1. **重启 Trae IDE**（完全关闭后重新打开）
2. 在AI助手中直接输入搜索查询，例如：
   - `北京，硕士，AI方向，近1个月`
   - `上海，博士，计算机`
   - `广州，本科，教师`

AI助手会自动识别并调用这个skill来获取实时招聘信息。

## 使用方法

### 1. 作为 OpenClaw Skill 使用

安装到OpenClaw后，在AI助手中直接输入搜索条件：

```
北京，硕士，AI方向，近1个月
```

或获取帮助：

```
help
```

### 2. Python API 调用

```python
import sys
import os

# 添加skill目录到路径
skill_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.trae', 'skills', 'gaoxiaorencai_search')
sys.path.insert(0, skill_dir)

from core import SearchService

# 创建搜索服务
service = SearchService()

# 执行搜索
result = service.search("北京，硕士，AI方向，近1个月")
print(result)
```

### 3. 命令行本地测试

运行本地测试脚本：

```bash
python test_skill_local.py
```

## 查询语法

输入格式：`地区，学历，专业方向，时效范围`

### 参数说明

| 参数 | 示例 | 说明 |
|------|------|------|
| 地区 | 北京、上海、广州、深圳、杭州 | 支持主要城市 |
| 学历 | 本科、硕士、博士、博士后 | 学历要求 |
| 专业方向 | AI、计算机、自动化、教育 | 专业关键词 |
| 时效范围 | 近7天、近1个月、近3个月 | 发布时间范围，默认近1个月 |

### 搜索示例

```
北京，硕士，AI方向，近1个月
上海，博士，计算机，近7天
广州，本科，教育类，近3个月
深圳，硕士，近1个月
北京，教师
上海，博士后
```

## 本地验证

### 方式一：运行测试脚本

```bash
python test_skill_local.py
```

测试脚本会执行多个搜索查询并显示结果，您可以修改脚本中的 `test_queries` 列表来测试不同的搜索条件。

### 方式二：交互式测试

创建测试文件 `my_test.py`：

```python
import sys
import os

skill_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.trae', 'skills', 'gaoxiaorencai_search')
sys.path.insert(0, skill_dir)

from core import SearchService

service = SearchService()

# 测试单个查询
result = service.search("北京，硕士")
print(result)
```

运行：

```bash
python my_test.py
```

### 验证要点

1. **数据真实性**：检查结果中是否包含真实的大学/学院名称（如：上海科技大学、北京交通大学等）
2. **链接有效性**：职位详情链接应为 `https://www.gaoxiaojob.com/job/detail/xxx.html` 格式
3. **信息完整性**：每个职位应包含标题、单位、地点、学历、发布时间等信息

## 输出示例

```
【高校人才网-实时搜索结果】（筛选条件：北京，硕士，近1个月）

共找到 15 条招聘信息，显示前 15 条：

1. 【急聘】工作人员-国际合作与交流处
   招聘单位：中国农业大学国际合作与交流处（双一流院校）
   工作地点：北京-北京
   学历要求：硕士研究生
   专业方向：专业不限
   招聘人数：1
   发布时间：2026-05-13
   薪资待遇：面议
   详情链接：https://www.gaoxiaojob.com/job/detail/2168794.html

2. 教学管理岗
   招聘单位：南京航空航天大学教师发展与教学评估中心（双一流院校）
   工作地点：江苏-南京
   学历要求：硕士研究生
   ...
```

## 安装依赖（用于本地开发/测试）

```bash
pip install -r requirements.txt
```

依赖包：
- requests
- beautifulsoup4

## 配置说明

在 `.trae/skills/gaoxiaorencai_search/utils.py` 中可以修改以下配置：

- `LOCATION_MAPPING`: 地区映射（添加更多城市）
- `EDUCATION_MAPPING`: 学历映射
- `MAJOR_KEYWORDS`: 专业方向关键词
- `TIME_RANGE_CONFIG`: 时效范围配置
- `SEARCH_CONFIG`: 搜索参数（超时时间、重试次数、请求间隔等）

## 注意事项

1. **请求频率**：skill内置了请求间隔限制（默认10秒），请合理控制搜索频率
2. **网络连接**：需要能够访问 `https://www.gaoxiaojob.com`
3. **数据时效**：搜索结果为实时获取，与官网同步
4. **结果数量**：每次搜索最多返回50条结果
5. **安装位置**：OpenClaw Skill需要安装在 `~\.trae\skills\` 目录下

## 常见问题

**Q: 如何在OpenClaw中使用这个skill？**  
A: 运行 `install_skill.ps1` 脚本安装，然后重启Trae IDE，在AI助手中直接输入搜索条件即可。

**Q: 搜索返回"暂时无法访问"？**  
A: 可能是网络问题或请求过于频繁，请稍后重试。

**Q: 搜索返回"未找到符合条件的招聘信息"？**  
A: 尝试放宽搜索条件，如扩大时间范围、更换关键词等。

**Q: 如何添加更多城市支持？**  
A: 在 `utils.py` 的 `LOCATION_MAPPING` 中添加城市名称和对应的代码。

**Q: 安装后AI助手没有调用skill？**  
A: 请确保：1) 安装脚本执行成功；2) 已重启Trae IDE；3) `~\.trae\skills.json` 文件配置正确。

## 许可证

MIT License
