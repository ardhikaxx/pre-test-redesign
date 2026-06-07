import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define the PIECES Categories and their question mappings (1-based index in the set of 20)
CATEGORIES = {
    'PERFORMANCE': [1, 2, 3, 4, 5, 6, 7],
    'INFORMATION': [8, 9, 10, 11],
    'ECONOMY': [12, 13],
    'CONTROL': [14, 15],
    'EFFICIENCY': [16, 17],
    'SERVICE': [18, 19, 20]
}

def load_data(kuesioner_type='kuesioner_1'):
    # File paths
    d3_file = os.path.join('data', '(D3)_Analisis_Kepuasan_Pengguna_Terhadap_Website_SIM_Online_Polije.ac.id_Menggunakan_Metode_PIECES_Framework_(Jawaban)_-_Form_Responses_1_(1).csv')
    d4_file = os.path.join('data', '(D4)_Analisis_Kepuasan_Pengguna_Terhadap_Website_SIM_Online_Polije.ac.id_Menggunakan_Metode_PIECES_Framework_(Jawaban)_-_Form_Responses_1_(1).csv')

    # Load data
    d3_df = pd.read_csv(d3_file)
    d4_df = pd.read_csv(d4_file)

    if kuesioner_type == 'kuesioner_1':
        # Process D3 Kuesioner 1 (Semester 1-4, columns 25-44)
        d3_data = d3_df[d3_df['Semester'] == '1-4'].iloc[:, 25:45].copy()
        # Process D4 Kuesioner 1 (Semester 1-6, columns 29-48)
        d4_data = d4_df[d4_df['Semester'] == '1-6'].iloc[:, 29:49].copy()
    else:
        # Process D3 Kuesioner 2 (Semester 5-6, columns 5-24)
        d3_data = d3_df[d3_df['Semester'] == '5-6'].iloc[:, 5:25].copy()
        # Process D4 Kuesioner 2 (Semester 7-8, columns 9-28)
        d4_data = d4_df[d4_df['Semester'] == '7-8'].iloc[:, 9:29].copy()

    d3_data.columns = [f'Q{i}' for i in range(1, 21)]
    d4_data.columns = [f'Q{i}' for i in range(1, 21)]
    
    d3_data['Program'] = 'D3'
    d4_data['Program'] = 'D4'

    # Combine data
    combined_data = pd.concat([d3_data, d4_data], axis=0).reset_index(drop=True)
    
    # Clean data
    combined_data = combined_data.dropna(how='all', subset=[f'Q{i}' for i in range(1, 21)])
    for i in range(1, 21):
        col = f'Q{i}'
        combined_data[col] = pd.to_numeric(combined_data[col], errors='coerce')
    
    combined_data = combined_data.dropna(subset=[f'Q{i}' for i in range(1, 21)])
    return combined_data

def calculate_pieces_scores(df):
    if len(df) == 0:
        return {cat: 0 for cat in CATEGORIES.keys()}
    results = {}
    for cat, qs in CATEGORIES.items():
        q_cols = [f'Q{i}' for i in qs]
        results[cat] = df[q_cols].mean(axis=1).mean()
    return results

def main():
    if not os.path.exists('output'):
        os.makedirs('output')

    print("Processing PIECES Framework - Pre-test Analysis...")
    
    k1_df = load_data('kuesioner_1')
    k2_df = load_data('kuesioner_2')
    
    programs = ['D3', 'D4']
    
    for prog in programs:
        print(f"\nGenerating Pre-test results for {prog}...")
        prog_path = os.path.join('output', prog)
        if not os.path.exists(prog_path):
            os.makedirs(prog_path)
            
        # Filter data for current program
        prog_k1 = k1_df[k1_df['Program'] == prog]
        prog_k2 = k2_df[k2_df['Program'] == prog]
        
        print(f"  Respondents - Kuesioner 1: {len(prog_k1)}, Kuesioner 2: {len(prog_k2)}")
        
        # Calculate scores
        k1_scores = calculate_pieces_scores(prog_k1)
        k2_scores = calculate_pieces_scores(prog_k2)
        
        # Create comparison data
        prog_comp = []
        for cat in CATEGORIES.keys():
            prog_comp.append({
                'Category': cat,
                'Kuesioner 1 Score': k1_scores[cat],
                'Kuesioner 2 Score': k2_scores[cat],
                'Difference': k2_scores[cat] - k1_scores[cat]
            })
        
        prog_df = pd.DataFrame(prog_comp)
        prog_df.to_csv(os.path.join(prog_path, f'pre_test_pieces_comparison_{prog}.csv'), index=False)
        
        # 1. Kuesioner 1 Chart
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Category', y='Kuesioner 1 Score', data=prog_df, palette='viridis')
        plt.ylim(0, 5)
        plt.title(f'Pre-test Analysis: Kuesioner 1 Satisfaction ({prog})')
        plt.axhline(y=3.41, color='red', linestyle='--', label='Satisfied Threshold (3.41)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(prog_path, f'pre_test_kuesioner_1_{prog}.png'))
        plt.close()

        # 2. Kuesioner 2 Chart
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Category', y='Kuesioner 2 Score', data=prog_df, palette='magma')
        plt.ylim(0, 5)
        plt.title(f'Pre-test Analysis: Kuesioner 2 Satisfaction ({prog})')
        plt.axhline(y=3.41, color='red', linestyle='--', label='Satisfied Threshold (3.41)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(prog_path, f'pre_test_kuesioner_2_{prog}.png'))
        plt.close()

        # 3. Comparison Chart (K1 vs K2)
        prog_melted = prog_df.melt(id_vars='Category', value_vars=['Kuesioner 1 Score', 'Kuesioner 2 Score'], 
                                   var_name='Kuesioner Type', value_name='Score')
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Category', y='Score', hue='Kuesioner Type', data=prog_melted, palette='muted')
        plt.ylim(0, 5)
        plt.title(f'Pre-test Analysis: Kuesioner 1 vs Kuesioner 2 ({prog})')
        plt.axhline(y=3.41, color='gray', linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(prog_path, f'pre_test_comparison_{prog}.png'))
        plt.close()
        
        print(f"  Files saved in {prog_path}")

    print("\nAll Pre-test separate reports have been generated successfully.")

if __name__ == "__main__":
    main()
