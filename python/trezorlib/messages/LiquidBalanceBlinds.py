# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .LiquidAmount import LiquidAmount

if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore


class LiquidBalanceBlinds(p.MessageType):

    def __init__(
        self,
        inputs: List[LiquidAmount] = None,
        outputs: List[LiquidAmount] = None,
    ) -> None:
        self.inputs = inputs if inputs is not None else []
        self.outputs = outputs if outputs is not None else []

    @classmethod
    def get_fields(cls):
        return {
            1: ('inputs', LiquidAmount, p.FLAG_REPEATED),
            2: ('outputs', LiquidAmount, p.FLAG_REPEATED),
        }
