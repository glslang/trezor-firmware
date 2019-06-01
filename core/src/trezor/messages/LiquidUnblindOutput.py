# Automatically generated by pb2py
# fmt: off
import protobuf as p

from .LiquidBlindedOutput import LiquidBlindedOutput


class LiquidUnblindOutput(p.MessageType):
    MESSAGE_WIRE_TYPE = 804

    def __init__(
        self,
        blinded: LiquidBlindedOutput = None,
        ecdh_privkey: bytes = None,
        master_blinding_key: bytes = None,
    ) -> None:
        self.blinded = blinded
        self.ecdh_privkey = ecdh_privkey
        self.master_blinding_key = master_blinding_key

    @classmethod
    def get_fields(cls):
        return {
            1: ('blinded', LiquidBlindedOutput, 0),
            2: ('ecdh_privkey', p.BytesType, 0),
            3: ('master_blinding_key', p.BytesType, 0),
        }
