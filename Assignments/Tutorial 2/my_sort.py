def my_sort(num_list):
    # merge sort base case
    if not num_list or len(num_list) == 1:
        return num_list
    
    mid = len(num_list)//2

    # recursive calls
    left_list = my_sort(num_list[:mid])
    right_list = my_sort(num_list[mid:])

    # recombine sorted lists
    return merge(left_list, right_list)
    
def merge(list1, list2):
    """ Utility for merging two sorted lists """
    i, j = 0, 0
    merged = []
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    
    while i < len(list1):
        merged.append(list1[i])
        i += 1
    
    while j < len(list2):
        merged.append(list2[j])
        j += 1

    return merged

if __name__ == "__main__":
    assert my_sort([]) == []
    assert my_sort([5]) == [5]
    assert my_sort([3,2,4,8,7,10,1]) == [1,2,3,4,7,8,10]
    assert my_sort([-666,420,1729,42,-10,0,1296,31]) == [-666,-10,0,31,42,420,1296,1729]