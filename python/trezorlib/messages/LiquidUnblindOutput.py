# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .LiquidBlindedOutput import LiquidBlindedOutput


class LiquidUnblindOutput(p.MessageType):
    MESSAGE_WIRE_TYPE = 804

    def __init__(
        self,
        blinded: LiquidBlindedOutput = None,
        ecdh_privkey: bytes = None,
        committed_script: bytes = None,
    ) -> None:
        self.blinded = blinded
        self.ecdh_privkey = ecdh_privkey
        self.committed_script = committed_script

    @classmethod
    def get_fields(cls):
        return {
            1: ('blinded', LiquidBlindedOutput, 0),
            2: ('ecdh_privkey', p.BytesType, 0),
            3: ('committed_script', p.BytesType, 0),
        }
