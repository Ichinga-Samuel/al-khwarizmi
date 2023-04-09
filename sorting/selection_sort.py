"""


"""


def find_smallest(array):
    """
    Find the smallest element in an array
    :param array:
    :return:
    """
    smallest = None
    for element in array:
        if smallest is None or element < smallest:
            smallest = element
    return smallest


def selection_sort(array):

    sorted_array = []
    while array:
        sorted_array.append(i := find_smallest(array))
        array.remove(i)
    return sorted_array


arr = [3, 2, 5, 9, 0]
print(selection_sort(arr))
