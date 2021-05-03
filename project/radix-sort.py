import urllib
import requests

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()

def countingSort(inputArray, placeValue, maxLength):
    countArray = [0] * 129
    inputSize = len(inputArray)

    for i in range(inputSize):
        #letterPlaceValue = len(inputArray[i])-1 % placeValue
        #print(inputArray[i])
        diff = maxLength-(len(inputArray[i])-1)
        #print(f"inputArray[i]: {inputArray[i]} and the index {i} and the countArray index: {placeValue-diff} and the diff {diff}")

        if placeValue < len(inputArray[i]):
            index = (inputArray[i][placeValue]) % 128
        else:
            index = 0
        countArray[index] += 1

    for i in range(len(countArray)-1):
        countArray[i] += countArray[i-1]

    #print(f"Before reconstruction: {countArray}")

    outputArray = [0] * inputSize
    i = inputSize - 1
    while i >= 0:
        diff = maxLength-(len(inputArray[i])-1)
        currentEl = inputArray[i]
        if placeValue < len(inputArray[i]):
            index = (inputArray[i][placeValue]) % 128
        else:
            index = 0
        countArray[index] -= 1
        newIndex = countArray[index]
        outputArray[newIndex] = currentEl
        i -= 1
        #print(f"During reconstruction: {countArray}")

    #print(f"After reconstruction:  {countArray}")
    return outputArray




def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    longestString = max(book_url, key=len)
    maxLength = len(longestString)
    outputArray = book_url
    #print(f"Max Length: {maxLength}")
    #print(countingSort(a, 1))
    for i in range(maxLength-1, -1, -1):
        #print(f"length of max element: {i}")
        outputArray = countingSort(outputArray,i,maxLength)
    return outputArray


a = [b'cwhfsw',b'qhgqqqqq',b'bastaaa',b'cwa',b'asd',b'evca',b'fui',b'you',b'ye',b'your']
b = book_to_words()
radix_a_book(b)
print("done")
#print(f"Sorted array: {sorted(b)}")
#print(radix_a_book(b)==sorted(b))
