"""
测试更新后的skill实现
"""
import sys
import os

# 添加skill目录到路径
skill_dir = os.path.join(os.path.dirname(__file__), '.trae', 'skills', 'gaoxiaorencai_search')
sys.path.insert(0, skill_dir)

from core import SearchService, QueryParser, SearchEngine, ResultFormatter

print("=" * 60)
print("测试更新后的Skill实现")
print("=" * 60)

# 测试1: 查询解析
print("\n【测试1】查询解析")
parser = QueryParser()
test_queries = [
    "北京，硕士，AI方向，近1个月",
    "上海，博士",
    "广州，本科，教育类",
    "深圳",
]

for query in test_queries:
    criteria = parser.parse(query)
    desc = parser.format_criteria(criteria)
    print(f"  输入: '{query}'")
    print(f"  解析: 地区={criteria.location}, 学历={criteria.education}, 专业={criteria.major}, 时间={criteria.time_range}")
    print(f"  描述: {desc}")
    print()

# 测试2: 搜索服务（带错误处理）
print("\n【测试2】搜索服务")
service = SearchService()

# 测试无效查询
print("  测试无效查询:")
result = service.search("")
print(f"    结果: {result[:50]}...")

# 测试正常查询（可能会遇到访问限制）
print("\n  测试正常查询（北京，硕士）:")
result = service.search("北京，硕士")
print(f"    结果:\n{result}")

# 测试3: 格式化器
print("\n【测试3】格式化器")
formatter = ResultFormatter()

# 测试空结果（访问错误）
print("  空结果（访问错误）:")
empty_result = formatter._format_empty("北京，硕士", is_access_error=True)
print(f"    {empty_result[:200]}...")

# 测试空结果（无匹配）
print("\n  空结果（无匹配）:")
empty_result2 = formatter._format_empty("北京，硕士", is_access_error=False)
print(f"    {empty_result2[:200]}...")

# 测试4: 搜索引擎
print("\n【测试4】搜索引擎")
engine = SearchEngine()

# 测试搜索（可能会遇到限制）
print("  尝试搜索...")
html = engine.search(keyword="教师", location="北京", education="")

if html:
    print(f"  ✓ 成功获取HTML，长度: {len(html)}")
else:
    print("  ✗ 获取HTML失败（可能遇到访问限制）")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
