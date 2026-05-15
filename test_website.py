"""
测试网站访问 - 检查gaoxiaojob.com的实际响应
"""
import requests
import time

# 测试1: 基础访问
print("=" * 60)
print("测试1: 基础访问 gaoxiaojob.com")
print("=" * 60)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

session = requests.Session()
session.headers.update(headers)

# 先访问首页获取cookie
print("\n访问首页...")
try:
    resp = session.get("https://www.gaoxiaojob.com", timeout=10)
    print(f"状态码: {resp.status_code}")
    print(f"响应长度: {len(resp.text)}")
    print(f"Cookies: {session.cookies.get_dict()}")
    
    if "验证码" in resp.text:
        print("⚠ 首页需要验证码")
    else:
        print("✓ 首页访问成功")
except Exception as e:
    print(f"✗ 访问失败: {e}")

# 测试2: 搜索页面
print("\n" + "=" * 60)
print("测试2: 访问搜索页面")
print("=" * 60)

time.sleep(2)

try:
    resp2 = session.get("https://www.gaoxiaojob.com/job", timeout=10)
    print(f"状态码: {resp2.status_code}")
    print(f"响应长度: {len(resp2.text)}")
    
    if "验证码" in resp2.text or "captcha" in resp2.text.lower():
        print("⚠ 搜索页面需要验证码")
        # 打印部分HTML查看
        print("\n响应内容片段:")
        print(resp2.text[:1000])
    else:
        print("✓ 搜索页面访问成功")
        # 检查是否有职位列表
        if "job" in resp2.text.lower() or "职位" in resp2.text:
            print("✓ 页面包含职位相关内容")
        else:
            print("? 页面可能不包含职位列表")
        print("\n响应内容片段:")
        print(resp2.text[:1500])
except Exception as e:
    print(f"✗ 访问失败: {e}")

# 测试3: 带参数的搜索
print("\n" + "=" * 60)
print("测试3: 带关键词搜索")
print("=" * 60)

time.sleep(2)

try:
    params = {"keyword": "教师", "page": 1}
    resp3 = session.get("https://www.gaoxiaojob.com/job", params=params, timeout=10)
    print(f"状态码: {resp3.status_code}")
    print(f"响应长度: {len(resp3.text)}")
    print(f"URL: {resp3.url}")
    
    if "验证码" in resp3.text:
        print("⚠ 搜索结果页需要验证码")
    else:
        print("✓ 搜索结果页访问成功")
        print("\n响应内容片段:")
        print(resp3.text[:1500])
except Exception as e:
    print(f"✗ 访问失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
