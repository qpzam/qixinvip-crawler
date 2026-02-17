"""
启信宝爬虫主程序
"""
import asyncio
import json
import sys
import io
from typing import List

# 设置 stdout 为 UTF-8 编码，避免 Windows GBK 编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from crawler import QixinbaoCrawler
from exporter import get_exporter
from utils import load_config


async def single_company_test():
    """单个公司测试模式"""
    print("=" * 60)
    print("启信宝爬虫 - 单公司测试模式")
    print("=" * 60)

    # 加载配置
    config = load_config()

    # 检查Cookie
    if config.get('cookie') == 'your_cookie_string_here':
        print("\n[!] 错误: 请先在 config.json 中配置你的启信宝VIP Cookie")
        print("\n获取Cookie步骤:")
        print("1. 在浏览器中登录启信宝VIP账号")
        print("2. 按F12打开开发者工具")
        print("3. 切换到 Network 标签")
        print("4. 刷新页面")
        print("5. 找到任意请求，复制 Request Headers 中的 Cookie")
        print("6. 将Cookie粘贴到 config.json 文件中\n")
        return

    # 创建爬虫实例
    async with QixinbaoCrawler() as crawler:
        # 测试公司
        test_company = input("\n请输入要测试的公司名称: ").strip()

        if not test_company:
            test_company = "腾讯科技（深圳）有限公司"
            print(f"使用默认测试公司: {test_company}")

        # 爬取数据
        print(f"\n开始爬取 {test_company} 的信息...")
        print("-" * 60)

        data = await crawler.crawl_single_company(test_company)

        if data:
            print("\n" + "=" * 60)
            print("爬取成功! 数据如下:")
            print("=" * 60)
            print(json.dumps(data, ensure_ascii=False, indent=2))

            # 导出到Excel
            print("\n正在导出到Excel...")
            exporter = get_exporter(config)
            exporter.add_company(data)
            exporter.save()
        else:
            print("\n爬取失败，请检查:")
            print("1. Cookie是否正确配置")
            print("2. VIP账号是否有效")
            print("3. 网络连接是否正常")
            print("4. 公司名称是否正确")


async def batch_mode():
    """批量爬取模式"""
    print("=" * 60)
    print("启信宝爬虫 - 批量爬取模式")
    print("=" * 60)

    # 加载配置
    config = load_config()

    # 检查Cookie
    if config.get('cookie') == 'your_cookie_string_here':
        print("\n[!] 错误: 请先在 config.json 中配置你的启信宝VIP Cookie")
        return

    # 读取公司列表
    print("\n请选择输入方式:")
    print("1. 从Excel文件读取")
    print("2. 从CSV文件读取")
    print("3. 从文本文件读取")
    print("4. 手动输入")

    choice = input("\n请选择 (1-4): ").strip()

    company_names = []

    if choice == '1':
        import pandas as pd
        file_path = input("请输入Excel文件路径: ").strip()
        sheet_name = input("请输入工作表名称 (默认为第一个): ").strip() or 0
        column = input("请输入公司名称所在的列名: ").strip()

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            company_names = df[column].dropna().tolist()
            print(f"[OK] 读取到 {len(company_names)} 个公司")
        except Exception as e:
            print(f"[X] 读取文件失败: {e}")
            return

    elif choice == '2':
        import pandas as pd
        file_path = input("请输入CSV文件路径: ").strip()
        column = input("请输入公司名称所在的列名: ").strip()

        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            company_names = df[column].dropna().tolist()
            print(f"[OK] 读取到 {len(company_names)} 个公司")
        except Exception as e:
            print(f"[X] 读取文件失败: {e}")
            return

    elif choice == '3':
        file_path = input("请输入文本文件路径 (每行一个公司名): ").strip()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                company_names = [line.strip() for line in f if line.strip()]
            print(f"[OK] 读取到 {len(company_names)} 个公司")
        except Exception as e:
            print(f"[X] 读取文件失败: {e}")
            return

    elif choice == '4':
        print("\n请输入公司名称，每行一个，输入空行结束:")
        while True:
            company = input("> ").strip()
            if not company:
                break
            company_names.append(company)

    else:
        print("无效选择")
        return

    if not company_names:
        print("没有有效的公司名称")
        return

    # 创建导出器
    exporter = get_exporter(config)

    # 进度回调
    async def progress_callback(current, total, company_name, success):
        status = "[OK]" if success else "[X]"
        print(f"\n进度: {current}/{total} {status} {company_name}")

    # 开始爬取
    print(f"\n开始批量爬取 {len(company_names)} 个公司...")
    print("=" * 60)

    async with QixinbaoCrawler() as crawler:
        results = await crawler.crawl_batch(company_names, progress_callback)

        # 保存结果
        for result in results:
            if result:
                exporter.add_company(result)

        exporter.save()

        # 显示摘要
        summary = exporter.get_summary()
        print("\n" + "=" * 60)
        print("批量爬取完成!")
        print(f"总计: {summary['total']} 个公司")
        print(f"成功: {summary['successful']} 个")
        print(f"失败: {summary['failed']} 个")
        print("=" * 60)


async def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("启信宝爬虫 - 交互式模式")
    print("=" * 60)

    config = load_config()

    # 检查Cookie
    if config.get('cookie') == 'your_cookie_string_here':
        print("\n[!] 错误: 请先在 config.json 中配置你的启信宝VIP Cookie")
        return

    async with QixinbaoCrawler() as crawler:
        exporter = get_exporter(config)

        print("\n已就绪! 输入公司名称开始爬取，输入 'quit' 退出，'save' 保存")

        while True:
            company_name = input("\n请输入公司名称: ").strip()

            if company_name.lower() == 'quit':
                break

            elif company_name.lower() == 'save':
                exporter.save()
                continue

            elif not company_name:
                continue

            data = await crawler.crawl_single_company(company_name)

            if data:
                print("\n[OK] 爬取成功:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                exporter.add_company(data)

        # 退出前保存
        if exporter.data:
            print("\n正在保存数据...")
            exporter.save()


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("       启信宝 VIP 爬虫 v1.0")
    print("=" * 60)

    print("\n请选择运行模式:")
    print("1. 单公司测试模式 (推荐首次使用)")
    print("2. 批量爬取模式")
    print("3. 交互式模式")

    mode = input("\n请选择 (1-3): ").strip()

    try:
        if mode == '1':
            asyncio.run(single_company_test())
        elif mode == '2':
            asyncio.run(batch_mode())
        elif mode == '3':
            asyncio.run(interactive_mode())
        else:
            print("无效选择")
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
