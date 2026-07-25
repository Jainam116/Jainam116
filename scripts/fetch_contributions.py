import os
import json
import requests
from bs4 import BeautifulSoup

USERNAME = "JainamKhara"

def fetch_contributions():
    url = f"https://github.com/users/{USERNAME}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching contribution calendar from {url}...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch contributions: HTTP {response.status_code}")
        
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    
    # Find all contribution day cells in the table / grid
    tooltips = {elem['for']: elem.text.strip() for elem in soup.find_all(id=True) if elem.get('for')}
    
    for rect in soup.find_all("td", class_="ContributionCalendar-day"):
        date = rect.get("data-date")
        level = rect.get("data-level", "0")
        rect_id = rect.get("id")
        
        count = 0
        if rect_id and rect_id in tooltips:
            tooltip_text = tooltips[rect_id]
            # e.g. "No contributions on January 15, 2024" or "5 contributions on..."
            if "No contributions" not in tooltip_text:
                parts = tooltip_text.split()
                if parts and parts[0].isdigit():
                    count = int(parts[0])
                    
        if date:
            days.append({
                "date": date,
                "count": count,
                "level": int(level)
            })
            
    total_contributions = sum(d["count"] for d in days)
    
    # Calculate streak statistics
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day = max(days, key=lambda x: x["count"]) if days else {"count": 0, "date": "N/A"}
    
    for d in days:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak ending today/yesterday
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break
            
    data = {
        "username": USERNAME,
        "total": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days
    }
    
    os.makedirs("data", exist_ok=True)
    output_file = "data/contributions.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully saved contribution data ({len(days)} days, {total_contributions} total contributions) to {output_file}")

if __name__ == "__main__":
    fetch_contributions()
