# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .LiquidSignature import LiquidSignature

if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore


class LiquidSignedTx(p.MessageType):
    MESSAGE_WIRE_TYPE = 808

    def __init__(
        self,
        sigs: List[LiquidSignature] = None,
    ) -> None:
        self.sigs = sigs if sigs is not None else []

    @classmethod
    def get_fields(cls):
        return {
            1: ('sigs', LiquidSignature, p.FLAG_REPEATED),
        }
