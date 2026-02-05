# RSS to LinkedIn Workflow

Generate LinkedIn posts from RSS feeds in your unique voice and style.

## Instructions

### Phase 1: Fetch RSS Feeds

1. **Fetch feeds** by running:
   ```bash
   cd ~/rss-to-linkedin && python3 fetch_feeds.py
   ```

2. **Read the updates** from `~/rss-to-linkedin/output/latest_updates.json`

### Phase 2: Apply Style and Filter

3. **Read the style guide** from `~/rss-to-linkedin/STYLE_GUIDE.md`

4. **Filter articles** using these rules:
   - Only last 24 hours (or 48 if specified by user)
   - Discard: off-topic, clickbait, duplicates
   - Check memory to exclude previously used articles

5. **Score and select 3 themes** using weighted criteria from config:
   - Pillar relevance (3x weight)
   - Data density (2x)
   - Counterintuitive potential (2x)
   - Strategy alignment (2x)
   - Timeliness (1x)

### Phase 3: Select Storytelling Angles

6. **Choose varied angles** for each post (no repeats):

   | Angle | When to Use | Structure |
   |-------|-------------|-----------|
   | **Data Bomb** | Strong numbers available | Numbers → Why → Implication |
   | **Practitioner Signal** | Operational news | News → Practical impact → Who cares |
   | **Contrarian Reframe** | Conventional wisdom exists | Common view → Challenge → New frame |
   | **History Arc** | Policy shifts, long trends | Present → Past → Insight |
   | **Forward Look** | Early signals, emerging | Event → Future → Watch |
   | **First Principles** | Complex topics | Concept → Breakdown → Big picture |

### Phase 4: Draft Posts

7. **Draft 3 posts** matching the style guide:
   - Match the voice profile exactly
   - Apply the selected angle's structure
   - 150-250 words each
   - Max 1 emoji, max 2 hashtags
   - NO product pitches

8. **Output format** for each post:
   ```
   POST [1/2/3] — ANGLE: [ANGLE NAME]
   Pillar: [content pillar]
   Source: [title + URL]
   Image: [suggested image path]

   [DRAFT TEXT]

   ---
   Alt hook: [alternative opening]
   Posting time: [Morning/Afternoon/Evening]
   ```

9. **Save drafts** to `~/rss-to-linkedin/output/latest_post.txt`

### Phase 5: Generate Images

10. **Generate images** for each post:
    ```python
    from generate_image import create_linkedin_image
    create_linkedin_image(
        lines_config=[
            ("Line 1 text", "white"),
            ("Line 2 text", "white"),
            ("emphasis.", "accent"),
        ],
        keywords=["relevant", "keywords"],
        output_filename="post1_image.jpg"
    )
    ```

### Phase 6: Archive to Google Docs

11. **Read config** from `~/rss-to-linkedin/config.yaml` for Google Docs URL

12. **Use Playwright** to open the Google Doc:
    - Navigate to end of document
    - Add date header
    - Paste all 3 posts with metadata

### Phase 7: Record to Memory

13. **Record posts** to memory:
    ```python
    from memory import record_post
    record_post(
        date="YYYY-MM-DD",
        post_number=1,
        pillar="Pillar Name",
        article_title="Article title",
        article_url="https://...",
        article_source="Source Name",
        hook="The hook text",
        post_content="Full post...",
        image_path="output/post1_image.jpg",
        published=False
    )
    ```

### Phase 8: Quality Check

14. If no quality stories exist, say so. Don't force weak content.

---

## Quick Commands

```bash
# View memory summary
python3 ~/rss-to-linkedin/memory.py

# Recent posts (last N days)
python3 ~/rss-to-linkedin/memory.py recent 7

# Search posts
python3 ~/rss-to-linkedin/memory.py search "keyword"

# Stats by pillar
python3 ~/rss-to-linkedin/memory.py stats
```

---

## User Overrides

The user may specify:
- `48 hours` — Look back 48 hours instead of 24
- `skip images` — Don't generate images
- `skip docs` — Don't paste to Google Docs
- `pillar: [name]` — Focus on specific content pillar
