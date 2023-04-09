import random


def quick_sort(array):
    if (size := len(array)) < 2:
        return array
    pivot = array.pop(random.choice(range(size)))
    less, greater = [], []
    for i in array:
        if i <= pivot:
            less.append(i)
            continue
        greater.append(i)
    return quick_sort(less) + [pivot] + quick_sort(greater)


arr = [1, 3, 0, 7, 3, 4, 9, 2, 56]
print(quick_sort(arr))
