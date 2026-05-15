"""
尝试其他数据源 - RSS、Sitemap等
"""
import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

session = requests.Session()
session.headers.update(headers)

print("=" * 60)
print("尝试其他数据源")
print("=" * 60)

# 尝试RSS
print("\n1. 尝试RSS feed:")
rss_urls = [
    "https://www.gaoxiaojob.com/rss",
    "https://www.gaoxiaojob.com/rss.xml",
    "https://www.gaoxiaojob.com/feed",
    "https://www.gaoxiaojob.com/feed.xml",
]
for url in rss_urls:
    try:
        r = session.get(url, timeout=5)
        print(f"   {url}: {r.status_code}, 长度: {len(r.text)}")
        if r.status_code == 200 and ('rss' in r.text or 'feed' in r.text):
            print(f"   ✓ 可能是RSS!")
    except Exception as e:
        print(f"   {url}: 错误")

# 尝试Sitemap
print("\n2. 尝试Sitemap:")
sitemap_urls = [
    "https://www.gaoxiaojob.com/sitemap.xml",
    "https://www.gaoxiaojob.com/sitemap.html",
]
for url in sitemap_urls:
    try:
        r = session.get(url, timeout=5)
        print(f"   {url}: {r.status_code}, 长度: {len(r.text)}")
    except:
        pass

# 尝试移动端网站
print("\n3. 尝试移动端网站:")
mobile_urls = [
    "https://m.gaoxiaojob.com/job",
    "https://m.gaoxiaojob.com",
]
for url in mobile_urls:
    try:
        r = session.get(url, headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        }, timeout=5)
        print(f"   {url}: {r.status_code}, 长度: {len(r.text)}")
        if r.status_code == 200:
            # 检查是否有职位数据
            if "job" in r.text.lower() or "职位" in r.text:
                print(f"   ✓ 包含职位相关内容")
    except:
        pass

# 尝试不同的搜索端点
print("\n4. 尝试不同的搜索端点:")
search_endpoints = [
    "https://www.gaoxiaojob.com/search",
    "https://www.gaoxiaojob.com/search/result",
    "https://www.gaoxiaojob.com/list",
    "https://www.gaoxiaojob.com/jobs",
    "https://www.gaoxiaojob.com/position",
]
for url in search_endpoints:
    try:
        r = session.get(url, params={"keyword": "教师"}, timeout=5)
        print(f"   {url}: {r.status_code}, 长度: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 10000:
            # 检查是否有职位数据
            job_count = r.text.count('job') + r.text.count('职位')
            print(f"      职位相关关键词出现 {job_count} 次")
    except:
        pass

# 尝试直接获取职位列表HTML
print("\n5. 分析/job页面的职位数据:")
try:
    r = session.get("https://www.gaoxiaojob.com/job?keyword=教师", timeout=10)
    html = r.text
    
    # 查找职位标题模式
    print("   查找职位标题模式...")
    
    # 尝试多种模式
    patterns = [
        r'<a[^>]*href="[^"]*job/detail[^"]*"[^>]*>([^<]+)</a>',
        r'<a[^>]*href="[^"]*/job/\d+\.html"[^>]*>([^<]+)</a>',
        r'data-job[^>]*>([^<]+)</a>',
        r'title="([^"]*招聘[^"]*)"',
        r'title="([^"]*教师[^"]*)"',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            print(f"   模式 '{pattern[:50]}...' 找到 {len(matches)} 个匹配")
            for m in matches[:5]:
                print(f"      - {m.strip()}")
    
    # 检查是否有Vue的数据绑定
    print("\n   检查Vue数据绑定:")
    vue_patterns = [
        r':title="([^"]+)"',
        r'v-text="([^"]+)"',
        r'\{\{\s*([^}]+)\s*\}\}',
    ]
    for pattern in vue_patterns:
        matches = re.findall(pattern, html)
        if matches:
            print(f"   找到 {len(matches)} 个Vue绑定")
            break
    
    # 检查页面源码中的职位信息
    print("\n   搜索具体职位名称:")
    job_keywords = ["教授", "讲师", "博士后", "研究员", "教师"]
    for kw in job_keywords:
        if kw in html:
            # 找到关键词周围的文本
            idx = html.find(kw)
            context = html[max(0, idx-100):idx+100]
            # 去除HTML标签
            text = re.sub(r'<[^>]+>', ' ', context)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 20:
                print(f"   找到 '{kw}': {text[:80]}...")
                break

except Exception as e:
    print(f"   错误: {e}")

print("\n" + "=" * 60)
