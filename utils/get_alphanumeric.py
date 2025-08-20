import string
import secrets
import logging

# Configurar logger
logger = logging.getLogger(__name__)

def get_alphanumeric(tamanho=9):
    """
    Gera um código alfanumérico seguro com o tamanho especificado.
    """
    alfabeto = string.ascii_uppercase + string.digits
    codigo = ''.join(secrets.choice(alfabeto) for _ in range(tamanho))
    logger.debug(f"Código alfanumérico gerado com tamanho {tamanho}")
    return codigo

if __name__ == "__main__":
    # Configurar logging básico para teste
    logging.basicConfig(level=logging.INFO)
    
    # Testando a função de geração de código alfanumérico
    # Exemplo de uso
    codigo_gerado = get_alphanumeric()
    logger.info(f"Código gerado: {codigo_gerado}")