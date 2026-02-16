def binary_search(arr, x):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

arr = []
count = int(input("enter number of data :"))

for i in range(count):
    num = int(input(f"number{i+1} enter numwinber  "))
    arr.append(num)


arr.sort()
print("Sorted list :", arr)

x = int(input('enter number that you want :  '))

result = binary_search(arr, x)
if result != -1:
    print("the number is in the list")
else:
    print("the number is not in the list")
