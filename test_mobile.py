"""
深入检查移动端网站
"""
import requests
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("检查移动端网站")
print("=" * 60)

# 访问移动端首页
print("\n1. 访问移动端首页:")
r = session.get("https://m.gaoxiaojob.com", timeout=10)
print(f"   状态: {r.status_code}, 长度: {len(r.text)}")

# 查找职位数据
html = r.text

# 查找职位标题
print("\n2. 查找职位信息:")
job_patterns = [
    r'<a[^>]*href="[^"]*/job/[^"]*"[^>]*>([^<]+)</a>',
    r'<div[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</div>',
    r'<span[^>]*class="[^"]*job[^"]*"[^>]*>([^<]+)</span>',
]

for pattern in job_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        print(f"   找到 {len(matches)} 个匹配")
        for m in matches[:5]:
            text = re.sub(r'<[^>]+>', '', m).strip()
            if text and len(text) > 3:
                print(f"      - {text}")

# 查找内嵌JSON数据
print("\n3. 查找内嵌JSON数据:")
json_patterns = [
    r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
    r'window\.__DATA__\s*=\s*({.*?});',
]
for pattern in json_patterns:
    match = re.search(pattern, html, re.DOTALL)
    if match:
        print(f"   ✓ 找到内嵌数据!")
        try:
            data = json.loads(match.group(1))
            print(f"   数据类型: {type(data)}")
        except:
            print(f"   数据片段: {match.group(1)[:300]}")

# 访问移动端搜索页
print("\n4. 访问移动端搜索页:")
r2 = session.get("https://m.gaoxiaojob.com/job?keyword=教师", timeout=10)
print(f"   状态: {r2.status_code}, 长度: {len(r2.text)}")

# 查找职位列表
html2 = r2.text
print("\n5. 在搜索页查找职位:")

# 查找职位链接
job_links = re.findall(r'href="(/job/[^"]+)"[^>]*>([^<]+)', html2)
if job_links:
    print(f"   找到 {len(job_links)} 个职位链接")
    for link, title in job_links[:10]:
        title_clean = re.sub(r'<[^>]+>', '', title).strip()
        if title_clean and len(title_clean) > 3:
            print(f"      - {title_clean} ({link})")

# 查找JSON数据
print("\n6. 查找搜索页的JSON数据:")
for pattern in json_patterns:
    match = re.search(pattern, html2, re.DOTALL)
    if match:
        print(f"   ✓ 找到内嵌数据!")
        try:
            data = json.loads(match.group(1))
            print(f"   数据键: {list(data.keys()) if isinstance(data, dict) else 'list with ' + str(len(data)) + ' items'}")
            print(f"   数据: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
        except Exception as e:
            print(f"   解析错误: {e}")
            print(f"   数据片段: {match.group(1)[:500]}")

# 查找script标签中的数据
print("\n7. 检查script标签:")
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html2, re.DOTALL)
for i, script in enumerate(scripts):
    if 'job' in script.lower() or 'list' in script.lower() or 'data' in script.lower():
        if len(script) > 500 and len(script) < 10000:
            print(f"\n   Script {i+1} (长度: {len(script)}):")
            # 尝试提取JSON
            json_matches = re.findall(r'[{\[][^\n]{100,5000}[}\]]', script)
            for jm in json_matches[:2]:
                try:
                    data = json.loads(jm)
                    print(f"   JSON数据: {json.dumps(data, ensure_ascii=False, indent=2)[:300]}")
                except:
                    pass

print("\n" + "=" * 60)
