import struct


class Message:
    """ The Message object grants the ability to create simple packets of data.
        Messages must be given an identifier (4 bytes) and a tuple of datatypes
        that the message will store.

        example_message = Message('EXAMPLE', ('int', 'int', 'float'))
        |- Msg Object -|         |- Msg id -| |- Required msg args -|

        The message_id argument is locked at 4 bytes at the moment. All message
        ids must be 4 bytes in length or errors will occur. This will be changed
        to a more dynamic solution in future releases, however it isn't that
        big of an issue.

        `VALID_DATATYPES` is a list of all the available data types currently
        allowed.
            int: 32bit integer
            float: 32bit float
            char: 8bit integer
            string: Char array or 8bit integer array - must specify length
            bool: Boolean value

            Will be adding support for much more data types (varstring, double...)
    """
    VALID_DATAYPES = ['int', 'float', 'char', 'string', 'bool']

    def __init__(self, message_id, message_datatypes, max_str_len=32, requires_ack=False):
        self.message_id = str(message_id).encode()
        self.message_datatypes = message_datatypes
        self.max_str_len = max_str_len

        self._msg_struct = struct.Struct(self._get_fmt_string())

        self.requires_ack = requires_ack

    def _get_fmt_string(self):
        """ Returns the format string required for the message struct based on the datatpyes.

            Since the Message object is a Struct, a format string must be provided.
            This private method builds the format string based on the given parameters set by
            the developer.

        """
        fmt = '>4s'
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

        return fmt

    def pack(self, *args):
        """ Returns a bytes given a list of arguments

            example_message = Message('EXPL', ('int', 'int', 'float'))
            message_to_send = example_message.pack(14, 89, 0.67)

        """
        return self._msg_struct.pack(self.message_id, *args)

    def unpack(self, raw_message):
        """ Returns a tuple with the unpacked values from the message.

        """
        return self._msg_struct.unpack(raw_message)


