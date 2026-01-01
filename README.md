# CodeEval
# 📘 Hướng dẫn cài đặt và sử dụng CodeBLEU

## 📖 Giới thiệu

**CodeBLEU** là một metric đánh giá chất lượng code được sinh ra tự động, kết hợp 4 thành phần:

- **🔤 N-gram Match (BLEU)** - Độ tương tự từ ngữ
- **🏷️ Weighted N-gram Match** - Ưu tiên từ khóa quan trọng  
- **🌳 Syntax Match (AST)** - So sánh cấu trúc cú pháp
- **🔗 Dataflow Match** - So sánh luồng dữ liệu/logic

## 🚀 Cài đặt

### ⚠️ Yêu cầu hệ thống

- **Python**: 3.9+
- **OS**: Windows, Linux, macOS
- **Dependencies**: tree-sitter, tree-sitter-python

### 📦 Cài đặt qua pip

```bash
# Cài đặt CodeBLEU
pip install codebleu

# Cài đặt tree-sitter với phiên bản tương thích
pip install "tree-sitter>=0.22.0,<0.24.0"

# Cài đặt parser cho Python (hoặc ngôn ngữ khác)
pip install "tree-sitter-python>=0.22.0,<0.24.0"
```

### 🌐 Cài đặt tất cả ngôn ngữ

```bash
# Cài đặt tất cả parsers
pip install codebleu[all]
```

### ⚙️ Cài đặt từ source

```bash
# Clone repository
git clone https://github.com/k4black/codebleu.git
cd codebleu

# Cài đặt dependencies
pip install "tree-sitter>=0.22.0,<0.24.0" "tree-sitter-python>=0.22.0,<0.24.0"

# Cài đặt development mode
pip install -e .
```

### ⚠️ Lưu ý về phiên bản

**Quan trọng**: Phải sử dụng tree-sitter version `>=0.22.0,<0.24.0` để tránh lỗi incompatible language version:

```bash
# ❌ Lỗi thường gặp với tree-sitter 0.25.x
ValueError: Incompatible Language version 15. Must be between 13 and 14

# ✅ Giải pháp: cài đặt đúng version
pip install "tree-sitter>=0.22.0,<0.24.0"
```

## 🌐 Ngôn ngữ được hỗ trợ

| Ngôn ngữ | Package | Keyword |
|----------|---------|---------|
| Python | `tree-sitter-python` | `python` |
| Java | `tree-sitter-java` | `java` |
| JavaScript | `tree-sitter-javascript` | `javascript` |
| C# | `tree-sitter-c-sharp` | `c_sharp` |
| C | `tree-sitter-c` | `c` |
| C++ | `tree-sitter-cpp` | `cpp` |
| Go | `tree-sitter-go` | `go` |
| PHP | `tree-sitter-php` | `php` |
| Ruby | `tree-sitter-ruby` | `ruby` |
| Rust | `tree-sitter-rust` | `rust` |

## 💻 Sử dụng cơ bản

### 📝 Python API

```python
from codebleu import calc_codebleu

# Ví dụ đơn giản
references = ["def foo(x):\n    return x"]
predictions = ["def bar(y):\n    return y"]

result = calc_codebleu(references, predictions, "python")

print(f"CodeBLEU Score: {result['codebleu']:.4f}")
print(f"N-gram: {result['ngram_match_score']:.4f}")
print(f"Weighted: {result['weighted_ngram_match_score']:.4f}")
print(f"Syntax: {result['syntax_match_score']:.4f}")
print(f"Dataflow: {result['dataflow_match_score']:.4f}")
```

### 🎛️ Tùy chỉnh weights

