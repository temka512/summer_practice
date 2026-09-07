# src/benchmark.py

import time

# Пытаемся импортировать tracemalloc, если он доступен
try:
    import tracemalloc
    TRACEMALLOC_AVAILABLE = True
except ImportError:
    TRACEMALLOC_AVAILABLE = False
    print("Предупреждение: tracemalloc недоступен (возможно, вы используете PyPy). "
          "Измерение памяти будет пропущено.")


def measure(algorithm, data):
    """
    Запускает algorithm на копии data, измеряет время выполнения и,
    если доступен tracemalloc, пиковое потребление памяти.

    Возвращает:
        elapsed_time_sec, peak_memory_mb (или None, если память не измерена)
    """
    arr = data[:]  # копия, чтобы не портить исходные данные

    # Включаем tracemalloc только если он доступен
    if TRACEMALLOC_AVAILABLE:
        tracemalloc.start()

    start_time = time.perf_counter()
    result = algorithm(arr)
    end_time = time.perf_counter()

    elapsed = end_time - start_time

    if TRACEMALLOC_AVAILABLE:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = peak / (1024 * 1024)
    else:
        peak_mb = None  # или 0, но лучше None для обозначения отсутствия данных

    return elapsed, peak_mb