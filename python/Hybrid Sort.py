def insertionSort(arr):
    comparisons = swaps = 0
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    return arr, comparisons, swaps

def selectionSort(arr):
    comparisons = swaps = 0
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return arr, comparisons, swaps

def hybridSort(theSeq, threshold=10):
    if len(theSeq) < threshold:
        return insertionSort(theSeq)
    else:
        return selectionSort(theSeq)
    
print(hybridSort([5,3,8,4,2], threshold=10))

