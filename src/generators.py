import random

def generate_random(n, seed=42):
    """Случайный список целых чисел в диапазоне [-n, n]."""
    random.seed(seed)
    return [random.randint(-n, n) for _ in range(n)]

def generate_sorted(n):
    """Отсортированный по возрастанию."""
    return list(range(n))

def generate_reversed(n):
    """Отсортированный по убыванию."""
    return list(range(n - 1, -1, -1))

def generate_almost_sorted(n, seed=42):
    """95% элементов на месте, 5% перемешаны."""
    random.seed(seed)
    arr = list(range(n))
    # Количество перемешиваемых элементов
    swap_count = max(1, int(n * 0.05))
    indices = list(range(n))
    random.shuffle(indices)
    # Берём первые swap_count индексов и перемешиваем их значения
    selected = indices[:swap_count]
    values = [arr[i] for i in selected]
    random.shuffle(values)
    for i, idx in enumerate(selected):
        arr[idx] = values[i]
    return arr