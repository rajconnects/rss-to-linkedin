#!/usr/bin/env python3
"""RSS Feed Fetcher - Collects updates from configured feeds."""

import csv
import json
import feedparser
from datetime import datetime, timedelta
from pathlib import Path
import time
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fix SSL certificate verification on macOS
ssl._create_default_https_context = ssl._create_unverified_context

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"

def load_feeds():
    """Load feed configurations from CSV."""
    feeds = []
    with open(DATA_DIR / "feeds.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get('RSS Feed URL', '').strip()
            if url and url != 'NO FEED' and not url.startswith('https://www.npci.org.in'):
                feeds.append({
                    'name': row['Source Name'],
                    'category': row['Category'],
                    'priority': row['Priority'],
                    'url': url,
                    'website': row.get('Website URL', ''),
                    'description': row.get('Coverage Description', '')
                })
    return feeds

def fetch_single_feed(feed, hours_back=24):
    """Fetch a single RSS feed and return recent entries."""
    cutoff = datetime.now() - timedelta(hours=hours_back)
    entries = []

    try:
        parsed = feedparser.parse(feed['url'])
        if parsed.bozo and not parsed.entries:
            return feed['name'], [], f"Error: {parsed.bozo_exception}"

        for entry in parsed.entries[:10]:  # Limit to 10 most recent
            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])

            # Include if no date or within timeframe
            if pub_date is None or pub_date > cutoff:
                entries.append({
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:300] if entry.get('summary') else '',
                    'published': pub_date.isoformat() if pub_date else 'Unknown',
                    'source': feed['name'],
                    'category': feed['category'],
                    'priority': feed['priority']
                })

        return feed['name'], entries, None
    except Exception as e:
        return feed['name'], [], str(e)

def fetch_all_feeds(hours_back=24, max_workers=10, filter_used=True):
    """Fetch all feeds concurrently.

    Args:
        hours_back: Hours to look back for articles
        max_workers: Concurrent fetch threads
        filter_used: If True, filters out previously used articles
    """
    feeds = load_feeds()
    all_entries = []
    errors = []

    print(f"\nFetching {len(feeds)} RSS feeds (looking back {hours_back} hours)...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_single_feed, feed, hours_back): feed for feed in feeds}

        for future in as_completed(futures):
            name, entries, error = future.result()
            if error:
                errors.append(f"  ✗ {name}: {error}")
            elif entries:
                print(f"  ✓ {name}: {len(entries)} items")
                all_entries.extend(entries)
            else:
                print(f"  ○ {name}: no new items")

    if errors:
        print("\nErrors:")
        for e in errors[:5]:  # Show first 5 errors
            print(e)

    # Filter out previously used articles
    if filter_used:
        try:
            from memory import filter_unused_articles
            before_count = len(all_entries)
            all_entries = filter_unused_articles(all_entries, days_lookback=30)
            filtered_count = before_count - len(all_entries)
            if filtered_count > 0:
                print(f"\n🧠 Memory: Filtered {filtered_count} previously used articles")
        except ImportError:
            pass  # Memory module not available

    # Sort by priority (Critical > High > Medium) then by date
    priority_order = {'Critical': 0, 'High': 1, 'Medium': 2}
    all_entries.sort(key=lambda x: (priority_order.get(x['priority'], 3), x['published']), reverse=False)
    all_entries.sort(key=lambda x: priority_order.get(x['priority'], 3))

    return all_entries

def save_updates(entries):
    """Save fetched entries to JSON."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = OUTPUT_DIR / f"updates_{timestamp}.json"

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    # Also save as latest
    latest = OUTPUT_DIR / "latest_updates.json"
    with open(latest, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    return filepath

def display_updates(entries):
    """Display updates grouped by category and priority."""
    if not entries:
        print("\nNo new updates found.")
        return

    print(f"\n{'='*60}")
    print(f"FOUND {len(entries)} UPDATES")
    print(f"{'='*60}\n")

    # Group by category
    by_category = {}
    for entry in entries:
        cat = entry['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(entry)

    for cat, items in by_category.items():
        print(f"\n## {cat} ({len(items)} items)")
        print("-" * 40)
        for i, item in enumerate(items, 1):
            priority_icon = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡'}.get(item['priority'], '⚪')
            print(f"\n{i}. {priority_icon} [{item['priority']}] {item['title'][:70]}")
            print(f"   Source: {item['source']}")
            print(f"   Link: {item['link'][:80]}...")
            if item['summary']:
                print(f"   Summary: {item['summary'][:150]}...")

if __name__ == "__main__":
    entries = fetch_all_feeds(hours_back=48)  # 48 hours for testing
    if entries:
        filepath = save_updates(entries)
        display_updates(entries)
        print(f"\n\nSaved to: {filepath}")
    else:
        print("\nNo updates found.")
