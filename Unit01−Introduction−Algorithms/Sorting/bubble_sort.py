# BUBBLE SORT

def bubblesort(arr, n):
    for i in range(n - 1):
        swapped = False

        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if swapped == False:
            break   # already sorted


arr = []
n = int(input("Size: "))

print("Enter elements of an array:")

for i in range(n):
    arr.append(int(input()))

bubblesort(arr, n)

print("Sorted array is:")

for i in range(n):
    print(arr[i])