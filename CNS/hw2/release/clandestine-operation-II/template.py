def header_signature():
    return b'NTLMSSP\x00'

def header_type(message_type):
    return message_type.to_bytes(4, "little")

def header_flags(flags):
    return flags.to_bytes(4, "little")

def write_security_buffer(input_bytes, offset):
    length = len(input_bytes).to_bytes(2, "little")
    allocated_size = length
    offset = offset.to_bytes(4, "little")
    return length + allocated_size + offset

def read_seurity_buffer(input_bytes):
    if isinstance(input_bytes, str):
        input_bytes = input_bytes.encode()

    length = int.from_bytes(input_bytes[:2], "little")
    allocated_size = int.from_bytes(input_bytes[2:4], "little")
    offset = int.from_bytes(input_bytes[4:8], "little")
    return length, allocated_size, offset

def gen_type1_msg():
    # TODO
    pass

def parse_type2_msg():
    # TODO
    pass

def gen_type3_msg():
    # TODO
    pass
