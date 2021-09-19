# Course: CS261 - Data Structures
# Assignment: 5
# Student: Artem Kuryachy
# Description: Min Heap Implementation (Portfolio Assignment)


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        This method adds a new object to the MinHeap maintaining heap property
        """

        # End of Array Index
        ins_ind = self.heap.length()

        if ins_ind == 0:
            self.heap.append(node)
            return

        # 1. Put new element in end of the array
        self.heap.append(node)

        # 2. Compute inserted elements parent index
        par_ind = (ins_ind - 1) // 2

        # 3. Compare value of inserted element with value of parent
        # Get parent value
        par_val = self.heap.get_at_index(par_ind)

        # Swap if parent value larger than inserted element value
        while par_val > node and ins_ind != 0:
            self.heap.swap(par_ind, ins_ind)
            ins_ind = par_ind
            par_ind = (ins_ind - 1) // 2
            par_val = self.heap.get_at_index(par_ind)

        pass

    def get_min(self) -> object:
        """
        This method returns an object with a minimum key without removing it from the heap. If
        the heap is empty, the method raises a MinHeapException.
        """

        # Check if empty
        if self.is_empty():
            raise MinHeapException
        # Return val at zero index
        return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        This method returns an object with a minimum key and removes it from the heap. If the
        heap is empty, the method raises a MinHeapException.
        """
        # Check if empty
        if self.is_empty():
            raise MinHeapException

        # 1. Get and remember value of first element in array.
        min_val = self.get_min()

        if self.heap.length() == 1:
            self.heap.pop()
            return min_val

        # 2. Replace the value of the first element in the array with the value of the last element
        # and remove the last element
        self.heap.swap(0, self.heap.length() - 1)
        if self.heap.get_at_index(0) == self.heap.get_at_index(self.heap.length() - 1):
            self.heap.pop()
            return min_val
        else:
            self.heap.pop()


        if self.heap.length() == 1:
            return min_val

        if self.heap.length() == 2:
            self.heap.swap(0, 1)
            return min_val
        # 3. Compute the indices of the children of the replacement element
        left_val = self.heap.get_at_index(1)
        right_val = self.heap.get_at_index(2)

        # 4. Compare the value of the replacement element with the minimum value of its two children
        # (or possibly one child). If replacement element's value is less than it's minimum child value, swap those two
        # elements in the array.
        # mcv = min child val
        if left_val < right_val:
            mcv_ind = 1
            mcv = left_val
        else:
            mcv_ind = 2
            mcv = right_val

        # Repeat process until heap structure achieved
        min_val_ind = 0
        while min_val <= mcv:
            self.heap.swap(min_val_ind, mcv_ind)

            min_val_ind = mcv_ind

            # Check bounds
            if (2 * min_val_ind + 1) > (self.heap.length() - 1):
                return min_val
            if (2 * min_val_ind + 2) > (self.heap.length() - 1):
                return min_val
            if (2 * min_val_ind + 1) < 0:
                return min_val
            if (2 * min_val_ind + 2) < 0:
                return min_val

            left_val = self.heap.get_at_index(2*min_val_ind+1)
            right_val = self.heap.get_at_index(2*min_val_ind+2)

            # mcv = min child val
            if left_val < right_val:
                mcv_ind = 2*min_val_ind+1
                mcv = left_val
            else:
                mcv_ind = 2*min_val_ind+2
                mcv = right_val

        if min_val == mcv:
            return min_val


    def build_heap(self, da: DynamicArray) -> None:
        """
        This method receives a dynamic array with objects in any order and builds a proper
        MinHeap from them. Current content of the MinHeap is lost.
        """

        # Create temporary array the size of da
        stor = DynamicArray()
        for _ in range(da.length()):
            stor.append(None)

        # Copy over elements of da into temp array
        for i in range(da.length()):
            da_val = da.get_at_index(i)
            stor.set_at_index(i, da_val)

        # Set temp equal to the heap
        self.heap = stor

        # Single Node is a valid heap
        if self.heap.length() == 1:
            return self.heap

        # Look at largest index in array and figure out it's parent
        last_ind = self.heap.length() - 1
        par_li = (last_ind - 1) // 2

        # Tru Count will track hte number of time the parent val is less than its children
        # If it's equal to the length of the heap, that means all parent vals are less than their children
        # and it is in proper min heap order. Adjustment loop repeats until this condition is met.
        tru_count = 0
        while tru_count != self.heap.length():

            if par_li < 0:
                par_li = (last_ind - 1) // 2

            # Start at par_li (parent of last index)
            par_li_val = self.heap.get_at_index(par_li)

            # Need to swap it with it's smallest child
            lc_ind = 2*par_li + 1
            if lc_ind < 0 or lc_ind > self.heap.length():
                return self.heap
            lc_val = self.heap.get_at_index(lc_ind)

            rc_ind = 2*par_li + 2
            if rc_ind < 0 or rc_ind > self.heap.length():
                return self.heap
            rc_val = self.heap.get_at_index(rc_ind)

            # Verify parent val is less than children
            if par_li_val < lc_val and par_li_val < rc_val:
                # Increase true count and move back an index to the next value to be addressed
                tru_count += 1
                par_li -= 1
                continue

            # Get index of smallest child
            if lc_val < rc_val:
                mci = lc_ind
            else:
                mci = rc_ind

            # Swap minimum child value and parent value
            self.heap.swap(par_li, mci)
            par_li -= 1

        return self.heap


# BASIC TESTING
if __name__ == '__main__':

    # print("\nPDF - add example 1")
    # print("-------------------")
    # h = MinHeap()
    # print(h, h.is_empty())
    # for value in range(300, 200, -15):
    #     h.add(value)
    #     print(h)
    #
    # print("\nPDF - add example 2")
    # print("-------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
    #     h.add(value)
    #     print(h)
    #
    #
    # print("\nPDF - get_min example 1")
    # print("-----------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # print(h.get_min(), h.get_min())


    print("\nPDF - remove_min example 1")
    print("--------------------------")
    # h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    h = MinHeap([1, 10, 2, 2, 2, 2, 2, 2, 2, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())


    # print("\nPDF - build_heap example 1")
    # print("--------------------------")
    # da = DynamicArray([32, 12, 2, 8, 16, 20, 24, 40, 4])
    # # da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    # h = MinHeap(['zebra', 'apple'])
    # print(h)
    # h.build_heap(da)
    # print(h)
    # da.set_at_index(0, 500)
    # print(da)
    # print(h)

