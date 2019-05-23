# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class LiquidSignTxInput(p.MessageType):

    def __init__(
        self,
        prev_hash: bytes = None,
        prev_index: int = None,
        sequence: int = None,
        amount: int = None,
        sign_privkey: bytes = None,
    ) -> None:
        self.prev_hash = prev_hash
        self.prev_index = prev_index
        self.sequence = sequence
        self.amount = amount
        self.sign_privkey = sign_privkey

    @classmethod
    def get_fields(cls):
        return {
            1: ('prev_hash', p.BytesType, 0),
            2: ('prev_index', p.UVarintType, 0),
            3: ('sequence', p.UVarintType, 0),
            4: ('amount', p.UVarintType, 0),
            5: ('sign_privkey', p.BytesType, 0),
        }
