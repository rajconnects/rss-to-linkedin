#!/usr/bin/env python3
"""
LinkedIn Post Helper
Reads the latest draft and provides instructions for Claude Code browser automation.
"""

from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"

def get_latest_post():
    """Read the latest post draft."""
    latest_path = OUTPUT_DIR / "latest_post.txt"
    if not latest_path.exists():
        return None
    return latest_path.read_text(encoding='utf-8')

def main():
    post = get_latest_post()

    if not post:
        print("❌ No draft found. Run workflow.py first.")
        return

    print("\n" + "="*70)
    print("  LINKEDIN POST DRAFT READY")
    print("="*70)
    print("\n" + post)
    print("\n" + "="*70)
    print("\n📋 POST CONTENT COPIED TO CLIPBOARD (if supported)")
    print("\n🤖 To post via Claude Code browser automation, say:")
    print('   "Open LinkedIn and help me post this draft"')
    print("\n   Claude will:")
    print("   1. Open browser to linkedin.com")
    print("   2. Wait for you to log in (if needed)")
    print("   3. Navigate to create post")
    print("   4. Paste the draft")
    print("   5. Stop for your review before publishing")
    print("\n")

    # Try to copy to clipboard (macOS)
    try:
        import subprocess
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(post.encode('utf-8'))
        print("✅ Post copied to clipboard!")
    except:
        pass

if __name__ == "__main__":
    main()
