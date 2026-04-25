import frontmatter
import json
from pathlib import Path
from datetime import datetime

def markdown_to_json_backup(
    source_dir: str = ".",
    output_file: str = "",  # Add prefered name for output_file
    recursive: bool = True
):
    source_path = Path(source_dir)
    posts = []

    # Choose search pattern
    pattern = "**/*.md" if recursive else "*.md"

    print(f"Scanning for .md files in: {source_path.resolve()}\n")

    for md_file in source_path.glob(pattern):
        if not md_file.is_file():
            continue

        try:
            post = frontmatter.load(md_file)

            # Build a clean dictionary for each post
            post_dict = {
                "filename": md_file.name,
                "filepath": str(md_file.relative_to(source_path)),
                "last_modified": datetime.fromtimestamp(
                    md_file.stat().st_mtime
                ).isoformat(),
                "metadata": dict(post.metadata),   # front matter as dict
                "content": post.content,           # markdown body
                "content_preview": post.content[:300] + "..." 
                    if len(post.content) > 300 else post.content,
            }

            posts.append(post_dict)
            print(f"✓ Processed: {md_file.name}")

        except Exception as e:
            print(f"✗ Error processing {md_file.name}: {e}")

    # Sort by filename
    posts.sort(key=lambda x: x["filename"])

    # Write to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n✅ Done! {len(posts)} posts saved to '{output_file}'")
    return posts


# ====================== RUN IT ======================
if __name__ == "__main__":
    markdown_to_json_backup(
        source_dir=".",     # Change to directory containing md files of your posts      
        output_file=".",    # Change to desired name for archive file
        recursive=True      # Set False if you don't want subfolders
    )