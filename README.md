# CodeBLEU Excel Processor

🚀 **Tool xử lý file Excel để tính CodeBLEU cho code được sinh tự động**

CodeBLEU là một metric đánh giá chất lượng code được sinh ra tự động, kết hợp 4 thành phần: N-gram Match, Weighted N-gram Match, Syntax Match, và Dataflow Match.

## 📖 Giới thiệu

**CodeBLEU** là một metric đánh giá chất lượng code được sinh ra tự động, kết hợp 4 thành phần:

- **🔤 N-gram Match (BLEU)** - Độ tương tự từ ngữ
- **🏷️ Weighted N-gram Match** - Ưu tiên từ khóa quan trọng  
- **🌳 Syntax Match (AST)** - So sánh cấu trúc cú pháp
- **🔗 Dataflow Match** - So sánh luồng dữ liệu/logic

### 📦 Cài đặt

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Hoặc cài từng package
pip install codebleu pandas openpyxl tqdm matplotlib seaborn
pip install "tree-sitter>=0.22.0,<0.24.0" "tree-sitter-python>=0.22.0,<0.24.0"
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
pip install "tree-sitter>=0.22.0,<0.24.0" "tree-sitter-python>=0.22.0,<0.24.0"
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

⭐ **Star this repo if it helps you!** 

🐛 **Report issues or request features via GitHub Issues**
