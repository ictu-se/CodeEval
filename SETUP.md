# Setup Guide

## 🚀 Quick Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/codebleu-excel-processor.git
cd codebleu-excel-processor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Important**: Make sure to use compatible tree-sitter versions:
```bash
pip install "tree-sitter>=0.22.0,<0.24.0" "tree-sitter-python>=0.22.0,<0.24.0"
```

### 3. Test Installation

```bash
# Create sample Excel file
python excel_processor.py --create-sample

# Process the sample
python excel_processor.py --file sample_code_data.xlsx

# Analyze results
python analyze_results.py --file codebleu_results.csv --no-plots
```

## 🐛 Troubleshooting

### Common Issues

1. **Tree-sitter compatibility error:**
```
ValueError: Incompatible Language version 15. Must be between 13 and 14
```
**Solution:**
```bash
pip uninstall tree-sitter tree-sitter-python
pip install "tree-sitter>=0.22.0,<0.24.0" "tree-sitter-python>=0.22.0,<0.24.0"
```

2. **CodeBLEU not found:**
```
ModuleNotFoundError: No module named 'codebleu'
```
**Solution:**
```bash
pip install codebleu
```

3. **Excel reading error:**
```bash
# Install Excel support
pip install openpyxl xlrd
```

## 💻 Development Setup

### For Contributors

```bash
# Clone repo
git clone https://github.com/yourusername/codebleu-excel-processor.git
cd codebleu-excel-processor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
python excel_processor.py --create-sample
python excel_processor.py --file sample_code_data.xlsx
```

## 🌐 Language Support

Install language-specific parsers:

```bash
# Python (default)
pip install tree-sitter-python

# Java
pip install tree-sitter-java

# JavaScript
pip install tree-sitter-javascript

# C/C++
pip install tree-sitter-c tree-sitter-cpp

# Go
pip install tree-sitter-go

# Other languages
pip install tree-sitter-rust tree-sitter-ruby tree-sitter-php
```

## 📊 Usage Examples

### Basic Usage:
```bash
python excel_processor.py --file your_data.xlsx
```

### Advanced Usage:
```bash
python excel_processor.py \
    --file data.xlsx \
    --ref-col "Ground Truth Code" \
    --hyp-col "AI Generated Code" \
    --lang java \
    --weights "0.3,0.3,0.2,0.2" \
    --output results.csv
```

## 🎯 System Requirements

- **Python**: 3.8+
- **OS**: Windows, Linux, macOS
- **Memory**: 2GB+ recommended for large datasets
- **Disk Space**: 100MB+ for dependencies

## 📧 Support

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: See README.md and EXAMPLES.md
- **Community**: Star ⭐ and share if helpful!