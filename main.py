"""
高校人才网实时搜索 - 主入口

命令行工具入口，支持直接运行搜索
"""
import sys
import argparse

from core import search
from utils import logger


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="高校人才网(gaoxiaojob.com)招聘信息实时搜索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py "北京，硕士，AI方向，近1个月"
  python main.py "上海，博士，计算机"
  python main.py "广州，本科，教育类，近3个月"
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="搜索查询（格式：地区，学历，专业方向，时效范围）"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="交互模式"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细日志"
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        import logging
        logger.setLevel(logging.DEBUG)
    
    # 交互模式
    if args.interactive or not args.query:
        run_interactive()
    else:
        # 单次搜索
        result = search(args.query)
        print(result)


def run_interactive():
    """交互模式"""
    print("=" * 60)
    print("高校人才网实时搜索工具")
    print("=" * 60)
    print()
    print("输入格式：地区，学历，专业方向，时效范围")
    print("示例：北京，硕士，AI方向，近1个月")
    print()
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'help' 获取帮助")
    print("-" * 60)
    print()
    
    while True:
        try:
            query = input("请输入搜索条件: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ["quit", "exit", "q", "退出"]:
                print("再见！")
                break
            
            if query.lower() in ["help", "?", "帮助"]:
                print_help()
                continue
            
            print()
            print("正在搜索，请稍候...")
            print()
            
            result = search(query)
            print(result)
            print()
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            print()


def print_help():
    """打印帮助信息"""
    help_text = """
【使用帮助】

输入格式：地区，学历，专业方向，时效范围

参数说明：
  地区：北京、上海、广州、深圳、杭州、南京等
  学历：本科、硕士、博士、博士后
  专业方向：AI、计算机、自动化、教育、医学等
  时效范围：近7天、近1个月、近3个月、近半年

示例：
  北京，硕士，AI方向，近1个月
  上海，博士，计算机，近7天
  广州，本科，教育类
  深圳，硕士，近3个月

注意事项：
  1. 地区、学历、专业方向至少提供一个
  2. 时效范围默认为近1个月
  3. 多个条件用逗号或空格分隔
  4. 搜索耗时约3-5秒，请耐心等待

命令：
  help  - 显示此帮助
  quit  - 退出程序
"""
    print(help_text)


if __name__ == "__main__":
    main()
