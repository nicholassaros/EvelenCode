############
#
# Streaming Payments Processor
#
# The function `process_payments()` is processing a large, but finite
# amount of payments in a streaming fashion.
#
# It relies on two library functions to do its job. The first function
# `stream_payments_to_storage(storage)` reads the payments from a payment
# processor and writes them to storage by calling `storage.write(buffer)`
# on it's `storage` argument. The `storage` argument is supplied by
# calling `get_payments_storage()` function. The API is defined below.
#
# TODO: Modify `process_payments()` to print a checksum of bytes written
# by `stream_payments_to_storage()`. The existing functionality
# should be preserved.
#
# The checksum is implemented as a simple arithmetic sum of bytes.
#
# For example, if bytes([1, 2, 3]) were written, you should print 6.
#
#
# NOTE: you need to take into account the following restrictions:
# - You are allowed only one call each to `get_payments_storage()` and
#       to `stream_payments_to_storage()`
# - You can not read from the storage.
# - You can not use disk as temporary storage.
# - Your system has limited memory that can not hold all payments.
#
############


# This is a library function, you can't modify it.
def get_payments_storage():
    """
    @returns an instance of
    https://docs.python.org/3/library/io.html#io.BufferedWriter
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    return open('/dev/null', 'wb')


# This is a library function, you can't modify it.
def stream_payments_to_storage(storage):
    """
    Loads payments and writes them to the `storage`.
    Returns when all payments have been written.

    @parameter `storage`: is an instance of
    https://docs.python.org/3/library/io.html#io.BufferedWriter
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in range(10):
        storage.write(bytes([1, 2, 3, 4, 5]))


class CheckSumWriter():
    def __init__(self, bufferWriter):
        self.bufferWriter = bufferWriter
        self.checksum = 0
        
    def write(self,data):
        #data is the bytes array. Ensure that sum is compadable
        self.checksum += sum(data)
        self.bufferWriter.write(data)

    def __getattr__(self, name):
        #uses the actual buffer writer implementation
        return getattr(self.bufferWriter, name)

    def getSum(self):
        return self.checkSum

def process_payments():
    """
    Store payments streamed by `stream_payments_to_storage` and
    print the checksum of payments stored
    """
    storage = get_payments_storage()

    #create instance of checkSumWriter, this wraps the write method to sum the buffer
    checkSumWriter = CheckSumWriter(storage)
    stream_payments_to_storage(checkSumWriter)
    print(checkSumWriter.getSum())

    


process_payments()


############
# Streaming Payments Processor, two vendors edition.
#
# We decided to improve the payment processor from the previous
# exercise and hired two vendors. One was to implement `stream_payments()`
# function, and another `store_payments()` function.
#
# The function `process_payments_2()` is processing a large, but finite
# amount of payments in a streaming fashion.
#
# Unfortunately the vendors did not coordinate their efforts, and delivered
# their functions with incompatible APIs.
#
# TODO: Your task is to analyse the APIs of `stream_payments()` and
# `store_payments()` and to write glue code in `process_payments_2()`
# that allows us to store the payments using these vendor functions.
#
# NOTE: you need to take into account the following restrictions:
# - You are allowed only one call each to `stream_payments()` and
#      to `store_payments()`
# - You can not read from the storage.
# - You can not use disk as temporary storage.
# - Your system has limited memory that can not hold all payments.
#
############
# This is a library function, you can't modify it.
def stream_payments(callback_fn):
    """
    Reads payments from a payment processor and calls `callback_fn(amount)`
    for each payment.

    Returns when there is no more payments.
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in range(10):
        callback_fn(i)


# This is a library function, you can't modify it.
def store_payments(amount_iterator):
    """
    Iterates over the payment amounts from amount_iterator
    and stores them to a remote system.
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in amount_iterator:
        print(i)

def callback_example(amount):
    print(amount)
    return True


import queue
import threading

def process_payments_2():
    q = queue.Queue()
    sentinel = object()

    def callback_fn(amount):
        q.put(amount)

    def producer():
        stream_payments(callback_fn)
        q.put(sentinel) 

    def amount_iterator():
        while True:
            item = q.get()
            if item is sentinel:
                break
            yield item

    t = threading.Thread(target=producer)
    t.start()

    store_payments(amount_iterator())

    t.join()


process_payments_2()

