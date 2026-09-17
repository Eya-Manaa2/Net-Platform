# AGENTS.md - Log Analyzer Project

This document is a specialized README for AI coding agents working on this project.

## Project Overview

**Log Analyzer** - A Python tool for analyzing log files and extracting metrics like errors, warnings, and timing information.

**Tech Stack**: Python 3.9+, argparse, re, json, csv

## Quick Start

### Installation

```bash
# No external dependencies required - uses only Python standard library
python --version  # Ensure Python 3.9+
```

### Running the Tool

```bash
# Basic usage
python log_analyzer.py sample.log --report

# Export to JSON
python log_analyzer.py sample.log --output-json results.json

# Export to CSV
python log_analyzer.py sample.log --output-csv results.csv

# Combined
python log_analyzer.py sample.log --report --output-json results.json --output-csv results.csv
```

## Project Structure

```
lab1/
├── log_analyzer.py       # Main application
├── sample.log           # Sample log file for testing
├── AGENTS.md           # This file
├── README.md           # User documentation
└── REFLECTION.md      # Lab 1 reflection
```

## Code Style & Conventions

### Python Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Docstrings for all functions and classes
- Maximum line length: 100 characters
- Use f-strings for string formatting

### Naming Conventions

- Classes: `PascalCase` (e.g., `LogAnalyzer`)
- Functions: `snake_case` (e.g., `analyze_file`)
- Variables: `snake_case` (e.g., `error_count`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)

### Error Handling

- Always handle file operations with try/except
- Return error dictionaries for file operations
- Use specific exception types when possible
- Log errors appropriately

## Testing

### Manual Testing

```bash
# Test with sample log file
python log_analyzer.py sample.log --report

# Verify JSON export
python log_analyzer.py sample.log --output-json test.json
cat test.json

# Verify CSV export
python log_analyzer.py sample.log --output-csv test.csv
cat test.csv
```

### Test Cases to Verify

1. **Basic Analysis**: Run with sample.log, verify metrics are correct
2. **Error Handling**: Test with non-existent file, should show error message
3. **JSON Export**: Verify JSON structure and data
4. **CSV Export**: Verify CSV format and data
5. **Empty File**: Test with empty log file
6. **No Matches**: Test with log file that has no errors/warnings

### Expected Results for sample.log

- Total lines: 20
- Errors: 3
- Warnings: 4
- Info: 13
- Error rate: 15%
- Warning rate: 20%

## Guardrails & Validation

### Code Quality Checks

Before committing or suggesting changes, verify:

1. **Syntax**: Code must be syntactically correct Python
2. **Type Hints**: All functions should have type hints
3. **Docstrings**: All functions/classes must have docstrings
4. **Error Handling**: File operations must have try/except blocks
5. **Imports**: Only use standard library imports (no external dependencies)

### Functional Validation

1. **Pattern Matching**: Log patterns must correctly identify ERROR, WARN, INFO
2. **Timestamp Extraction**: Must handle standard timestamp formats
3. **Duration Parsing**: Must handle both ms and s units
4. **Export Formats**: JSON and CSV must be valid
5. **Edge Cases**: Handle empty files, missing files, malformed logs

### Security Considerations

- No execution of user-provided code
- No network operations
- No file system writes outside specified output files
- Sanitize all file paths

## Architecture

### Core Components

1. **LogAnalyzer Class**: Main analysis engine
   - `parse_line()`: Parse individual log lines
   - `analyze_file()`: Process entire log file
   - `calculate_summary()`: Compute statistics
   - `generate_report()`: Create human-readable output
   - `export_json()`: Export to JSON format
   - `export_csv()`: Export to CSV format

2. **Pattern Matching**: Regex patterns for log levels and metrics
3. **Metrics Collection**: Dictionary-based metrics storage
4. **Export Formats**: JSON and CSV generation

### Data Flow

```
Log File → Parse Line → Extract Metrics → Calculate Summary → Export
```

## Common Tasks

### Adding New Log Patterns

1. Add regex pattern to `self.log_patterns` in `__init__`
2. Update `parse_line()` to extract new pattern
3. Update `calculate_summary()` to include new metric
4. Update `generate_report()` to display new metric
5. Update export methods to include new metric

### Modifying Export Formats

1. Update `export_json()` for JSON changes
2. Update `export_csv()` for CSV changes
3. Ensure backward compatibility if possible
4. Update documentation

### Adding Command-Line Options

1. Add argument to `argparse` in `main()`
2. Implement logic to handle new option
3. Update help text
4. Test with new option

## Dependencies

**Standard Library Only** (no external dependencies):

- `re`: Regular expressions
- `json`: JSON handling
- `csv`: CSV handling
- `datetime`: Date/time operations
- `collections`: Data structures
- `typing`: Type hints
- `argparse`: Command-line parsing

## Performance Considerations

- File reading is line-by-line (memory efficient)
- Regex patterns are compiled once in `__init__`
- Metrics are calculated in a single pass
- Suitable for files up to several GB

## Known Limitations

1. **Timestamp Format**: Expects `YYYY-MM-DD HH:MM:SS` format
2. **Duration Format**: Expects `duration: X ms` or `duration: X s`
3. **Log Levels**: Case-sensitive matching for [ERROR], [WARN], [INFO]
4. **Memory**: Loads entire parsed lines into memory (not suitable for massive files)
5. **Encoding**: Assumes UTF-8 encoding

## Troubleshooting

### Common Issues

**Issue**: "File not found" error
- **Solution**: Verify file path is correct and file exists

**Issue**: No metrics extracted
- **Solution**: Check log format matches expected patterns

**Issue**: Incorrect duration values
- **Solution**: Verify duration format in logs matches pattern

**Issue**: Export files not created
- **Solution**: Check write permissions in output directory

## Extension Points

### Future Enhancements

1. **Configurable Patterns**: Allow custom regex patterns via config file
2. **Multiple File Support**: Process multiple log files at once
3. **Real-time Monitoring**: Monitor log files as they're written
4. **Alerting**: Send alerts when error thresholds exceeded
5. **Visualization**: Generate charts and graphs
6. **Database Storage**: Store metrics in database
7. **API**: REST API for log analysis

## Contact & Support

For issues or questions about this project:
- Check the main README.md
- Review the REFLECTION.md for workflow insights
- Test with sample.log before using custom logs
