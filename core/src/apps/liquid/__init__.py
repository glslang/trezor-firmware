from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED


def boot():
    ns = [["secp256k1"]]
    wire.add(MessageType.LiquidGetBlindedAddress, __name__, "get_blinded_address", ns)
    wire.add(MessageType.LiquidBlindTx, __name__, "blind_tx", ns)
    wire.add(MessageType.LiquidUnblindOutput, __name__, "unblind_output", ns)
    wire.add(MessageType.LiquidSignTx, __name__, "sign_tx", ns)  # WIP - NOT SAFE!!!
