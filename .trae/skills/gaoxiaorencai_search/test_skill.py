"""
Skill 测试脚本

用于验证 gaoxiaorencai_search Skill 是否可以正常工作
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_import():
    """测试模块导入"""
    print("=" * 50)
    print("测试 1: 模块导入")
    print("=" * 50)
    
    try:
        import utils
        print("✓ utils 模块导入成功")
        
        import parsers
        print("✓ parsers 模块导入成功")
        
        import core
        print("✓ core 模块导入成功")
        
        import __init__ as skill_module
        print("✓ __init__ 模块导入成功")
        
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False


def test_utils():
    """测试工具函数"""
    print("\n" + "=" * 50)
    print("测试 2: 工具函数")
    print("=" * 50)
    
    try:
        from utils import normalize_date, logger, LOCATION_MAPPING
        
        # 测试日期标准化
        result = normalize_date("04-29")
        print(f"✓ normalize_date('04-29') = {result}")
        
        # 测试配置数据
        print(f"✓ LOCATION_MAPPING 包含 {len(LOCATION_MAPPING)} 个地区")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def test_parsers():
    """测试解析器"""
    print("\n" + "=" * 50)
    print("测试 3: 解析器")
    print("=" * 50)
    
    try:
        from parsers import JobParser, JobInfo
        
        parser = JobParser()
        print("✓ JobParser 实例化成功")
        
        # 测试空HTML
        jobs = parser.parse_job_list("")
        print(f"✓ 空HTML返回 {len(jobs)} 个职位")
        
        # 测试 JobInfo
        job = JobInfo(title="测试职位", company="测试公司")
        print(f"✓ JobInfo 创建成功: {job.title}")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_core():
    """测试核心模块"""
    print("\n" + "=" * 50)
    print("测试 4: 核心模块")
    print("=" * 50)
    
    try:
        from core import QueryParser, SearchCriteria, SearchEngine, SearchService
        
        # 测试查询解析
        parser = QueryParser()
        criteria = parser.parse("北京，硕士，AI方向")
        print(f"✓ 查询解析成功")
        print(f"  - 地区: {criteria.location}")
        print(f"  - 学历: {criteria.education}")
        print(f"  - 专业: {criteria.major}")
        print(f"  - 关键词: {criteria.keyword}")
        
        # 测试格式化
        desc = parser.format_criteria(criteria)
        print(f"✓ 条件描述: {desc}")
        
        # 测试 SearchService
        service = SearchService()
        print("✓ SearchService 实例化成功")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_skill_interface():
    """测试 Skill 接口"""
    print("\n" + "=" * 50)
    print("测试 5: Skill 接口")
    print("=" * 50)
    
    try:
        import __init__ as skill
        
        # 测试 help
        help_text = skill.help()
        print("✓ help() 调用成功")
        print(f"  帮助文本长度: {len(help_text)} 字符")
        
        # 测试 metadata
        meta = skill.metadata()
        print("✓ metadata() 调用成功")
        print(f"  Skill 名称: {meta.get('name')}")
        print(f"  版本: {meta.get('version')}")
        
        # 测试 run (帮助请求)
        result = skill.run("help")
        print("✓ run('help') 调用成功")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search_functionality():
    """测试实际搜索功能（需要网络）"""
    print("\n" + "=" * 50)
    print("测试 6: 实际搜索功能（需要网络）")
    print("=" * 50)
    
    try:
        import __init__ as skill
        
        print("正在执行搜索测试，请稍候...")
        print("查询: 北京，硕士，近1个月")
        
        # 执行搜索
        result = skill.run("北京，硕士，近1个月")
        
        print("✓ 搜索完成")
        print(f"  结果长度: {len(result)} 字符")
        print("\n搜索结果预览（前200字符）:")
        print("-" * 50)
        print(result[:200])
        print("-" * 50)
        
        return True
    except Exception as e:
        print(f"✗ 搜索失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  gaoxiaorencai_search Skill 测试程序")
    print("=" * 60 + "\n")
    
    results = []
    
    # 运行所有测试
    results.append(("模块导入", test_import()))
    results.append(("工具函数", test_utils()))
    results.append(("解析器", test_parsers()))
    results.append(("核心模块", test_core()))
    results.append(("Skill 接口", test_skill_interface()))
    
    # 询问是否执行网络测试
    print("\n" + "=" * 50)
    response = input("是否执行网络搜索测试？(y/n): ")
    if response.lower() == 'y':
        results.append(("搜索功能", test_search_functionality()))
    else:
        print("跳过网络测试")
    
    # 打印总结
    print("\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status}: {name}")
    
    print("-" * 60)
    print(f"  总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n  🎉 所有测试通过！Skill 可以正常工作。")
    else:
        print(f"\n  ⚠️ 有 {total - passed} 项测试失败，请检查错误信息。")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
