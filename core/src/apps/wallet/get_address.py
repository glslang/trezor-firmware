from trezor.messages import InputScriptType
from trezor.messages.Address import Address

from apps.common import coins, seed
from apps.common.layout import address_n_to_str, show_address, show_qr
from apps.common.paths import validate_path
from apps.wallet.sign_tx import addresses


async def get_address(ctx, msg, keychain):
    coin_name = msg.coin_name or "Bitcoin"
    coin = coins.by_name(coin_name)

    await validate_path(
        ctx,
        addresses.validate_full_path,
        keychain,
        msg.address_n,
        coin.curve_name,
        coin=coin,
        script_type=msg.script_type,
    )

    node = keychain.derive(msg.address_n, coin.curve_name)
    derive_blinding_pubkey = None
    if coin.blinded_address_type is not None:
        mbk = msg.master_blinding_key or keychain.master_blinding_key()
        derive_blinding_pubkey = lambda script: seed.derive_blinding_public_key(
            script=script, master_blinding_key=mbk
        )

    address = addresses.get_address(
        msg.script_type,
        coin,
        node,
        msg.multisig,
        derive_blinding_pubkey=derive_blinding_pubkey,
    )
    address_short = addresses.address_short(coin, address)
    if msg.script_type == InputScriptType.SPENDWITNESS:
        address_qr = address.upper()  # bech32 address
    else:
        address_qr = address  # base58 address

    if msg.show_display:
        if msg.multisig:
            desc = "Multisig %d of %d" % (msg.multisig.m, len(msg.multisig.pubkeys))
        else:
            desc = address_n_to_str(msg.address_n)

        while True:
            if await show_address(ctx, address_short, desc=desc):
                break
            if await show_qr(ctx, address_qr, desc=desc):
                break

    return Address(address=address)
