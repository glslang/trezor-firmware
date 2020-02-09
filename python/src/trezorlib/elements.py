from . import messages
from .tools import expect


@expect(messages.ElementsRangeProofNonce, field="nonce")
def get_rangeproof_nonce(client, ecdh_pubkey, script_pubkey):
    return client.call(
        messages.ElementsGetRangeProofNonce(
            ecdh_pubkey=ecdh_pubkey, script_pubkey=script_pubkey
        )
    )

@expect(messages.ElementsBlindingPubKey, field="pubkey")
def get_blinding_pubkey(client, script_pubkey):
    return client.call(
        messages.ElementsGetBlindingPubKey(
            script_pubkey=script_pubkey
        )
    )