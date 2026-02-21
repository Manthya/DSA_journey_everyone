import os
import re
from datetime import datetime

# Configuration
DIRECTORIES = {
    "Linear": "bucket-a-linear/README.md",
    "Structural": "bucket-b-structural/README.md",
    "Graphs": "bucket-c-graphs/README.md",
    "Optimization": "bucket-d-optimization/README.md",
    "FAANG": "faang-practice/README.md"
}

ROOT_README = "README.md"

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

def generate_progress_bar(completed, total, length=10):
    if total == 0:
        return "░" * length
    filled_length = int(length * completed // total)
    bar = "█" * filled_length + "░" * (length - filled_length)
    return bar

def get_streak():
    """
    Very basic streak calculation: Check if any of the READMEs were modified today.
    A more advanced version would parse git logs or a specific streak tracker file.
    """
    today = datetime.now().date()
    modified_today = False
    
    for _, filepath in DIRECTORIES.items():
        if os.path.exists(filepath):
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath)).date()
            if mtime == today:
                modified_today = True
                break
    
    # We will just return 1 if modified today, 0 if not. 
    # To track long streaks without a server, we would need to store the streak in a hidden file.
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
        # If it's been more than 1 day since last modification, reset streak
        if last_mod_date and (today - last_mod_date).days > 1:
            current_streak = 0
            with open(streak_file, 'w') as f:
                f.write(f"0,{last_mod_date.strftime('%Y-%m-%d')}")

    return current_streak

def update_readme():
    stats = {}
    for name, filepath in DIRECTORIES.items():
        total, completed = count_progress(filepath)
        stats[name] = {"total": total, "completed": completed}

    streak = get_streak()
    
    # Determine Strongest/Weakest Areas
    core_buckets = ["Linear", "Structural", "Graphs", "Optimization"]
    percentages = {}
    for b in core_buckets:
        if stats[b]["total"] > 0:
            percentages[b] = (stats[b]["completed"] / stats[b]["total"]) * 100
        else:
            percentages[b] = 0
            
    # filter out 0% for weakest if nothing started, but if all 0, it's just none
    started_buckets = {k: v for k, v in percentages.items() if stats[k]["completed"] > 0}
    
    if started_buckets:
        strongest = max(started_buckets, key=started_buckets.get)
        weakest = min(started_buckets, key=started_buckets.get)
    else:
        strongest = "-"
        weakest = "-"

    # Build Dashboard Markdown
    dashboard = "<!-- DASHBOARD START -->\n"
    dashboard += "# 🧠 DSA Architect Dashboard\n\n"
    dashboard += "🔥 Current Week: 1\n"
    dashboard += f"📅 Streak: {streak} days\n\n"
    dashboard += "Bucket Progress:\n"
    
    for bucket in core_buckets:
        t = stats[bucket]["total"]
        c = stats[bucket]["completed"]
        pct = int((c / t) * 100) if t > 0 else 0
        bar = generate_progress_bar(c, t)
        
        icon = "🟢" if bucket == "Linear" else "🔵" if bucket == "Structural" else "🟣" if bucket == "Graphs" else "🔴"
        dashboard += f"{icon} {bucket}: [{bar}] {c} / {t} ({pct}%)\n"

    dashboard += "\n"
    t = stats["FAANG"]["total"]
    c = stats["FAANG"]["completed"]
    pct = int((c / t) * 100) if t > 0 else 0
    bar = generate_progress_bar(c, t)
    dashboard += f"🏢 FAANG Problems Solved: [{bar}] {c} / {t} ({pct}%)\n\n"
    
    dashboard += f"Weakest Area: {weakest}\n"
    dashboard += f"Strongest Area: {strongest}\n"
    dashboard += "<!-- DASHBOARD END -->"

    # Read the existing README and replace the placeholder block
    with open(ROOT_README, 'r') as f:
        content = f.read()

    new_content = re.sub(
        r'<!-- DASHBOARD START -->.*?<!-- DASHBOARD END -->', 
        dashboard, 
        content, 
        flags=re.DOTALL
    )

    with open(ROOT_README, 'w') as f:
        f.write(new_content)
    
    print("Dashboard stats generated successfully!")
    print(dashboard)

if __name__ == "__main__":
    update_readme()
