import bcrypt


def hash_password(password):
    # Parolayı byte dizisine dönüştür
    password = bytes(password, 'utf-8')

    # Salt oluştur
    salt = bcrypt.gensalt()

    # Hash oluştur
    hashed_password = bcrypt.hashpw(password, salt)

    # Byte dizisini string'e dönüştür ve döndür
    return hashed_password.decode('utf-8')


def check_password(password, hashed_password):
    # Taking user entered password and hashed password and encoding them
    user_bytes = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    # checking password
    return bcrypt.checkpw(user_bytes, hashed_password)
