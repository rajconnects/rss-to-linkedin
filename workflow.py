#!/usr/bin/env python3
"""
RSS to LinkedIn Workflow
1. Fetch RSS feeds
2. Shortlist and prioritize updates
3. Generate LinkedIn post draft
4. Save draft for review
"""

import json
from datetime import datetime
from pathlib import Path
from fetch_feeds import fetch_all_feeds, save_updates

OUTPUT_DIR = Path(__file__).parent / "output"

def display_for_selection(entries):
    """Display entries with numbers for selection."""
    print(f"\n{'='*70}")
    print(f"  UPDATES FOR REVIEW - {len(entries)} items")
    print(f"{'='*70}")

    # Group by priority first
    by_priority = {'Critical': [], 'High': [], 'Medium': []}
    for i, e in enumerate(entries):
        by_priority.get(e['priority'], []).append((i, e))

    for priority in ['Critical', 'High', 'Medium']:
        items = by_priority.get(priority, [])
        if not items:
            continue

        icon = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡'}[priority]
        print(f"\n{icon} {priority.upper()} PRIORITY ({len(items)} items)")
        print("-" * 60)

        for idx, entry in items:
            title = entry['title'][:65]
            source = entry['source'][:20]
            print(f"  [{idx:2d}] {title}")
            print(f"       └─ {source} | {entry['category']}")

def get_user_selection(entries):
    """Get user's selection of articles to include in post."""
    print("\n" + "="*70)
    print("  SELECT ARTICLES FOR YOUR LINKEDIN POST")
    print("="*70)
    print("\nEnter article numbers separated by commas (e.g., 0,3,7,12)")
    print("Or type 'all' for all items, 'critical' for critical only")
    print("Type 'quit' to exit\n")

    selection = input("Your selection: ").strip().lower()

    if selection == 'quit':
        return None
    elif selection == 'all':
        return entries
    elif selection == 'critical':
        return [e for e in entries if e['priority'] == 'Critical']
    elif selection == 'high':
        return [e for e in entries if e['priority'] in ['Critical', 'High']]
    else:
        try:
            indices = [int(x.strip()) for x in selection.split(',')]
            return [entries[i] for i in indices if 0 <= i < len(entries)]
        except:
            print("Invalid selection. Please try again.")
            return get_user_selection(entries)

def generate_post_draft(selected_entries, audience="Business/Startup"):
    """Generate a LinkedIn post draft from selected entries."""

    # Group by theme/category
    themes = {}
    for entry in selected_entries:
        cat = entry['category']
        if cat not in themes:
            themes[cat] = []
        themes[cat].append(entry)

    # Build draft structure
    draft = {
        'generated_at': datetime.now().isoformat(),
        'selected_count': len(selected_entries),
        'themes': list(themes.keys()),
        'articles': selected_entries,
        'suggested_post': None
    }

    # Create a suggested post template
    post_lines = []
    post_lines.append("📊 What's moving in payments, fintech & cross-border trade this week:\n")

    for cat, items in themes.items():
        if items:
            post_lines.append(f"\n🔹 {cat}:")
            for item in items[:3]:  # Max 3 per category
                title = item['title'][:80]
                post_lines.append(f"• {title}")

    post_lines.append("\n\n💡 Key takeaway for founders & operators:")
    post_lines.append("[Add your analysis here - what does this mean for your audience?]")
    post_lines.append("\n\n#fintech #payments #crossborder #india #startup")

    draft['suggested_post'] = '\n'.join(post_lines)

    return draft

def save_draft(draft):
    """Save the draft to a file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save full draft data
    draft_path = OUTPUT_DIR / f"draft_{timestamp}.json"
    with open(draft_path, 'w', encoding='utf-8') as f:
        json.dump(draft, f, indent=2, ensure_ascii=False)

    # Save just the post text
    post_path = OUTPUT_DIR / f"post_{timestamp}.txt"
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(draft['suggested_post'])

    # Save as latest
    latest_path = OUTPUT_DIR / "latest_post.txt"
    with open(latest_path, 'w', encoding='utf-8') as f:
        f.write(draft['suggested_post'])

    return draft_path, post_path

def display_draft(draft):
    """Display the generated draft."""
    print("\n" + "="*70)
    print("  GENERATED LINKEDIN POST DRAFT")
    print("="*70)
    print("\n" + draft['suggested_post'])
    print("\n" + "="*70)

def main():
    print("\n" + "🚀 RSS TO LINKEDIN WORKFLOW".center(70))
    print("="*70)

    # Step 1: Fetch feeds
    print("\n📡 Step 1: Fetching RSS feeds...")
    entries = fetch_all_feeds(hours_back=48)

    if not entries:
        print("No updates found. Try again later.")
        return

    save_updates(entries)

    # Step 2: Display for selection
    print("\n📋 Step 2: Review updates...")
    display_for_selection(entries)

    # Step 3: Get user selection
    print("\n✅ Step 3: Select articles...")
    selected = get_user_selection(entries)

    if selected is None:
        print("Exiting.")
        return

    if not selected:
        print("No articles selected.")
        return

    print(f"\nSelected {len(selected)} articles.")

    # Step 4: Generate draft
    print("\n✍️  Step 4: Generating post draft...")
    draft = generate_post_draft(selected)

    # Step 5: Display and save
    display_draft(draft)
    draft_path, post_path = save_draft(draft)

    print(f"\n📁 Files saved:")
    print(f"   Draft data: {draft_path}")
    print(f"   Post text:  {post_path}")
    print(f"   Latest:     {OUTPUT_DIR / 'latest_post.txt'}")

    print("\n" + "="*70)
    print("  NEXT STEPS")
    print("="*70)
    print("\n1. Edit the post at: ~/rss-to-linkedin/output/latest_post.txt")
    print("2. When ready, run: python3 ~/rss-to-linkedin/post_to_linkedin.py")
    print("   (This will open browser and paste your draft)")
    print("\n")

if __name__ == "__main__":
    main()
