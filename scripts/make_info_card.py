import os

def generate_info_card(output_path="info-card.svg"):
    width = 440
    height = 500
    
    sections = [
        {"type": "header", "title": "avi@github"},
        {"type": "kv", "key": "Now", "val": "Software Engineer @ Dock.us", "key_color": "#ff7b72"},
        {"type": "kv", "key": "Prev", "val": "Founding Engineer @ Turgon AI", "key_color": "#ff7b72"},
        {"type": "kv", "key": "Also", "val": "SDE + Instructor @ AccioJob (YC'21)", "key_color": "#ff7b72"},
        {"type": "kv", "key": "Edu", "val": "B.Tech CS, IIIT Delhi '24", "key_color": "#ff7b72"},
        {"type": "divider", "title": "Stack"},
        {"type": "kv", "key": "Frontend", "val": "React, Next.js, TypeScript, R3F", "key_color": "#ff7b72"},
        {"type": "kv", "key": "Backend", "val": "Node, NestJS, GraphQL, Django", "key_color": "#ff7b72"},
        {"type": "kv", "key": "AI / ML", "val": "LangChain, Vercel AI SDK, OpenAI", "key_color": "#ff7b72"},
        {"type": "kv", "key": "Cloud", "val": "AWS, Docker, Vercel, Prisma", "key_color": "#ff7b72"},
        {"type": "divider", "title": "Highlights"},
        {"type": "bullet", "val": "Taught 100,000+ developers to code", "color": "#7ee787"},
        {"type": "bullet", "val": "2 books • 100k+ podcast streams", "color": "#7ee787"},
    ]
    
    is_static = os.getenv("STATIC") == "1"
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; stroke: #21262d; stroke-width: 1px; }')
    svg.append('    .header-border { stroke: #21262d; stroke-width: 1px; }')
    svg.append('    .dot-red { fill: #ff5f56; }')
    svg.append('    .dot-yellow { fill: #ffbd2e; }')
    svg.append('    .dot-green { fill: #27c93f; }')
    svg.append('    .title { font-family: "SFMono-Regular", Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    .username { font-family: "SFMono-Regular", Consolas, monospace; font-size: 18px; fill: #58a6ff; font-weight: bold; }')
    svg.append('    .divider-text { font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }')
    svg.append('    .divider-line { stroke: #21262d; stroke-width: 1px; }')
    svg.append('    .key { font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; font-weight: bold; }')
    svg.append('    .val { font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; fill: #c9d1d9; }')
    svg.append('    .bullet { font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; fill: #7ee787; }')
    
    if not is_static:
        svg.append('    .fade-row { opacity: 0; animation: fadeIn 0.4s ease-out forwards; }')
        svg.append('    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }')
    svg.append('  </style>')
    
    # Outer Terminal Frame rx=12 ry=12
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" rx="12" ry="12" />')
    
    # Inner border line
    svg.append(f'  <path class="header-border" d="M 0 36 L {width} 36" />')
    svg.append('  <circle class="dot-red" cx="18" cy="18" r="5" />')
    svg.append('  <circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg.append('  <circle class="dot-green" cx="50" cy="18" r="5" />')
    svg.append(f'  <text class="title" x="{width/2}" y="22" text-anchor="middle">avi@github: ~$ neofetch</text>')
    
    current_y = 65
    row_count = 0
    
    for item in sections:
        item_type = item["type"]
        delay = 0.15 + row_count * 0.1
        style_attr = f'style="animation-delay: {delay:.2f}s;"' if not is_static else ''
        row_class = 'fade-row' if not is_static else ''
        
        if item_type == "header":
            svg.append(f'  <g class="{row_class}" {style_attr}>')
            svg.append(f'    <text class="username" x="25" y="{current_y}">{item["title"]}</text>')
            svg.append(f'    <line class="divider-line" x1="120" y1="{current_y-6}" x2="{width-25}" y2="{current_y-6}" />')
            svg.append('  </g>')
            current_y += 32
        elif item_type == "divider":
            current_y += 8
            svg.append(f'  <g class="{row_class}" {style_attr}>')
            svg.append(f'    <text class="divider-text" x="25" y="{current_y}">- {item["title"]}</text>')
            svg.append(f'    <line class="divider-line" x1="110" y1="{current_y-4}" x2="{width-25}" y2="{current_y-4}" />')
            svg.append('  </g>')
            current_y += 28
        elif item_type == "kv":
            key_color = item.get("key_color", "#ff7b72")
            escaped_val = item["val"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            svg.append(f'  <g class="{row_class}" {style_attr}>')
            svg.append(f'    <text class="key" fill="{key_color}" x="25" y="{current_y}">{item["key"]}</text>')
            svg.append(f'    <text class="val" x="125" y="{current_y}">{escaped_val}</text>')
            svg.append('  </g>')
            current_y += 25
        elif item_type == "bullet":
            escaped_val = item["val"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            svg.append(f'  <g class="{row_class}" {style_attr}>')
            svg.append(f'    <text class="bullet" x="25" y="{current_y}">•</text>')
            svg.append(f'    <text class="val" x="45" y="{current_y}">{escaped_val}</text>')
            svg.append('  </g>')
            current_y += 24
            
        row_count += 1
        
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated Neofetch Card SVG ({width}x{height}) at {output_path}")

if __name__ == "__main__":
    generate_info_card()
