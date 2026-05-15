"""
测试配置API - 获取职位分类数据
"""
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.gaoxiaojob.com/job",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("测试配置类API")
print("=" * 60)

# 测试配置API
config_apis = [
    "/api/config/get-all-category-job-list",
    "/api/config/get-hierarchy-city-list",
    "/api/config/get-education-list",
]

for api in config_apis:
    url = f"https://www.gaoxiaojob.com{api}"
    try:
        r = session.get(url, timeout=10)
        print(f"\n{api}:")
        print(f"  状态: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  响应码: {data.get('code')}")
                print(f"  消息: {data.get('msg')}")
                if data.get('data'):
                    print(f"  数据类型: {type(data['data'])}")
                    if isinstance(data['data'], list):
                        print(f"  数据条数: {len(data['data'])}")
                        if len(data['data']) > 0:
                            print(f"  第一条: {data['data'][0]}")
                    elif isinstance(data['data'], dict):
                        print(f"  数据键: {list(data['data'].keys())}")
            except:
                print(f"  响应: {r.text[:300]}")
    except Exception as e:
        print(f"{api}: 错误 - {e}")

# 尝试找到真正的职位列表API
print("\n" + "=" * 60)
print("尝试其他可能的职位API")
print("=" * 60)

# 可能是不同的路径格式
job_apis = [
    ("/api/job/list", {"page": 1, "limit": 20}),
    ("/api/position/list", {"page": 1, "limit": 20}),
    ("/api/recruit/list", {"page": 1, "limit": 20}),
    ("/api/announcement/list", {"page": 1, "limit": 20}),
    ("/api/search/list", {"page": 1, "limit": 20}),
    
    # 尝试POST
    ("/api/job/list", {}),
    ("/api/position/search", {"keyword": "教师"}),
]

for api, params in job_apis:
    url = f"https://www.gaoxiaojob.com{api}"
    try:
        if params:
            r = session.get(url, params=params, timeout=5)
        else:
            r = session.post(url, json={"page": 1, "limit": 20}, timeout=5)
        
        if r.status_code == 200:
            try:
                data = r.json()
                if data.get('code') == 1 and data.get('data'):
                    print(f"\n✓ {api}")
                    print(f"  参数: {params}")
                    print(f"  数据: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
            except:
                pass
    except:
        pass

# 尝试直接获取职位详情页看是否有列表
print("\n" + "=" * 60)
print("尝试获取职位详情页")
print("=" * 60)

# 先访问首页获取一些职位ID
try:
    r = session.get("https://www.gaoxiaojob.com", timeout=10)
    # 查找职位ID
    job_ids = re.findall(r'/job/(\d+)\.html', r.text)
    print(f"找到 {len(job_ids)} 个职位ID")
    for jid in job_ids[:5]:
        print(f"  - {jid}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 60)
