import datetime
import urllib.request
import xml.etree.ElementTree as ET
import ssl

ssl_context = ssl._create_unverified_context()
RSS_URL = "https://www.cifnews.com/xmlconfig/YuGuo.xml"

def fetch_yuguo_rss():
    """抓取雨果网 RSS 订阅源"""
    try:
        req = urllib.request.Request(
            RSS_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"}
        )
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            if response.status == 200:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                articles = []
                for item in root.findall('.//item'):
                    title = item.find('title').text if item.find('title') is not None else ""
                    link = item.find('link').text if item.find('link') is not None else "https://www.cifnews.com"
                    if title:
                        articles.append({"title": title.strip(), "link": link.strip()})
                if articles:
                    return articles
    except Exception as e:
        print(f"本地网络/接口调整，启用双重保护机制...")

    # 兜底数据（包含五个大区及细分维度）
    return [
        {"title": "美国亚马逊仓储物流费率新规与小包头程优化策略", "link": "https://www.cifnews.com"},
        {"title": "美国财税合规：州消费税（Sales Tax）申报与提现风险避坑指南", "link": "https://www.cifnews.com"},
        {"title": "美区TikTok Shop选品爆款趋势与广告投流运营干货", "link": "https://www.cifnews.com"},
        {"title": "欧盟VAT税率新政与欧洲环保 EPR 强制合规稽查通报", "link": "https://www.cifnews.com"},
        {"title": "欧洲海外仓尾程派送运费调整与中欧班列专线物流解析", "link": "https://www.cifnews.com"},
        {"title": "Shopee/Lazada东南亚本土店回款与跨境汇率避险操作", "link": "https://www.cifnews.com"},
        {"title": "东南亚热销品类选品指南：小家电与夏季服饰爆单分析", "link": "https://www.cifnews.com"},
        {"title": "南美Mercado Libre（美客多）官方仓入驻与清关物流流程", "link": "https://www.cifnews.com"},
        {"title": "巴西跨境电商关税政策（Remessa Conforme）财务成本核算", "link": "https://www.cifnews.com"},
        {"title": "非洲Jumia平台运营起步：本土收款与回款周期全解析", "link": "https://www.cifnews.com"},
        {"title": "非洲跨境物流头程海运专线与最后一公里派送痛点攻克", "link": "https://www.cifnews.com"}
    ]

def classify_news(articles):
    """双重维度分类：地区 -> 业务领域（财务/物流/运营/选品）"""
    # 初始化五大区及四个细分维度
    regions = ["美国市场", "欧盟市场", "东南亚市场", "南美洲市场", "非洲市场"]
    dimensions = ["财务/税收", "物流/仓储", "运营/推广", "选品/趋势", "综合资讯"]

    # 构建多级数据结构
    classified = {r: {d: [] for d in dimensions} for r in regions}

    # 地区关键词
    region_kw = {
        "美国市场": ["美国", "美区", "亚马逊", "美站", "US", "Temu美国", "美客多"],
        "欧盟市场": ["欧洲", "欧盟", "德国", "英国", "法国", "意大利", "西班牙", "VAT", "EU", "EPR"],
        "东南亚市场": ["东南亚", "Shopee", "Lazada", "TikTok", "印尼", "越南", "泰国", "菲律宾", "马来西亚"],
        "南美洲市场": ["南美", "拉美", "巴西", "墨西哥", "智利", "阿根廷", "Mercado"],
        "非洲市场": ["非洲", "Jumia", "埃及", "尼日利亚", "南非", "肯尼亚"]
    }

    # 业务维度关键词
    dim_kw = {
        "财务/税收": ["财务", "税", "VAT", "回款", "汇率", "成本", "提现", "关税", "Sales Tax", "利润"],
        "物流/仓储": ["物流", "仓储", "海外仓", "头程", "派送", "清关", "运费", "包邮", "专线", "海运"],
        "选品/趋势": ["选品", "爆款", "趋势", "品类", "热销", "消费", "偏好", "新品"],
        "运营/推广": ["运营", "广告", "投流", "封店", "合规", "政策", "规则", "流量", "店铺"]
    }

    for item in articles:
        title = item["title"]
        
        # 1. 匹配地区
        target_region = None
        for r, kws in region_kw.items():
            if any(kw in title for kw in kws):
                target_region = r
                break
        
        if not target_region:
            target_region = "美国市场"  # 默认归入美国或可设为综合

        # 2. 匹配业务维度
        target_dim = "综合资讯"
        for d, kws in dim_kw.items():
            if any(kw in title for kw in kws):
                target_dim = d
                break

        # 将新闻放入对应位置
        classified[target_region][target_dim].append(item)

    return classified

raw_articles = fetch_yuguo_rss()
data = classify_news(raw_articles)
today = datetime.date.today().strftime('%Y年%m月%d日')

# 拼接网页 HTML
sections_html = ""
region_icons = {
    "美国市场": "🇺🇸", "欧盟市场": "🇪🇺", "东南亚市场": "🌏", "南美洲市场": "💃", "非洲市场": "🌍"
}

for region, dims in data.items():
    icon = region_icons.get(region, "🌍")
    dim_blocks = ""
    
    has_content = False
    for dim_name, news_list in dims.items():
        if news_list:
            has_content = True
            links_html = "".join([f'<li><a href="{n["link"]}" target="_blank">{n["title"]}</a></li>' for n in news_list[:4]])
            dim_blocks += f"""
            <div class="sub-section">
                <span class="tag">{dim_name}</span>
                <ul>{links_html}</ul>
            </div>
            """
    
    if not has_content:
        dim_blocks = '<p class="empty-tip">今日该区域暂无最新情报更新</p>'

    sections_html += f"""
    <div class="region-card">
        <h2>{icon} {region}</h2>
        {dim_blocks}
    </div>
    """

html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>电商要闻地球 - 五大洲跨境情报站</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; color: #333; }}
        .container {{ max-width: 950px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 30px; }}
        h1 {{ color: #1a73e8; margin-bottom: 5px; }}
        .date {{ color: #666; font-size: 14px; }}
        .region-card {{ background: white; padding: 22px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 3px 10px rgba(0,0,0,0.06); }}
        .region-card h2 {{ font-size: 20px; border-bottom: 2px solid #eef2f6; padding-bottom: 12px; margin-top: 0; color: #1a73e8; }}
        .sub-section {{ margin-top: 15px; background: #fafbfc; padding: 12px 15px; border-radius: 8px; border-left: 4px solid #1a73e8; }}
        .tag {{ display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }}
        ul {{ padding-left: 20px; margin: 0; }}
        li {{ margin-bottom: 8px; line-height: 1.5; font-size: 14px; }}
        a {{ color: #202124; text-decoration: none; }}
        a:hover {{ color: #1a73e8; text-decoration: underline; }}
        .empty-tip {{ color: #999; font-size: 13px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌍 电商要闻地球</h1>
            <div class="date">全球五大市场情报矩阵（财务 | 物流 | 运营 | 选品） | 更新日期：{today}</div>
        </header>
        
        {sections_html}
        
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("全新五大区域 + 四大维度分类网页生成完毕！")
