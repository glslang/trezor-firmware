# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class LiquidBlindedOutput(p.MessageType):
    MESSAGE_WIRE_TYPE = 803

    def __init__(
        self,
        conf_value: bytes = None,
        conf_asset: bytes = None,
        ecdh_pubkey: bytes = None,
        script_pubkey: bytes = None,
        range_proof: bytes = None,
        surjection_proof: bytes = None,
    ) -> None:
        self.conf_value = conf_value
        self.conf_asset = conf_asset
        self.ecdh_pubkey = ecdh_pubkey
        self.script_pubkey = script_pubkey
        self.range_proof = range_proof
        self.surjection_proof = surjection_proof

    @classmethod
    def get_fields(cls):
        return {
            1: ('conf_value', p.BytesType, 0),
            2: ('conf_asset', p.BytesType, 0),
            3: ('ecdh_pubkey', p.BytesType, 0),
            4: ('script_pubkey', p.BytesType, 0),
            5: ('range_proof', p.BytesType, 0),
            6: ('surjection_proof', p.BytesType, 0),
        }