```python
# Weights mặc định: (0.25, 0.25, 0.25, 0.25)
# (alpha, beta, gamma, theta) = (ngram, weighted_ngram, syntax, dataflow)

# Ưu tiên logic/dataflow
weights = (0.2, 0.2, 0.2, 0.4)
result = calc_codebleu(references, predictions, "python", weights=weights)

# Ưu tiên syntax
weights = (0.2, 0.2, 0.4, 0.2)
result = calc_codebleu(references, predictions, "python", weights=weights)

# Chỉ quan tâm BLEU + logic  
weights = (0.5, 0.0, 0.0, 0.5)
result = calc_codebleu(references, predictions, "python", weights=weights)
```

### 📋 Multiple references

```python
# Nhiều reference cho 1 prediction
references = [
    ["def add(a, b):\n    return a + b"],           # Reference 1
    ["def sum_two(x, y):\n    return x + y"]        # Reference 2
]
predictions = ["def add_nums(a, b):\n    return a + b"]

result = calc_codebleu(references, predictions, "python")
```

### 🔧 Custom tokenizer

```python
def custom_tokenizer(code):
    # Custom tokenization logic
    return code.replace("(", " ( ").replace(")", " ) ").split()

result = calc_codebleu(
    references, 
    predictions, 
    "python", 
    tokenizer=custom_tokenizer
)
```

## 🖥️ Command Line Interface

### 📄 Chuẩn bị files

```bash
# reference.py
def calculate_area(radius):
    pi = 3.14159
    area = pi * radius * radius
    return area

# prediction.py  
def calculate_area(r):
    import math
    area = math.pi * r ** 2
    return area
```

### 🚀 Chạy CLI

```bash
# Cú pháp cơ bản
python -m codebleu --refs reference.py --hyp prediction.py --lang python

# Kết quả
# ngram_match: 0.0606
# weighted_ngram_match: 0.0676
# syntax_match: 0.3846
# dataflow_match: 0.3333
# CodeBLEU score: 0.2115
```

### ⚙️ Tùy chọn CLI

```bash
# Với custom weights (alpha,beta,gamma,theta)
python -m codebleu --refs ref.py --hyp pred.py --lang python --params "0.3,0.3,0.2,0.2"

# Nhiều reference files
python -m codebleu --refs ref1.py ref2.py ref3.py --hyp pred.py --lang python

# Xem help
python -m codebleu --help
```

## 🧪 Ví dụ chi tiết

### 1️⃣ Perfect Match

```python
references = ["def hello():\n    print('hi')"]
predictions = ["def hello():\n    print('hi')"]

result = calc_codebleu(references, predictions, "python")
# CodeBLEU: 1.0000 (hoàn hảo)
```

### 2️⃣ Variable Rename

```python
references = ["x = 5\ny = x * 2"]
predictions = ["a = 5\nb = a * 2"]

result = calc_codebleu(references, predictions, "python")
# CodeBLEU: ~0.54 (syntax và dataflow cao, n-gram thấp)
```

### 3️⃣ Logic Difference

```python
references = ["result = a + b"]
predictions = ["result = a * b"]

result = calc_codebleu(references, predictions, "python")
# CodeBLEU: ~0.64 (syntax cao, dataflow và n-gram trung bình)
```

### 4️⃣ Completely Different

```python
references = ["def add(x, y): return x + y"]
predictions = ["print('hello world')"]

result = calc_codebleu(references, predictions, "python")
# CodeBLEU: 0.25 (chỉ có theta=1 khi dataflow_match_score=0)
```

## 🔬 Hiểu về các thành phần

### 📊 Score Components

```python
result = calc_codebleu(references, predictions, "python")

# result dictionary chứa:
{
    'codebleu': 0.5439,                      # Tổng điểm
    'ngram_match_score': 0.0879,             # BLEU score
    'weighted_ngram_match_score': 0.0879,    # BLEU với trọng số keywords
    'syntax_match_score': 1.0000,            # AST similarity
    'dataflow_match_score': 1.0000           # Dataflow similarity
}
```

### 🧮 Công thức tính

```
CodeBLEU = α × ngram_score + β × weighted_ngram_score + γ × syntax_score + θ × dataflow_score

Với weights mặc định: α=β=γ=θ=0.25
```

