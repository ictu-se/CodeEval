# CodeBLEU Excel Processor
**CodeBLEU** là một metric đánh giá chất lượng code được sinh ra tự động, kết hợp 4 thành phần:

- **🔤 N-gram Match (BLEU)** - Độ tương tự từ ngữ
- **🏷️ Weighted N-gram Match** - Ưu tiên từ khóa quan trọng  
- **🌳 Syntax Match (AST)** - So sánh cấu trúc cú pháp
- **🔗 Dataflow Match** - So sánh luồng dữ liệu/logic
```python
def calc_codebleu(references, predictions, lang, weights=(0.25,0.25,0.25,0.25)):
    # 1. Tính BLEU score (n-gram matching)
    ngram_match_score = bleu.corpus_bleu(tokenized_refs, tokenized_hyps)
    
    # 2. Tính Weighted BLEU (ưu tiên keywords)  
    weighted_ngram_match_score = weighted_ngram_match.corpus_bleu(...)
    
    # 3. Tính Syntax Match (AST similarity)
    syntax_match_score = syntax_match.corpus_syntax_match(...)
    
    # 4. Tính Dataflow Match (logic similarity)
    dataflow_match_score = dataflow_match.corpus_dataflow_match(...)
    
    # 5. Kết hợp với trọng số
    codebleu = α*ngram + β*weighted + γ*syntax + θ*dataflow
```
Có nghĩa là điểm CodeBleu được tính bằng tổ hợp có trọng số từ 4 thành phần



### 📦 Cài đặt

```bash
# Cài đặt dependencies
pip install -r requirements.txt
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


### 🚀 Sử dụng nhanh

1. **Tạo file Excel mẫu:**
```bash
python excel_processor.py --create-sample
```

2. **Xử lý file Excel của bạn:**
```bash
python excel_processor.py --file your_data.xlsx
```

3. **Phân tích kết quả:**
```bash
python analyze_results.py --file codebleu_results.csv
```

## 📊 Cấu trúc file Excel

File Excel cần có 2 cột:
- **Cột 1**: Reference Code (code mẫu/đúng)
- **Cột 2**: Hypothesis Code (code do AI sinh ra)

| Reference Code                    | Hypothesis Code                   |
|-----------------------------------|-----------------------------------|
| def add(a, b): return a + b       | def sum(x, y): return x + y      |
| print("Hello World")              | print('Hello World')             |
| for i in range(10): print(i)     | for j in range(10): print(j)     |

## 🛠️ Tools

### 1. `excel_processor.py` - Tool chính
Xử lý file Excel và tính CodeBLEU cho toàn bộ dữ liệu.

```bash
# Cú pháp đầy đủ
python excel_processor.py \
    --file data.xlsx \
    --ref-col "Reference Code" \
    --hyp-col "AI Generated Code" \
    --lang python \
    --weights "0.25,0.25,0.25,0.25" \
    --output results.csv
```

**Options:**
- `--file`: Đường dẫn file Excel
- `--ref-col`: Tên cột reference code
- `--hyp-col`: Tên cột hypothesis code  
- `--lang`: Ngôn ngữ (python, java, javascript, etc.)
- `--weights`: Trọng số (alpha,beta,gamma,theta)
- `--output`: File kết quả CSV
- `--create-sample`: Tạo file Excel mẫu

### 2. `analyze_results.py` - Phân tích kết quả
Phân tích và tạo biểu đồ từ kết quả CodeBLEU.

```bash
python analyze_results.py --file results.csv
```

### 3. `simple_excel_processor.py` - Tool đơn giản
Interface đơn giản với prompts tương tác.

```bash
python simple_excel_processor.py
```

## 🎯 Ví dụ kết quả

```
📊 THỐNG KÊ KẾT QUẢ:
✅ Thành công: 100/100 dòng (100.0%)
🎯 CodeBLEU trung bình: 0.7245
📊 Phân loại chất lượng:
   🟢 Excellent (≥0.8): 45 (45.0%)
   🟡 Good (0.6-0.8): 30 (30.0%)
   🟠 Moderate (0.4-0.6): 20 (20.0%)
   🔴 Low (<0.4): 5 (5.0%)
```

## 🌐 Ngôn ngữ hỗ trợ

- Python, Java, JavaScript, C#, C, C++
- Go, PHP, Ruby, Rust

## 📈 Output

### CSV Results
File CSV chứa:
- Index, Reference, Hypothesis
- CodeBLEU score tổng
- Điểm từng thành phần (N-gram, Weighted, Syntax, Dataflow)
- Thông tin lỗi (nếu có)

### Visualization
- Distribution charts
- Score correlations  
- Quality breakdowns
- Component analysis

## 🐛 Troubleshooting

### Lỗi phổ biến

1. **Tree-sitter version conflict:**
```bash
pip uninstall tree-sitter tree-sitter-python
pip install tree-sitter==0.22.3 tree-sitter-python==0.21.0
```

2. **Module not found:**
```bash
pip install codebleu
```

3. **Empty results:**
- Kiểm tra format code trong Excel
- Đảm bảo không có dòng trống
- Chọn đúng ngôn ngữ

## 📚 Paper & References

- [CodeBLEU: a Method for Automatic Evaluation of Code Synthesis](https://arxiv.org/abs/2009.10297)
- [Original CodeBLEU Implementation](https://github.com/k4black/codebleu)
- [CodeXGLUE Project](https://github.com/microsoft/CodeXGLUE)

## 📝 License

MIT License - see LICENSE file for details.

---






