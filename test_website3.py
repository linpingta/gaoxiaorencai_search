"""
检查职位数据 - 分析页面结构和AJAX接口
"""
import requests
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("分析职位数据加载方式")
print("=" * 60)

# 访问搜索页
resp = session.get("https://www.gaoxiaojob.com/job?keyword=教师", timeout=10)
html = resp.text

# 检查是否有职位列表容器
print("\n1. 检查职位列表容器:")
containers = [
    r'<div[^>]*class="[^"]*job[^"]*"[^>]*>',
    r'<div[^>]*class="[^"]*position[^"]*"[^>]*>',
    r'<div[^>]*class="[^"]*list[^"]*"[^>]*>',
    r'<ul[^>]*class="[^"]*list[^"]*"[^>]*>',
]
for pattern in containers:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"   找到 {len(matches)} 个匹配: {pattern}")
        if len(matches) <= 3:
            for m in matches:
                print(f"      {m[:100]}")

# 检查是否有初始数据嵌入在页面中
print("\n2. 检查页面内嵌数据:")
# 查找可能的JSON数据
json_patterns = [
    r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
    r'window\.__DATA__\s*=\s*({.*?});',
    r'var\s+initialData\s*=\s*({.*?});',
]
for pattern in json_patterns:
    match = re.search(pattern, html, re.DOTALL)
    if match:
        print(f"   ✓ 找到内嵌数据: {pattern}")
        try:
            data = json.loads(match.group(1))
            print(f"   数据类型: {type(data)}")
            if isinstance(data, dict):
                print(f"   数据键: {list(data.keys())[:5]}")
        except:
            print(f"   数据片段: {match.group(1)[:200]}")

# 检查AJAX接口
print("\n3. 检查可能的AJAX接口:")
api_patterns = [
    r'api["\']?\s*:\s*["\']([^"\']+)["\']',
    r'url["\']?\s*:\s*["\']([^"\']+job[^"\']*)["\']',
    r'url["\']?\s*:\s*["\']([^"\']+search[^"\']*)["\']',
]
for pattern in api_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        unique = list(set(matches))[:5]
        print(f"   找到API: {unique}")

# 检查Vue/React组件
print("\n4. 检查前端框架:")
if "vue" in html.lower():
    print("   ✓ 使用Vue.js")
if "react" in html.lower():
    print("   ✓ 使用React")
if "element-plus" in html.lower():
    print("   ✓ 使用Element Plus")

# 尝试直接访问API
print("\n5. 尝试访问API接口:")
api_urls = [
    "https://www.gaoxiaojob.com/api/job/search",
    "https://www.gaoxiaojob.com/api/jobs",
    "https://www.gaoxiaojob.com/job/list",
]
for url in api_urls:
    try:
        r = session.get(url, params={"keyword": "教师", "page": 1}, timeout=5)
        print(f"   {url}: {r.status_code}, 长度: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 100:
            print(f"      响应片段: {r.text[:200]}")
    except Exception as e:
        print(f"   {url}: 失败 - {e}")

# 检查页面是否有具体的职位信息
print("\n6. 检查具体职位信息:")
job_title_pattern = r'<a[^>]*href="[^"]*job[^"]*"[^>]*>([^<]+)</a>'
titles = re.findall(job_title_pattern, html)
if titles:
    print(f"   找到 {len(titles)} 个职位链接")
    for t in titles[:5]:
        print(f"      - {t.strip()}")

print("\n" + "=" * 60)
