from cryptography.fernet import Fernet

chave = Fernet.generate_key().decode()
print("Chave gerada:", chave)
