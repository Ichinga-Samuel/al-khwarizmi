def merge_sort(array):
    if (size := len(array)) < 2:
        return array
    mid = size // 2
    a, b = merge_sort(array[: mid]), merge_sort(array[mid:])
    output = []
    m, n = 0, 0
    sa, sb = len(a), len(b)
    while m < sa and n < sb:
        if (ai := a[m]) < (bi := b[n]):
            output.append(ai)
            m += 1
            continue
        output.append(bi)
        n += 1

    output.extend(a[m:] + b[n:])
    return output


arr = [1, 3, 0, 7, 3, 4, 9, 2, 56]
print(merge_sort(arr))
