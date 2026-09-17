"""
Simple Log Analyzer Tool
Analyzes log files and extracts metrics like errors, warnings, and timing information.
"""

import re
import json
import csv
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple
import argparse


class LogAnalyzer:
    """Analyzes log files and extracts metrics."""
    
    def __init__(self):
        self.log_patterns = {
            'error': re.compile(r'\[ERROR\]', re.IGNORECASE),
            'warning': re.compile(r'\[WARN\]', re.IGNORECASE),
            'info': re.compile(r'\[INFO\]', re.IGNORECASE),
            'timestamp': re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'),
            'duration': re.compile(r'duration[:\s]+(\d+(?:\.\d+)?)\s*(ms|s)', re.IGNORECASE)
        }
        self.metrics = {
            'total_lines': 0,
            'errors': 0,
            'warnings': 0,
            'info': 0,
            'timestamps': [],
            'durations': [],
            'error_messages': [],
            'warning_messages': []
        }
    
    def parse_line(self, line: str) -> Dict:
        """Parse a single log line and extract information."""
        result = {
            'line': line.strip(),
            'level': None,
            'timestamp': None,
            'duration': None,
            'is_error': False,
            'is_warning': False
        }
        
        # Detect log level
        if self.log_patterns['error'].search(line):
            result['level'] = 'ERROR'
            result['is_error'] = True
            self.metrics['error_messages'].append(line.strip())
        elif self.log_patterns['warning'].search(line):
            result['level'] = 'WARNING'
            result['is_warning'] = True
            self.metrics['warning_messages'].append(line.strip())
        elif self.log_patterns['info'].search(line):
            result['level'] = 'INFO'
        
        # Extract timestamp
        ts_match = self.log_patterns['timestamp'].search(line)
        if ts_match:
            result['timestamp'] = ts_match.group()
            self.metrics['timestamps'].append(result['timestamp'])
        
        # Extract duration
        dur_match = self.log_patterns['duration'].search(line)
        if dur_match:
            value = float(dur_match.group(1))
            unit = dur_match.group(2).lower()
            if unit == 's':
                value *= 1000  # Convert to ms
            result['duration'] = value
            self.metrics['durations'].append(value)
        
        return result
    
    def analyze_file(self, filepath: str) -> Dict:
        """Analyze a log file and return metrics."""
        self.metrics = {
            'total_lines': 0,
            'errors': 0,
            'warnings': 0,
            'info': 0,
            'timestamps': [],
            'durations': [],
            'error_messages': [],
            'warning_messages': []
        }
        
        parsed_lines = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    self.metrics['total_lines'] += 1
                    parsed = self.parse_line(line)
                    parsed_lines.append(parsed)
                    
                    if parsed['is_error']:
                        self.metrics['errors'] += 1
                    elif parsed['is_warning']:
                        self.metrics['warnings'] += 1
                    elif parsed['level'] == 'INFO':
                        self.metrics['info'] += 1
        
        except FileNotFoundError:
            return {'error': f'File not found: {filepath}'}
        except Exception as e:
            return {'error': f'Error reading file: {str(e)}'}
        
        return {
            'metrics': self.calculate_summary(),
            'parsed_lines': parsed_lines
        }
    
    def calculate_summary(self) -> Dict:
        """Calculate summary statistics from metrics."""
        summary = {
            'total_lines': self.metrics['total_lines'],
            'error_count': self.metrics['errors'],
            'warning_count': self.metrics['warnings'],
            'info_count': self.metrics['info'],
            'error_rate': 0,
            'warning_rate': 0,
            'avg_duration_ms': 0,
            'max_duration_ms': 0,
            'min_duration_ms': 0,
            'sample_errors': self.metrics['error_messages'][:5],
            'sample_warnings': self.metrics['warning_messages'][:5]
        }
        
        if self.metrics['total_lines'] > 0:
            summary['error_rate'] = (self.metrics['errors'] / self.metrics['total_lines']) * 100
            summary['warning_rate'] = (self.metrics['warnings'] / self.metrics['total_lines']) * 100
        
        if self.metrics['durations']:
            summary['avg_duration_ms'] = sum(self.metrics['durations']) / len(self.metrics['durations'])
            summary['max_duration_ms'] = max(self.metrics['durations'])
            summary['min_duration_ms'] = min(self.metrics['durations'])
        
        return summary
    
    def generate_report(self, analysis_result: Dict) -> str:
        """Generate a human-readable report."""
        if 'error' in analysis_result:
            return f"Error: {analysis_result['error']}"
        
        metrics = analysis_result['metrics']
        
        report = []
        report.append("=" * 60)
        report.append("LOG ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Total lines analyzed: {metrics['total_lines']}")
        report.append(f"Errors: {metrics['error_count']} ({metrics['error_rate']:.2f}%)")
        report.append(f"Warnings: {metrics['warning_count']} ({metrics['warning_rate']:.2f}%)")
        report.append(f"Info messages: {metrics['info_count']}")
        
        if metrics['avg_duration_ms'] > 0:
            report.append(f"\nDuration Statistics:")
            report.append(f"  Average: {metrics['avg_duration_ms']:.2f} ms")
            report.append(f"  Max: {metrics['max_duration_ms']:.2f} ms")
            report.append(f"  Min: {metrics['min_duration_ms']:.2f} ms")
        
        if metrics['sample_errors']:
            report.append(f"\nSample Errors (first 5):")
            for i, error in enumerate(metrics['sample_errors'], 1):
                report.append(f"  {i}. {error[:100]}...")
        
        if metrics['sample_warnings']:
            report.append(f"\nSample Warnings (first 5):")
            for i, warning in enumerate(metrics['sample_warnings'], 1):
                report.append(f"  {i}. {warning[:100]}...")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_json(self, analysis_result: Dict, output_file: str):
        """Export analysis results to JSON."""
        if 'error' in analysis_result:
            return
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'metrics': analysis_result['metrics']
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
    
    def export_csv(self, analysis_result: Dict, output_file: str):
        """Export analysis results to CSV."""
        if 'error' in analysis_result:
            return
        
        metrics = analysis_result['metrics']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Total Lines', metrics['total_lines']])
            writer.writerow(['Errors', metrics['error_count']])
            writer.writerow(['Warnings', metrics['warning_count']])
            writer.writerow(['Info', metrics['info_count']])
            writer.writerow(['Error Rate (%)', f"{metrics['error_rate']:.2f}"])
            writer.writerow(['Warning Rate (%)', f"{metrics['warning_rate']:.2f}"])
            writer.writerow(['Avg Duration (ms)', f"{metrics['avg_duration_ms']:.2f}"])
            writer.writerow(['Max Duration (ms)', f"{metrics['max_duration_ms']:.2f}"])
            writer.writerow(['Min Duration (ms)', f"{metrics['min_duration_ms']:.2f}"])


def main():
    """Main entry point for the log analyzer."""
    parser = argparse.ArgumentParser(description='Analyze log files and extract metrics')
    parser.add_argument('logfile', help='Path to the log file to analyze')
    parser.add_argument('--output-json', help='Export results to JSON file')
    parser.add_argument('--output-csv', help='Export results to CSV file')
    parser.add_argument('--report', action='store_true', help='Print human-readable report')
    
    args = parser.parse_args()
    
    analyzer = LogAnalyzer()
    result = analyzer.analyze_file(args.logfile)
    
    if args.report:
        print(analyzer.generate_report(result))
    
    if args.output_json:
        analyzer.export_json(result, args.output_json)
        print(f"JSON report saved to {args.output_json}")
    
    if args.output_csv:
        analyzer.export_csv(result, args.output_csv)
        print(f"CSV report saved to {args.output_csv}")
    
    if not (args.report or args.output_json or args.output_csv):
        print(analyzer.generate_report(result))


if __name__ == '__main__':
    main()
