import os
from PIL import Image, ImageOps

RAMP = " .`':;=+*#%@"

def image_to_ascii(img_path, width=54):
    if not os.path.exists(img_path):
        return []

    img = Image.open(img_path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.48)
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    
    pixels = img_resized.get_flattened_data() if hasattr(img_resized, 'get_flattened_data') else img_resized.getdata()
    ascii_lines = []
    ramp_len = len(RAMP)
    
    for y in range(height):
        row = []
        for x in range(width):
            pixel = pixels[y * width + x]
            index = int((255 - pixel) / 255 * (ramp_len - 1))
            row.append(RAMP[index])
        ascii_lines.append("".join(row))
        
    return ascii_lines

def generate_ascii_svg(ascii_lines, output_path="avi-ascii.svg"):
    num_rows = len(ascii_lines)
    num_cols = max(len(row) for row in ascii_lines) if num_rows > 0 else 54
    
    char_width = 7.2
    char_height = 11.5
    
    term_padding_x = 16
    term_padding_y = 45
    
    card_width = 420
    card_height = 500  # Exact matching height with info-card.svg
    
    total_duration = 3.0
    row_delay = total_duration / max(num_rows, 1)
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_width} {card_height}" width="{card_width}" height="{card_height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; stroke: #21262d; stroke-width: 1px; }')
    svg.append('    .header { fill: #161b22; }')
    svg.append('    .header-border { stroke: #21262d; stroke-width: 1px; }')
    svg.append('    .dot-red { fill: #ff5f56; }')
    svg.append('    .dot-yellow { fill: #ffbd2e; }')
    svg.append('    .dot-green { fill: #27c93f; }')
    svg.append('    .title { font-family: "SFMono-Regular", Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    .ascii-text { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 9.5px; fill: #8b949e; white-space: pre; }')
    svg.append('    .footer { font-family: "SFMono-Regular", Consolas, monospace; font-size: 10px; fill: #79c0ff; }')
    svg.append('  </style>')
    
    # Outer Terminal Frame with rounded corners rx=12 ry=12
    svg.append(f'  <rect class="bg" width="{card_width}" height="{card_height}" rx="12" ry="12" />')
    
    # Inner subtle window boundary path / line
    svg.append(f'  <path class="header-border" d="M 0 36 L {card_width} 36" />')
    svg.append('  <circle class="dot-red" cx="18" cy="18" r="5" />')
    svg.append('  <circle class="dot-yellow" cx="34" cy="18" r="5" />')
    svg.append('  <circle class="dot-green" cx="50" cy="18" r="5" />')
    svg.append(f'  <text class="title" x="{card_width/2}" y="22" text-anchor="middle">avi@github: ~ ./portrait.sh</text>')
    
    # Animated ASCII Rows
    for i, line in enumerate(ascii_lines):
        y_pos = term_padding_y + i * char_height
        if y_pos > card_height - 30:
            break
        delay = i * row_delay
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&#160;')
        
        svg.append(f'  <g transform="translate({term_padding_x}, {y_pos})">')
        svg.append(f'    <clipPath id="clip-row-{i}">')
        svg.append(f'      <rect x="0" y="-10" width="0" height="{char_height + 4}">')
        svg.append(f'        <animate attributeName="width" from="0" to="{card_width}" begin="{delay:.2f}s" dur="{row_delay * 1.5:.2f}s" fill="freeze" />')
        svg.append(f'      </rect>')
        svg.append(f'    </clipPath>')
        svg.append(f'    <text class="ascii-text" y="0" clip-path="url(#clip-row-{i})">{escaped_line}</text>')
        svg.append(f'  </g>')
        
    # Terminal Footer
    footer_y = card_height - 12
    svg.append(f'  <text class="footer" x="{term_padding_x}" y="{footer_y}">avi@github:~$ whoami Avi Vashishta</text>')
    
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated ASCII Terminal SVG ({card_width}x{card_height}) at {output_path}")

if __name__ == "__main__":
    prepped_photo = "source-prepped.png"
    ascii_lines = image_to_ascii(prepped_photo, width=52)
    generate_ascii_svg(ascii_lines, "avi-ascii.svg")
