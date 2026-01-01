#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBLEU Excel Processor
Script xử lý file Excel với dữ liệu code để tính CodeBLEU

Author: GitHub Copilot Assistant
License: MIT
"""

import pandas as pd
from codebleu import calc_codebleu
import json
import os
from tqdm import tqdm
import argparse

def process_excel_codebleu(
    excel_file, 
    ref_col='Reference Code', 
    hyp_col='Hypothesis Code',
    lang='python',
    weights=(0.25, 0.25, 0.25, 0.25),
    output_file='codebleu_results.csv',
    sheet_name=0
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
        sheet_name: Tên hoặc index của sheet
    
    Returns:
        pandas.DataFrame: Kết quả CodeBLEU
    """
    
    print(f"📖 Đọc file Excel: {excel_file}")
    
    # Kiểm tra file tồn tại
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"File không tồn tại: {excel_file}")
    
    # Đọc file Excel
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
    except Exception as e:
        raise Exception(f"Lỗi đọc file Excel: {e}")
    
    print(f"📋 Thông tin file:")
    print(f"   - Số dòng: {len(df)}")
    print(f"   - Số cột: {len(df.columns)}")
    print(f"   - Các cột: {list(df.columns)}")
    
    # Kiểm tra cột có tồn tại
    if ref_col not in df.columns:
        available_cols = list(df.columns)
        raise ValueError(f"Không tìm thấy cột '{ref_col}'. Các cột có sẵn: {available_cols}")
    if hyp_col not in df.columns:
        available_cols = list(df.columns)
        raise ValueError(f"Không tìm thấy cột '{hyp_col}'. Các cột có sẵn: {available_cols}")
    
    print(f"\n🔧 Cấu hình:")
    print(f"   - Reference column: '{ref_col}'")
    print(f"   - Hypothesis column: '{hyp_col}'")
    print(f"   - Language: {lang}")
    print(f"   - Weights: {weights}")
    
    # Khởi tạo kết quả
    results = []
    errors = []
    
    # Xử lý từng dòng
    print(f"\n⚡ Bắt đầu tính CodeBLEU...")
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
        ref_code = str(row[ref_col]).strip() if pd.notna(row[ref_col]) else ""
        hyp_code = str(row[hyp_col]).strip() if pd.notna(row[hyp_col]) else ""
        
        # Bỏ qua dòng trống
        if not ref_code or not hyp_code or ref_code == 'nan' or hyp_code == 'nan':
            results.append({
                'index': idx,
                'reference': ref_code,
                'hypothesis': hyp_code,
                'codebleu': None,
                'ngram_match': None,
                'weighted_ngram_match': None,
                'syntax_match': None,
                'dataflow_match': None,
                'error': 'Empty or invalid code'
            })
            continue
        
        try:
            # Tính CodeBLEU
            result = calc_codebleu([ref_code], [hyp_code], lang, weights=weights)
            
            results.append({
                'index': idx,
                'reference': ref_code,
                'hypothesis': hyp_code,
                'codebleu': round(result['codebleu'], 4),
                'ngram_match': round(result['ngram_match_score'], 4),
                'weighted_ngram_match': round(result['weighted_ngram_match_score'], 4),
                'syntax_match': round(result['syntax_match_score'], 4),
                'dataflow_match': round(result['dataflow_match_score'], 4),
                'error': None
            })
            
        except Exception as e:
            error_msg = str(e)
            results.append({
                'index': idx,
                'reference': ref_code,
                'hypothesis': hyp_code,
                'codebleu': None,
                'ngram_match': None,
                'weighted_ngram_match': None,
                'syntax_match': None,
                'dataflow_match': None,
                'error': error_msg
            })
            errors.append({'index': idx, 'error': error_msg})
    
    # Tạo DataFrame kết quả
    results_df = pd.DataFrame(results)
    
    # Lưu kết quả
    results_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n💾 Đã lưu kết quả vào: {output_file}")
    
    # Thống kê
    valid_results = results_df[results_df['codebleu'].notna()]
    
    print(f"\n📈 THỐNG KÊ KẾT QUẢ:")
    print("="*50)
    
    if len(valid_results) > 0:
        print(f"✅ Thành công: {len(valid_results)}/{len(df)} ({len(valid_results)/len(df)*100:.1f}%)")
        print(f"❌ Lỗi: {len(errors)} ({len(errors)/len(df)*100:.1f}%)")
        print(f"\n📊 CodeBLEU Statistics:")
        print(f"   🎯 Trung bình: {valid_results['codebleu'].mean():.4f}")
        print(f"   📊 Trung vị:   {valid_results['codebleu'].median():.4f}")
        print(f"   📊 Min:        {valid_results['codebleu'].min():.4f}")
        print(f"   📊 Max:        {valid_results['codebleu'].max():.4f}")
        print(f"   📊 Std:        {valid_results['codebleu'].std():.4f}")
        
        # Phân loại chất lượng
        excellent = len(valid_results[valid_results['codebleu'] >= 0.8])
        good = len(valid_results[(valid_results['codebleu'] >= 0.6) & (valid_results['codebleu'] < 0.8)])
        moderate = len(valid_results[(valid_results['codebleu'] >= 0.4) & (valid_results['codebleu'] < 0.6)])
        low = len(valid_results[valid_results['codebleu'] < 0.4])
        
        print(f"\n📊 Phân loại chất lượng:")
        print(f"   🟢 Excellent (≥0.8): {excellent} ({excellent/len(valid_results)*100:.1f}%)")
        print(f"   🟡 Good (0.6-0.8): {good} ({good/len(valid_results)*100:.1f}%)")
        print(f"   🟠 Moderate (0.4-0.6): {moderate} ({moderate/len(valid_results)*100:.1f}%)")
        print(f"   🔴 Low (<0.4): {low} ({low/len(valid_results)*100:.1f}%)")
    else:
        print("❌ Không có dữ liệu hợp lệ!")
    
    if errors:
        print(f"\n⚠️  Chi tiết lỗi (Top 5):")
        for i, error in enumerate(errors[:5]):
            print(f"   {i+1}. Dòng {error['index']}: {error['error']}")
        if len(errors) > 5:
            print(f"   ... và {len(errors)-5} lỗi khác")
    
    return results_df

