"""
本地测试 gaoxiaorencai_search Skill

运行方式:
    python test_skill_local.py

可以修改下面的 test_queries 列表来测试不同的搜索条件
"""
import sys
import os

# 添加skill目录到路径
skill_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.trae', 'skills', 'gaoxiaorencai_search')
sys.path.insert(0, skill_dir)

print("=" * 70)
print("  本地测试 gaoxiaorencai_search Skill")
print("=" * 70)
print()

# 导入模块
try:
    from core import SearchService
    print("✓ 模块导入成功")
    print()
except Exception as e:
    print(f"✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 创建搜索服务
service = SearchService()

# 测试不同的搜索查询
# 您可以修改这里来测试其他搜索条件
test_queries = [
    "北京，硕士",           # 北京地区硕士职位
    "上海，博士",           # 上海地区博士职位
    "广州，本科",           # 广州地区本科职位
    "北京，教师",           # 北京地区教师职位
    "上海，AI方向",         # 上海地区AI相关职位
    "深圳，博士后",         # 深圳地区博士后职位
]

print("开始测试搜索...")
print("-" * 70)

for i, query in enumerate(test_queries, 1):
    print(f"\n【测试 {i}/{len(test_queries)}】搜索: {query}")
    print("-" * 70)
    
    try:
        result = service.search(query)
        
        # 显示结果
        print(result)
        print()
        
    except Exception as e:
        print(f"✗ 搜索失败: {e}")
        import traceback
        traceback.print_exc()

print("=" * 70)
print("  测试完成")
print("=" * 70)
print()
print("提示: 您可以修改脚本中的 test_queries 列表来测试其他搜索条件")
print("支持的搜索格式:")
print("  - 地区，学历（如：北京，硕士）")
print("  - 地区，专业方向（如：上海，AI方向）")
print("  - 地区，学历，专业方向（如：广州，博士，计算机）")
