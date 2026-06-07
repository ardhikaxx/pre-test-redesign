import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.container import BarContainer

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
    
    # Load all data
    k1_df = load_data('kuesioner_1')
    k2_df = load_data('kuesioner_2')
    
    # Merge K1 and K2
    all_data = pd.concat([k1_df, k2_df], axis=0).reset_index(drop=True)
    
    programs = ['D3', 'D4']
    program_results = {}
    
    for prog in programs:
        print(f"\nProcessing merged results for {prog}...")
        prog_path = os.path.join('output', prog)
        if not os.path.exists(prog_path):
            os.makedirs(prog_path)
            
        # Filter merged data for current program
        prog_df = all_data[all_data['Program'] == prog]
        print(f"  Total Respondents (K1+K2): {len(prog_df)}")
        
        # Calculate scores
        scores = calculate_pieces_scores(prog_df)
        program_results[prog] = scores
        
        # Save individual program results
        res_df = pd.DataFrame(list(scores.items()), columns=['Category', 'Score'])
        res_df.to_csv(os.path.join(prog_path, f'pieces_results_{prog}.csv'), index=False)
        
        # Program Chart
        plt.figure(figsize=(10, 6))
        # Fix: Assign hue to avoid FutureWarning
        ax = sns.barplot(x='Category', y='Score', hue='Category', data=res_df, palette='viridis', legend=False)
        plt.ylim(0, 5)
        plt.title(f'Pre-test Analysis: Total Satisfaction ({prog})')
        plt.axhline(y=3.41, color='red', linestyle='--', label='Satisfied Threshold (3.41)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(prog_path, f'pieces_total_{prog}.png'))
        plt.close()
        
        print(f"  Files saved in {prog_path}")

    # Final Comparison between D3 and D4
    print("\nGenerating final comparison between D3 and D4...")
    comparison_data = []
    for cat in CATEGORIES.keys():
        comparison_data.append({
            'Category': cat,
            'D3 Score': program_results['D3'][cat],
            'D4 Score': program_results['D4'][cat],
            'Difference': program_results['D4'][cat] - program_results['D3'][cat]
        })
    
    comp_df = pd.DataFrame(comparison_data)
    comp_df.to_csv(os.path.join('output', 'comparison_D3_vs_D4.csv'), index=False)
    
    # Comparison Chart
    comp_melted = comp_df.melt(id_vars='Category', value_vars=['D3 Score', 'D4 Score'], 
                               var_name='Program', value_name='Score')
    plt.figure(figsize=(12, 7))
    ax = sns.barplot(x='Category', y='Score', hue='Program', data=comp_melted, palette='Set2')
    plt.ylim(0, 5)
    plt.title('Pre-test Analysis Comparison: D3 vs D4 (K1+K2 Merged)')
    plt.axhline(y=3.41, color='gray', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join('output', 'comparison_D3_vs_D4.png'))
    plt.close()
    
    print("Final comparison files saved in output/")
    print("\nAll reports have been generated successfully.")

if __name__ == "__main__":
    main()
