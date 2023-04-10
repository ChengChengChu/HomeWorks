from cryptography.hazmat.primitives.ciphers.modes import CBC
flag1 = "CNS{Aka_BIT_f1ipp1N9_atTaCk!}"#'CNS{IloveChihuahua_1?!}'
flag2 = 'bbb'
key = b'a' * 16
iv = b'a' * 16
mode = CBC(iv)
