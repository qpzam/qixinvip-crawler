"""
数据导出模块
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict
from utils import generate_timestamp, sanitize_filename


class ExcelExporter:
    """Excel导出器"""

    def __init__(self, config: Dict):
        """
        初始化导出器

        Args:
            config: 配置字典
        """
        self.config = config
        self.output_config = config.get('output', {})
        self.data: List[Dict] = []

        # 生成文件名
        base_filename = self.output_config.get('filename', 'qixinbao_companies')
        if self.output_config.get('timestamp', True):
            self.filename = f"{base_filename}_{generate_timestamp()}.xlsx"
        else:
            self.filename = f"{base_filename}.xlsx"

        # 清理文件名
        self.filename = sanitize_filename(self.filename)

    def add_company(self, company_data: Dict):
        """
        添加公司数据

        Args:
            company_data: 公司数据字典
        """
        self.data.append(company_data)
        print(f"已添加: {company_data.get('company_name', 'Unknown')}")

    def save(self):
        """保存数据到Excel文件"""
        if not self.data:
            print("没有数据需要保存")
            return

        # 创建DataFrame
        df = pd.DataFrame(self.data)

        # 定义列顺序和中文列名
        column_mapping = {
            'company_name': '公司名称',
            'legal_person': '法定代表人',
            'registered_capital': '注册资本',
            'establish_date': '成立日期',
            'status': '经营状态',
            'phone': '联系电话',
            'email': '企业邮箱',
            'address': '注册地址',
            'business_scope': '经营范围',
            'industry': '所属行业',
            'taxpayer_type': '纳税人资质',
            'organization_code': '统一社会信用代码',
            'shareholders': '股东信息',
            'executives': '主要人员',
            'branches': '分支机构',
            'crawl_time': '爬取时间'
        }

        # 只保留存在的列
        existing_columns = [col for col in column_mapping.keys() if col in df.columns]
        if existing_columns:
            df = df[existing_columns]
            # 重命名列为中文
            df.rename(columns=column_mapping, inplace=True)

        # 保存到Excel
        try:
            df.to_excel(self.filename, index=False, engine='openpyxl')
            print(f"\n[OK] 数据已成功保存到: {self.filename}")
            print(f"[OK] 共保存 {len(self.data)} 条记录")
            print(f"[OK] 包含 {len(df.columns)} 个字段")
        except Exception as e:
            print(f"保存失败: {e}")
            raise

    def get_summary(self) -> Dict:
        """获取数据摘要"""
        if not self.data:
            return {'total': 0, 'successful': 0, 'failed': 0}

        total = len(self.data)
        successful = sum(1 for item in self.data if item.get('company_name') != 'N/A')
        failed = total - successful

        return {
            'total': total,
            'successful': successful,
            'failed': failed
        }


class CSVExporter:
    """CSV导出器"""

    def __init__(self, config: Dict):
        """
        初始化CSV导出器

        Args:
            config: 配置字典
        """
        self.config = config
        self.output_config = config.get('output', {})
        self.data: List[Dict] = []

        # 生成文件名
        base_filename = self.output_config.get('filename', 'qixinbao_companies')
        if self.output_config.get('timestamp', True):
            self.filename = f"{base_filename}_{generate_timestamp()}.csv"
        else:
            self.filename = f"{base_filename}.csv"

    def add_company(self, company_data: Dict):
        """添加公司数据"""
        self.data.append(company_data)

    def save(self):
        """保存数据到CSV文件"""
        if not self.data:
            print("没有数据需要保存")
            return

        df = pd.DataFrame(self.data)

        # 列名映射
        column_mapping = {
            'company_name': '公司名称',
            'legal_person': '法定代表人',
            'registered_capital': '注册资本',
            'establish_date': '成立日期',
            'status': '经营状态',
            'phone': '联系电话',
            'email': '企业邮箱',
            'address': '注册地址',
            'shareholders': '股东信息',
            'executives': '主要人员'
        }

        existing_columns = [col for col in column_mapping.keys() if col in df.columns]
        if existing_columns:
            df = df[existing_columns]
            df.rename(columns=column_mapping, inplace=True)

        df.to_csv(self.filename, index=False, encoding='utf-8-sig')
        print(f"数据已保存到: {self.filename}")


def get_exporter(config: Dict):
    """
    根据配置获取导出器

    Args:
        config: 配置字典

    Returns:
        导出器实例
    """
    output_format = config.get('output', {}).get('format', 'excel').lower()

    if output_format == 'csv':
        return CSVExporter(config)
    else:
        return ExcelExporter(config)
