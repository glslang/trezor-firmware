# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class MoneroTransactionSignInputAck(p.MessageType):
    MESSAGE_WIRE_TYPE = 516

    def __init__(
        self,
        signature: bytes = None,
        pseudo_out: bytes = None,
    ) -> None:
        self.signature = signature
        self.pseudo_out = pseudo_out

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('signature', p.BytesType, 0),
            2: ('pseudo_out', p.BytesType, 0),
        }
