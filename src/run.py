# src/run.py

import csv
import os
import argparse
from sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    quick_sort,
    merge_sort,
    heap_sort,
    counting_sort,
    radix_sort,
    bucket_sort,
    built_in_sort,
)
from generators import (
    generate_random,
    generate_sorted,
    generate_reversed,
    generate_almost_sorted,
)
from benchmark import measure

# === Аргументы командной строки ===
parser = argparse.ArgumentParser(description="Запуск бенчмарка сортировок")
parser.add_argument(
    "--interpreter",
    type=str,
    default="CPython",
    help="Имя интерпретатора (CPython, PyPy, ...)"
)
parser.add_argument(
    "--output",
    type=str,
    default="../results/results.csv",
    help="Путь к выходному CSV-файлу"
)
args = parser.parse_args()

# === Конфигурация ===
ALGORITHMS = [
    ("Bubble", bubble_sort),
    ("Selection", selection_sort),
    ("Insertion", insertion_sort),
    ("Quick", quick_sort),
    ("Merge", merge_sort),
    ("Heap", heap_sort),
    ("Counting", counting_sort),
    ("Radix", radix_sort),
    ("Bucket", bucket_sort),
    ("Builtin", built_in_sort),
]

SIZES = [10, 500, 1000, 50000, 1000000]

DATA_TYPES = {
    "Random": generate_random,
    "Sorted": generate_sorted,
    "Reversed": generate_reversed,
    "AlmostSorted": generate_almost_sorted,
}

SLOW_ALGORITHMS = {"Bubble", "Selection", "Insertion"}
SLOW_SIZE_LIMIT = 5000

# === Создаём папку для результатов (если её нет) ===
out_dir = os.path.dirname(args.output)
if out_dir:
    os.makedirs(out_dir, exist_ok=True)

# === Запуск ===
with open(args.output, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Interpreter", "Algorithm", "DataType", "Size", "Time (s)", "PeakMemory (MB)"])

    for alg_name, alg_func in ALGORITHMS:
        for size in SIZES:
            if alg_name in SLOW_ALGORITHMS and size > SLOW_SIZE_LIMIT:
                print(f"Пропускаем {alg_name} для размера {size} (слишком медленно)")
                continue

            for data_type, gen_func in DATA_TYPES.items():
                print(f"[{args.interpreter}] Запуск {alg_name} на {data_type} размер {size}...")
                data = gen_func(size)
                elapsed, peak = measure(alg_func, data)

                # Обработка peak, если tracemalloc недоступен
                if peak is None:
                    peak_display = "N/A"
                    peak_write = "N/A"
                else:
                    peak_display = f"{peak:.2f} МБ"
                    peak_write = peak

                print(f"  Время: {elapsed:.6f} с, Память: {peak_display}")

                # Запись в CSV
                writer.writerow([args.interpreter, alg_name, data_type, size, elapsed, peak_write])
                f.flush()

print(f"Результаты сохранены в {args.output}")