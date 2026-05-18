def countInversionsNaive(arr):
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i+1, n):
            if arr[i] > arr[j]:
                count += 1
    return count

def mergeCount(arr):
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr)//2
    left, inv_left = mergeCount(arr[:mid])
    right, inv_right = mergeCount(arr[mid:])
    merged = []
    i = j = inv_split = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inv_split += len(left) - i
            j += 1

    merged += left[i:]
    merged += right[j:]

    return merged, inv_left + inv_right + inv_split

def countInversionsSmart(arr):
    _, count = mergeCount(arr)
    return count

arr = [2,4,1,3,5]

print("Naive:", countInversionsNaive(arr))
print("Smart:", countInversionsSmart(arr))