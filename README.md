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

## 📊 Xử lý dữ liệu từ file Excel

### 📋 Cấu trúc file Excel

File Excel cần có 2 cột:
- **Cột A**: Reference code (code mẫu/đúng)
- **Cột B**: Hypothesis/Prediction code (code do AI sinh ra)

```
| Reference Code                    | Hypothesis Code                   |
|-----------------------------------|-----------------------------------|
| def add(a, b): return a + b       | def sum(x, y): return x + y      |
| print("Hello World")              | print('Hello World')             |
| for i in range(10): print(i)     | for j in range(10): print(j)     |
```

### 🐍 Script xử lý Excel

```python
import pandas as pd
from codebleu import calc_codebleu
import json
from tqdm import tqdm

def process_excel_codebleu(
    excel_file, 
    ref_col='Reference Code', 
    hyp_col='Hypothesis Code',
    lang='python',
    weights=(0.25, 0.25, 0.25, 0.25),
    output_file='codebleu_results.csv'
):
    """
    Tính CodeBLEU cho toàn bộ dữ liệu trong file Excel
    
    Args:
        excel_file: Đường dẫn file Excel
        ref_col: Tên cột chứa reference code
        hyp_col: Tên cột chứa hypothesis code  
        lang: Ngôn ngữ lập trình
        weights: Trọng số (alpha, beta, gamma, theta)
        output_file: File output kết quả
    """
    
    print(f"📖 Đọc file Excel: {excel_file}")
    
    # Đọc file Excel
    df = pd.read_excel(excel_file)
    
    # Kiểm tra cột có tồn tại
    if ref_col not in df.columns:
        raise ValueError(f"Không tìm thấy cột '{ref_col}' trong file Excel")
    if hyp_col not in df.columns:
        raise ValueError(f"Không tìm thấy cột '{hyp_col}' trong file Excel")
    
    print(f"📊 Tổng số dòng: {len(df)}")
    print(f"🌐 Ngôn ngữ: {lang}")
    print(f"⚖️  Weights: {weights}")
    
    # Khởi tạo kết quả
    results = []
    errors = []
    
    # Xử lý từng dòng
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Tính CodeBLEU"):
        ref_code = str(row[ref_col]).strip()
        hyp_code = str(row[hyp_col]).strip()
        
        # Bỏ qua dòng trống
        if ref_code == 'nan' or hyp_code == 'nan' or not ref_code or not hyp_code:
            results.append({
                'index': idx,
                'reference': ref_code,
                'hypothesis': hyp_code,
                'codebleu': None,
                'ngram_match': None,
                'weighted_ngram_match': None,
                'syntax_match': None,
                'dataflow_match': None,
                'error': 'Empty code'
            })
            continue
        
        try:
            # Tính CodeBLEU
            result = calc_codebleu([ref_code], [hyp_code], lang, weights=weights)
            
            results.append({
                'index': idx,
                'reference': ref_code,
                'hypothesis': hyp_code,
                'codebleu': result['codebleu'],
                'ngram_match': result['ngram_match_score'],
                'weighted_ngram_match': result['weighted_ngram_match_score'],
                'syntax_match': result['syntax_match_score'],
                'dataflow_match': result['dataflow_match_score'],
                'error': None
            })
            
        except Exception as e:
            results.append({
                'index': idx,
                'reference': ref_code,
                'hypothesis': hyp_code,
                'codebleu': None,
                'ngram_match': None,
                'weighted_ngram_match': None,
                'syntax_match': None,
                'dataflow_match': None,
                'error': str(e)
            })
            errors.append({'index': idx, 'error': str(e)})
    
    # Tạo DataFrame kết quả
    results_df = pd.DataFrame(results)
    
    # Lưu kết quả
    results_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"💾 Đã lưu kết quả vào: {output_file}")
    
    # Thống kê
    valid_results = results_df[results_df['codebleu'].notna()]
    
    if len(valid_results) > 0:
        print(f"\n📈 Thống kê:")
        print(f"   ✅ Thành công: {len(valid_results)}/{len(df)} dòng")
        print(f"   ❌ Lỗi: {len(errors)} dòng")
        print(f"   🎯 CodeBLEU trung bình: {valid_results['codebleu'].mean():.4f}")
        print(f"   📊 CodeBLEU min: {valid_results['codebleu'].min():.4f}")
        print(f"   📊 CodeBLEU max: {valid_results['codebleu'].max():.4f}")
        print(f"   📊 CodeBLEU std: {valid_results['codebleu'].std():.4f}")
    
    if errors:
        print(f"\n⚠️  Có {len(errors)} lỗi xảy ra:")
        for error in errors[:5]:  # Hiển thị 5 lỗi đầu
            print(f"   - Dòng {error['index']}: {error['error']}")
        if len(errors) > 5:
            print(f"   ... và {len(errors)-5} lỗi khác")
    
    return results_df

# Ví dụ sử dụng
if __name__ == "__main__":
    # Xử lý file Excel
    results = process_excel_codebleu(
        excel_file='code_data.xlsx',  # Đường dẫn file Excel
        ref_col='Reference Code',     # Tên cột reference
        hyp_col='AI Generated Code',  # Tên cột hypothesis
        lang='python',                # Ngôn ngữ
        weights=(0.25, 0.25, 0.25, 0.25),  # Weights
        output_file='results.csv'    # File output
    )
```

