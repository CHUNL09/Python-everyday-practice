import random,time
def bubble_sort(array):
    for i in range(len(array)-1):  # i from 0---9
        for j in range(i+1,len(array)):  # j from
            if array[i]>= array[j]:
                tmp=array[i]
                array[i]=array[j]
                array[j]=tmp
        #print(array)

def insertion_sort(array):
    for j in range(1,len(array)):
        key=array[j]
        i=j-1
        while i>=0 and array[i]>key:
            array[i+1]=array[i]
            i=i-1
        array[i+1]=key

def selection_sort(array):
    for i in range(len(array)):
        min_val=array[i]
        for j in range(i+1,len(array)):
            if array[j]<min_val:
                min_val=array[j]
                array[j]=array[i]
                array[i]=min_val

def quick_sort(array,left,right):
    if left>=right:
        return
    low=left
    high=right
    key=array[low]

    while low<high:
        while low<high and array[high]>key:
            high-=1
        array[low]=array[high]
        array[high]=key

        while low<high and array[low]<=key:
            low+=1
        array[high]=array[low]
        array[low]=key

    quick_sort(array,left,low-1)
    quick_sort(array,low+1,right)


if __name__=='__main__':
    original =[]
    for i in range(1000):
        original.append(random.randrange(100000))

    print("---------------Bubble_sort-----------")
    source=original
    print("before: ",source)
    time_start = time.time()
    bubble_sort(source)
    time_end = time.time()
    print("after: ",source[0:100])
    print("cost:",time_end-time_start)

    print("---------------Insertion_sort-----------")
    source=original
    print("before: ",source)
    time_start = time.time()
    insertion_sort(source)
    time_end = time.time()
    print("after: ",source[0:100])
    print("cost:",time_end-time_start)

    print("---------------selection_sort-----------")
    source=original
    print("before: ",source)
    time_start = time.time()
    selection_sort(source)
    time_end = time.time()
    print("after: ",source[0:100])
    print("cost:",time_end-time_start)

    print("---------------quick_sort-----------")
    source=original
    print("before: ",source)
    time_start = time.time()
    quick_sort(source,0,len(source)-1)
    time_end = time.time()
    print("after: ",source[0:100])
    print("cost:",time_end-time_start)
