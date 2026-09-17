# Log Pattern Matcher Skill

## Overview

A reusable skill for matching and extracting patterns from log files. This skill provides a flexible, configurable way to parse log lines and extract structured data.

## Purpose

Extract structured information from unstructured log text using regex patterns. Common use cases:
- Error detection and counting
- Performance metric extraction
- Timestamp parsing
- Custom field extraction

## Installation

Copy this skill folder to your project's `skills/` directory.

## Usage

### Basic Usage

```python
from skills.log_pattern-matcher.pattern_matcher import PatternMatcher

matcher = PatternMatcher()

# Add custom patterns
matcher.add_pattern('error', r'\[ERROR\]', 'error')
matcher.add_pattern('warning', r'\[WARN\]', 'warning')
matcher.add_pattern('duration', r'duration[:\s]+(\d+(?:\.\d+)?)\s*(ms|s)', 'duration')

# Match patterns in text
result = matcher.match_line("2024-01-15 [ERROR] Failed to connect, duration: 150ms")
# Returns: {'error': True, 'warning': False, 'duration': '150ms'}
```

### Advanced Usage

```python
# Load patterns from configuration
matcher = PatternMatcher.from_config('patterns.yaml')

# Batch processing
results = matcher.match_file('application.log')

# Get statistics
stats = matcher.get_statistics()
```

## API Reference

### PatternMatcher Class

#### Methods

- `__init__()`: Initialize with default patterns
- `add_pattern(name, regex, type)`: Add a custom pattern
- `match_line(text)`: Match patterns in a single line
- `match_file(filepath)`: Match patterns in entire file
- `get_statistics()`: Get pattern match statistics
- `reset_statistics()`: Clear accumulated statistics
- `from_config(config_path)`: Load patterns from YAML config

### Pattern Types

- `'bool'`: Returns True/False if pattern matches
- `'capture'`: Returns captured groups
- `'count'`: Counts occurrences
- `'timestamp'`: Parses and returns datetime object
- `'duration'`: Parses and returns duration in milliseconds

## Configuration

### YAML Config Example

```yaml
patterns:
  - name: error
    regex: '\[ERROR\]'
    type: bool
  
  - name: warning
    regex: '\[WARN\]'
    type: bool
  
  - name: timestamp
    regex: '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    type: timestamp
    format: '%Y-%m-%d %H:%M:%S'
  
  - name: duration
    regex: 'duration[:\s]+(\d+(?:\.\d+)?)\s*(ms|s)'
    type: duration
```

## Examples

### Example 1: Error Detection

```python
matcher = PatternMatcher()
matcher.add_pattern('error', r'\[ERROR\]', 'bool')

log_line = "[ERROR] Database connection failed"
result = matcher.match_line(log_line)
# result = {'error': True}
```

### Example 2: Metric Extraction

```python
matcher = PatternMatcher()
matcher.add_pattern('response_time', r'response_time[:\s]+(\d+)ms', 'capture')

log_line = "Request completed, response_time: 250ms"
result = matcher.match_line(log_line)
# result = {'response_time': '250'}
```

### Example 3: File Processing

```python
matcher = PatternMatcher()
matcher.add_pattern('error', r'\[ERROR\]', 'bool')
matcher.add_pattern('warning', r'\[WARN\]', 'bool')

results = matcher.match_file('application.log')
stats = matcher.get_statistics()
# stats = {'error': 15, 'warning': 8, 'total_lines': 100}
```

## Testing

### Unit Tests

```python
import pytest
from skills.log-pattern-matcher.pattern_matcher import PatternMatcher

def test_error_pattern():
    matcher = PatternMatcher()
    matcher.add_pattern('error', r'\[ERROR\]', 'bool')
    result = matcher.match_line('[ERROR] Test error')
    assert result['error'] == True

def test_warning_pattern():
    matcher = PatternMatcher()
    matcher.add_pattern('warning', r'\[WARN\]', 'bool')
    result = matcher.match_line('[WARN] Test warning')
    assert result['warning'] == True
```

### Integration Tests

```bash
# Run with sample log file
python -m skills.log-pattern-matcher.test_matcher
```

## Performance

- **Single Line**: < 1ms per pattern match
- **File Processing**: ~1000 lines/second
- **Memory**: O(1) for line-by-line processing

## Limitations

1. Regex complexity affects performance
2. Large files may require streaming
3. Pattern conflicts may cause unexpected results
4. Case-sensitive by default (use `(?i)` for case-insensitive)

## Best Practices

1. **Test patterns** with sample data before production
2. **Use specific patterns** to avoid false positives
3. **Cache compiled patterns** for repeated use
4. **Handle exceptions** for malformed input
5. **Document custom patterns** in code comments

## Troubleshooting

### Pattern Not Matching

- Check regex syntax using regex tester
- Verify pattern type matches expected output
- Use `re.DEBUG` to see regex matching steps

### Performance Issues

- Simplify complex regex patterns
- Use pre-compiled patterns
- Process files in chunks if memory constrained

### Unexpected Results

- Check for pattern conflicts
- Verify pattern order (first match wins)
- Test with edge cases

## Extension Points

### Custom Pattern Types

```python
def custom_extractor(match):
    # Custom extraction logic
    return extracted_value

matcher.add_pattern('custom', regex, 'custom', extractor=custom_extractor)
```

### Post-Processing

```python
def post_process(results):
    # Transform results after matching
    return transformed_results

results = matcher.match_file('log.txt')
processed = post_process(results)
```

## Dependencies

- Python 3.9+
- re (standard library)
- yaml (optional, for config files)
- datetime (standard library)

## License

MIT License - Feel free to use and modify

## Contributing

To contribute improvements:
1. Add tests for new features
2. Update documentation
3. Follow existing code style
4. Submit pull request

## Version History

- v1.0.0: Initial release with basic pattern matching
- v1.1.0: Added YAML config support
- v1.2.0: Added duration and timestamp types
