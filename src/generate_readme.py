# src/generate_readme.py

import os
import sys
import pandas as pd
from datetime import datetime

print("START")
sys.stdout.flush()

CSV_PATH = "../results/results.csv"
README_PATH = "../README.md"
IMG_DIR = "../img"


def pivot_table(df, value_col, index_cols, columns_col):
    pivot = df.pivot_table(index=index_cols, columns=columns_col, values=value_col, aggfunc='first')
    pivot = pivot.fillna('-')
    try:
        cols = sorted(pivot.columns, key=int)
    except:
        cols = pivot.columns
    pivot = pivot[cols]
    lines = []
    header = [''] + list(pivot.columns)
    lines.append('| ' + ' | '.join(str(h) for h in header) + ' |')
    lines.append('|' + '|'.join(['---'] * len(header)) + '|')
    for idx, row in pivot.iterrows():
        if isinstance(idx, tuple):
            idx_str = ' | '.join(str(i) for i in idx)
        else:
            idx_str = str(idx)
        row_strs = []
        for v in row:
            if v == '-':
                row_strs.append('-')
            else:
                if isinstance(v, (int, float)):
                    if abs(v) < 0.0001:
                        row_strs.append(f'{v:.6e}')
                    else:
                        row_strs.append(f'{v:.6f}')
                else:
                    row_strs.append(str(v))
        lines.append('| ' + idx_str + ' | ' + ' | '.join(row_strs) + ' |')
    return '\n'.join(lines)


def generate_readme():
    print("generate_readme() START")
    sys.stdout.flush()
    
    if not os.path.exists(CSV_PATH):
        print("CSV not found")
        return

    print("Reading CSV...")
    sys.stdout.flush()
    df = pd.read_csv(CSV_PATH)
    df['Size'] = df['Size'].astype(int)
    df = df.sort_values('Size')

    if "Interpreter" not in df.columns:
        print("No Interpreter column")
        return

    print("Building tables...")
    sys.stdout.flush()
    index_cols = ['Interpreter', 'Algorithm', 'DataType']
    time_table = pivot_table(df, 'Time (s)', index_cols, 'Size')
    memory_table = pivot_table(df, 'PeakMemory (MB)', index_cols, 'Size')

    print("Looking for images...")
    sys.stdout.flush()
    img_files = []
    if os.path.exists(IMG_DIR):
        img_files = sorted([f for f in os.listdir(IMG_DIR) if f.endswith('.png')])
    print(f"Found {len(img_files)} images")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Generating README...")
    sys.stdout.flush()
    
    readme_content = f"""# Experimental Analysis of Sorting Algorithms

**Report generated:** {now}

## Machine Specifications

| Component           | Value                         |
|---------------------|-------------------------------|
| PC Model            | 82RN (Lenovo)                 |
| CPU                 | AMD Ryzen 5 5625U with Radeon Graphics |
| Cores/Threads       | 6 cores / 12 threads          |
| RAM                 | 16 GB DDR4                    |
| Storage             | SSD                           |
| Interpreter versions| CPython 3.12.10, PyPy 7.3.23  |

## Results

### Execution Time (seconds)

{time_table}

### Peak Memory Usage (MB)

{memory_table}

## Plots

"""
    for img in img_files:
        readme_content += f"![{img}](img/{img})\n\n"

    readme_content += """
## Analysis

Fill in your analysis here based on the tables and plots.

## Reproduction Instructions

### Requirements

- Operating System: Windows
- Installed interpreters: CPython 3.11+, PyPy 7.3.17+
- Required packages: pandas, matplotlib

Install packages:
```bash
pip install pandas matplotlib
"""