# 电商用户行为数据仓库与可视化看板

## 项目背景
本项目模拟电商平台的离线数据仓库建设，对用户行为数据（点击、收藏、加购、购买）进行 ETL 处理，并产出业务报表，最终通过 Flask + ECharts 实现可视化看板。

## 技术栈
- Python (pandas, sqlalchemy, pymysql)
- MySQL (数据仓库)
- Flask (Web 后端)
- ECharts (数据可视化)

## 数据源
阿里云天池 - 淘宝用户行为数据集（约 200 万条记录）

## 系统架构
![架构图.png](%E6%9E%B6%E6%9E%84%E5%9B%BE.png)

## 数据流转
CSV → ODS(原始层) → DWD(明细层) → DWS(汇总层) → ADS(应用层) → 可视化看板

## 核心功能
1. 自动化 ETL：分块读取大数据文件，清洗并存入 MySQL DWD 表
2. 数仓分层建模：ODS → DWD → DWS → ADS
3. 业务指标分析：日活跃用户(DAU)、转化漏斗、热门商品等
4. 可视化看板：展示 DAU 趋势图

## 如何运行

### 1. 环境准备
- 安装 MySQL 8.0+
- 创建数据库 `itcast`
- 安装 Python 依赖：`pip install -r requirements.txt`

### 2. 执行 ETL
```bash
# 创建表
mysql -u root -p itcast < etl/create_tables.sql
# 运行 DWD ETL（需要修改文件路径）
python etl/dwd_etl.py
# 执行 DWS 和 ADS 聚合
mysql -u root -p itcast < etl/dws_etl.sql
mysql -u root -p itcast < etl/ads_etl.sql
```
### 3. 启动可视化看板
```bash
cd flask_app
python app.py
```
- 访问 http://127.0.0.1:5000 查看图表。

- 项目效果
https://images/dau_chart.png

- 下一步优化
使用调度工具（如 Airflow）定时执行 ETL、
部署到云服务器

作者
平成城
GitHub: [你的主页链接]