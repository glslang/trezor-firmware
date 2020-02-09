# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        pass


class ElementsGetBlindingPubKey(p.MessageType):
    MESSAGE_WIRE_TYPE = 902

    def __init__(
        self,
        script_pubkey: bytes = None,
    ) -> None:
        self.script_pubkey = script_pubkey

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('script_pubkey', p.BytesType, 0),
        }
