import struct


class Message:
    """ The Message object grants the ability to create simple packets of data.
        Messages must be given an identifier (4 bytes) and a tuple of datatypes
        that the message will store.

        example_message = Message('EXPL', ('int', 'int', 'float'))

    """
    VALID_DATAYPES = ['int', 'float', 'char', 'string', 'varstring', 'bool']

    def __init__(self, message_id, message_datatypes, max_str_len=32):
        self.message_id = message_id
        self.message_datatypes = message_datatypes
        self.max_str_len = max_str_len
        self._msg_struct = struct.Struct(self._get_fmt_string())

    def _get_fmt_string(self):
        """ Returns the format string required for the message struct based on the datatpyes.

        """
        fmt = '>'
        for datatype in self.message_datatypes:
            if datatype in self.VALID_DATAYPES:
                if datatype == 'int':
                    fmt += 'I'
                if datatype == 'float':
                    fmt += 'f'
                if datatype == 'double':
                    fmt += 'd'
                if datatype == 'char':
                    fmt += 'c'
                if datatype == 'string':
                    fmt += str(self.max_str_len)+'s'
                if datatype == 'bool':
                    fmt += 'b'
            else:
                raise('Bad datatype')

        return fmt

    def pack(self, *args):
        """ Returns a byte string given a list of arguments

            example_message = Message('EXPL', ('int', 'int', 'float'))
            message_to_send = example_message.pack(14, 89, 0.67)

        """
        return self._msg_struct.pack(*args)

    def unpack(self, raw_message):
        """ Returns a tuple with the unpacked values from the message.

        """
        return self._msg_struct.unpack(raw_message)


