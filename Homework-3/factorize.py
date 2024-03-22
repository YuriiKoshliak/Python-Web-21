import time
from multiprocessing import Pool, cpu_count

# Функція для факторизації одного числа
def factorize_number(n):
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

# Синхронна версія функції factorize
def factorize_sync(numbers):
    start_time = time.time()
    results = list(map(factorize_number, numbers))
    end_time = time.time()
    print(f"Синхронне виконання: {end_time - start_time} секунд")
    return results

# Асинхронна версія функції factorize
def factorize_async(numbers):
    start_time = time.time()
    with Pool(cpu_count()) as pool:
        results = pool.map(factorize_number, numbers)
    end_time = time.time()
    print(f"Асинхронне виконання: {end_time - start_time} секунд")
    return results

if __name__ == '__main__':
    numbers = [128, 255, 8128, 99999, 10651060, 39916801, 99999999]  # Список чисел для факторизації
    sync_results = factorize_sync(numbers)
    async_results = factorize_async(numbers)
    print(sync_results)
    
