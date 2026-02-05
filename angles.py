#!/usr/bin/env python3
"""
Post Angle Selector
Adds variety to LinkedIn posts by rotating through different storytelling angles.
"""

import random
from typing import List, Dict, Tuple

# Define available angles
ANGLES = {
    "history_arc": {
        "name": "History Arc",
        "description": "Connect to past events, show evolution over time",
        "triggers": ["policy", "regulatory", "fta", "agreement", "reform", "scheme"],
        "opening_templates": [
            "This didn't come out of nowhere.",
            "The backstory matters here.",
            "This is a chapter in a longer book.",
            "{topic} has a history worth knowing.",
        ],
        "structure": "Present → Past context → Back to present with insight",
        "weight": 1.0
    },
    "data_bomb": {
        "name": "Data Bomb",
        "description": "Lead with surprising numbers, let data speak",
        "triggers": ["billion", "million", "percent", "%", "growth", "surge", "record"],
        "opening_templates": [
            "[Stat 1]. [Stat 2]. [Stat 3]. Let that sink in.",
            "The numbers tell the story:",
            "Three data points that matter:",
            "Here's what the data shows:",
        ],
        "structure": "Numbers → Why they matter → Implication",
        "weight": 1.2  # Slightly favor for EximPe's analytical brand
    },
    "practitioner_signal": {
        "name": "Practitioner Signal",
        "description": "Ground-level operational insight, what this means in practice",
        "triggers": ["banks", "exporters", "msme", "compliance", "implementation", "circular"],
        "opening_templates": [
            "If you're {doing X}, this changes things.",
            "Here's what this means on the ground:",
            "The operational reality:",
            "For anyone {doing X}, pay attention:",
        ],
        "structure": "News → Practical impact → Who should care",
        "weight": 1.1
    },
    "contrarian_reframe": {
        "name": "Contrarian Reframe",
        "description": "Challenge conventional narrative, offer fresh perspective",
        "triggers": ["market", "sentiment", "outlook", "forecast", "consensus"],
        "opening_templates": [
            "The common view: {X}. The reframe: {Y}.",
            "Everyone's talking about {X}. They're missing {Y}.",
            "The headline says {X}. The real story is {Y}.",
            "Conventional wisdom says {X}. Here's another lens:",
        ],
        "structure": "Common view → Challenge → New frame → Evidence",
        "weight": 1.0
    },
    "forward_look": {
        "name": "Forward Look",
        "description": "What this means for the future, emerging patterns",
        "triggers": ["talks", "negotiations", "pilot", "launch", "begin", "start", "new"],
        "opening_templates": [
            "This is the 10-year play, not the 10-month play.",
            "Watch this space.",
            "What happens next matters more than the announcement.",
            "The signal for what's coming:",
        ],
        "structure": "Current event → Future implications → What to watch",
        "weight": 0.9
    },
    "first_principles": {
        "name": "First Principles",
        "description": "Break down fundamentals, explain why something matters",
        "triggers": ["infrastructure", "framework", "system", "mechanism", "structure"],
        "opening_templates": [
            "Let's break this down.",
            "The fundamentals matter here.",
            "First principles: {X}",
            "Why does this matter? Start here:",
        ],
        "structure": "Concept → Breakdown → Connect to bigger picture",
        "weight": 0.8
    }
}


def score_article_for_angle(article: Dict, angle_key: str) -> float:
    """Score how well an article matches an angle."""
    angle = ANGLES[angle_key]
    text = (article.get('title', '') + ' ' + article.get('summary', '')).lower()

    # Count trigger matches
    trigger_matches = sum(1 for trigger in angle['triggers'] if trigger in text)

    # Apply weight
    score = trigger_matches * angle['weight']

    # Bonus for data-heavy articles matching data_bomb
    if angle_key == 'data_bomb':
        import re
        numbers = len(re.findall(r'\d+\.?\d*%|\$\d+|₹\d+|\d+ billion|\d+ million|\d+ crore', text))
        score += numbers * 0.5

    return score


def select_angles_for_posts(articles: List[Dict], num_posts: int = 3) -> List[Tuple[Dict, str, Dict]]:
    """
    Select the best angle for each post, ensuring diversity.

    Args:
        articles: List of article dicts (already scored/ranked)
        num_posts: Number of posts to generate

    Returns:
        List of (article, angle_key, angle_info) tuples
    """
    if len(articles) < num_posts:
        raise ValueError(f"Need at least {num_posts} articles")

    results = []
    used_angles = set()

    for i in range(num_posts):
        article = articles[i]

        # Score all angles for this article
        angle_scores = {}
        for angle_key in ANGLES:
            if angle_key not in used_angles:  # Diversity: don't reuse angles
                angle_scores[angle_key] = score_article_for_angle(article, angle_key)

        if not angle_scores:
            # All angles used, reset (shouldn't happen with 3 posts, 6 angles)
            angle_scores = {k: score_article_for_angle(article, k) for k in ANGLES}

        # Select best matching angle (with some randomness for ties)
        max_score = max(angle_scores.values())
        top_angles = [k for k, v in angle_scores.items() if v >= max_score * 0.8]

        selected_angle = random.choice(top_angles)
        used_angles.add(selected_angle)

        results.append((article, selected_angle, ANGLES[selected_angle]))

    return results


def get_opening_for_angle(angle_key: str, article: Dict) -> str:
    """Get a randomized opening line for the angle."""
    angle = ANGLES[angle_key]
    template = random.choice(angle['opening_templates'])

    # Simple template filling (can be enhanced)
    topic = article.get('title', 'This development')[:30]
    return template.replace('{topic}', topic)


def display_angle_selection(selections: List[Tuple[Dict, str, Dict]]):
    """Display the angle selections for review."""
    print("\n" + "=" * 60)
    print("  ANGLE SELECTION FOR TODAY'S POSTS")
    print("=" * 60)

    for i, (article, angle_key, angle_info) in enumerate(selections, 1):
        print(f"\n📝 POST {i}")
        print(f"   Article: {article['title'][:50]}...")
        print(f"   Angle: {angle_info['name']}")
        print(f"   Structure: {angle_info['structure']}")
        print(f"   Opening hint: {get_opening_for_angle(angle_key, article)}")

    print("\n" + "=" * 60)


def suggest_angle(article: Dict) -> Tuple[str, Dict]:
    """Suggest the best angle for a single article."""
    scores = {k: score_article_for_angle(article, k) for k in ANGLES}
    best_angle = max(scores, key=scores.get)
    return best_angle, ANGLES[best_angle]


# CLI interface
if __name__ == "__main__":
    # Demo with sample articles
    sample_articles = [
        {
            "title": "India and Gulf Cooperation Council sign terms of reference",
            "summary": "India and the GCC have signed terms to begin FTA negotiations. Trade at $180 billion."
        },
        {
            "title": "RBI extends interest subvention for export credit",
            "summary": "Banks and MSMEs can now access cheaper export financing under new scheme."
        },
        {
            "title": "India-US trade deal lifts market sentiment",
            "summary": "Markets respond positively as trade talks progress. Analysts recommend portfolio rebalancing."
        }
    ]

    selections = select_angles_for_posts(sample_articles)
    display_angle_selection(selections)
