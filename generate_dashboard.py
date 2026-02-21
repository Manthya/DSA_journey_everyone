import os
import re
from datetime import datetime
import random

# Configuration
DIRECTORIES = {
    "Linear": "bucket-a-linear/README.md",
    "Structural": "bucket-b-structural/README.md",
    "Graphs": "bucket-c-graphs/README.md",
    "Optimization": "bucket-d-optimization/README.md",
    "FAANG": "faang-practice/README.md"
}

DASHBOARD_FILE = "DASHBOARD.md"

QUOTES = [
    "The only way to learn a new programming language is by writing programs in it. – Dennis Ritchie",
    "Experience is the name everyone gives to their mistakes. – Oscar Wilde",
    "In order to be irreplaceable, one must always be different. – Coco Chanel",
    "First, solve the problem. Then, write the code. – John Johnson",
    "Make it work, make it right, make it fast. – Kent Beck",
    "Talk is cheap. Show me the code. – Linus Torvalds",
    "Continuous effort - not strength or intelligence - is the key to unlocking our potential. – Liane Cardes",
    "Do not pray for an easy life, pray for the strength to endure a difficult one. – Bruce Lee"
]

def count_progress(filepath):
    total = 0
    completed = 0
    if not os.path.exists(filepath):
        return total, completed

    with open(filepath, 'r') as f:
        for line in f:
            if re.match(r'^\s*-\s*\[x\]', line, re.IGNORECASE):
                completed += 1
                total += 1
            elif re.match(r'^\s*-\s*\[ \]', line):
                total += 1
    return total, completed

def generate_progress_bar(completed, total, length=20):
    if total == 0:
        return "░" * length
    filled_length = int(length * completed // total)
    bar = "█" * filled_length + "░" * (length - filled_length)
    return bar

def get_streak():
    today = datetime.now().date()
    modified_today = False
    
    for _, filepath in DIRECTORIES.items():
        if os.path.exists(filepath):
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath)).date()
            if mtime == today:
                modified_today = True
                break
    
    streak_file = ".streak_data"
    current_streak = 0
    last_mod_date = None

    if os.path.exists(streak_file):
        with open(streak_file, 'r') as f:
            data = f.read().split(',')
            if len(data) == 2:
                current_streak = int(data[0])
                try:
                    last_mod_date = datetime.strptime(data[1].strip(), "%Y-%m-%d").date()
                except ValueError:
                    pass
    
    if modified_today:
        if last_mod_date != today:
            if last_mod_date and (today - last_mod_date).days == 1:
                current_streak += 1
            else:
                current_streak = 1
        with open(streak_file, 'w') as f:
            f.write(f"{current_streak},{today.strftime('%Y-%m-%d')}")
    else:
        if last_mod_date and (today - last_mod_date).days > 1:
            current_streak = 0
            with open(streak_file, 'w') as f:
                f.write(f"0,{last_mod_date.strftime('%Y-%m-%d')}")

    return current_streak

def get_level_info(completed):
    levels = [
        (0, "Initiate 🥚", 50),
        (50, "Apprentice 🐣", 150),
        (150, "Explorer 🐥", 250),
        (250, "Warrior 🦅", 350),
        (350, "Master 🐉", 450),
        (450, "Grandmaster 🌌", 500),
        (500, "Architect 👑", 9999)
    ]
    for i in range(len(levels)-1, -1, -1):
        if completed >= levels[i][0]:
            next_tier = levels[i][2]
            return levels[i][1], next_tier
    return "Initiate 🥚", 50

def update_readme():
    stats = {}
    total_all = 0
    completed_all = 0
    
    for name, filepath in DIRECTORIES.items():
        total, completed = count_progress(filepath)
        stats[name] = {"total": total, "completed": completed}
        total_all += total
        completed_all += completed

    streak = get_streak()
    level_name, next_tier = get_level_info(completed_all)
    quote = random.choice(QUOTES)
    
    core_buckets = ["Linear", "Structural", "Graphs", "Optimization"]
    percentages = {}
    for b in core_buckets:
        if stats[b]["total"] > 0:
            percentages[b] = (stats[b]["completed"] / stats[b]["total"]) * 100
        else:
            percentages[b] = 0
            
    started_buckets = {k: v for k, v in percentages.items() if stats[k]["completed"] > 0}
    
    if started_buckets:
        strongest = max(started_buckets, key=started_buckets.get)
        weakest = min(started_buckets, key=started_buckets.get)
    else:
        strongest = "-"
        weakest = "-"

    total_pct = int((completed_all / total_all) * 100) if total_all > 0 else 0
    total_bar = generate_progress_bar(completed_all, total_all, 20)
    
    dashboard = "<!-- DASHBOARD START -->\n"
    
    dashboard += "### 🏆 Player Stats\n\n"
    dashboard += "| 💎 Level | 🔥 Streak | 🌟 Total XP | 📈 Next Title |\n"
    dashboard += "| :---: | :---: | :--- | :--- |\n"
    
    if next_tier < 9000:
        next_rank_str = f"{next_tier} Solved ({next_tier - completed_all} to go!)"
    else:
        next_rank_str = "MAX LEVEL ACHIEVED"
        
    dashboard += f"| **{level_name}** | **{streak} days** | `{total_bar}` **{completed_all} / {total_all} ({total_pct}%)** | {next_rank_str} |\n\n"
        
    dashboard += "---\n\n"
    dashboard += "### 🪣 Bucket Progress\n\n"
    dashboard += "| 🗂️ Category | Progress | Solved | % |\n"
    dashboard += "| :--- | :--- | :---: | :---: |\n"
    
    for bucket in core_buckets:
        t = stats[bucket]["total"]
        c = stats[bucket]["completed"]
        pct = int((c / t) * 100) if t > 0 else 0
        bar = generate_progress_bar(c, t, 20)
        icon = "🟢" if bucket == "Linear" else "🔵" if bucket == "Structural" else "🟣" if bucket == "Graphs" else "🔴"
        
        dashboard += f"| {icon} **{bucket}** | `{bar}` | {c} / {t} | **{pct}%** |\n"

    t = stats["FAANG"]["total"]
    c = stats["FAANG"]["completed"]
    pct = int((c / t) * 100) if t > 0 else 0
    bar = generate_progress_bar(c, t, 20)
    
    dashboard += f"| 🏢 **FAANG Practice** | `{bar}` | {c} / {t} | **{pct}%** |\n\n"
    dashboard += "---\n\n"
    
    dashboard += f"💡 **Strongest Area:** {strongest}\n"
    dashboard += f"🚧 **Needs Focus:** {weakest}\n\n"
    
    dashboard += f"> *\"{quote}\"*\n"
    dashboard += "<!-- DASHBOARD END -->"

    if os.path.exists(DASHBOARD_FILE):
        with open(DASHBOARD_FILE, 'r') as f:
            content = f.read()

        new_content = re.sub(
            r'<!-- DASHBOARD START -->.*?<!-- DASHBOARD END -->', 
            dashboard, 
            content, 
            flags=re.DOTALL
        )

        with open(DASHBOARD_FILE, 'w') as f:
            f.write(new_content)
        
        print(f"Dashboard stats generated successfully in {DASHBOARD_FILE}!")
    else:
        print(f"Could not find {DASHBOARD_FILE}.")

if __name__ == "__main__":
    update_readme()
