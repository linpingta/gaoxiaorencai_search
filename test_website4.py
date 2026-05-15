"""
查找正确的API端点 - 分析Vue应用的网络请求
"""
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.gaoxiaojob.com/job",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("尝试各种API端点")
print("=" * 60)

# 常见的API模式
api_endpoints = [
    # 直接搜索
    "https://www.gaoxiaojob.com/api/job/list",
    "https://www.gaoxiaojob.com/api/jobs/list",
    "https://www.gaoxiaojob.com/api/search/jobs",
    "https://www.gaoxiaojob.com/api/v1/jobs",
    "https://www.gaoxiaojob.com/api/position/list",
    
    # 带完整路径
    "https://www.gaoxiaojob.com/index.php/api/job/list",
    "https://www.gaoxiaojob.com/index.php/api/jobs",
    
    # 可能的移动端API
    "https://m.gaoxiaojob.com/api/job/list",
    "https://api.gaoxiaojob.com/job/list",
]

params_list = [
    {"keyword": "教师", "page": 1, "limit": 20},
    {"keyword": "教师", "page": 1, "size": 20},
    {"q": "教师", "page": 1},
    {"search": "教师", "page": 1},
]

for endpoint in api_endpoints[:5]:  # 测试前5个
    print(f"\n测试: {endpoint}")
    for params in params_list[:2]:  # 测试前2种参数
        try:
            r = session.get(endpoint, params=params, timeout=5)
            if r.status_code == 200:
                content_type = r.headers.get('Content-Type', '')
                print(f"  参数 {params}: {r.status_code}, Content-Type: {content_type}")
                if 'json' in content_type or r.text.startswith('{'):
                    print(f"    ✓ 可能是JSON API!")
                    print(f"    响应: {r.text[:300]}")
                    break
                elif len(r.text) > 500:
                    print(f"    响应长度: {len(r.text)}")
            else:
                print(f"  参数 {params}: {r.status_code}")
        except Exception as e:
            print(f"  参数 {params}: 错误 - {str(e)[:50]}")

# 检查页面JS文件中的API定义
print("\n" + "=" * 60)
print("从JS文件中查找API")
print("=" * 60)

resp = session.get("https://www.gaoxiaojob.com/job", headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})
html = resp.text

# 提取JS文件URL
js_urls = re.findall(r'src="([^"]+\.js)"', html)
print(f"找到 {len(js_urls)} 个JS文件")

for js_url in js_urls[:3]:
    if js_url.startswith('//'):
        js_url = 'https:' + js_url
    elif js_url.startswith('/'):
        js_url = 'https://www.gaoxiaojob.com' + js_url
    
    try:
        js_resp = session.get(js_url, timeout=5)
        if js_resp.status_code == 200:
            js_content = js_resp.text
            # 查找API路径
            api_matches = re.findall(r'["\'](/api/[^"\'\s]+)["\']', js_content)
            if api_matches:
                unique_apis = list(set(api_matches))[:5]
                print(f"\n  {js_url.split('/')[-1]}:")
                for api in unique_apis:
                    print(f"    - {api}")
    except:
        pass

print("\n" + "=" * 60)
