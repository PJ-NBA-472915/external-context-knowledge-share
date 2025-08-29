#!/usr/bin/env python3
"""
Fix Checksums Script

This script updates all placeholder checksums in context files with actual calculated checksums.
"""

import hashlib
import yaml
from pathlib import Path
from typing import Dict, Tuple


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content
        
    try:
        # Find the end of frontmatter
        end_marker = content.find("---", 3)
        if end_marker == -1:
            return {}, content
            
        frontmatter_text = content[3:end_marker].strip()
        frontmatter = yaml.safe_load(frontmatter_text)
        body = content[end_marker + 3:].strip()
        
        return frontmatter or {}, body
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        return {}, content


def calculate_checksum(content: str) -> str:
    """Calculate SHA256 checksum of content (excluding frontmatter)."""
    _, body = parse_frontmatter(content)
    return f"sha256:{hashlib.sha256(body.encode('utf-8')).hexdigest()}"


def generate_frontmatter(metadata: Dict) -> str:
    """Generate YAML frontmatter from metadata."""
    frontmatter_lines = ["---"]
    
    # Add version metadata
    for key, value in metadata.items():
        if key in ["version", "version_type", "last_updated", "change_log", 
                   "dependencies", "breaking_changes", "author", "checksum"]:
            if isinstance(value, list):
                frontmatter_lines.append(f"{key}: {value}")
            elif isinstance(value, bool):
                frontmatter_lines.append(f"{key}: {str(value).lower()}")
            else:
                frontmatter_lines.append(f"{key}: {value}")
    
    # Add description and other fields if present
    for key, value in metadata.items():
        if key not in ["version", "version_type", "last_updated", "change_log", 
                      "dependencies", "breaking_changes", "author", "checksum"]:
            if isinstance(value, list):
                frontmatter_lines.append(f"{key}: {value}")
            elif isinstance(value, bool):
                frontmatter_lines.append(f"{key}: {str(value).lower()}")
            else:
                frontmatter_lines.append(f"{key}: {value}")
    
    frontmatter_lines.append("---")
    return "\n".join(frontmatter_lines)


def fix_file_checksum(file_path: Path) -> bool:
    """Fix checksum in a single file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        frontmatter, body = parse_frontmatter(content)
        
        if not frontmatter or "checksum" not in frontmatter:
            print(f"Skipping {file_path}: No checksum field")
            return False
        
        # Check if checksum is placeholder
        current_checksum = frontmatter.get("checksum", "")
        if "initial_checksum_placeholder" not in current_checksum:
            print(f"Skipping {file_path}: Checksum already set")
            return False
        
        # Calculate new checksum
        new_checksum = calculate_checksum(content)
        frontmatter["checksum"] = new_checksum
        
        # Generate new content
        new_frontmatter = generate_frontmatter(frontmatter)
        new_content = f"{new_frontmatter}\n\n{body}"
        
        # Write updated file
        file_path.write_text(new_content, encoding='utf-8')
        
        print(f"Updated {file_path} with checksum: {new_checksum}")
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False


def main():
    """Main function to fix all checksums."""
    context_root = Path("memory-bank")
    
    # Files to process
    files_to_process = [
        context_root / "context" / "entrypoint.md",
        context_root / "rules" / "external-context-management.md",
        context_root / "rules" / "task-file-usage.mdc",
        context_root / "rules" / "terminal-safety.md",
        context_root / "rules" / "multi-agent-locking-workflow.md",
        context_root / "rules" / "conventional-commits-no-scope.md",
        context_root / "rules" / "context-entrypoint.mdc",
        context_root / "gemini" / "GEMINI.md"
    ]
    
    updated_count = 0
    
    for file_path in files_to_process:
        if file_path.exists():
            if fix_file_checksum(file_path):
                updated_count += 1
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nUpdated {updated_count} files with new checksums")


if __name__ == "__main__":
    main()
