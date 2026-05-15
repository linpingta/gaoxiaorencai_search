"""
从JS文件中提取API端点
"""
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("从JS文件中提取API端点")
print("=" * 60)

# 获取页面
resp = session.get("https://www.gaoxiaojob.com/job")
html = resp.text

# 提取JS文件URL
js_urls = re.findall(r'src="([^"]+\.js[^"]*)"', html)
print(f"找到 {len(js_urls)} 个JS文件引用")

all_apis = set()

for js_url in js_urls:
    # 处理URL
    if js_url.startswith('//'):
        js_url = 'https:' + js_url
    elif js_url.startswith('/'):
        js_url = 'https://www.gaoxiaojob.com' + js_url
    elif not js_url.startswith('http'):
        js_url = 'https://www.gaoxiaojob.com/' + js_url
    
    # 去除版本参数
    js_url_clean = js_url.split('?')[0]
    
    try:
        js_resp = session.get(js_url, timeout=10)
        if js_resp.status_code == 200:
            js_content = js_resp.text
            
            # 查找各种API模式
            patterns = [
                r'["\'](/api/[^"\'\s]+)["\']',
                r'["\'](api/[^"\'\s]+)["\']',
                r'url\s*:\s*["\']([^"\']*api[^"\']*)["\']',
                r'path\s*:\s*["\']([^"\']*api[^"\']*)["\']',
                r'baseURL\s*[=:]\s*["\']([^"\']+)["\']',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, js_content, re.IGNORECASE)
                for match in matches:
                    if len(match) > 5 and not any(x in match for x in ['.css', '.js', '.png', '.jpg']):
                        all_apis.add(match)
    except Exception as e:
        pass

print(f"\n找到 {len(all_apis)} 个可能的API端点:")
for api in sorted(all_apis):
    print(f"  - {api}")

# 测试找到的API
print("\n" + "=" * 60)
print("测试找到的API端点")
print("=" * 60)

# 优先测试看起来像是职位相关的API
job_related = [api for api in all_apis if any(x in api.lower() for x in ['job', 'position', 'search', 'list'])]

for api in list(job_related)[:10]:
    if not api.startswith('/'):
        api = '/' + api
    url = f"https://www.gaoxiaojob.com{api}"
    
    try:
        r = session.get(url, params={"page": 1, "limit": 10}, timeout=5)
        if r.status_code == 200:
            content_type = r.headers.get('Content-Type', '')
            print(f"\n{api}:")
            print(f"  状态: {r.status_code}, Content-Type: {content_type}")
            if 'json' in content_type:
                print(f"  响应: {r.text[:500]}")
    except Exception as e:
        pass

print("\n" + "=" * 60)
