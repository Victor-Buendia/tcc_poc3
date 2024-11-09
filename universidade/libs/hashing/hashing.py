import bcrypt

def hash_text(text):
    salt = bcrypt.gensalt() # String aleatória para obfuscar a senha
    hashed_text = bcrypt.hashpw(text.encode('utf-8'), salt)
    return hashed_text.decode('utf-8')

def verify_hash(text, hashed_text):
    return bcrypt.checkpw(text.encode('utf-8'), hashed_text.encode('utf-8'))

if __name__ == '__main__':
    print(hash_text('123456'))
    # print(verify_hash('123456', hash_text('123456')))