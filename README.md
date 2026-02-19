# RSS to LinkedIn

**Automated LinkedIn content generation from RSS feeds with AI-powered writing and image creation.**

Transform industry news into engaging LinkedIn posts that match your unique voice and style. Claude Code reads your RSS feeds, scores articles for relevance, drafts posts in your tone, generates branded images, and archives everything to Google Docs.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple.svg)

> **v2.0 Update (Feb 2026):** Now with 20 strategic frameworks, 6-dimension scoring (max 30 points), and ~500-word post depth. See [Strategic Frameworks](#strategic-frameworks) and [6-Dimension Scoring](#6-dimension-scoring-system) sections below.

---

## How It Works

```
RSS Feeds → Article Scoring → Post Drafting → Image Generation → Google Docs Archive
                  ↓                 ↓                                    ↓
            Memory System    Style Matching              Playwright Browser Automation
```

1. **Ingest** — Fetches articles from your RSS feeds (last 24-48 hours)
2. **Filter** — Removes duplicates, off-topic content, and previously used articles
3. **Score** — Ranks articles using 6-dimension scoring: non-obviousness, business impact, problem-solving, framework strength, analogy potential, and evidence quality (max 30 points)
4. **Draft** — Generates 3 LinkedIn posts using varied storytelling angles
5. **Image** — Creates branded images with text overlays for each post
6. **Archive** — Pastes posts to Google Docs via Playwright (one tab per day)
7. **Remember** — Tracks what's been posted to avoid repetition

---

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/rss-to-linkedin.git
cd rss-to-linkedin
pip install -r requirements.txt
```

### 2. Configure Your Setup

```bash
cp config.example.yaml config.yaml
cp examples/style_guide.example.md STYLE_GUIDE.md
cp examples/feeds.example.csv data/feeds.csv
```

Edit these files:
- `config.yaml` — Google Docs URL, posting preferences
- `STYLE_GUIDE.md` — Your voice, tone, and content pillars
- `data/feeds.csv` — Your RSS feed sources

### 3. Train Your Style

Add content samples to `examples/content_samples/`:

```
examples/content_samples/
├── linkedin_posts.md      # Your best LinkedIn posts
├── comments.md            # Thoughtful comments you've written
├── articles.md            # Blog posts or articles
└── voice_notes.md         # Raw voice/style notes
```

### 4. Run with Claude Code

```bash
claude
> /rss-linkedin
```

Or run the workflow manually:

```bash
python workflow.py
```

---

## Configuration

### config.yaml

```yaml
# Google Docs settings
google_docs:
  url: "https://docs.google.com/document/d/YOUR_DOC_ID/edit"
  create_daily_tabs: true

# Content settings
content:
  posts_per_day: 3
  lookback_hours: 24
  min_relevance_score: 0.6

# Posting schedule (IST)
schedule:
  morning: "8:00-9:00"
  afternoon: "12:30-13:30"
  evening: "18:00-19:00"

# Image settings
images:
  enabled: true
  style: "dark_gradient"
  font: "BebasNeue"
```

### RSS Feeds (data/feeds.csv)

| Source Name | Category | Priority | RSS Feed URL | Coverage Description |
|-------------|----------|----------|--------------|---------------------|
| TechCrunch | Tech News | High | https://techcrunch.com/feed/ | Startup and tech coverage |
| Reuters Business | Finance | Critical | https://feeds.reuters.com/reuters/businessNews | Global business news |

**Priority levels:** Critical (always include), High (prefer), Medium (fill gaps)

---

## Style Guide

Your `STYLE_GUIDE.md` defines how posts are written. Include:

### Voice Profile
- Tone (authoritative, conversational, provocative)
- Sentence style (short and punchy vs. flowing)
- Vocabulary preferences
- What to avoid

### Content Pillars
Define 3-5 themes you consistently write about:
1. Industry trends and analysis
2. Practical how-to insights
3. Contrarian takes on conventional wisdom
4. Data-driven observations
5. Founder/practitioner perspectives

### Post Structure (v2.0)
- **Length:** ~500 words (400-600 range) for depth
- **Hook:** Analogy-driven or pattern recognition (not data-first)
- **Structure:** Paragraphs (2-4 sentences each), not bullets
- **Style:** Assertive, no hedging ("The data shows..." not "I think maybe...")
- **Elements:** Historical compression, business problem, unsexy truths, "Think X, not Y" framing

### Content Samples
Include 3-5 examples of posts you've written that capture your voice.

See `examples/style_guide.example.md` for a template.

---

## Strategic Frameworks

The v2.0 workflow uses 20 strategic frameworks to identify high-value insights:

### Pattern Recognition Frameworks

1. **Historical Compression** — Doing in 5 years what took others 30
2. **Infrastructure Inversion** — Infrastructure enabling unexpected outcomes
3. **Dead Zone Serve** — Underserved markets becoming strategic overnight
4. **Unsexy Champions** — Hidden B2B winners in supply chains
5. **Quality Repositioning** — From "cheap" to "premium" perception shift

### Policy & Structure Frameworks

6. **Bilateral Framework Leverage** — FTAs as strategic tools, not just tariffs
7. **Formalization Unlock** — Regulatory changes creating competitive moats
8. **Velocity Mismatch** — Speed differences creating opportunity windows
9. **Accidental Infrastructure** — Policy creating unintended capabilities
10. **Compliance as Moat** — Regulated players gaining structural advantage

### Data & Transparency Frameworks

11. **Data Trail Emergence** — Transparency becoming competitive edge
12. **Market Size Correction** — Debunking narratives with real data
13. **Middle Layer Solution** — Mid-complexity opportunity recognition
14. **Transparency Premium** — Visibility creating credit access

### Infrastructure & Evolution Frameworks

15. **Payment Rails Maturation** — Infrastructure → platform evolution
16. **Currency Corridor Emergence** — New settlement routes opening
17. **Value Chain Invisibility** — Hidden players in supply chains
18. **Parallel System Evolution** — Multiple systems developing simultaneously
19. **Legitimacy Shift** — Informal → formal transition effects
20. **Policy Clarity Unlock** — Regulatory certainty enabling investment

Each post fits 1-2 frameworks. Posts in a daily batch use different frameworks to ensure content diversity.

---

## 6-Dimension Scoring System

Articles are scored on a 30-point scale (1-5 per dimension):

| Dimension | What It Measures | Target |
|-----------|------------------|--------|
| **Non-Obviousness** | Hidden insights most would miss | Unsexy truths, second-order effects |
| **Business Impact** | Changes how companies think about strategy | Market entry, operations, positioning |
| **Problem-Solving** | Addresses critical business challenges | Viability, revenue, logistics |
| **Framework Strength** | Fits strategic frameworks cleanly | Clear pattern recognition |
| **Analogy Potential** | Historical parallels exist | Makes complex insights accessible |
| **Evidence Quality** | Data/proof available | Specific numbers, timelines |

**Scoring Thresholds:**
- **24-30** — Breakthrough insight (top priority)
- **20-23** — Strong strategic value
- **16-19** — Useful context
- **<16** — Skip

Target: Select posts scoring 23+ with different frameworks for maximum content diversity.

---

## Memory System

The workflow tracks:

- **Articles used** — 30-day lookback prevents repetition
- **Posts by pillar** — Ensures balanced content mix
- **Hooks and angles** — Avoids similar openings

```bash
# View memory
python memory.py

# Recent posts
python memory.py recent 7

# Search posts
python memory.py search "keyword"

# Stats by pillar
python memory.py stats
```

---

## Image Generation

Creates LinkedIn-optimized images (1200x627px) with:

- **Text overlay** — Top-left aligned, bold condensed font
- **Emphasis** — Last line in accent color with underline
- **Background** — Auto-selected from Unsplash based on keywords
- **Gradient** — Dark fade on left side for text readability

```python
from generate_image import create_linkedin_image

create_linkedin_image(
    lines_config=[
        ("$180 billion", "white"),
        ("in trade.", "white"),
        ("watch this.", "accent"),  # Accent color + underline
    ],
    keywords=["trade", "shipping"],
    output_filename="post_image.jpg"
)
```

---

## Google Docs Integration

The workflow uses Playwright to:

1. Open your Google Doc
2. Navigate to end of document (or create new tab)
3. Paste formatted posts with metadata
4. Include source links and image paths

**Requirements:**
- Google Doc must be publicly editable (or you must be signed in)
- Playwright browser installed: `npx playwright install chromium`

---

## Project Structure

```
rss-to-linkedin/
├── README.md
├── requirements.txt
├── config.yaml              # Your configuration
├── STYLE_GUIDE.md           # Your voice and tone
├── workflow.py              # Main orchestrator
├── fetch_feeds.py           # RSS feed fetcher
├── angles.py                # Storytelling angle selector
├── generate_image.py        # Image generator
├── memory.py                # Post tracking system
├── data/
│   ├── feeds.csv            # Your RSS sources
│   └── post_memory.json     # Memory database
├── output/
│   ├── latest_post.txt      # Most recent drafts
│   ├── latest_updates.json  # Fetched articles
│   └── *.jpg                # Generated images
├── assets/
│   └── fonts/               # Typography
├── examples/
│   ├── config.example.yaml
│   ├── style_guide.example.md
│   ├── feeds.example.csv
│   └── content_samples/     # Your writing samples
└── .claude/
    └── commands/
        └── rss-linkedin.md  # Claude Code skill
```

---

## Claude Code Skill

Add the skill to your Claude Code commands:

```bash
mkdir -p ~/.claude/commands
cp .claude/commands/rss-linkedin.md ~/.claude/commands/
```

Then invoke with:
```
> /rss-linkedin
```

---

## Requirements

- Python 3.9+
- Claude Code CLI
- Playwright (for Google Docs integration)

```bash
pip install feedparser pillow requests pyyaml
npx playwright install chromium
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built for use with [Claude Code](https://claude.ai/code) by Anthropic.
