import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
MONTHS = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"total": 0, "current_streak": 0, "longest_streak": 0, "days": []}
        
    days = data.get("days", [])
    total_contribs = data.get("total", 0)
    
    box_size = 11
    box_gap = 4
    col_width = box_size + box_gap
    row_height = box_size + box_gap
    
    margin_left = 35
    margin_top = 35
    
    cols = 53
    rows = 7
    
    width = 860
    height = 200
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: transparent; }')
    svg.append('    .title-stat { font-family: "SFMono-Regular", Consolas, monospace; font-size: 14px; fill: #ffffff; font-weight: bold; }')
    svg.append('    .label { font-family: "SFMono-Regular", Consolas, monospace; font-size: 11px; fill: #7d8590; }')
    svg.append('    .box { rx: 2px; ry: 2px; opacity: 0; animation: slideDown 0.3s ease-out forwards; }')
    svg.append('    @keyframes slideDown { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }')
    svg.append('  </style>')
    
    # Month Labels across top
    for i, month in enumerate(MONTHS):
        mx = margin_left + i * 4 * col_width
        if mx < width - 40:
            svg.append(f'  <text class="label" x="{mx}" y="20">{month}</text>')
            
    # Day of week labels (Mon, Wed, Fri)
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for label, r in day_labels:
        y_pos = margin_top + r * row_height + 9
        svg.append(f'  <text class="label" x="5" y="{y_pos}">{label}</text>')
        
    # Render day boxes
    num_days = len(days)
    for idx in range(min(num_days, cols * rows)):
        c = idx // rows
        r = idx % rows
        
        day_info = days[idx] if idx < num_days else {"level": 0}
        level = min(day_info.get("level", 0), len(PALETTE) - 1)
        color = PALETTE[level]
        
        x = margin_left + c * col_width
        y = margin_top + r * row_height
        
        delay = 0.05 + (c + r) * 0.012
        
        svg.append(f'  <rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" style="animation-delay: {delay:.3f}s;" />')
        
    # Bottom Stats Line: "9,272 contributions in the last year"
    svg.append(f'  <text class="title-stat" x="35" y="{height - 10}">{total_contribs:,} contributions in the last year</text>')
    
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated frameless Heatmap SVG at {output_path}")

if __name__ == "__main__":
    render_heatmap_svg()
