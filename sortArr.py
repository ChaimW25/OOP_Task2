

class SortArray(object):
    def __init__(self, size, defaultValue = None):
        self.size = size
        if(defaultValue == None):
            self.items = list()
            for i in range(size):
                self.items.append(defaultValue)
        else:
            self.items = list()

            if(len(defaultValue) == size or len(defaultValue) < size):
                for j in range(len(defaultValue)):
                    if(defaultValue[j]):
                        self.items.append(defaultValue[j])
                for i in range(len(defaultValue), size):
                    self.items.append(None)
            else:
                print('Elements are more than the size specified')

    def myLen(self):
        length = 0
        for i in self.items:
            if i == None:
                continue
            else:
                length += 1
        return length

    def insert(self, element):
        if (self.myLen() < self.size):
            for i in range(self.myLen(), 0, -1):
                self.items[i] = self.items[i - 1]
            self.items[0] = element
        else:
            print('Element index out of range')

    # def insertAtIndex(self, index, element):
    #     if (self.myLen() < self.size):
    #         for i in range(self.myLen(), index, -1):
    #             self.items[i] = self.items[i - 1]
    #         self.items[index] = element
    #     else:
    #         print('Element index out of range')

    # def insertAfterIndex(self, index, element):
    #     if (self.myLen() < self.size):
    #         for i in range(self.myLen(), index + 1, -1):
    #             self.items[i] = self.items[i - 1]
    #         self.items[index + 1] = element
    #     else:
    #         print('Element index out of range')

    # def insertBeforeIndex(self, index, element):
    #     if (self.myLen() < self.size):
    #         for i in range(self.myLen(), index - 1, -1):
    #             self.items[i] = self.items[i - 1]
    #         self.items[index - 1] = element
    #     else:
    #         print('Element index out of range')

    def delete(self, element):
        if element in self.items:
            Index = self.items.index(element)
            self.items[Index] = None
        else:
            print('This element is not in the Array!')

    def search(self, element):
        if element in self.items:
            position = 0
            for i in range(self.myLen()):
                if(self.items[i] == element):
                    break
                else:
                    position += 1

            print('Element {} found at position {}'.format(element, position))
        else:
            print('This element is not in the Array!')