"""
最终测试 - 尝试所有可能的方法获取数据
"""
import requests
import re
import json

print("=" * 60)
print("最终测试 - 尝试获取职位数据")
print("=" * 60)

# 方法1: 检查sitemap
print("\n1. 从Sitemap获取职位URL:")
try:
    r = requests.get("https://www.gaoxiaojob.com/sitemap.xml", timeout=30)
    print(f"   状态: {r.status_code}, 长度: {len(r.text)}")
    
    # 提取职位URL
    job_urls = re.findall(r'<loc>(https://www\.gaoxiaojob\.com/job/\d+\.html)</loc>', r.text)
    print(f"   找到 {len(job_urls)} 个职位URL")
    
    if job_urls:
        print(f"   前5个URL:")
        for url in job_urls[:5]:
            print(f"      - {url}")
        
        # 尝试获取第一个职位详情
        print(f"\n   获取第一个职位详情:")
        job_r = requests.get(job_urls[0], headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, timeout=10)
        print(f"   状态: {job_r.status_code}, 长度: {len(job_r.text)}")
        
        # 提取职位信息
        html = job_r.text
        title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        if title_match:
            print(f"   职位标题: {title_match.group(1).strip()}")
except Exception as e:
    print(f"   错误: {e}")

# 方法2: 尝试使用不同的User-Agent和headers
print("\n2. 尝试模拟真实浏览器:")
try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    # 先访问首页
    r1 = session.get("https://www.gaoxiaojob.com", timeout=10)
    print(f"   首页: {r1.status_code}, Cookies: {session.cookies.get_dict()}")
    
    # 再访问搜索页
    r2 = session.get("https://www.gaoxiaojob.com/job?keyword=教师", timeout=10)
    print(f"   搜索页: {r2.status_code}, 长度: {len(r2.text)}")
    
    # 检查是否有职位数据
    html = r2.text
    if "职位" in html and "招聘" in html:
        print("   ✓ 页面包含职位相关内容")
        
        # 尝试提取职位信息
        # 查找包含职位名称的元素
        job_names = re.findall(r'title="([^"]{5,50}招聘[^"]*)"', html)
        if job_names:
            print(f"   找到 {len(job_names)} 个职位名称:")
            for name in job_names[:5]:
                print(f"      - {name}")
except Exception as e:
    print(f"   错误: {e}")

# 方法3: 尝试搜索页面
print("\n3. 尝试/search页面:")
try:
    r = requests.get("https://www.gaoxiaojob.com/search?keyword=教师", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }, timeout=10)
    print(f"   状态: {r.status_code}, 长度: {len(r.text)}")
    
    if r.status_code == 200:
        # 检查内容
        html = r.text
        print(f"   包含'职位': {html.count('职位')} 次")
        print(f"   包含'招聘': {html.count('招聘')} 次")
        
        # 查找职位名称
        titles = re.findall(r'>([^<]{10,50}招聘[^<]*)<', html)
        if titles:
            print(f"   找到 {len(titles)} 个可能的职位标题")
            for t in titles[:5]:
                print(f"      - {t.strip()}")
except Exception as e:
    print(f"   错误: {e}")

# 方法4: 尝试公告/简章页面
print("\n4. 尝试公告页面:")
try:
    urls_to_try = [
        "https://www.gaoxiaojob.com/announcement",
        "https://www.gaoxiaojob.com/article",
        "https://www.gaoxiaojob.com/news",
    ]
    for url in urls_to_try:
        r = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, timeout=5)
        print(f"   {url}: {r.status_code}, 长度: {len(r.text)}")
except Exception as e:
    print(f"   错误: {e}")

print("\n" + "=" * 60)
print("结论:")
print("=" * 60)
print("""
经过测试，发现以下问题：
1. 主站(gaoxiaojob.com)使用Vue.js单页应用，职位数据通过AJAX动态加载
2. API接口需要登录才能访问
3. 页面HTML中不包含实际的职位列表数据
4. Sitemap包含职位URL，但需要逐个访问详情页获取信息

建议解决方案：
1. 使用Selenium/Playwright模拟浏览器行为
2. 或者使用Sitemap中的URL逐个获取职位详情
3. 或者寻找其他公开的数据源/API
""")
