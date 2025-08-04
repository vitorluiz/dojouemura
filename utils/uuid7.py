# backend/libs/uuid7.py

import time
import random
import uuid

_last_v7_timestamp = -1
_last_v7_random = -1

def uuid7() -> uuid.UUID:
    """
    Gera um UUIDv7, conforme descrito no rascunho da RFC.
    Este é um UUID ordenado por tempo, útil para ordenação em bases de dados.
    """
    global _last_v7_timestamp, _last_v7_random
    timestamp_ms = int(time.time() * 1000)

    if timestamp_ms <= _last_v7_timestamp:
        timestamp_ms = _last_v7_timestamp
        # O timestamp é o mesmo ou retrocedeu. Incrementa os bits aleatórios.
        random_bits = _last_v7_random + 1
        # Verifica o overflow
        if random_bits >= (1 << 74):
            # Os bits aleatórios estouraram. Espera pelo próximo milissegundo.
            while timestamp_ms <= _last_v7_timestamp:
                timestamp_ms = int(time.time() * 1000)
            random_bits = random.getrandbits(74)
    else:
        random_bits = random.getrandbits(74)

    _last_v7_timestamp = timestamp_ms
    _last_v7_random = random_bits

    # 48 bits do timestamp
    uuid_int = timestamp_ms << 80

    # 4 bits da versão (7)
    uuid_int |= 7 << 76

    # 74 bits aleatórios, com a variante (2)
    # A variante tem 2 bits (10), então precisamos abrir espaço para ela.
    # Variante nos bits 62 e 63.
    # Pega os 12 bits superiores dos 74 bits aleatórios
    uuid_int |= (random_bits >> 62) << 64
    # Define a variante
    uuid_int |= 2 << 62
    # Adiciona os 62 bits inferiores restantes
    uuid_int |= random_bits & ((1 << 62) - 1)

    return uuid.UUID(int=uuid_int)
