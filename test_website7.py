"""
尝试找到职位列表API - 通过分析页面请求
"""
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.gaoxiaojob.com/job",
    "X-Requested-With": "XMLHttpRequest",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("尝试找到职位搜索API")
print("=" * 60)

# 尝试一些常见的API路径
apis_to_try = [
    # 可能的分页列表API
    ("https://www.gaoxiaojob.com/api/announcement/job-list", {"page": 1, "limit": 20}),
    ("https://www.gaoxiaojob.com/api/job/announcement-list", {"page": 1, "limit": 20}),
    ("https://www.gaoxiaojob.com/api/person/announcement/job-list", {"page": 1, "limit": 20}),
    
    # 可能是不同的参数格式
    ("https://www.gaoxiaojob.com/api/announcement/job-list", {"page": 1, "pageSize": 20}),
    ("https://www.gaoxiaojob.com/api/announcement/job-list", {"current": 1, "size": 20}),
]

for url, params in apis_to_try:
    try:
        r = session.get(url, params=params, timeout=5)
        print(f"\n{url}")
        print(f"  参数: {params}")
        print(f"  状态: {r.status_code}")
        if r.status_code == 200:
            content_type = r.headers.get('Content-Type', '')
            print(f"  Content-Type: {content_type}")
            if 'json' in content_type:
                print(f"  响应: {r.text[:500]}")
    except Exception as e:
        print(f"{url}: 错误 - {e}")

# 尝试从页面中找到所有可能的API端点
print("\n" + "=" * 60)
print("从页面中提取所有API引用")
print("=" * 60)

resp = session.get("https://www.gaoxiaojob.com/job")
html = resp.text

# 查找所有/api/路径
api_paths = re.findall(r'["\'](/api/[^"\'\s<>]+)["\']', html)
unique_apis = sorted(set(api_paths))
print(f"找到 {len(unique_apis)} 个API路径:")
for api in unique_apis:
    print(f"  - {api}")

# 测试这些API
print("\n" + "=" * 60)
print("测试提取的API")
print("=" * 60)

for api in unique_apis[:10]:
    if 'job' in api.lower() or 'list' in api.lower():
        url = f"https://www.gaoxiaojob.com{api}"
        try:
            r = session.get(url, timeout=5)
            if r.status_code == 200:
                content_type = r.headers.get('Content-Type', '')
                if 'json' in content_type:
                    print(f"\n✓ {api}")
                    print(f"  响应: {r.text[:400]}")
        except:
            pass

print("\n" + "=" * 60)
