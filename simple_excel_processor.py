#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Excel to CodeBLEU Processor
Script đơn giản để tính CodeBLEU từ file Excel với interface tương tác

Author: GitHub Copilot Assistant
License: MIT
"""

import pandas as pd
from codebleu import calc_codebleu
from tqdm import tqdm
import os

def simple_excel_to_codebleu():
    """Script đơn giản để tính CodeBLEU từ file Excel"""
    
    print("🎯 CODEBLEU EXCEL PROCESSOR")
    print("="*50)
    
    # Input file Excel
    while True:
        excel_file = input("📁 Nhập đường dẫn file Excel: ").strip()
        if os.path.exists(excel_file):
            break
        print("❌ File không tồn tại! Vui lòng thử lại.")
    
    # Đọc file và hiển thị thông tin
    try:
        df = pd.read_excel(excel_file)
        print(f"📊 File có {len(df)} dòng và {len(df.columns)} cột")
        print(f"📋 Các cột: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")
        return
    
    # Chọn cột Reference
    print(f"\n🔍 Chọn cột Reference Code:")
    for i, col in enumerate(df.columns):
        print(f"   {i}: {col}")
    
    while True:
        try:
            ref_idx = int(input("Nhập số thứ tự cột Reference: "))
            ref_col = df.columns[ref_idx]
            break
        except (ValueError, IndexError):
            print("❌ Số không hợp lệ! Vui lòng thử lại.")
    
    # Chọn cột Hypothesis  
    print(f"\n🤖 Chọn cột Hypothesis Code:")
    for i, col in enumerate(df.columns):
        print(f"   {i}: {col}")
    
    while True:
        try:
            hyp_idx = int(input("Nhập số thứ tự cột Hypothesis: "))
            hyp_col = df.columns[hyp_idx]
            break
        except (ValueError, IndexError):
            print("❌ Số không hợp lệ! Vui lòng thử lại.")
    
    # Chọn ngôn ngữ
    languages = ['python', 'java', 'javascript', 'c_sharp', 'c', 'cpp', 'go', 'php', 'ruby', 'rust']
    print(f"\n🌐 Chọn ngôn ngữ:")
    for i, lang in enumerate(languages):
        print(f"   {i}: {lang}")
    
    while True:
        try:
            lang_idx = int(input("Nhập số thứ tự ngôn ngữ (mặc định 0=python): ") or "0")
            language = languages[lang_idx]
            break
        except (ValueError, IndexError):
            print("❌ Số không hợp lệ! Sử dụng python.")
            language = "python"
    
    # Xác nhận
    print(f"\n✅ Cấu hình:")
    print(f"   📁 File: {excel_file}")
    print(f"   📚 Reference: {ref_col}")
    print(f"   🤖 Hypothesis: {hyp_col}")
    print(f"   🌐 Language: {language}")
    
    confirm = input("\n🚀 Tiến hành tính CodeBLEU? (y/n): ").lower().strip()
    if confirm != 'y':
        print("❌ Đã hủy.")
        return
    
    # Tính CodeBLEU
    print(f"\n⚡ Đang tính CodeBLEU...")
    
    results = []
    errors = 0
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
        ref_code = str(row[ref_col]).strip() if pd.notna(row[ref_col]) else ""
        hyp_code = str(row[hyp_col]).strip() if pd.notna(row[hyp_col]) else ""
        
        if not ref_code or not hyp_code:
            results.append({
                'Index': idx + 1,  # 1-based indexing for users
                'Reference': ref_code[:50] + "..." if len(ref_code) > 50 else ref_code,
                'Hypothesis': hyp_code[:50] + "..." if len(hyp_code) > 50 else hyp_code,
                'CodeBLEU': None,
                'Status': 'Empty'
            })
            errors += 1
            continue
        
        try:
            result = calc_codebleu([ref_code], [hyp_code], language)
            results.append({
                'Index': idx + 1,
                'Reference': ref_code[:50] + "..." if len(ref_code) > 50 else ref_code,
                'Hypothesis': hyp_code[:50] + "..." if len(hyp_code) > 50 else hyp_code,
                'CodeBLEU': round(result['codebleu'], 4),
                'N-gram': round(result['ngram_match_score'], 4),
                'Weighted': round(result['weighted_ngram_match_score'], 4),
                'Syntax': round(result['syntax_match_score'], 4),
                'Dataflow': round(result['dataflow_match_score'], 4),
                'Status': 'Success'
            })
        except Exception as e:
            results.append({
                'Index': idx + 1,
                'Reference': ref_code[:50] + "..." if len(ref_code) > 50 else ref_code,
                'Hypothesis': hyp_code[:50] + "..." if len(hyp_code) > 50 else hyp_code,
                'CodeBLEU': None,
                'Status': f'Error: {str(e)[:30]}...'
            })
            errors += 1
    
    # Lưu kết quả
    results_df = pd.DataFrame(results)
    output_file = 'codebleu_results.csv'
    results_df.to_csv(output_file, index=False, encoding='utf-8')
    
    # Thống kê
    valid_results = results_df[results_df['CodeBLEU'].notna()]
    
    print(f"\n📊 KẾT QUẢ:")
    print("="*50)
    print(f"✅ Thành công: {len(valid_results)}/{len(df)} ({len(valid_results)/len(df)*100:.1f}%)")
    print(f"❌ Lỗi: {errors}")
    
    if len(valid_results) > 0:
        print(f"🎯 CodeBLEU trung bình: {valid_results['CodeBLEU'].mean():.4f}")
        print(f"📊 CodeBLEU cao nhất: {valid_results['CodeBLEU'].max():.4f}")
        print(f"📊 CodeBLEU thấp nhất: {valid_results['CodeBLEU'].min():.4f}")
        
        # Top 5 best
        print(f"\n🏆 TOP 5 ĐIỂM CAO:")
        top5 = valid_results.nlargest(5, 'CodeBLEU')[['Index', 'CodeBLEU']]
        for _, row in top5.iterrows():
            print(f"   Dòng {row['Index']}: {row['CodeBLEU']}")
        
        # Top 5 worst
        print(f"\n⚠️  TOP 5 ĐIỂM THẤP:")
        bottom5 = valid_results.nsmallest(5, 'CodeBLEU')[['Index', 'CodeBLEU']]
        for _, row in bottom5.iterrows():
            print(f"   Dòng {row['Index']}: {row['CodeBLEU']}")
    
    print(f"\n💾 Kết quả đã lưu: {output_file}")
    print(f"🎉 Hoàn thành!")

if __name__ == "__main__":
    try:
        simple_excel_to_codebleu()
    except KeyboardInterrupt:
        print("\n❌ Đã hủy bởi người dùng.")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()