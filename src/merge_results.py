# Объединяет все CSV-файлы вида results_*.csv в папке results в один файл results.csv
import os
import glob
import pandas as pd

RESULTS_DIR = "../results"
OUTPUT_FILE = os.path.join(RESULTS_DIR, "results.csv")

def merge_csv():
    # Находим все файлы, начинающиеся с "results_" и заканчивающиеся на ".csv"
    pattern = os.path.join(RESULTS_DIR, "results_*.csv")
    files = glob.glob(pattern)
    if not files:
        print("Не найдено файлов results_*.csv в папке", RESULTS_DIR)
        return

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        # Если колонка Interpreter отсутствует, извлекаем из имени файла
        if "Interpreter" not in df.columns:
            # Из имени results_cpython.csv извлекаем cpython
            base = os.path.basename(f)
            # удаляем results_ и .csv
            interp = base.replace("results_", "").replace(".csv", "")
            df["Interpreter"] = interp.capitalize()  # чтобы было CPython, PyPy и т.д.
        dfs.append(df)
    
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(OUTPUT_FILE, index=False)
    print(f"Объединённый файл сохранён как {OUTPUT_FILE}")
    print(f"Всего записей: {len(merged)}")

if __name__ == "__main__":
    merge_csv()