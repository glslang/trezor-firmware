# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class LiquidBlindTxRequest(p.MessageType):
    MESSAGE_WIRE_TYPE = 802

    def __init__(
        self,
        output_index: int = None,
    ) -> None:
        self.output_index = output_index

    @classmethod
    def get_fields(cls):
        return {
            1: ('output_index', p.UVarintType, 0),
        }
