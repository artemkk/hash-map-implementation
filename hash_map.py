# Course: CS261 - Data Structures
# Assignment: 5
# Student: Artem Kuryachy
# Description: Hash Map Implementation (Portfolio Assignment)


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the content of the hash map. It does not change underlying hash table
        capacity.
        """

        # Iterate through the bueckets
        for i in range(self.capacity):
            # Pick up the SLL in the bucket
            sll_at_bucket = self.buckets.get_at_index(i)
            # Iterate through the k/v pairs in the SLL and set all to None
            for node in sll_at_bucket:
                node.key = None
                node.value = None

        # Reset size
        self.size = 0

        pass

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        # Convert key to index
        hash = self.hash_function(key)
        index = hash % self.capacity

        # Get SLL at index
        sll_at_bucket = self.buckets.get_at_index(index)

        # Iterate through SLL until key is found
        for node in sll_at_bucket:
            if node.key == key:
                return node.value

        # Return None if not found
        return None

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map.
        """

        # Convert key to hash index
        hash = self.hash_function(key)
        index = hash % self.capacity

        # Add value to bucket at index
        if index < self.capacity:
            sll_at_bucket = self.buckets.get_at_index(index)

            # Check if given key exists
            if sll_at_bucket.contains(key):
                # If key not unique, replace the old k/v pair and insert the new pair in it's place
                sll_at_bucket.remove(key)
                sll_at_bucket.insert(key, value)
            else:
                # Insert if key is unique
                sll_at_bucket.insert(key, value)
                self.size += 1
        pass

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.
        """
        # Iterate through buckets
        for i in range(self.capacity):
            # Grab SLL at bucket
            sll_at_bucket = self.buckets.get_at_index(i)
            # Check in bucket if key is within; remove k/v pair if yes and reduce size
            if sll_at_bucket.contains(key):
                sll_at_bucket.remove(key)
                self.size -= 1

        pass

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False.
        """

        # Check if map is empty
        if self.size == 0:
            return False

        # Get index
        hash = self.hash_function(key)
        index = hash % self.capacity

        # Get SLL at index
        sll_at_bucket = self.buckets.get_at_index(index)
        # Check if key is in SLL
        if sll_at_bucket.contains(key):
            return True

        return False

    def empty_buckets(self) -> int:
        """
        This method returns a number of empty buckets in the hash table.
        """

        # Initialize counter
        emp_count = 0

        # Iterate through buckets
        for i in range(self.capacity):
            # Grab SLL in bucket
            sll_at_bucket = self.buckets.get_at_index(i)
            # Check if bucket is empty and tally if it is
            if sll_at_bucket.length() == 0:
                emp_count += 1

        return emp_count

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """

        # Count the total number of elements stored
        num_elem = 0
        for i in range(self.capacity):
            sll_at_bucket = self.buckets.get_at_index(i)
            num_elem = num_elem + sll_at_bucket.length()

        # Get the number of buckets
        num_buck = self.capacity
        # Calculate table load factor
        load_factor = num_elem / num_buck

        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs
        must remain in the new hash map and all hash table links must be rehashed
        """

        # Invalid input
        if new_capacity < 1:
            return

        # Store old hash table
        old_buckets = self.buckets
        old_cap = self.capacity

        # Create new self.buckets and set self.capacity to new value
        self.buckets = DynamicArray()
        self.capacity = new_capacity
        self.size = 0

        for _ in range(new_capacity):
            self.buckets.append(LinkedList())

        # Iterate over content of old_buckets and for each k/v pair, add that to self.buckets
        for i in range(old_cap):
            sll_old = old_buckets.get_at_index(i)
            for node in sll_old:
                self.put(node.key, node.value)


    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all keys stored in your hash map.
        """

        # Create DA object
        dyn_arr_keys = DynamicArray()

        # Iterate through buckets
        for i in range(self.capacity):
            # Grab SLL in bucket
            sll_at_bucket = self.buckets.get_at_index(i)
            # Iterate through SLL
            for node in sll_at_bucket:
                dyn_arr_keys.append(node.key)

        return dyn_arr_keys


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