def create_sample_excel():
    """Tạo file Excel mẫu để test"""
    sample_data = {
        'Reference Code': [
            'def add(a, b):\n    return a + b',
            'def multiply(x, y):\n    return x * y',
            'for i in range(10):\n    print(i)',
            'x = 5\ny = x * 2\nprint(y)',
            'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)',
            'class Person:\n    def __init__(self, name):\n        self.name = name',
            'import math\nprint(math.pi)',
            'list_nums = [1, 2, 3, 4, 5]\nprint(sum(list_nums))',
            'def is_even(x):\n    return x % 2 == 0',
            'try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print("Error")'
        ],
        'Hypothesis Code': [
            'def sum_two(a, b):\n    return a + b',
            'def mult(a, b):\n    return a * b', 
            'for j in range(10):\n    print(j)',
            'a = 5\nb = a * 2\nprint(b)',
            'def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n-1)',
            'class Human:\n    def __init__(self, name):\n        self.name = name',
            'import math as m\nprint(m.pi)',
            'numbers = [1, 2, 3, 4, 5]\nprint(sum(numbers))',
            'def check_even(num):\n    return num % 2 == 0',
            'try:\n    result = 10 / 0\nexcept:\n    print("Division by zero")'
        ]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_excel('sample_code_data.xlsx', index=False)
    print("📁 Đã tạo file mẫu: sample_code_data.xlsx")

def main():
    parser = argparse.ArgumentParser(description='Tính CodeBLEU cho file Excel')
    parser.add_argument('--file', '-f', type=str, help='Đường dẫn file Excel')
    parser.add_argument('--ref-col', '-r', type=str, default='Reference Code', help='Tên cột reference')
    parser.add_argument('--hyp-col', '-y', type=str, default='Hypothesis Code', help='Tên cột hypothesis')
    parser.add_argument('--lang', '-l', type=str, default='python', help='Ngôn ngữ lập trình')
    parser.add_argument('--output', '-o', type=str, default='codebleu_results.csv', help='File output')
    parser.add_argument('--weights', '-w', type=str, default='0.25,0.25,0.25,0.25', help='Weights (alpha,beta,gamma,theta)')
    parser.add_argument('--create-sample', action='store_true', help='Tạo file Excel mẫu')
    parser.add_argument('--sheet', type=str, default='0', help='Tên hoặc index của sheet')
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_excel()
        return
    
    if not args.file:
        print("❌ Vui lòng cung cấp đường dẫn file Excel với --file")
        print("💡 Hoặc dùng --create-sample để tạo file mẫu")
        return
    
    # Parse weights
    try:
        weights = tuple(map(float, args.weights.split(',')))
        if len(weights) != 4:
            raise ValueError("Weights phải có 4 giá trị")
    except:
        print("❌ Weights không hợp lệ. Ví dụ: 0.25,0.25,0.25,0.25")
        return
    
    # Parse sheet
    try:
        sheet = int(args.sheet) if args.sheet.isdigit() else args.sheet
    except:
        sheet = args.sheet
    
    # Xử lý file
    try:
        results = process_excel_codebleu(
            excel_file=args.file,
            ref_col=args.ref_col,
            hyp_col=args.hyp_col,
            lang=args.lang,
            weights=weights,
            output_file=args.output,
            sheet_name=sheet
        )
        
        print(f"\n🎉 Hoàn thành! Kết quả đã được lưu vào {args.output}")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()