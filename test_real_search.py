"""
测试真实网络搜索 - 验证是否能获取gaoxiaojob.com的实际数据
"""
import sys
import os

# 添加skill目录到路径
skill_dir = os.path.join(os.path.dirname(__file__), '.trae', 'skills', 'gaoxiaorencai_search')
sys.path.insert(0, skill_dir)

from core import QueryParser, SearchEngine, ResultFormatter, SearchCriteria
from parsers import JobParser

print("=" * 60)
print("测试真实网络搜索 - 高校人才网(gaoxiaojob.com)")
print("=" * 60)

# 测试1: 搜索北京+博士
print("\n【测试1】搜索: 北京，博士")
print("-" * 40)

parser = QueryParser()
criteria = parser.parse("北京，博士")
print(f"解析结果: 地区={criteria.location}, 学历={criteria.education}, 关键词={criteria.keyword}")

engine = SearchEngine()
html = engine.search(keyword=criteria.keyword or "教师", location=criteria.location, education=criteria.education)

if html:
    print(f"✓ 成功获取HTML响应，长度: {len(html)} 字符")
    
    job_parser = JobParser()
    jobs = job_parser.parse_job_list(html)
    print(f"✓ 解析到 {len(jobs)} 个职位")
    
    if jobs:
        print("\n前3个职位:")
        for i, job in enumerate(jobs[:3], 1):
            print(f"  {i}. {job.title} | {job.company} | {job.location} | {job.publish_date}")
            print(f"     链接: {job.url}")
    else:
        # 检查HTML内容
        print("\n未能解析职位，检查HTML内容片段:")
        print(html[:500])
else:
    print("✗ 获取HTML失败")

# 测试2: 搜索AI方向
print("\n" + "=" * 60)
print("【测试2】搜索: AI方向")
print("-" * 40)

criteria2 = parser.parse("AI方向，近1个月")
print(f"解析结果: 专业={criteria2.major}, 时间范围={criteria2.time_range}")

html2 = engine.search(keyword="AI 人工智能", location="", education="")

if html2:
    print(f"✓ 成功获取HTML响应，长度: {len(html2)} 字符")
    
    jobs2 = job_parser.parse_job_list(html2)
    print(f"✓ 解析到 {len(jobs2)} 个职位")
    
    if jobs2:
        print("\n前3个职位:")
        for i, job in enumerate(jobs2[:3], 1):
            print(f"  {i}. {job.title} | {job.company} | {job.location}")
else:
    print("✗ 获取HTML失败")

# 测试3: 搜索上海+硕士
print("\n" + "=" * 60)
print("【测试3】搜索: 上海，硕士")
print("-" * 40)

html3 = engine.search(keyword="", location="上海", education="硕士")

if html3:
    print(f"✓ 成功获取HTML响应，长度: {len(html3)} 字符")
    
    jobs3 = job_parser.parse_job_list(html3)
    print(f"✓ 解析到 {len(jobs3)} 个职位")
    
    if jobs3:
        print("\n前3个职位:")
        for i, job in enumerate(jobs3[:3], 1):
            print(f"  {i}. {job.title} | {job.company} | {job.location}")
else:
    print("✗ 获取HTML失败")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
