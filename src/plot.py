#Скрипт для построения графиков по результатам бенчмарка с учётом интерпретатора

import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_PATH = "../results/results.csv"
IMG_DIR = "../img"
os.makedirs(IMG_DIR, exist_ok=True)

# ========== Чтение данных ==========
df = pd.read_csv(RESULTS_PATH)
df["Size"] = df["Size"].astype(int)
df = df.sort_values("Size")

# ========== ДИАГНОСТИКА ==========
print("=== ДИАГНОСТИКА ДАННЫХ ===")
print("Уникальные интерпретаторы:", df["Interpreter"].unique())
print("Количество записей для CPython:", len(df[df["Interpreter"] == "CPython"]))
print("Количество записей для PyPy:", len(df[df["Interpreter"] == "PyPy"]))

# Проверим наличие данных для каждого алгоритма
print("\nНаличие данных по алгоритмам:")
for alg in df["Algorithm"].unique():
    cpython_count = len(df[(df["Algorithm"] == alg) & (df["Interpreter"] == "CPython")])
    pypy_count = len(df[(df["Algorithm"] == alg) & (df["Interpreter"] == "PyPy")])
    print(f"  {alg}: CPython={cpython_count}, PyPy={pypy_count}")

print("\nТип колонки Time (s):", df["Time (s)"].dtype)
print("Примеры значений Time (s):", df["Time (s)"].head(10))
print("====================================\n")

# ========== Очистка данных ==========
# Приводим время к числовому типу, ошибки превращаем в NaN
df["Time (s)"] = pd.to_numeric(df["Time (s)"], errors='coerce')

# Очищаем названия интерпретаторов от пробелов и лишних символов
df["Interpreter"] = df["Interpreter"].str.strip()

# Удаляем строки с NaN во времени (они не отобразятся на графике)
df = df.dropna(subset=["Time (s)"])

if "Interpreter" not in df.columns:
    df["Interpreter"] = "Default"

interpreters = df["Interpreter"].unique()
algorithms = df["Algorithm"].unique()
data_types = df["DataType"].unique()

print(f"После очистки интерпретаторы: {interpreters}")
print(f"Алгоритмы: {algorithms}")
print(f"Типы данных: {data_types}")

# ========== 1. Индивидуальные графики для каждого алгоритма ==========
for alg in algorithms:
    alg_data = df[df["Algorithm"] == alg]

    # ---- Время ----
    plt.figure(figsize=(12, 8))
    for dtype in data_types:
        for interp in interpreters:
            sub = alg_data[(alg_data["DataType"] == dtype) & (alg_data["Interpreter"] == interp)]
            if not sub.empty:
                plt.plot(sub["Size"], sub["Time (s)"],
                         marker='o', linestyle='-', linewidth=2,
                         label=f"{dtype} ({interp})")
    plt.title(f"Execution time of {alg}")
    plt.xlabel("Array size (N)")
    plt.ylabel("Time (s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, f"time_{alg}.png"))
    plt.close()

    # ---- Память ----
    # Для памяти аналогично, но с учётом, что для PyPy может быть 'N/A'
    df_mem = df.copy()
    df_mem["PeakMemory (MB)"] = pd.to_numeric(df_mem["PeakMemory (MB)"], errors='coerce')
    df_mem = df_mem.dropna(subset=["PeakMemory (MB)"])
    alg_data_mem = df_mem[df_mem["Algorithm"] == alg]

    plt.figure(figsize=(12, 8))
    for dtype in data_types:
        for interp in interpreters:
            sub = alg_data_mem[(alg_data_mem["DataType"] == dtype) & (alg_data_mem["Interpreter"] == interp)]
            if not sub.empty:
                plt.plot(sub["Size"], sub["PeakMemory (MB)"],
                         marker='o', linestyle='-', linewidth=2,
                         label=f"{dtype} ({interp})")
    plt.title(f"Peak memory of {alg}")
    plt.xlabel("Array size (N)")
    plt.ylabel("Memory (MB)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, f"memory_{alg}.png"))
    plt.close()

# ========== 2. Сводные графики по типам данных ==========
for dtype in data_types:
    dtype_data = df[df["DataType"] == dtype]

    # ---- Время ----
    plt.figure(figsize=(14, 10))
    for alg in algorithms:
        for interp in interpreters:
            sub = dtype_data[(dtype_data["Algorithm"] == alg) & (dtype_data["Interpreter"] == interp)]
            if not sub.empty:
                plt.plot(sub["Size"], sub["Time (s)"],
                         marker='.', linestyle='-', linewidth=1.5,
                         label=f"{alg} ({interp})")
    plt.title(f"Time comparison on '{dtype}' data")
    plt.xlabel("Array size (N)")
    plt.ylabel("Time (s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, f"time_comparison_{dtype}.png"))
    plt.close()

    # ---- Память ----
    dtype_data_mem = df_mem[df_mem["DataType"] == dtype]
    plt.figure(figsize=(14, 10))
    for alg in algorithms:
        for interp in interpreters:
            sub = dtype_data_mem[(dtype_data_mem["Algorithm"] == alg) & (dtype_data_mem["Interpreter"] == interp)]
            if not sub.empty:
                plt.plot(sub["Size"], sub["PeakMemory (MB)"],
                         marker='.', linestyle='-', linewidth=1.5,
                         label=f"{alg} ({interp})")
    plt.title(f"Memory comparison on '{dtype}' data")
    plt.xlabel("Array size (N)")
    plt.ylabel("Memory (MB)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, f"memory_comparison_{dtype}.png"))
    plt.close()

# ========== 3. Сравнительные графики (CPython vs PyPy) ==========
for alg in algorithms:
    alg_data = df[df["Algorithm"] == alg]
    for dtype in data_types:
        sub = alg_data[alg_data["DataType"] == dtype]
        if sub.empty:
            continue

        # Время
        plt.figure(figsize=(10, 6))
        for interp in interpreters:
            data = sub[sub["Interpreter"] == interp]
            if not data.empty:
                plt.plot(data["Size"], data["Time (s)"],
                         marker='s', linestyle='-', linewidth=2, label=interp)
        plt.title(f"{alg} on {dtype} – time")
        plt.xlabel("Array size (N)")
        plt.ylabel("Time (s)")
        plt.xscale("log")
        plt.yscale("log")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(IMG_DIR, f"time_{alg}_{dtype}_interp.png"))
        plt.close()

# ========== 4. Сравнительные графики для памяти (только где есть данные) ==========
df_mem = df.copy()
df_mem["PeakMemory (MB)"] = pd.to_numeric(df_mem["PeakMemory (MB)"], errors='coerce')
df_mem = df_mem.dropna(subset=["PeakMemory (MB)"])

for alg in algorithms:
    alg_data_mem = df_mem[df_mem["Algorithm"] == alg]
    for dtype in data_types:
        sub = alg_data_mem[alg_data_mem["DataType"] == dtype]
        if sub.empty:
            continue

        # Память
        plt.figure(figsize=(10, 6))
        for interp in interpreters:
            data = sub[sub["Interpreter"] == interp]
            if not data.empty:
                plt.plot(data["Size"], data["PeakMemory (MB)"],
                         marker='s', linestyle='-', linewidth=2, label=interp)
        plt.title(f"{alg} on {dtype} – memory")
        plt.xlabel("Array size (N)")
        plt.ylabel("Memory (MB)")
        plt.xscale("log")
        plt.yscale("log")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(IMG_DIR, f"memory_{alg}_{dtype}_interp.png"))
        plt.close()

print(f"Все графики сохранены в {IMG_DIR}")