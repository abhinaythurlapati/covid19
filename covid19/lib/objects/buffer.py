

class Buffer:
    Min_Size = 1
    Max_Size = 1000

    def __init__(self, min_size=Min_Size, max_size=Max_Size):
        if not isinstance(min_size, int):
            raise ValueError('kw_arg:"min_size" is not of type "int"')

        if not isinstance(max_size, int):
            raise ValueError('kw_arg:"max_size" is not of type "int"')

        if min_size <= 0:
            raise ValueError('kw_arg:"size" should be greater than 0')
        if max_size > 1000:
            raise OverflowError('Buffer Max_Limit: {}'.format(Buffer.Max_size))

        self.min_size = min_size
        self.max_size = max_size
        self.buffer_data = list()

    def add(self, data):
        if len(data) <= 0:
            raise ValueError("No data to add to the buffer")

        #if not isinstance(data, dict):
        #    raise TypeError("Expected kw_arg:'data' type: 'dict'; found: {}".type(data))

        if not self.is_overflowed():
            self.buffer_data.append(data)
        else:
            raise OverflowError

    def clear(self):
        self.buffer_data = list()

    def size(self):
        """
        returns the current size of the buffer
        :return:
        """
        return len(self.buffer_data)

    def is_overflowed(self):
        if len(self.buffer_data) > self.max_size:
            return True
        else:
            return False