### 📊 Script phân tích kết quả

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_codebleu_results(results_file='results.csv'):
    """Phân tích và visualize kết quả CodeBLEU"""
    
    # Đọc kết quả
    df = pd.read_csv(results_file)
    valid_df = df[df['codebleu'].notna()]
    
    print(f"📊 PHÂN TÍCH KẾT QUẢ CODEBLEU")
    print("="*50)
    
    # Thống kê cơ bản
    print(f"📋 Tổng số mẫu: {len(df)}")
    print(f"✅ Mẫu hợp lệ: {len(valid_df)}")
    print(f"❌ Mẫu lỗi: {len(df) - len(valid_df)}")
    
    if len(valid_df) == 0:
        print("❌ Không có dữ liệu hợp lệ để phân tích!")
        return
    
    # Thống kê điểm số
    print(f"\n📈 THỐNG KÊ ĐIỂM SỐ:")
    print(f"   🎯 CodeBLEU:")
    print(f"      - Trung bình: {valid_df['codebleu'].mean():.4f}")
    print(f"      - Trung vị: {valid_df['codebleu'].median():.4f}")
    print(f"      - Min: {valid_df['codebleu'].min():.4f}")
    print(f"      - Max: {valid_df['codebleu'].max():.4f}")
    print(f"      - Độ lệch chuẩn: {valid_df['codebleu'].std():.4f}")
    
    # Phân loại theo mức độ
    excellent = len(valid_df[valid_df['codebleu'] >= 0.8])
    good = len(valid_df[(valid_df['codebleu'] >= 0.6) & (valid_df['codebleu'] < 0.8)])
    moderate = len(valid_df[(valid_df['codebleu'] >= 0.4) & (valid_df['codebleu'] < 0.6)])
    low = len(valid_df[valid_df['codebleu'] < 0.4])
    
    print(f"\n📊 PHÂN LOẠI CHẤT LƯỢNG:")
    print(f"   🟢 Excellent (≥0.8): {excellent} ({excellent/len(valid_df)*100:.1f}%)")
    print(f"   🟡 Good (0.6-0.8): {good} ({good/len(valid_df)*100:.1f}%)")
    print(f"   🟠 Moderate (0.4-0.6): {moderate} ({moderate/len(valid_df)*100:.1f}%)")
    print(f"   🔴 Low (<0.4): {low} ({low/len(valid_df)*100:.1f}%)")
    
    # Top 10 và bottom 10
    print(f"\n🏆 TOP 10 ĐIỂM CAO NHẤT:")
    top10 = valid_df.nlargest(10, 'codebleu')[['index', 'codebleu']]
    for _, row in top10.iterrows():
        print(f"   Dòng {int(row['index'])}: {row['codebleu']:.4f}")
    
    print(f"\n⚠️  TOP 10 ĐIỂM THẤP NHẤT:")
    bottom10 = valid_df.nsmallest(10, 'codebleu')[['index', 'codebleu']]
    for _, row in bottom10.iterrows():
        print(f"   Dòng {int(row['index'])}: {row['codebleu']:.4f}")
    
    # Visualizations
    plt.figure(figsize=(15, 10))
    
    # 1. Histogram của CodeBLEU scores
    plt.subplot(2, 3, 1)
    plt.hist(valid_df['codebleu'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('Distribution of CodeBLEU Scores')
    plt.xlabel('CodeBLEU Score')
    plt.ylabel('Frequency')
    plt.axvline(valid_df['codebleu'].mean(), color='red', linestyle='--', label='Mean')
    plt.legend()
    
    # 2. Box plot của tất cả các scores
    plt.subplot(2, 3, 2)
    scores_cols = ['codebleu', 'ngram_match', 'weighted_ngram_match', 'syntax_match', 'dataflow_match']
    valid_df[scores_cols].boxplot()
    plt.title('Score Components Comparison')
    plt.xticks(rotation=45)
    
    # 3. Scatter plot: ngram vs syntax
    plt.subplot(2, 3, 3)
    plt.scatter(valid_df['ngram_match'], valid_df['syntax_match'], alpha=0.6)
    plt.xlabel('N-gram Match')
    plt.ylabel('Syntax Match')
    plt.title('N-gram vs Syntax Match')
    
    # 4. Scatter plot: syntax vs dataflow
    plt.subplot(2, 3, 4)
    plt.scatter(valid_df['syntax_match'], valid_df['dataflow_match'], alpha=0.6)
    plt.xlabel('Syntax Match')
    plt.ylabel('Dataflow Match')
    plt.title('Syntax vs Dataflow Match')
    
    # 5. Correlation heatmap
    plt.subplot(2, 3, 5)
    corr_matrix = valid_df[scores_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Score Correlation Matrix')
    
    # 6. Score distribution pie chart
    plt.subplot(2, 3, 6)
    categories = ['Excellent', 'Good', 'Moderate', 'Low']
    sizes = [excellent, good, moderate, low]
    colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    plt.pie(sizes, labels=categories, colors=colors, autopct='%1.1f%%')
    plt.title('Quality Distribution')
    
    plt.tight_layout()
    plt.savefig('codebleu_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n💾 Biểu đồ đã được lưu: codebleu_analysis.png")

# Sử dụng
if __name__ == "__main__":
    analyze_codebleu_results('results.csv')
```

### ⚡ Script nhanh cho Excel đơn giản

```python
import pandas as pd
from codebleu import calc_codebleu

# Đọc file Excel
df = pd.read_excel('your_data.xlsx')

# Tính CodeBLEU cho từng dòng
results = []
for idx, row in df.iterrows():
    ref_code = row['Reference Code']  # Thay tên cột nếu cần
    hyp_code = row['Hypothesis Code'] # Thay tên cột nếu cần
    
    try:
        result = calc_codebleu([ref_code], [hyp_code], "python")
        results.append({
            'Index': idx,
            'CodeBLEU': result['codebleu'],
            'N-gram': result['ngram_match_score'],
            'Weighted': result['weighted_ngram_match_score'],
            'Syntax': result['syntax_match_score'],
            'Dataflow': result['dataflow_match_score']
        })
    except Exception as e:
        results.append({
            'Index': idx,
            'CodeBLEU': None,
            'Error': str(e)
        })

# Lưu kết quả
results_df = pd.DataFrame(results)
results_df.to_csv('codebleu_results.csv', index=False)

print(f"✅ Hoàn thành! Kết quả lưu trong codebleu_results.csv")
print(f"📊 CodeBLEU trung bình: {results_df['CodeBLEU'].mean():.4f}")
```

### 📋 Cài đặt thêm dependencies

```bash
# Cài đặt pandas để xử lý Excel
pip install pandas openpyxl xlrd

# Cài đặt matplotlib và seaborn cho visualization
pip install matplotlib seaborn

# Cài đặt tqdm cho progress bar
pip install tqdm
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
