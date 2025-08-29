#!/usr/bin/env python3
"""
Context Version Control Tool

This script provides automated version bumping for context files in the memory-bank system.
It handles semantic versioning, metadata updates, and version history management.
"""

import argparse
import hashlib
import os
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ContextVersionManager:
    """Manages version control for context files in the memory-bank system."""
    
    def __init__(self, context_root: str = "memory-bank"):
        self.context_root = Path(context_root).resolve()
        self.versions_dir = self.context_root / "context" / "versions"
        
    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
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
            print(f"Error parsing frontmatter: {e}")
            return {}, content
    
    def generate_frontmatter(self, metadata: Dict) -> str:
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
    
    def calculate_checksum(self, content: str) -> str:
        """Calculate SHA256 checksum of content (excluding frontmatter)."""
        # Remove frontmatter for checksum calculation
        _, body = self.parse_frontmatter(content)
        return f"sha256:{hashlib.sha256(body.encode('utf-8')).hexdigest()}"
    
    def bump_version(self, current_version: str, bump_type: str) -> str:
        """Bump version according to semantic versioning rules."""
        if not re.match(r'^\d+\.\d+\.\d+', current_version):
            raise ValueError(f"Invalid version format: {current_version}")
        
        major, minor, patch = map(int, current_version.split('.')[:3])
        
        if bump_type == "patch":
            patch += 1
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "pre-release":
            # Handle pre-release versions
            if "-" in current_version:
                pre_part = current_version.split("-", 1)[1]
                if "." in pre_part:
                    pre_type, pre_num = pre_part.split(".", 1)
                    pre_num = int(pre_num) + 1
                    return f"{major}.{minor}.{patch}-{pre_type}.{pre_num}"
                else:
                    return f"{major}.{minor}.{patch}-{pre_part}.1"
            else:
                return f"{major}.{minor}.{patch}-alpha.1"
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        return f"{major}.{minor}.{patch}"
    
    def update_file_metadata(self, file_path: Path, bump_type: str, change_log: str) -> bool:
        """Update file metadata with new version information."""
        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, body = self.parse_frontmatter(content)
            
            if not frontmatter:
                print(f"Warning: No frontmatter found in {file_path}")
                return False
            
            # Get current version
            current_version = frontmatter.get("version", "1.0.0")
            
            # Bump version
            new_version = self.bump_version(current_version, bump_type)
            
            # Update metadata
            frontmatter.update({
                "version": new_version,
                "version_type": bump_type,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "change_log": change_log
            })
            
            # Generate new content
            new_frontmatter = self.generate_frontmatter(frontmatter)
            new_content = f"{new_frontmatter}\n\n{body}"
            
            # Calculate new checksum
            new_checksum = self.calculate_checksum(new_content)
            frontmatter["checksum"] = new_checksum
            
            # Generate final content with updated checksum
            final_frontmatter = self.generate_frontmatter(frontmatter)
            final_content = f"{final_frontmatter}\n\n{body}"
            
            # Write updated file
            file_path.write_text(final_content, encoding='utf-8')
            
            print(f"Updated {file_path} to version {new_version}")
            return True
            
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
            return False
    
    def create_version_history(self, file_path: Path, version: str, metadata: Dict) -> bool:
        """Create version history entry."""
        try:
            # Determine relative path from context root
            rel_path = file_path.relative_to(self.context_root)
            
            # Create version history directory structure
            version_dir = self.versions_dir / rel_path.parent / rel_path.stem
            version_dir.mkdir(parents=True, exist_ok=True)
            
            # Create version history file
            history_file = version_dir / f"{version}.md"
            
            # Generate history content
            history_content = self.generate_version_history_content(file_path, version, metadata)
            history_file.write_text(history_content, encoding='utf-8')
            
            print(f"Created version history: {history_file}")
            return True
            
        except Exception as e:
            print(f"Error creating version history: {e}")
            return False
    
    def generate_version_history_content(self, file_path: Path, version: str, metadata: Dict) -> str:
        """Generate content for version history file."""
        rel_path = file_path.relative_to(self.context_root)
        
        content = f"""# {file_path.stem} - Version {version}

**File**: `{rel_path}`  
**Version**: {version}  
**Date**: {metadata.get('last_updated', 'N/A')}  
**Author**: {metadata.get('author', 'N/A')}  
**Change Type**: {metadata.get('version_type', 'N/A')}  

## Change Log
{metadata.get('change_log', 'N/A')}

## Content Summary
This version includes the following changes and features:

- Version metadata implementation
- Automated version bumping
- Change tracking and history

## Dependencies
{metadata.get('dependencies', [])}

## Breaking Changes
{metadata.get('breaking_changes', False)}

## Migration Notes
- This version introduces version control metadata
- Existing files have been updated with version information

## File Checksum
{metadata.get('checksum', 'N/A')}

---

*This file is part of the version history for {rel_path}. It represents the state of the file at version {version}.*
"""
        return content
    
    def bump_file_version(self, file_path: str, bump_type: str, change_log: str) -> bool:
        """Main method to bump version of a context file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist")
            return False
        
        if not file_path.is_file():
            print(f"Error: {file_path} is not a file")
            return False
        
        # Update file metadata
        if not self.update_file_metadata(file_path, bump_type, change_log):
            return False
        
        # Read updated metadata
        content = file_path.read_text(encoding='utf-8')
        frontmatter, _ = self.parse_frontmatter(content)
        
        # Create version history
        if not self.create_version_history(file_path, frontmatter["version"], frontmatter):
            return False
        
        print(f"Successfully bumped {file_path} to version {frontmatter['version']}")
        return True
    
    def list_versioned_files(self) -> List[Path]:
        """List all context files that have version metadata."""
        versioned_files = []
        
        # Scan context, rules, and gemini directories
        scan_dirs = [
            self.context_root / "context",
            self.context_root / "rules", 
            self.context_root / "gemini"
        ]
        
        for scan_dir in scan_dirs:
            if scan_dir.exists():
                for file_path in scan_dir.rglob("*.md"):
                    if file_path.is_file():
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            frontmatter, _ = self.parse_frontmatter(content)
                            
                            if frontmatter and "version" in frontmatter:
                                versioned_files.append(file_path)
                        except Exception as e:
                            print(f"Warning: Could not read {file_path}: {e}")
            else:
                print(f"Warning: Directory {scan_dir} does not exist")
        
        return versioned_files
    
    def show_file_status(self, file_path: str) -> bool:
        """Show version status of a specific file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist")
            return False
        
        content = file_path.read_text(encoding='utf-8')
        frontmatter, _ = self.parse_frontmatter(content)
        
        if not frontmatter or "version" not in frontmatter:
            print(f"{file_path}: No version metadata")
            return False
        
        print(f"{file_path}:")
        print(f"  Version: {frontmatter.get('version', 'N/A')}")
        print(f"  Type: {frontmatter.get('version_type', 'N/A')}")
        print(f"  Last Updated: {frontmatter.get('last_updated', 'N/A')}")
        print(f"  Change Log: {frontmatter.get('change_log', 'N/A')}")
        print(f"  Author: {frontmatter.get('author', 'N/A')}")
        print(f"  Breaking Changes: {frontmatter.get('breaking_changes', 'N/A')}")
        
        dependencies = frontmatter.get('dependencies', [])
        if dependencies:
            print(f"  Dependencies: {', '.join(dependencies)}")
        
        return True


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Context Version Control Tool")
    parser.add_argument("command", choices=["bump", "status", "list"], 
                       help="Command to execute")
    parser.add_argument("--file", "-f", help="Target file path")
    parser.add_argument("--type", "-t", choices=["patch", "minor", "major", "pre-release"],
                       help="Version bump type")
    parser.add_argument("--change-log", "-c", help="Change log description")
    parser.add_argument("--context-root", default="memory-bank",
                       help="Context root directory")
    
    args = parser.parse_args()
    
    manager = ContextVersionManager(args.context_root)
    
    if args.command == "bump":
        if not args.file or not args.type or not args.change_log:
            print("Error: bump command requires --file, --type, and --change-log")
            sys.exit(1)
        
        success = manager.bump_file_version(args.file, args.type, args.change_log)
        sys.exit(0 if success else 1)
    
    elif args.command == "status":
        if not args.file:
            print("Error: status command requires --file")
            sys.exit(1)
        
        success = manager.show_file_status(args.file)
        sys.exit(0 if success else 1)
    
    elif args.command == "list":
        versioned_files = manager.list_versioned_files()
        if versioned_files:
            print("Versioned context files:")
            for file_path in versioned_files:
                print(f"  {file_path}")
        else:
            print("No versioned context files found")
    
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
