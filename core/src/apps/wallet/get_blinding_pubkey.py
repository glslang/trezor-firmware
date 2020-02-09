from trezor.crypto.curve import secp256k1_zkp
from trezor.crypto.hashlib import sha256
from trezor.messages.ElementsBlindingPubKey import ElementsBlindingPubKey


async def get_blinding_pubkey(ctx, msg, keychain):
    pubkey = keychain.derive_slip77_blinding_public_key(msg.script_pubkey)
    return ElementsBlindingPubKey(pubkey=pubkey)
