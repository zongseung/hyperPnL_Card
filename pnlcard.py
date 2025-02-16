import os
from PIL import Image, ImageDraw, ImageFont

# ✅ 파일 경로 설정
up_path = "/Users/ijongseung/pnlc/up.jpeg"

# ✅ 파일 존재 여부 확인
if not os.path.exists(up_path):
    raise FileNotFoundError(f"{up_path} 파일이 존재하지 않습니다!")

# ✅ 이미지 불러오기
up_image = Image.open(up_path)
draw = ImageDraw.Draw(up_image)

# ✅ 이미지 크기 확인
img_width, img_height = up_image.size

####################################################################
# 폰트 설정 (PnL 수익률 크기 조정)
font_path = "/Library/Fonts/noto/NotoSans-Bold.ttf"
font_pnl_title = ImageFont.truetype(font_path, 70)  # ✅ PnL 제목 크기 조정
font_pnl_value = ImageFont.truetype(font_path, 80)  # ✅ PnL 수익률 크기 감소
font_header = ImageFont.truetype(font_path, 25)  
font_small = ImageFont.truetype(font_path, 20)  
font_address = ImageFont.truetype(font_path, 25)  
font_bottom = ImageFont.truetype(font_path, 20)  

# ✅ 지갑 주소 및 하단 텍스트 추가 (위치 수정)
eth_address = "0x157a44B0555B31A0642fd0aF47f6806D3b86Ec9f"  
text_top = "Your Address Number:"
text_bottom = "Created by hypurrQuant.xyz"

text_pnl = "Your Portfolio PnL"

# ✅ 헤더 설정 및 간격 조정
header_labels = ["Asset", "Quantity", "Avg Price ($)", "Market Price ($)", "PnL ($)", "PnL (%)"]

padding = 60
shift_x = 10

header_spacing = [
    padding + shift_x,
    (img_width // 7) + shift_x,  
    ((img_width // 7) * 2) + shift_x,  
    ((img_width // 7) * 3) + shift_x,
    ((img_width // 7) * 4) + shift_x,  
    ((img_width // 7) * 5) + shift_x  
]  

y_header = img_height // 2  # ✅ 헤더를 더 아래로 이동

# ✅ "Your Address Number:" 및 지갑 주소 출력 (위치 조정)
draw.text((padding, 40), text_top, fill=(255, 255, 255), font=font_header)  # ✅ 더 위로 올림
draw.text((padding, 80), eth_address, fill=(173, 216, 230), font=font_address)  # ✅ 지갑 주소 색상 파란색

# ✅ 포트폴리오 PnL (%) 계산
assets = [
    ["ETH", 1.5, 3200, 3300],
    ["BTC", 0.8, 42000, 41500],
    ["SOL", 10, 150, 180]
]

total_pnl = 0  
total_investment = 0  

for asset in assets:
    _, quantity, avg_price, market_price = asset
    pnl = (market_price - avg_price) * quantity
    total_pnl += pnl
    total_investment += avg_price * quantity

portfolio_pnl_percent = (total_pnl / total_investment) * 100 if total_investment > 0 else 0

# ✅ PnL 텍스트 위치 조정 (겹치지 않도록)
x_pnl = padding
y_pnl = y_header - 300  # ✅ 더 위로 올려서 안 겹치게 함
draw.text((x_pnl, y_pnl), text_pnl, fill=(256, 256, 256), font=font_pnl_title)

x_pnl_value = x_pnl + 20  # ✅ 좌우 정렬 미세 조정
y_pnl_value = y_pnl + 80  # ✅ 수익률을 더 아래로 배치
pnl_value_color = (173, 216, 230)
draw.text((x_pnl_value, y_pnl_value), f"{portfolio_pnl_percent:.2f}%", 
fill=pnl_value_color, font=font_pnl_value)

# ✅ 헤더 출력 (간격 조정된 상태)
for i, label in enumerate(header_labels):
    bbox = draw.textbbox((0, 0), label, font=font_header)
    text_width = bbox[2] - bbox[0]
    x_position = header_spacing[i] - (text_width // 2)  
    draw.text((x_position, y_header), label, fill=(211, 211, 211), font=font_header)

# ✅ 보유 중인 자산 정보 (간격 조정)
y_asset = y_header + 60  

for asset in assets:
    asset_name, quantity, avg_price, market_price = asset

    pnl = (market_price - avg_price) * quantity
    pnl_percent = ((market_price - avg_price) / avg_price) * 100

    asset_data = [
        asset_name, 
        f"{quantity:.2f}",  
        f"{avg_price:,}",  
        f"{market_price:,}",  
        f"{pnl:,.2f}",  
        f"{pnl_percent:.2f}%"  
    ]

    for i, value in enumerate(asset_data):
        bbox = draw.textbbox((0, 0), value, font=font_small)  
        text_width = bbox[2] - bbox[0]
        x_position = header_spacing[i] - (text_width // 2)  
        draw.text((x_position, y_asset), value, fill=(255, 255, 255), font=font_small)

    y_asset += 45  

# ✅ 하단 문구 추가 ("Created by hypurrQuant.xyz")
x_bottom = padding
y_bottom = img_height - 50  
draw.text((x_bottom, y_bottom), text_bottom, fill=(255, 255, 255), font=font_bottom)

# ✅ 이미지 저장 및 출력
up_image.show()
output_path = "/Users/ijongseung/pnl_card/output_image.png"
up_image.save(output_path)

print(f"✅ 이미지 출력 완료: {output_path}")