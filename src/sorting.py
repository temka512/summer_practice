import random


#--- Квадратичные ---


def bubble_sort(mass): #Сортировка пузырьком
    n = len(mass)
    for i in range(n):
        for j in range(0, n - i - 1):
            if mass[j] > mass[j + 1]:
                mass[j], mass[j + 1] = mass[j + 1], mass[j]
    return mass


def selection_sort(mass): #Сортировка выбором
    n = len(mass)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if mass[j] < mass[min_idx]:
                min_idx = j
        mass[i], mass[min_idx] = mass[min_idx], mass[i]
    return mass


def insertion_sort(mass): #Сортировка вставками
    for i in range(1, len(mass)):
        key = mass[i]
        j = i - 1
        while j >= 0 and mass[j] > key:
            mass[j + 1] = mass[j]
            j -= 1
        mass[j + 1] = key
    return mass


# --- Логарифмичные ---


def quick_sort(mass): #Быстрая сортировка 
    if len(mass) <= 1:
        return mass
    pivot = mass[len(mass) // 2]
    left = [x for x in mass if x < pivot]
    middle = [x for x in mass if x == pivot]
    right = [x for x in mass if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(mass): # Сортировка слиянием 
    if len(mass) <= 1:
        return mass
    mid = len(mass) // 2
    left = merge_sort(mass[:mid])
    right = merge_sort(mass[mid:])
    
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heap_sort(mass): #Сортировка кучей
    def heapify(a, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and a[l] > a[largest]:
            largest = l
        if r < n and a[r] > a[largest]:
            largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(a, n, largest)

    n = len(mass)
    for i in range(n // 2 - 1, -1, -1):
        heapify(mass, n, i)
    for i in range(n - 1, 0, -1):
        mass[i], mass[0] = mass[0], mass[i]
        heapify(mass, i, 0)
    return mass


# --- Линейные ---


def counting_sort(mass):
    # Сортировка подсчетом (Counting Sort)
    if not mass:
        return mass
    min_val, max_val = min(mass), max(mass)
    count = [0] * (max_val - min_val + 1)
    for num in mass:
        count[num - min_val] += 1
    
    result = []
    for i, cnt in enumerate(count):
        result.extend([i + min_val] * cnt)
    return result


def radix_sort(mass):
    # Поразрядная сортировка (Radix Sort)
    if not mass:
        return mass
    # Сдвигаем числа в плюс, если есть отрицательные
    min_val = min(mass)
    data = [x - min_val for x in mass]
    max_num = max(data)
    
    exp = 1
    while max_num // exp > 0:
        buckets = [[] for _ in range(10)]
        for num in data:
            digit = (num // exp) % 10
            buckets[digit].append(num)
        data = [num for bucket in buckets for num in bucket]
        exp *= 10
        
    return [x + min_val for x in data]


def bucket_sort(mass): #Блочная 
    if not mass:
        return mass
    min_val, max_val = min(mass), max(mass)
    bucket_count = int(len(mass) ** 0.5) or 1
    buckets = [[] for _ in range(bucket_count)]
    
    val_range = (max_val - min_val) or 1
    for num in mass:
        idx = int((num - min_val) / val_range * (bucket_count - 1))
        buckets[idx].append(num)
        
    result = []
    for bucket in buckets: #Для сортировки внутри бакетов используем быструю вставку
        for i in range(1, len(bucket)):
            key = bucket[i]
            j = i - 1
            while j >= 0 and bucket[j] > key:
                bucket[j + 1] = bucket[j]
                j -= 1
            bucket[j + 1] = key
        result.extend(bucket)
    return result


# --- Sort() ---

def built_in_sort(mass):
    return sorted(mass)



