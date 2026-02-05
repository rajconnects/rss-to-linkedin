#!/usr/bin/env python3
"""
Memory System for RSS to LinkedIn Workflow
Tracks published posts to avoid repetition and enable lookback.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

MEMORY_FILE = Path(__file__).parent / "data" / "post_memory.json"


def _load_memory():
    """Load memory from JSON file."""
    if not MEMORY_FILE.exists():
        return {"posts": [], "articles_used": {}}

    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_memory(memory):
    """Save memory to JSON file."""
    MEMORY_FILE.parent.mkdir(exist_ok=True)
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def is_article_used(article_url: str, days_lookback: int = 30) -> bool:
    """
    Check if an article has been used in a post within the lookback period.

    Args:
        article_url: URL of the article
        days_lookback: Number of days to look back (default 30)

    Returns:
        True if article was used recently, False otherwise
    """
    memory = _load_memory()

    if article_url not in memory["articles_used"]:
        return False

    last_used = datetime.fromisoformat(memory["articles_used"][article_url])
    cutoff = datetime.now() - timedelta(days=days_lookback)

    return last_used > cutoff


def filter_unused_articles(articles: list, days_lookback: int = 30) -> list:
    """
    Filter out articles that have been used recently.

    Args:
        articles: List of article dicts with 'link' key
        days_lookback: Number of days to look back

    Returns:
        Filtered list of unused articles
    """
    return [a for a in articles if not is_article_used(a.get('link', ''), days_lookback)]


def record_post(
    date: str,
    post_number: int,
    pillar: str,
    article_title: str,
    article_url: str,
    article_source: str,
    hook: str,
    post_content: str,
    image_path: Optional[str] = None,
    published: bool = False
):
    """
    Record a post to memory.

    Args:
        date: Date string (YYYY-MM-DD)
        post_number: Post number (1, 2, or 3)
        pillar: Content pillar name
        article_title: Title of source article
        article_url: URL of source article
        article_source: Publication name
        hook: The hook/headline used
        post_content: Full post text
        image_path: Path to generated image
        published: Whether post was actually published
    """
    memory = _load_memory()

    post_record = {
        "id": f"{date}_post{post_number}",
        "date": date,
        "post_number": post_number,
        "pillar": pillar,
        "article": {
            "title": article_title,
            "url": article_url,
            "source": article_source
        },
        "hook": hook,
        "content": post_content,
        "image_path": image_path,
        "published": published,
        "created_at": datetime.now().isoformat()
    }

    # Add to posts list
    memory["posts"].append(post_record)

    # Mark article as used
    memory["articles_used"][article_url] = datetime.now().isoformat()

    _save_memory(memory)
    print(f"✅ Recorded: {date} Post {post_number} - {hook[:50]}...")

    return post_record


def mark_published(post_id: str):
    """Mark a post as published."""
    memory = _load_memory()

    for post in memory["posts"]:
        if post["id"] == post_id:
            post["published"] = True
            post["published_at"] = datetime.now().isoformat()
            _save_memory(memory)
            print(f"✅ Marked as published: {post_id}")
            return True

    return False


def get_recent_posts(days: int = 7) -> list:
    """Get posts from the last N days."""
    memory = _load_memory()
    cutoff = datetime.now() - timedelta(days=days)

    recent = []
    for post in memory["posts"]:
        post_date = datetime.fromisoformat(post["created_at"])
        if post_date > cutoff:
            recent.append(post)

    return sorted(recent, key=lambda x: x["created_at"], reverse=True)


def get_posts_by_pillar(pillar: str, limit: int = 10) -> list:
    """Get recent posts for a specific content pillar."""
    memory = _load_memory()

    pillar_posts = [p for p in memory["posts"] if pillar.lower() in p["pillar"].lower()]
    return sorted(pillar_posts, key=lambda x: x["created_at"], reverse=True)[:limit]


def get_post_history(limit: int = 20) -> list:
    """Get post history for reference."""
    memory = _load_memory()
    return sorted(memory["posts"], key=lambda x: x["created_at"], reverse=True)[:limit]


def search_posts(query: str) -> list:
    """Search posts by keyword in hook or content."""
    memory = _load_memory()
    query = query.lower()

    results = []
    for post in memory["posts"]:
        if (query in post["hook"].lower() or
            query in post["content"].lower() or
            query in post["article"]["title"].lower()):
            results.append(post)

    return results


def get_pillar_stats() -> dict:
    """Get statistics on posts by content pillar."""
    memory = _load_memory()

    stats = {}
    for post in memory["posts"]:
        pillar = post["pillar"]
        if pillar not in stats:
            stats[pillar] = {"count": 0, "last_post": None}
        stats[pillar]["count"] += 1
        stats[pillar]["last_post"] = post["date"]

    return stats


def display_memory_summary():
    """Display a summary of the memory system."""
    memory = _load_memory()

    total_posts = len(memory["posts"])
    total_articles = len(memory["articles_used"])

    print("\n" + "=" * 60)
    print("  POST MEMORY SUMMARY")
    print("=" * 60)
    print(f"\nTotal posts recorded: {total_posts}")
    print(f"Unique articles used: {total_articles}")

    if total_posts > 0:
        print("\n📊 Posts by Pillar:")
        stats = get_pillar_stats()
        for pillar, data in stats.items():
            print(f"   • {pillar}: {data['count']} posts (last: {data['last_post']})")

        print("\n📅 Recent Posts:")
        recent = get_recent_posts(7)
        for post in recent[:5]:
            status = "✓" if post["published"] else "○"
            print(f"   {status} [{post['date']}] {post['hook'][:50]}...")

    print("\n" + "=" * 60)


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        display_memory_summary()
    elif sys.argv[1] == "recent":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        posts = get_recent_posts(days)
        for p in posts:
            print(f"[{p['date']}] Post {p['post_number']}: {p['hook']}")
    elif sys.argv[1] == "search":
        query = " ".join(sys.argv[2:])
        results = search_posts(query)
        print(f"Found {len(results)} posts matching '{query}':")
        for p in results:
            print(f"  [{p['date']}] {p['hook'][:60]}...")
    elif sys.argv[1] == "stats":
        stats = get_pillar_stats()
        for pillar, data in stats.items():
            print(f"{pillar}: {data['count']} posts")
    else:
        print("Usage: python memory.py [recent N | search QUERY | stats]")
