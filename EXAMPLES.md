# Examples

## 📊 Demo với file Excel mẫu

### 1. Tạo file mẫu và test:

```bash
# Tạo file Excel mẫu
python excel_processor.py --create-sample

# Xử lý file mẫu  
python excel_processor.py --file sample_code_data.xlsx

# Phân tích kết quả
python analyze_results.py --file codebleu_results.csv
```

### 2. Kết quả mẫu:

```
📊 THỐNG KÊ KẾT QUẢ:
✅ Thành công: 10/10 dòng (100.0%)
🎯 CodeBLEU trung bình: 0.6935
📊 Phân loại chất lượng:
   🟢 Excellent (≥0.8): 4 (40.0%)
   🟡 Good (0.6-0.8): 2 (20.0%)
   🟠 Moderate (0.4-0.6): 4 (40.0%)
   🔴 Low (<0.4): 0 (0.0%)
```

## 📝 Ví dụ file Excel

| Reference Code | Hypothesis Code |
|----------------|-----------------|
| `def add(a, b):\n    return a + b` | `def sum_two(a, b):\n    return a + b` |
| `for i in range(10):\n    print(i)` | `for j in range(10):\n    print(j)` |
| `x = 5\ny = x * 2` | `a = 5\nb = a * 2` |

## 🛠️ Advanced Usage

### Custom weights:

```bash
python excel_processor.py \
    --file data.xlsx \
    --weights "0.3,0.3,0.2,0.2"  # Ưu tiên n-gram và weighted
```

### Multiple languages:

```bash
# Java
python excel_processor.py --file java_data.xlsx --lang java

# JavaScript  
python excel_processor.py --file js_data.xlsx --lang javascript

# C++
python excel_processor.py --file cpp_data.xlsx --lang cpp
```

### Different column names:

```bash
python excel_processor.py \
    --file data.xlsx \
    --ref-col "Ground Truth" \
    --hyp-col "Generated Code"
```

## 📈 Output Format

### CSV Results Structure:
```
index,reference,hypothesis,codebleu,ngram_match,weighted_ngram_match,syntax_match,dataflow_match,error
0,"def add(a,b): return a+b","def sum(x,y): return x+y",0.8252,0.5774,0.5774,1.0,1.0,
1,"print('hello')","print(""hello"")",0.5233,0.0464,0.0464,1.0,1.0,
```

### Analysis Charts:
- Distribution histograms
- Component correlation matrix  
- Quality breakdown pie chart
- Score progression plots

## 🎯 Use Cases

### 1. AI Code Generation Evaluation:
```python
# Compare GPT-4 vs CodeT5 vs GitHub Copilot
references = ["original_code_dataset.xlsx"] 
predictions = ["gpt4_outputs.xlsx", "codet5_outputs.xlsx", "copilot_outputs.xlsx"]
```

### 2. Code Translation Assessment:
```python  
# Java to Python translation quality
java_to_python = pd.read_excel("java_python_translation.xlsx")
# Columns: Java_Code, Python_Generated
```

### 3. Code Refactoring Quality:
```python
# Before vs After refactoring
refactoring = pd.read_excel("refactoring_dataset.xlsx") 
# Columns: Original_Code, Refactored_Code
```