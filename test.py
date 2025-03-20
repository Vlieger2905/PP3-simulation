class Queue():

    def __init__(self):
        self.s1 = LibraryStack()
        self.s2 = LibraryStack()

    """
    Returns whether the queue is empty.
    @return true if there are no elements left, false otherwise.
    """
    def isEmpty(self):
        return self.s1.length()== 0

    """
    Returns the number of elements in the queue.
    @return the number of elements in the queue.
    """
    def size(self):
        return self.s1.length()

    """
    Adds an element to the queue.
    @param i element to enqueue.
    """
    def enqueue(self,i):
        self.s1.append(i)

    """
    Removes the first element from the queue.
    @return the first element from the queue.
    """
    def dequeue(self):
        self.s1.pop()

    """
    Returns the first element from the queue without removing it.
    @return the first element from the queue.
    """
    def first(self):
        return self.s1[0]