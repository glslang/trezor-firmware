# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .TxConfidentialValue import TxConfidentialValue

if __debug__:
    try:
        from typing import Dict, List, Optional
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class TxOutputBinType(p.MessageType):

    def __init__(
        self,
        amount: int = None,
        script_pubkey: bytes = None,
        decred_script_version: int = None,
        confidential_value: TxConfidentialValue = None,
    ) -> None:
        self.amount = amount
        self.script_pubkey = script_pubkey
        self.decred_script_version = decred_script_version
        self.confidential_value = confidential_value

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('amount', p.UVarintType, 0),  # required
            2: ('script_pubkey', p.BytesType, 0),  # required
            3: ('decred_script_version', p.UVarintType, 0),
            4: ('confidential_value', TxConfidentialValue, 0),
        }
