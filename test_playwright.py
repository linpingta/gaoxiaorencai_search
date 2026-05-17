"""
使用Playwright测试获取实际数据
"""
import asyncio
from playwright.async_api import async_playwright

async def test_playwright():
    print("=" * 60)
    print("使用Playwright测试获取职位数据")
    print("=" * 60)
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            # 访问高校人才网
            print("\n1. 访问首页...")
            await page.goto("https://www.gaoxiaojob.com", wait_until="networkidle", timeout=30000)
            print("   ✓ 首页加载完成")
            
            # 等待页面加载
            await page.wait_for_timeout(2000)
            
            # 访问搜索页
            print("\n2. 访问搜索页...")
            await page.goto("https://www.gaoxiaojob.com/job?keyword=教师", wait_until="networkidle", timeout=30000)
            print("   ✓ 搜索页加载完成")
            
            # 等待职位列表加载
            await page.wait_for_timeout(3000)
            
            # 尝试多种选择器查找职位
            selectors = [
                ".job-item",
                ".position-item", 
                ".list-item",
                "[class*='job']",
                "[class*='position']",
            ]
            
            print("\n3. 查找职位元素...")
            jobs_found = False
            for selector in selectors:
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"   ✓ 找到 {len(elements)} 个元素 (选择器: {selector})")
                    jobs_found = True
                    
                    # 提取前3个职位的信息
                    print("\n4. 提取职位信息:")
                    for i, elem in enumerate(elements[:3]):
                        try:
                            # 尝试获取文本内容
                            text = await elem.inner_text()
                            if text.strip():
                                print(f"   职位 {i+1}: {text.strip()[:100]}...")
                        except:
                            pass
                    break
            
            if not jobs_found:
                print("   ✗ 未找到职位元素")
                # 获取页面HTML查看
                html = await page.content()
                print(f"\n   页面HTML长度: {len(html)}")
                
                # 检查是否有职位相关文本
                if "职位" in html:
                    print("   ✓ 页面包含'职位'文本")
                if "招聘" in html:
                    print("   ✓ 页面包含'招聘'文本")
            
            # 截图保存
            await page.screenshot(path="screenshot.png")
            print("\n5. 已保存截图: screenshot.png")
            
        except Exception as e:
            print(f"\n错误: {e}")
        finally:
            await browser.close()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_playwright())
