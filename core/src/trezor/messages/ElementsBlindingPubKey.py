# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        pass


class ElementsBlindingPubKey(p.MessageType):
    MESSAGE_WIRE_TYPE = 903

    def __init__(
        self,
        pubkey: bytes = None,
    ) -> None:
        self.pubkey = pubkey

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('pubkey', p.BytesType, 0),
        }
