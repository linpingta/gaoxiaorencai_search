"""
尝试其他方法获取职位数据
"""
import requests
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("尝试各种搜索参数组合")
print("=" * 60)

# 测试不同的搜索URL模式
search_urls = [
    "https://www.gaoxiaojob.com/job/search",
    "https://www.gaoxiaojob.com/search/job",
    "https://www.gaoxiaojob.com/job/index",
    "https://www.gaoxiaojob.com/index/job",
]

for url in search_urls:
    try:
        r = session.get(url, params={"keyword": "教师"}, timeout=5)
        print(f"{url}: {r.status_code}, 长度: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 10000:
            print(f"  ✓ 可能包含数据")
    except Exception as e:
        print(f"{url}: 错误 - {e}")

# 尝试POST请求
print("\n" + "=" * 60)
print("尝试POST请求")
print("=" * 60)

post_urls = [
    "https://www.gaoxiaojob.com/api/job/list",
    "https://www.gaoxiaojob.com/api/jobs",
]

for url in post_urls:
    try:
        r = session.post(url, json={"keyword": "教师", "page": 1}, timeout=5)
        print(f"POST {url}: {r.status_code}")
        print(f"  响应: {r.text[:300]}")
    except Exception as e:
        print(f"POST {url}: 错误 - {e}")

# 检查页面中是否有隐藏的数据
print("\n" + "=" * 60)
print("检查页面隐藏数据")
print("=" * 60)

resp = session.get("https://www.gaoxiaojob.com/job?keyword=教师")
html = resp.text

# 查找可能包含职位数据的元素
print("\n1. 查找职位相关div:")
div_pattern = r'<div[^>]*>([^<]{20,200})</div>'
divs = re.findall(div_pattern, html)
job_related_divs = [d for d in divs if any(k in d for k in ['招聘', '教师', '教授', '博士', '硕士', '学院', '大学'])]
print(f"   找到 {len(job_related_divs)} 个可能相关的div")
for d in job_related_divs[:5]:
    print(f"   - {d[:80]}...")

# 查找所有链接文本
print("\n2. 查找链接文本:")
link_pattern = r'<a[^>]*href="/job/[^"]*"[^>]*>([^<]+)</a>'
links = re.findall(link_pattern, html)
print(f"   找到 {len(links)} 个职位链接")
for link in links[:10]:
    print(f"   - {link.strip()}")

# 检查是否有script标签中的JSON数据
print("\n3. 检查script标签中的数据:")
script_pattern = r'<script[^>]*>(.*?)</script>'
scripts = re.findall(script_pattern, html, re.DOTALL)
for i, script in enumerate(scripts):
    if 'job' in script.lower() or 'position' in script.lower() or 'list' in script.lower():
        if len(script) > 200 and len(script) < 5000:
            print(f"\n   Script {i+1} (长度: {len(script)}):")
            print(f"   {script[:500]}...")

print("\n" + "=" * 60)