### 📈 Thang điểm

| Score | Ý nghĩa |
|-------|---------|
| **0.8 - 1.0** | 🟢 Excellent - Code rất tương tự |
| **0.6 - 0.8** | 🟡 Good - Có một số khác biệt |
| **0.4 - 0.6** | 🟠 Moderate - Khác biệt đáng kể |
| **0.0 - 0.4** | 🔴 Low - Code rất khác nhau |

## 🐛 Troubleshooting

### ❌ Lỗi thường gặp

#### 1. Incompatible Language Version

```bash
ValueError: Incompatible Language version 15. Must be between 13 and 14
```

**Giải pháp:**
```bash
pip uninstall tree-sitter tree-sitter-python
pip install "tree-sitter>=0.22.0,<0.24.0" "tree-sitter-python>=0.22.0,<0.24.0"
```

#### 2. ModuleNotFoundError

```bash
ModuleNotFoundError: No module named 'codebleu'
```

**Giải pháp:**
```bash
pip install codebleu
# Hoặc nếu từ source: pip install -e .
```

#### 3. Tree-sitter language not found

```bash
FileNotFoundError: [WinError 2] The system cannot find the file specified
```

**Giải pháp:**
```bash
# Cài đặt parser cho ngôn ngữ cần thiết
pip install tree-sitter-python  # cho Python
pip install tree-sitter-java    # cho Java
# etc.
```

### ⚠️ Warning messages

```
WARNING: There is no reference data-flows extracted from the whole corpus, 
and the data-flow match score degenerates to 0.
```

**Ý nghĩa**: Code quá đơn giản, không có dataflow để phân tích. Điểm dataflow sẽ là 0 hoặc 1.

## 🎯 Best Practices

### ✅ Dos

1. **Sử dụng đúng phiên bản tree-sitter** (`>=0.22.0,<0.24.0`)
2. **Chọn ngôn ngữ chính xác** (python, java, javascript, etc.)
3. **Test với code có ý nghĩa** (tránh code quá đơn giản)
4. **Sử dụng weights phù hợp** với use case
5. **So sánh multiple references** khi có thể

### ❌ Don'ts

1. **Không dùng cho code quá ngắn** (1-2 dòng) - kết quả không đáng tin cậy
2. **Không dựa hoàn toàn vào CodeBLEU** - kết hợp với human evaluation
3. **Không bỏ qua warnings** - có thể ảnh hưởng kết quả
4. **Không so sánh cross-language** (Java vs Python) - không có ý nghĩa

## 🔗 Tài liệu tham khảo

### 📚 Papers

- [CodeBLEU: a Method for Automatic Evaluation of Code Synthesis](https://arxiv.org/abs/2009.10297)
- [CodeXGLUE Original Implementation](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans/evaluator/CodeBLEU)

### 🌐 Links

- **PyPI**: [https://pypi.org/project/codebleu/](https://pypi.org/project/codebleu/)
- **GitHub**: [https://github.com/k4black/codebleu](https://github.com/k4black/codebleu)
- **HuggingFace Evaluate**: [https://huggingface.co/spaces/evaluate-metric/code_eval](https://huggingface.co/spaces/evaluate-metric/code_eval)

### 🧪 Example Scripts

Tham khảo các file demo trong thư mục:
- `demo_codebleu.py` - Demo cơ bản
- `simple_demo.py` - Demo đơn giản
- `interactive_demo.py` - Demo tương tác

---

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy:

1. **Kiểm tra phiên bản** dependencies
2. **Đọc error messages** kỹ càng  
3. **Tham khảo GitHub Issues**: [https://github.com/k4black/codebleu/issues](https://github.com/k4black/codebleu/issues)
4. **Tạo minimal reproduction example**

---

*📝 Hướng dẫn này được tạo cho CodeBLEU v0.7.1 - Cập nhật: January 2026*
