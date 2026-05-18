def mergeThreeSortedLists(listA, listB, listC):
    i = j = k = 0
    result = []

    while i < len(listA) or j < len(listB) or k < len(listC):
        values = []

        if i < len(listA):
            values.append((listA[i], 'A'))
        if j < len(listB):
            values.append((listB[j], 'B'))
        if k < len(listC):
            values.append((listC[k], 'C'))

        val, source = min(values)
        result.append(val)

        if source == 'A':
            i += 1
        elif source == 'B':
            j += 1
        else:
            k += 1

    return result

print(mergeThreeSortedLists([1,5,9], [2,6,10], [3,4,7]))