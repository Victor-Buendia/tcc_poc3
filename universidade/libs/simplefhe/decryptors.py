from seal import Plaintext, Ciphertext

import libs.simplefhe as simplefhe


def decrypt(item):
    decryptor = simplefhe._decryptor

    if simplefhe._private_key is None:
        raise ValueError('Private key has not been set. Decryption not possible.')

    if simplefhe._relin_keys is None:
        raise ValueError('Relinearization keys have not been set. Decryption not possible.')

    result = Plaintext()
    decryptor.decrypt(item._ciphertext, result)

    mode = item._mode
    if mode['type'] == 'int':
        if decryptor.invariant_noise_budget(item._ciphertext) == 0:
            raise ValueError(
                'The noise budget has been exhausted.'
                + ' Try calling `simplefhe.initialize` with a larger `poly_modulus_degree` or a smaller `max_int`.'
            )
        result = result.to_string()
        result = int(result, 16) 
        if result > mode['modulus'] // 2:
            result -= mode['modulus']
        return result
    else:
        decoded = item._mode['encoder'].decode(result)
        return float(decoded[0])
