def my_sort(num_list):
    mid = len(num_list)//2
    left_list = merge_sort(num_list[:mid])
    right_list = merge_sort(num_list[mid:])
    return merge(left_list, right_list)

def merge_sort(nums):
    # base case
    if not nums or len(nums) == 1:
        return nums
    
    mid = len(nums)//2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    return merge(left, right)
    
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
    assert merge_sort([]) == []
    assert merge_sort([5]) == [5]
    assert merge_sort([3,2,4,8,7,10,1]) == [1,2,3,4,7,8,10]
    assert merge_sort([-666,420,1729,42,-10,0,1296,31]) == [-666,-10,0,31,42,420,1296,1729]