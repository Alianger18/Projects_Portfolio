from hashlib import md5


ex_word = "Oblivieet"
cipher_text = md5(ex_word.encode())

print(cipher_text)