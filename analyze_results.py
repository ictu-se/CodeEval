#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBLEU Results Analyzer
Script phân tích và visualization kết quả CodeBLEU từ file CSV

Author: GitHub Copilot Assistant
License: MIT
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse

# Set style cho đẹp hơn
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def analyze_codebleu_results(results_file='codebleu_results.csv', save_plots=True):
    """Phân tích và visualize kết quả CodeBLEU"""
    
    print(f"📊 PHÂN TÍCH KẾT QUẢ CODEBLEU")
    print("="*60)
    print(f"📁 File: {results_file}")
    
    # Đọc kết quả
    try:
        df = pd.read_csv(results_file)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {results_file}")
        return
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")
        return
    
    valid_df = df[df['codebleu'].notna()]
    error_df = df[df['codebleu'].isna()]
    
    # Thống kê cơ bản
    print(f"\n📋 THỐNG KÊ TỔNG QUAN:")
    print(f"   📄 Tổng số mẫu: {len(df)}")
    print(f"   ✅ Mẫu hợp lệ: {len(valid_df)} ({len(valid_df)/len(df)*100:.1f}%)")
    print(f"   ❌ Mẫu lỗi: {len(error_df)} ({len(error_df)/len(df)*100:.1f}%)")
    
    if len(valid_df) == 0:
        print("❌ Không có dữ liệu hợp lệ để phân tích!")
        return
    
    # Thống kê điểm số
    print(f"\n📈 THỐNG KÊ ĐIỂM SỐ CODEBLEU:")
    codebleu_stats = valid_df['codebleu'].describe()
    print(f"   🎯 Trung bình:    {codebleu_stats['mean']:.4f}")
    print(f"   📊 Trung vị:      {codebleu_stats['50%']:.4f}")
    print(f"   📊 Min:           {codebleu_stats['min']:.4f}")
    print(f"   📊 Max:           {codebleu_stats['max']:.4f}")
    print(f"   📊 Độ lệch chuẩn: {codebleu_stats['std']:.4f}")
    print(f"   📊 Q1 (25%):      {codebleu_stats['25%']:.4f}")
    print(f"   📊 Q3 (75%):      {codebleu_stats['75%']:.4f}")
    
    # Phân loại theo mức độ
    excellent = len(valid_df[valid_df['codebleu'] >= 0.8])
    good = len(valid_df[(valid_df['codebleu'] >= 0.6) & (valid_df['codebleu'] < 0.8)])
    moderate = len(valid_df[(valid_df['codebleu'] >= 0.4) & (valid_df['codebleu'] < 0.6)])
    low = len(valid_df[valid_df['codebleu'] < 0.4])
    
    print(f"\n📊 PHÂN LOẠI CHẤT LƯỢNG:")
    print(f"   🟢 Excellent (≥0.8): {excellent:4d} ({excellent/len(valid_df)*100:5.1f}%)")
    print(f"   🟡 Good (0.6-0.8):   {good:4d} ({good/len(valid_df)*100:5.1f}%)")
    print(f"   🟠 Moderate (0.4-0.6): {moderate:4d} ({moderate/len(valid_df)*100:5.1f}%)")
    print(f"   🔴 Low (<0.4):       {low:4d} ({low/len(valid_df)*100:5.1f}%)")
    
    # Thống kê từng component
    score_cols = ['ngram_match', 'weighted_ngram_match', 'syntax_match', 'dataflow_match']
    score_cols = [col for col in score_cols if col in valid_df.columns]
    
    if score_cols:
        print(f"\n📊 THỐNG KÊ CÁC THÀNH PHẦN:")
        for col in score_cols:
            mean_score = valid_df[col].mean()
            std_score = valid_df[col].std()
            print(f"   {col:20}: {mean_score:.4f} ± {std_score:.4f}")
    
    # Top 10 và bottom 10
    print(f"\n🏆 TOP 10 ĐIỂM CAO NHẤT:")
    top10 = valid_df.nlargest(10, 'codebleu')[['index', 'codebleu']]
    for i, (_, row) in enumerate(top10.iterrows(), 1):
        print(f"   {i:2d}. Dòng {int(row['index']):4d}: {row['codebleu']:.4f}")
    
    print(f"\n⚠️  TOP 10 ĐIỂM THẤP NHẤT:")
    bottom10 = valid_df.nsmallest(10, 'codebleu')[['index', 'codebleu']]
    for i, (_, row) in enumerate(bottom10.iterrows(), 1):
        print(f"   {i:2d}. Dòng {int(row['index']):4d}: {row['codebleu']:.4f}")
    
    # Lỗi phổ biến
    if len(error_df) > 0:
        print(f"\n❌ PHÂN TÍCH LỖI:")
        error_counts = error_df['error'].value_counts()
        print(f"   Các loại lỗi phổ biến:")
        for error_type, count in error_counts.head(5).items():
            print(f"   - {error_type}: {count} lần")
    
    # Visualization nếu có yêu cầu
    if save_plots:
        create_visualizations(valid_df, excellent, good, moderate, low)
    
    return valid_df

