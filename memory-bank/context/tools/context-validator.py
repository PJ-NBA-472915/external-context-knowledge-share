#!/usr/bin/env python3
"""
Context Validation Tool

This script validates context files in the memory-bank system for:
- Version metadata consistency
- Dependency integrity
- Checksum validation
- File structure compliance
"""

import argparse
import hashlib
import os
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set


class ContextValidator:
    """Validates context files for version control consistency."""
    
    def __init__(self, context_root: str = "memory-bank"):
        self.context_root = Path(context_root).resolve()
        self.versions_dir = self.context_root / "context" / "versions"
        self.validation_errors = []
        self.validation_warnings = []
        
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
            self.validation_errors.append(f"YAML parsing error: {e}")
            return {}, content
    
    def calculate_checksum(self, content: str) -> str:
        """Calculate SHA256 checksum of content (excluding frontmatter)."""
        _, body = self.parse_frontmatter(content)
        return f"sha256:{hashlib.sha256(body.encode('utf-8')).hexdigest()}"
    
    def validate_version_format(self, version: str) -> bool:
        """Validate semantic version format."""
        # Basic semantic versioning pattern
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'
        return bool(re.match(pattern, version))
    
    def validate_timestamp_format(self, timestamp: str) -> bool:
        """Validate timestamp format (YYYY-MM-DD HH:MM)."""
        try:
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False
    
    def validate_required_fields(self, frontmatter: Dict, file_path: Path) -> bool:
        """Validate that all required fields are present."""
        required_fields = [
            "version", "version_type", "last_updated", 
            "change_log", "breaking_changes", "author", "checksum"
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in frontmatter:
                missing_fields.append(field)
        
        if missing_fields:
            self.validation_errors.append(
                f"{file_path}: Missing required fields: {', '.join(missing_fields)}"
            )
            return False
        
        return True
    
    def validate_field_types(self, frontmatter: Dict, file_path: Path) -> bool:
        """Validate field types and formats."""
        valid = True
        
        # Validate version format
        if not self.validate_version_format(frontmatter["version"]):
            self.validation_errors.append(
                f"{file_path}: Invalid version format: {frontmatter['version']}"
            )
            valid = False
        
        # Validate version_type
        valid_types = ["patch", "minor", "major", "pre-release"]
        if frontmatter["version_type"] not in valid_types:
            self.validation_errors.append(
                f"{file_path}: Invalid version_type: {frontmatter['version_type']}"
            )
            valid = False
        
        # Validate timestamp
        if not self.validate_timestamp_format(frontmatter["last_updated"]):
            self.validation_errors.append(
                f"{file_path}: Invalid timestamp format: {frontmatter['last_updated']}"
            )
            valid = False
        
        # Validate breaking_changes is boolean
        if not isinstance(frontmatter["breaking_changes"], bool):
            self.validation_errors.append(
                f"{file_path}: breaking_changes must be boolean, got {type(frontmatter['breaking_changes'])}"
            )
            valid = False
        
        # Validate dependencies is list
        if "dependencies" in frontmatter and not isinstance(frontmatter["dependencies"], list):
            self.validation_errors.append(
                f"{file_path}: dependencies must be list, got {type(frontmatter['dependencies'])}"
            )
            valid = False
        
        return valid
    
    def validate_checksum(self, frontmatter: Dict, content: str, file_path: Path) -> bool:
        """Validate that stored checksum matches calculated checksum."""
        stored_checksum = frontmatter.get("checksum", "")
        calculated_checksum = self.calculate_checksum(content)
        
        if stored_checksum != calculated_checksum:
            self.validation_errors.append(
                f"{file_path}: Checksum mismatch\n"
                f"  Stored: {stored_checksum}\n"
                f"  Calculated: {calculated_checksum}"
            )
            return False
        
        return True
    
    def validate_version_consistency(self, frontmatter: Dict, file_path: Path) -> bool:
        """Validate version consistency between version and version_type."""
        version = frontmatter["version"]
        version_type = frontmatter["version_type"]
        
        # Extract major.minor.patch
        if "-" in version:
            version = version.split("-")[0]
        
        major, minor, patch = map(int, version.split('.')[:3])
        
        # Check if version_type matches version increment
        if version_type == "major" and minor != 0:
            self.validation_warnings.append(
                f"{file_path}: Major version {version} has non-zero minor component"
            )
        
        if version_type == "minor" and patch != 0:
            self.validation_warnings.append(
                f"{file_path}: Minor version {version} has non-zero patch component"
            )
        
        return True
    
    def validate_dependencies(self, frontmatter: Dict, file_path: Path) -> bool:
        """Validate that referenced dependencies exist."""
        dependencies = frontmatter.get("dependencies", [])
        valid = True
        
        for dep in dependencies:
            # Resolve relative path
            if dep.startswith("../"):
                dep_path = file_path.parent / dep
            else:
                dep_path = file_path.parent / dep
            
            if not dep_path.exists():
                self.validation_errors.append(
                    f"{file_path}: Dependency not found: {dep} -> {dep_path}"
                )
                valid = False
            else:
                # Check if dependency has version metadata
                try:
                    dep_content = dep_path.read_text(encoding='utf-8')
                    dep_frontmatter, _ = self.parse_frontmatter(dep_content)
                    
                    if not dep_frontmatter or "version" not in dep_frontmatter:
                        self.validation_warnings.append(
                            f"{file_path}: Dependency {dep} has no version metadata"
                        )
                except Exception as e:
                    self.validation_warnings.append(
                        f"{file_path}: Could not read dependency {dep}: {e}"
                    )
        
        return valid
    
    def validate_file_structure(self, file_path: Path) -> bool:
        """Validate file structure and markdown formatting."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Check if file has content
            if not content.strip():
                self.validation_errors.append(f"{file_path}: File is empty")
                return False
            
            # Check if file has frontmatter
            if not content.startswith("---"):
                self.validation_errors.append(f"{file_path}: Missing YAML frontmatter")
                return False
            
            # Check if frontmatter is properly closed
            if content.count("---") < 2:
                self.validation_errors.append(f"{file_path}: Incomplete YAML frontmatter")
                return False
            
            # Parse frontmatter
            frontmatter, body = self.parse_frontmatter(content)
            
            if not frontmatter:
                self.validation_errors.append(f"{file_path}: Could not parse frontmatter")
                return False
            
            # Validate required fields
            if not self.validate_required_fields(frontmatter, file_path):
                return False
            
            # Validate field types
            if not self.validate_field_types(frontmatter, file_path):
                return False
            
            # Validate checksum
            if not self.validate_checksum(frontmatter, content, file_path):
                return False
            
            # Validate version consistency
            if not self.validate_version_consistency(frontmatter, file_path):
                return False
            
            # Validate dependencies
            if not self.validate_dependencies(frontmatter, file_path):
                return False
            
            return True
            
        except Exception as e:
            self.validation_errors.append(f"{file_path}: Error reading file: {e}")
            return False
    
    def validate_version_history(self, file_path: Path) -> bool:
        """Validate that version history files exist and are consistent."""
        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter, _ = self.parse_frontmatter(content)
            version = frontmatter.get("version", "")
            
            if not version:
                return True  # Skip if no version
            
            # Determine version history path
            rel_path = file_path.relative_to(self.context_root)
            
            # Handle special case for entrypoint.md
            if file_path.name == "entrypoint.md":
                history_file = self.versions_dir / "entrypoint" / f"{version}.md"
            else:
                version_dir = self.versions_dir / rel_path.parent / rel_path.stem
                history_file = version_dir / f"{version}.md"
            
            if not history_file.exists():
                self.validation_warnings.append(
                    f"{file_path}: Version history file not found: {history_file}"
                )
                return False
            
            return True
            
        except Exception as e:
            self.validation_warnings.append(f"{file_path}: Error checking version history: {e}")
            return False
    
    def validate_all_files(self) -> bool:
        """Validate all context files in the system."""
        scan_dirs = [
            self.context_root / "context",
            self.context_root / "rules", 
            self.context_root / "gemini"
        ]
        
        total_files = 0
        valid_files = 0
        
        for scan_dir in scan_dirs:
            if scan_dir.exists():
                for file_path in scan_dir.rglob("*.md"):
                    if file_path.is_file():
                        # Skip version history files, spec files, and virtual environment
                        if ("versions" in file_path.parts or "spec" in file_path.parts or 
                            "venv" in file_path.parts):
                            continue
                            
                        total_files += 1
                        print(f"Validating {file_path}...")
                        
                        if self.validate_file_structure(file_path):
                            valid_files += 1
                            
                            # Also validate version history
                            self.validate_version_history(file_path)
                        else:
                            print(f"  ❌ Validation failed")
            
            else:
                print(f"Warning: Directory {scan_dir} does not exist")
        
        print(f"\nValidation Summary:")
        print(f"  Total files: {total_files}")
        print(f"  Valid files: {valid_files}")
        print(f"  Errors: {len(self.validation_errors)}")
        print(f"  Warnings: {len(self.validation_warnings)}")
        
        if self.validation_errors:
            print(f"\nValidation Errors:")
            for error in self.validation_errors:
                print(f"  ❌ {error}")
        
        if self.validation_warnings:
            print(f"\nValidation Warnings:")
            for warning in self.validation_warnings:
                print(f"  ⚠️  {warning}")
        
        return len(self.validation_errors) == 0
    
    def validate_single_file(self, file_path: str) -> bool:
        """Validate a single context file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist")
            return False
        
        if not file_path.is_file():
            print(f"Error: {file_path} is not a file")
            return False
        
        print(f"Validating {file_path}...")
        
        if self.validate_file_structure(file_path):
            print(f"  ✅ File structure validation passed")
            
            # Validate version history
            print(f"  Checking version history...")
            if self.validate_version_history(file_path):
                print(f"  ✅ Version history validation passed")
            else:
                print(f"  ⚠️  Version history validation failed")
            
            return True
        else:
            print(f"  ❌ File structure validation failed")
            return False


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Context Validation Tool")
    parser.add_argument("command", choices=["validate", "validate-file"], 
                       help="Command to execute")
    parser.add_argument("--file", "-f", help="Target file path for single file validation")
    parser.add_argument("--context-root", default="memory-bank",
                       help="Context root directory")
    
    args = parser.parse_args()
    
    validator = ContextValidator(args.context_root)
    
    if args.command == "validate":
        success = validator.validate_all_files()
        sys.exit(0 if success else 1)
    
    elif args.command == "validate-file":
        if not args.file:
            print("Error: validate-file command requires --file")
            sys.exit(1)
        
        success = validator.validate_single_file(args.file)
        sys.exit(0 if success else 1)
    
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
