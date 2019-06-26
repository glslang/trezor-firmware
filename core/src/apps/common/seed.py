from trezor import wire
from trezor.crypto import bip32, curve, hashlib, hmac

from apps.common import HARDENED, cache, mnemonic, storage
from apps.common.request_passphrase import protect_by_passphrase

allow = list


class Keychain:
    """
    Keychain provides an API for deriving HD keys from previously allowed
    key-spaces.
    """

    def __init__(self, seed: bytes, namespaces: list):
        self.seed = seed
        self.namespaces = namespaces
        self.roots = [None] * len(namespaces)

    def __del__(self):
        for root in self.roots:
            if root is not None:
                root.__del__()
        del self.roots
        del self.seed

    def validate_path(self, checked_path: list, checked_curve: str):
        for curve, *path in self.namespaces:
            if path == checked_path[: len(path)] and curve == checked_curve:
                if "ed25519" in curve and not _path_hardened(checked_path):
                    break
                return
        raise wire.DataError("Forbidden key path")

    def derive(self, node_path: list, curve_name: str = "secp256k1") -> bip32.HDNode:
        # find the root node index
        root_index = 0
        for curve, *path in self.namespaces:
            prefix = node_path[: len(path)]
            suffix = node_path[len(path) :]
            if curve == curve_name and path == prefix:
                break
            root_index += 1
        else:
            raise wire.DataError("Forbidden key path")

        # create the root node if not cached
        root = self.roots[root_index]
        if root is None:
            root = bip32.from_seed(self.seed, curve_name)
            root.derive_path(path)
            self.roots[root_index] = root

        # TODO check for ed25519?
        # derive child node from the root
        node = root.clone()
        node.derive_path(suffix)
        return node

    def master_blinding_key(self, curve_name: str = "secp256k1") -> bytes:
        node = self.derive([HARDENED | 10077], curve_name)
        return hashlib.sha256(node.private_key()).digest()


def derive_blinding_private_key(master_blinding_key: bytes, script: bytes) -> bytes:
    """Deterministic derivation of blinding keys (see SLIP-0077)."""
    assert len(master_blinding_key) == 32
    return hmac.new(
        key=master_blinding_key, msg=script, digestmod=hashlib.sha256
    ).digest()


def derive_blinding_public_key(master_blinding_key: bytes, script: bytes) -> bytes:
    private_key = derive_blinding_private_key(master_blinding_key, script)
    return curve.secp256k1.publickey(private_key)


async def get_keychain(ctx: wire.Context, namespaces: list) -> Keychain:
    if not storage.is_initialized():
        raise wire.ProcessError("Device is not initialized")
    seed = cache.get_seed()
    if seed is None:
        passphrase = cache.get_passphrase()
        if passphrase is None:
            passphrase = await protect_by_passphrase(ctx)
            cache.set_passphrase(passphrase)
        seed = mnemonic.get_seed(passphrase)
        cache.set_seed(seed)
    keychain = Keychain(seed, namespaces)
    return keychain


def derive_node_without_passphrase(
    path: list, curve_name: str = "secp256k1"
) -> bip32.HDNode:
    if not storage.is_initialized():
        raise Exception("Device is not initialized")
    seed = mnemonic.get_seed(progress_bar=False)
    node = bip32.from_seed(seed, curve_name)
    node.derive_path(path)
    return node


def remove_ed25519_prefix(pubkey: bytes) -> bytes:
    # 0x01 prefix is not part of the actual public key, hence removed
    return pubkey[1:]


def _path_hardened(path: list) -> bool:
    return all(i & HARDENED for i in path)
