# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class LiquidSignature(p.MessageType):

    def __init__(
        self,
        digest: bytes = None,
        pubkey: bytes = None,
        sigder: bytes = None,
    ) -> None:
        self.digest = digest
        self.pubkey = pubkey
        self.sigder = sigder

    @classmethod
    def get_fields(cls):
        return {
            1: ('digest', p.BytesType, 0),
            2: ('pubkey', p.BytesType, 0),
            3: ('sigder', p.BytesType, 0),
        }
