import string
import secrets

def get_alphanumeric(tamanho=9):
    """
    Gera um código alfanumérico seguro com o tamanho especificado.
    """
    alfabeto = string.ascii_uppercase + string.digits
    codigo = ''.join(secrets.choice(alfabeto) for _ in range(tamanho))
    return codigo

if __name__ == "__main__":
    # Testando a função de geração de código alfanumérico
    # Exemplo de uso
    codigo_gerado = get_alphanumeric()
    print(f"Código gerado: {codigo_gerado}")