def create_visualizations(valid_df, excellent, good, moderate, low):
    """Tạo các biểu đồ phân tích"""
    
    print(f"\n📈 Tạo biểu đồ phân tích...")
    
    # Setup figure
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Histogram của CodeBLEU scores
    plt.subplot(3, 3, 1)
    plt.hist(valid_df['codebleu'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(valid_df['codebleu'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {valid_df["codebleu"].mean():.3f}')
    plt.axvline(valid_df['codebleu'].median(), color='orange', linestyle='--', linewidth=2, label=f'Median: {valid_df["codebleu"].median():.3f}')
    plt.title('Distribution of CodeBLEU Scores', fontsize=14, fontweight='bold')
    plt.xlabel('CodeBLEU Score')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Box plot của tất cả các scores
    plt.subplot(3, 3, 2)
    score_cols = ['codebleu', 'ngram_match', 'weighted_ngram_match', 'syntax_match', 'dataflow_match']
    score_cols = [col for col in score_cols if col in valid_df.columns]
    
    box_data = [valid_df[col].dropna() for col in score_cols]
    box = plt.boxplot(box_data, labels=[col.replace('_', '\n') for col in score_cols], patch_artist=True)
    
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
    for patch, color in zip(box['boxes'], colors[:len(score_cols)]):
        patch.set_facecolor(color)
    
    plt.title('Score Components Distribution', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.ylabel('Score Value')
    plt.grid(True, alpha=0.3)
    
    # 3. Quality distribution pie chart
    plt.subplot(3, 3, 3)
    categories = ['Excellent\n(≥0.8)', 'Good\n(0.6-0.8)', 'Moderate\n(0.4-0.6)', 'Low\n(<0.4)']
    sizes = [excellent, good, moderate, low]
    colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    
    # Chỉ hiển thị categories có dữ liệu
    non_zero_data = [(cat, size, color) for cat, size, color in zip(categories, sizes, colors) if size > 0]
    if non_zero_data:
        cats, szs, cols = zip(*non_zero_data)
        wedges, texts, autotexts = plt.pie(szs, labels=cats, colors=cols, autopct='%1.1f%%', startangle=90)
        plt.title('Quality Distribution', fontsize=14, fontweight='bold')
    
    # 4. Scatter plot: ngram vs syntax
    if 'ngram_match' in valid_df.columns and 'syntax_match' in valid_df.columns:
        plt.subplot(3, 3, 4)
        plt.scatter(valid_df['ngram_match'], valid_df['syntax_match'], alpha=0.6, s=50)
        plt.xlabel('N-gram Match Score')
        plt.ylabel('Syntax Match Score')
        plt.title('N-gram vs Syntax Match', fontsize=14, fontweight='bold')
        
        # Add trend line
        z = np.polyfit(valid_df['ngram_match'].dropna(), valid_df['syntax_match'].dropna(), 1)
        p = np.poly1d(z)
        plt.plot(valid_df['ngram_match'], p(valid_df['ngram_match']), "r--", alpha=0.8)
        plt.grid(True, alpha=0.3)
    
    # 5. Scatter plot: syntax vs dataflow
    if 'syntax_match' in valid_df.columns and 'dataflow_match' in valid_df.columns:
        plt.subplot(3, 3, 5)
        plt.scatter(valid_df['syntax_match'], valid_df['dataflow_match'], alpha=0.6, s=50, color='orange')
        plt.xlabel('Syntax Match Score')
        plt.ylabel('Dataflow Match Score')
        plt.title('Syntax vs Dataflow Match', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
    
    # 6. Correlation heatmap
    if len(score_cols) > 1:
        plt.subplot(3, 3, 6)
        corr_matrix = valid_df[score_cols].corr()
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, mask=mask,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5}, fmt='.3f')
        plt.title('Score Correlation Matrix', fontsize=14, fontweight='bold')
    
    # 7. Score progression (if index represents some order)
    plt.subplot(3, 3, 7)
    plt.plot(valid_df['index'], valid_df['codebleu'], alpha=0.7, linewidth=1, marker='o', markersize=3)
    plt.xlabel('Sample Index')
    plt.ylabel('CodeBLEU Score')
    plt.title('CodeBLEU Score by Sample Order', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # 8. Score components comparison
    if len(score_cols) > 2:
        plt.subplot(3, 3, 8)
        component_means = [valid_df[col].mean() for col in score_cols]
        x_pos = range(len(score_cols))
        bars = plt.bar(x_pos, component_means, alpha=0.7, 
                      color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6'][:len(score_cols)])
        plt.xlabel('Score Components')
        plt.ylabel('Average Score')
        plt.title('Average Scores by Component', fontsize=14, fontweight='bold')
        plt.xticks(x_pos, [col.replace('_', '\n') for col in score_cols], rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, component_means):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
    
    # 9. Score distribution violin plot
    plt.subplot(3, 3, 9)
    if len(score_cols) > 1:
        score_data = []
        score_labels = []
        for col in score_cols:
            score_data.extend(valid_df[col].dropna().tolist())
            score_labels.extend([col.replace('_', ' ').title()] * len(valid_df[col].dropna()))
        
        plot_df = pd.DataFrame({'Score': score_data, 'Component': score_labels})
        sns.violinplot(data=plot_df, x='Component', y='Score', palette='Set2')
        plt.xticks(rotation=45)
        plt.title('Score Distribution by Component', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout(pad=3.0)
    
    # Lưu biểu đồ
    filename = 'codebleu_analysis.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"💾 Biểu đồ đã được lưu: {filename}")
    
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Phân tích kết quả CodeBLEU')
    parser.add_argument('--file', '-f', type=str, default='codebleu_results.csv', help='File CSV chứa kết quả')
    parser.add_argument('--no-plots', action='store_true', help='Không tạo biểu đồ')
    
    args = parser.parse_args()
    
    try:
        analyze_codebleu_results(args.file, save_plots=not args.no_plots)
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()