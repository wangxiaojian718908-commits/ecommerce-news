import datetime

# 1. 获取今天的日期
today = datetime.date.today().strftime('%Y年%m月%d日')

# 2. 网页要展示的内容
html_code = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>电商要闻地球</title>
    <style>
        body {{ font-family: sans-serif; padding: 40px; background-color: #f9f9f9; }}
        .card {{ background: white; padding: 20px; border-radius: 10px; max-width: 600px; margin: 0 auto; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a73e8; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🌍 电商要闻地球</h1>
        <p><strong>更新日期：</strong>{today}</p>
        <hr>
        <p>🎉 恭喜！这是你的第一个自动化网页原型。</p>
    </div>
</body>
</html>
"""

# 3. 将内容写入网页文件 index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("网页生成成功！文件夹里现在多了一个 index.html 文件！")