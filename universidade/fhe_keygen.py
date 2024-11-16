from pathlib import Path
from libs.simplefhe import generate_keypair
from logger.log import get_logger

log = get_logger('fhe_keygen')

public_key, private_key, relin_keys = generate_keypair()

Path('keys').mkdir(exist_ok=True)
public_key.save('keys/public.key')
private_key.save('keys/private.key')
relin_keys.save('keys/relin.key')

log.info('Keypair saved to keys/ directory')