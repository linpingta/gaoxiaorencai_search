"""
详细检查网站响应 - 分析验证码检测逻辑
"""
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("检查网站响应内容")
print("=" * 60)

resp = session.get("https://www.gaoxiaojob.com/job?keyword=教师", timeout=10)
html = resp.text

# 检查验证码关键词的位置
print("\n1. 检查'验证码'关键词:")
if "验证码" in html:
    idx = html.find("验证码")
    print(f"   找到'验证码'，位置: {idx}")
    print(f"   上下文: ...{html[max(0,idx-50):idx+50]}...")
else:
    print("   未找到'验证码'关键词")

# 检查captcha
print("\n2. 检查'captcha'关键词:")
if "captcha" in html.lower():
    idx = html.lower().find("captcha")
    print(f"   找到'captcha'，位置: {idx}")
    print(f"   上下文: ...{html[max(0,idx-50):idx+50]}...")
else:
    print("   未找到'captcha'关键词")

# 检查是否有职位列表相关的内容
print("\n3. 检查职位列表相关内容:")
job_keywords = ["职位", "招聘", "job-title", "job-item", "position-list", "list-item"]
for kw in job_keywords:
    if kw in html:
        count = html.count(kw)
        print(f"   ✓ 找到 '{kw}': {count} 次")

# 检查页面主要内容
print("\n4. 页面主要内容区域:")
# 尝试提取body内容
body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
if body_match:
    body = body_match.group(1)
    print(f"   Body长度: {len(body)} 字符")
    
    # 检查是否有实际的职位数据
    if "暂无数据" in html:
        print("   ⚠ 页面显示'暂无数据'")
    if "没有相关职位" in html:
        print("   ⚠ 页面显示'没有相关职位'")

# 检查script标签中的数据
print("\n5. 检查Script标签中的数据:")
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"   找到 {len(scripts)} 个script标签")
for i, script in enumerate(scripts[:3]):
    if len(script.strip()) > 100:
        print(f"   Script {i+1} 长度: {len(script)} 字符")

# 打印页面可见文本内容（去除标签）
print("\n6. 页面可见文本片段:")
# 简单的标签去除
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(f"   纯文本长度: {len(text)} 字符")
print(f"   前500字符: {text[:500]}")

print("\n" + "=" * 60)
