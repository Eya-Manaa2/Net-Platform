"""
Log Pattern Matcher Skill
A flexible, configurable pattern matching system for log files.
"""

import re
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path


class PatternMatcher:
    """Flexible pattern matcher for log files."""
    
    def __init__(self):
        """Initialize with empty pattern set."""
        self.patterns: Dict[str, Dict] = {}
        self.compiled_patterns: Dict[str, re.Pattern] = {}
        self.statistics: Dict[str, int] = {'total_lines': 0, 'matches': {}}
    
    def add_pattern(self, name: str, regex: str, pattern_type: str = 'bool', 
                    extractor: Optional[Callable] = None, **kwargs) -> None:
        """
        Add a pattern to match.
        
        Args:
            name: Unique name for the pattern
            regex: Regular expression pattern
            pattern_type: Type of pattern (bool, capture, count, timestamp, duration)
            extractor: Custom extraction function
            **kwargs: Additional pattern-specific options
        """
        self.patterns[name] = {
            'regex': regex,
            'type': pattern_type,
            'extractor': extractor,
            'options': kwargs
        }
        self.compiled_patterns[name] = re.compile(regex)
        self.statistics['matches'][name] = 0
    
    def match_line(self, text: str) -> Dict[str, Any]:
        """
        Match all patterns against a single line of text.
        
        Args:
            text: Text line to match
            
        Returns:
            Dictionary with match results for each pattern
        """
        results = {}
        self.statistics['total_lines'] += 1
        
        for name, pattern in self.patterns.items():
            compiled = self.compiled_patterns[name]
            match = compiled.search(text)
            
            if match:
                self.statistics['matches'][name] += 1
                results[name] = self._extract_match(match, pattern)
            else:
                results[name] = self._default_value(pattern['type'])
        
        return results
    
    def match_file(self, filepath: str) -> List[Dict[str, Any]]:
        """
        Match patterns against an entire file.
        
        Args:
            filepath: Path to the file to process
            
        Returns:
            List of match results for each line
        """
        results = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line_result = self.match_line(line.strip())
                    results.append(line_result)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get match statistics.
        
        Returns:
            Dictionary with statistics for each pattern
        """
        return {
            'total_lines': self.statistics['total_lines'],
            'pattern_matches': self.statistics['matches'].copy(),
            'match_rates': {
                name: (count / self.statistics['total_lines'] * 100) 
                if self.statistics['total_lines'] > 0 else 0
                for name, count in self.statistics['matches'].items()
            }
        }
    
    def reset_statistics(self) -> None:
        """Reset all statistics to zero."""
        self.statistics = {'total_lines': 0, 'matches': {name: 0 for name in self.patterns}}
    
    @classmethod
    def from_config(cls, config_path: str) -> 'PatternMatcher':
        """
        Load patterns from a YAML configuration file.
        
        Args:
            config_path: Path to YAML config file
            
        Returns:
            PatternMatcher instance with loaded patterns
        """
        matcher = cls()
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        for pattern_config in config.get('patterns', []):
            matcher.add_pattern(
                name=pattern_config['name'],
                regex=pattern_config['regex'],
                pattern_type=pattern_config.get('type', 'bool'),
                **{k: v for k, v in pattern_config.items() 
                   if k not in ['name', 'regex', 'type']}
            )
        
        return matcher
    
    def _extract_match(self, match: re.Match, pattern: Dict) -> Any:
        """Extract value from regex match based on pattern type."""
        pattern_type = pattern['type']
        extractor = pattern.get('extractor')
        
        if extractor:
            return extractor(match)
        
        if pattern_type == 'bool':
            return True
        elif pattern_type == 'capture':
            return match.group(1) if match.groups() else True
        elif pattern_type == 'count':
            return len(match.groups())
        elif pattern_type == 'timestamp':
            format_str = pattern.get('options', {}).get('format', '%Y-%m-%d %H:%M:%S')
            return datetime.strptime(match.group(), format_str)
        elif pattern_type == 'duration':
            value = float(match.group(1))
            unit = match.group(2).lower() if len(match.groups()) > 1 else 'ms'
            return value * 1000 if unit == 's' else value
        else:
            return match.group()
    
    def _default_value(self, pattern_type: str) -> Any:
        """Return default value for pattern type when no match."""
        defaults = {
            'bool': False,
            'capture': None,
            'count': 0,
            'timestamp': None,
            'duration': 0
        }
        return defaults.get(pattern_type, None)


# Convenience functions for common patterns

def create_standard_matcher() -> PatternMatcher:
    """Create a PatternMatcher with standard log patterns."""
    matcher = PatternMatcher()
    
    # Standard log levels
    matcher.add_pattern('error', r'\[ERROR\]', 'bool')
    matcher.add_pattern('warning', r'\[WARN\]', 'bool')
    matcher.add_pattern('info', r'\[INFO\]', 'bool')
    matcher.add_pattern('debug', r'\[DEBUG\]', 'bool')
    
    # Common metrics
    matcher.add_pattern('timestamp', r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', 'timestamp')
    matcher.add_pattern('duration', r'duration[:\s]+(\d+(?:\.\d+)?)\s*(ms|s)', 'duration')
    matcher.add_pattern('response_time', r'response_time[:\s]+(\d+(?:\.\d+)?)\s*(ms|s)', 'duration')
    
    return matcher


def create_custom_matcher(patterns: List[Dict]) -> PatternMatcher:
    """
    Create a PatternMatcher from a list of pattern configurations.
    
    Args:
        patterns: List of pattern configuration dictionaries
        
    Returns:
        Configured PatternMatcher instance
    """
    matcher = PatternMatcher()
    
    for pattern in patterns:
        matcher.add_pattern(**pattern)
    
    return matcher
