# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import ctypes

import pytest

from trezorlib import liquid, messages as proto
from trezorlib.tools import parse_path

from . import secp256k1_zkp as lib
from .common import TrezorTest


@pytest.mark.liquid
@pytest.mark.skip_t1
class TestMsgLiquidFixed(TrezorTest):

    INPUT_AMOUNTS = [
        proto.LiquidAmount(
            value=2099999199946660,
            value_blind=bytes.fromhex(
                "5fa920cecd0db99028e5191e60001b29d36e853d240b78461b18aec61231d206"
            ),
            asset=bytes.fromhex(
                "230f4f5d4b7c6fa845806ee4f67713459e1b69e8e60fcee2e4940c7a0d5de1b2"
            ),
            asset_blind=bytes.fromhex(
                "e3eab79f0bf70ef52008cb5f3d4f0c837a5345ffaa32061c5f9326118eeb2901"
            ),
        )
    ]
    # To be blinded
    OUTPUT_AMOUNTS = [
        proto.LiquidAmount(
            value=2099997399936660,
            value_blind=bytes.fromhex(
                "4420823cfde6f1c26b30f90ec7dd01e4887534a20f0b0d04c36ed80e71e0fd77"
            ),
            asset=bytes.fromhex(
                "230f4f5d4b7c6fa845806ee4f67713459e1b69e8e60fcee2e4940c7a0d5de1b2"
            ),
            asset_blind=bytes.fromhex(
                "b07670eb940bd5335f973daad8619b91ffc911f57cced458bbbf2ce03753c9bd"
            ),
        ),
        proto.LiquidAmount(
            value=11_0000_0000,
            value_blind=bytes.fromhex(
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ),  # to be rebalanced on device
            asset=bytes.fromhex(
                "230f4f5d4b7c6fa845806ee4f67713459e1b69e8e60fcee2e4940c7a0d5de1b2"
            ),
            asset_blind=bytes.fromhex(
                "189c24279e9851d5814204136feb5713c166b13269dd63fc35c797ff08a6cd90"
            ),
        ),
    ]
    EXPLICIT_AMOUNTS = [
        proto.LiquidAmount(
            value=7_0000_0000,  # explicit amount (not blinded)
            asset=bytes.fromhex(
                "230f4f5d4b7c6fa845806ee4f67713459e1b69e8e60fcee2e4940c7a0d5de1b2"
            ),
        ),
        proto.LiquidAmount(
            value=1_0000,  # fee (not blinded)
            asset=bytes.fromhex(
                "230f4f5d4b7c6fa845806ee4f67713459e1b69e8e60fcee2e4940c7a0d5de1b2"
            ),
        ),
    ]

    BLIND_OUTPUTS = [
        proto.LiquidBlindOutput(
            amount=OUTPUT_AMOUNTS[0],
            ecdh_pubkey=bytes.fromhex(
                "03e51618ad58667e40208978c4dff3683b694154dc7552143c3779d30d56881220"
            ),
            ecdh_privkey=bytes.fromhex(
                "fa0ff0169dc9575674066676cfb0b4eb8902c44269da1cf6ba66d3f8b6d4b100"
            ),
            script_pubkey=bytes.fromhex(
                "76a914f24bb0c13089fb711ecf5c133e7df0818e1b1a5988ac"
            ),
            random_seed32=bytes.fromhex(
                "a9ea0e755a5c2e8210242a08e7078f7f89385eb09423555182568b96e8a4fef2"
            ),
        ),
        proto.LiquidBlindOutput(
            amount=OUTPUT_AMOUNTS[1],
            ecdh_pubkey=bytes.fromhex(
                "023407bcc7467fbd727f408a87e129a0c9a61ae0f05da8cb916ed1d69e8b7290a2"
            ),
            ecdh_privkey=bytes.fromhex(
                "095066a745addb6d8831c2b0f87821142b4456556d89aa82bcadae3a9578fa45"
            ),
            script_pubkey=bytes.fromhex(
                "76a914248036444a09a71e10ff91c8034ba213a179af9d88ac"
            ),
            random_seed32=bytes.fromhex(
                "35a414d025c24b40ae3ac127722988ba973aea8d37179706072ed33a14607ad7"
            ),
        ),
    ]

    BLINDED_OUTPUTS = [
        proto.LiquidBlindedOutput(
            conf_value=bytes.fromhex(
                "0916f3edd39bf22ccb0fd0a88ef58bffdc664c91d1f36b5b362de28be17ef43239"
            ),
            conf_asset=bytes.fromhex(
                "0a706c19c4b7698acfb620a8966d5c256b938c100f8e885e57e21e8c3761916853"
            ),
            ecdh_pubkey=bytes.fromhex(
                "03fab5f773776dfb8b14226ae7b9981757c56c667fda28e90d343786a8fbaa72d1"
            ),
            script_pubkey=BLIND_OUTPUTS[0].script_pubkey,
            surjection_proof=bytes.fromhex(
                "01000188f65964cf16dd257486fc4331928dbba045a50f702dc948c38eb7c2d9684ff5ebd22d101c5bb2d0060264eabcc94e630bbf9eb5d0205c0bd63166a53b261194"
            ),
            range_proof=bytes.fromhex(
                "603200000000000000010f3f370161b262fc9e0f200d15d38f1c7452f35ca4ab091f325551c4a060c94eee160dc5881b42ae4b384482b0b9dbf9c25a72fbbaa0545a7d2a784d2be471a22af7b444efc416ca77d6ae24146c63b766da445daac910d9ae911007905ec096cb74066cdb728a81c6a2aaa62de69352da60491a6788eee093429757832a6cc22ba2948042d898a8a94eee22e16292e1f78df489ee4f07a17b406a21fe75a2a312661af694e33be69e0b6bf20dca39650736ebcfad392bfdfbf768d66cad2e7dded69322827e1de7db608441c1e38bde98afc1e96d3de3933673ecfbc8c586a5a382012167bb25e5fd895fe613a6a6d9851f56e2db1c0d6a224e190a7e37821244864446e0178886d05ab12260eee78068e26007d4e83afc67e483c3c49295d44b17cff02ebe6bf27d225aa771ec4dd5aa10020f19d494990274b13b7c0022a7ed86ce07a8d21d30cd9d4fb35c3194fe3d6c127f600f5fc2966bc90cfbecf996f8e8fba86a1d473fc54f3a5f9d99d5379b7b3a41285f494926f439ff510e1d3e8d6c20e87f8ed1c242e3219fe4c4f6de31b16c00b3d43bd86fe15765dd9d8a40a9831d80e1dba603bba36097127eec11416bc45679b9b35a1e6b07086a63c3bbe22fd5bdb044371936bcf7aad27da16be98c3db24e43df3c9dccb081fd55fe361806ed56d49e9c71d38978efd31f531c25b80d89c43e476782823d52e45efdf84c4fd2cf283c66a0b3d9517c1d5b1a25b37ec88635c0b867e89191cff5c5fa0acf0c9d6d26d1f7e403e8e2af02f9f5d133678fa19276243ed0b93f390e06224271bb8d7f29967600c71feb9b5497a278108a1c2f7fc50fc7209945b3360181e8ef3ce5476d7c287c25d5d0581ecad1d30f453f68d67e0523356e212c78d4d9080f7011c1b4baae1962560b8c6e28e74ed56b4fea78f1639a2edd4a34ee848268eff30cc9cdfb049bc91bb1c9968a6291da7ae1bfc7ee97a1e76b361fe92dec4dedfd3c4227b2e8d8d8c948b9402893658dfff14dc18b79d65da17ce5c4c5309f2d3948e3a69ffac29e66f35cc1a40f502a314950378260524e655175f8477307139540fa9905e3e57268e3f3bcfda8a062811854c02be60f71111c6ca44d5eaef80953cc3a6eb9ef7e24e9cd416776eae5a21b8c5d351f203529ef495cc54188b34cb6c66c8362467cf9089fd2b0ed3ccd698d867d566551600143281aa802143a01a2d85c9a85bd1bd75518b767788c57c04f1040d566f05c9293a615510415b9ec3186f815293dc0376988bf4e356020ff0d2ec4ee769dead1ab8c32c63f9ebd85d595fd995472c5cbd778db75d1d53bc0391f9e9ce5cf9d42b9ad919087ea6d7ec0b6b7749c6e91ef062fa9c3803805a55a0532be785a7172454acf73e7132cb9e0b036a823dd895c86fa880786aaace6900709a3c29abc7b69e7dfb523ba482ed324f547d5e9a20bfadb9d85175e5ee8b8e1aba9a5c8ad22409f8fd6deac641f33c9bd7c6b4a8b8c05510bf6e06ad19f9f90177f7511db1972db8579143c7d4709da6b50c968bfe1eae9fb7e11c67b2dd1b53bfb1e1fa5c500fe752101af8793010bc38129e17c9fcb71891012b250bf78bac68358383a14c8c8e26a30594457074d6d530c26472e821ea153311fcb5be6b433b5ee716b208802fb27887e75642f382aaf81ec1f77abc9ea71e9bdb589d7b3ec74af7ba022c90c4ab1acd00c5d9810b0243c9c91e988ad709edc9d9f664791cf6c4ed5b30b0d63dace054f635605a990d6d7288d5095fffae6316d5bb03f095a8fb4c118801ffc16e4dddf9afb05e38cff24605e0403d05a10f6234fca829e93ed6086fb9c255517213e39bb724375c310a99a194d016c17f7eac8ec953879e07efb72f79b5ba5e3fbeaf734023327fc867e825450afa23a18b27183396f7a46683d11f81f68db99a6753b9a3670e51fe81c2482b15a4e0938626c712b4b1be0ef83f2db7727455eac52e76af3e13ad2e12c7ba4c50f68f53b036ddf2c69140e8a84ab14279b34000e16fdc9bab5ec3e5b00cc0c7e4739ae778c496f94808429006e7dea90294e68c9d2c4e4e55d31f78bfe19da947bdf4963fe27516d4a464d72a26685b7ad8d471a7e54a79f20f95124fdae04d89bb8a057562a066e1dece6b3d9c00dbf6d7da910e3513de0b0db99e2c9eef538b86b55c46969a798be9150305cff5de1e1588e1cc4d5d42521e306aaec91b276f1f97f031e4b9e50991f75cd8baec2940feca28ef1d2205d9f887037cc4cb0b8d30f6ffbd5e878b7f82391f1094764d2c6bfa1a476ac24b3c63f4263381df535760ab6054239f517efb5a3efba63a2b747d01e5d064f0cf712f3682379c83ec55a87d302aefca3d91c78ba1d6203d0dfb1d71804f4930f2565eccebbb59af9f6be4f66301b86151cdb3d6ef22dc0752fa24ad96cfe33753e37e86862ce76fe8482b68d6ad97ad3f92cf118e0e4fc5e8114d6c3d300e7987b00d6def749f17a2fae044acf24dd7f8efb939357ca16cf32129bf98de0ad2fe82a312ccb456af4b4f2a881f8345201211343d01e3d97fffe272e968775edfa83636cfe2865956f4d80fcda467a861ebb326722b2f0f5db4ffae60f999c5bf1e97a74bc987e317c1dd94aaced7f8dcab3a3fc8a35cb9ed6b68fb715885fd7f6196ca1d7c104381eb4795bbe533c64b5b2407d74c19c9acb2bb83d0d680d475696c4f7277f8fc75e5cdc032b0237092df706f98a126883f160c8d24293b0e426a93cf3b49a28cd93a9d28e6eed7f1d21630c4390534e317fcdc32518da0cef28320dd9ea2d79ef4b7f72e59b675d42fcba94d146ba6efe71e1f8272484daf9c261d57095698376db8af2b39d29f9ae23e7f25bb36b414134f5d6286fe6afea6424648a6c78c930bf666799a499778f20e93a713ed725e3e26c2d28e02359250ac35b7c8239285a9e72594f94f656ed737829c16f8d096b8640c6fa993471cdbdd08875d4c230e5ca48303c2021beb4fa0b6755ffaccdd94cdc9f6b2421afbc9b224aa76be8e6a684170b6b0022c714d252212f615296b083319c0ed9cbadba7d3a5be0931bb5154ab55ec51ca583e487c4addcb8bd5855fa070828adea592daa04a40ad69191d089ac71a9f5dd673df9c33e3f55332a788756fb7c0a97386d51fdda6c1b083d4345837dec96a4a56fe9a4f52afb626f173f171bbad5a7b6fe836cc551338f68389bcd67956eab8299dd3a4dd1bdecf5bd4f643e3d738fe3da589ff45236f0c74b29e110046dfc4415aefa3e31011de80aa92b268bd0a5e14bd63e6d084a0e4a3adc791c247e1e702330806f50531240a6c14b6af990c846b937a72b35bcf15c4851332f9e62efb8107da3442c6d46106f5a2105ef1826349f71c5175986598699c6573abb881ac18bd7d6a70711af49bad0c88605cab8366709c251b22defcaffba5019c4daa5a6cf521933d42b9a2629e48500597df369215e2b115d89ff2bd85fbeada7599542b6afb3526e62cbda2b243f6388fa7cf664ed6ff68df09060af7bcf5200ff2e2f77bb591d265288f1a6b4918793ea9a20eddf9ce4a0d4855e6cd6976bff3e2009466d0802dffe612275df9fc9efa50d8b00df5727a06a47cee7bbfbf8821e89d4318c90a397c8957dfd81e24ead3ae46c5c86dbac766492b94f30976ebfc355f1dc25cd5c2a214a6ca451cab26e0b825bd228993583a454775f43cc97b97ea30ebaac9b565d6366e5ba0b18eaff98c8d6b6cc957e07f2896d42a20809ecc6d4f25f40090bce7d80ff6eeae90b865443ddd56c2746380a71826420cb29466fff63f697f574bd51143eb201a61f8afdddfce871389826105bd0ebefb0dd01f1f3d844d7d179ec249daa756789d9e369596c79cfb2c5896c8c27cf20ec79dd7a1188eb1ea938cd22229e73c359cd5f537acd02bb843cbe2100cf36a8212d3d2fca6737ddea5f9c99859280ca407fe879bd0b6adaf5f37d91d9c629f214235a4d92942a5e4dae6e710406c175aab3b39aadf792343ea9716ce975dc256852d80ab88c6bc03f89095e9915d863fb29346950bd40af6f0e363ac908d26ce6cfe87a4d20674b7528df0e80a2490417b73d9808a53780409e7e8d39025ecfd0ae7836ae21b934a3b09a9e8aa3fb10532f1640d987779d502cf86d0035feb1c39b9e0eac58f27b29bdebedd2a3af0415774955d28788481c89c954843b89d3e2db9da774fde76b661f37534685ae28bda52455c077cebcfac901da021e6fb10e6627e41bb719424ee6b51f90038fad9aca3fe4329cd1b0d566f609301abb3ff88b1a5ed4d1129a7bc088bd9fa1da88be439a39c291f5accd9ada308599e46f333d2d3cf25335a5b9421c9709556df3f4f6a3a8c7ca708b412b64dac7cb0452d47dcaf4f3a71feb13b6ae5a9c49c071c622a1793312346739fdbf4318e0fb2149c2f83181c3802c8df9ee0ea14404c3a3ccf40afecf3ef18976c9fa274b946162fbf9f4dd0de764874a969520337fa034a69ad55ba799f6c32171526823430ab1bf79a57af74c4c775760761942b430b49618bd9127d06fa9394bd4bfa2efe9a3ce740a7c0da66a1b13ac1f64a1db5ddc28ed29253f4e3b7fd64b3ad2d95a4fb342d8e9335e42bc186736b72b9fc6cecc3faf0566d60222b95e09cbde3cd47079f0bc14a35d48d18eb30ffd45c8ed844f897aa0723f25ab54b8268af927d604257325457347ac849dd97af2fd63dcb1807977d9ef9c0496b3d9717e7d36cf4f9f7e0d3fd5a251bcffb643693f9b4d9448c902ab029a1ca73319ef87b98e45f94c7869f3207a6e825a26b93a0c7ca40dbd616e60f039b420359fbc598e70f0683c214338316327e904739963c6448c9cadef52331d52755a26cc820cd5a73a106a2467b4569e906c11798cbd0cecca0b9400a64a7268904c5a2d9c4c22410e80393f3c29293c2bcf26b20a38cf31432019eae0d0eb60cf70350e1dac095ce8f55f65928ddb633ed04d9a82c4ea53311c7d3405da89e1f13010565be8c3ad16371e93feeb846d7b4e8b1b49b5164814f59f9943ce36000f08049a8b782637356df3d5d4f1c04007b3ae1700256903a5fc72b3efdd23ad74200e37ac74eb98ff6add09c0d83429722697a8155e0aa73c8a626b83897c516240241c981d554190700992681d1c80269a27474d762ab817c71652d35ca9a7563ec911e138a29412b690efe7c6d17b1b2b0aa4a23de2599015c1fe0784bd44614fe498b8204928531e7944083bb0c01196770ce0ee7752f539b9f876c9660c821694daee5d100008cb76e2dee919227deabf735b4ba5fdd0b5ff6b26cab9d03689fef2884ff3993171a8718d906e872066144458315f6c7a1178d4e50e55b6a059e8fca900e99a7bd54530f071c01fd7d92367de76557275a0dccda1241d96dcab684719d128217551df2e593ebd75f5c58f4f8a6b415dc60f13f639ccec4987b26751a53d9d065ccc7e3b836bb3f4ed974060d4ab5708473665bdc7b3a71f9df4ef88a946253b83bf7ccd999c14015b717a60f0399f85e4f499b5e811c26b8aac1820afbdb4e239f290bef1e6eca90f36d58b85722c29de40d3bb4bec875a8861af7b553181fe4139b01f9ea12e0dc5a32195766222e23add937580fff4fbec96e817c0fd8c717b898d115be1946fef895cf663fed351fa8196261cd60ba79fd5ce01abed4b1e0ee78123e95756f2850dd63b19f2bb50f611dd8f1d2eda7cdbdc929725f1c9106f6ffda10cee89974140caab66a2b315f6cb609b090dbbfd2e52f4fd6a"
            ),
        ),
        proto.LiquidBlindedOutput(
            conf_value=bytes.fromhex(
                "08cbb1068fcc876832b14633b9d048a678398abe4a10b0497f8351810a3fa2046e"
            ),
            conf_asset=bytes.fromhex(
                "0a37c228ce75c9d15c9a45b39b837675705eed3f5fcd32681c7bd2b91019f35ede"
            ),
            ecdh_pubkey=bytes.fromhex(
                "02b7b6f81ad08e284922d8b0d7bb0f73a35e3fdfe97a91cad787f7bbfb416fa1bd"
            ),
            script_pubkey=BLIND_OUTPUTS[1].script_pubkey,
            surjection_proof=bytes.fromhex(
                "0100019da19bccf1d87248d87057daa99ec55b7ba44a76488f234f895f943419404631758c156ce2307e2f5d739da7356a705e820ccf730a812f7e01f471842fa5329e"
            ),
            range_proof=bytes.fromhex(
                "601f0000000000000001650ee4eea11efdb5c573ef9ddc478f2eddf6bbb71888169440bd59b5b121fd24ef0afb82034fa0f44e3e4d58c930588ef653b6224e75780efecee86e699bbf2f61101fd7cd65798fedd1cd0fe0d37e527cf16bc35de0845a4950a2b92c5eed80bf7677394e02b6c8d94ea80773c3c4943f08f863318cd1ae72239982496bb7cf60ffadc491ded73608b6d77c8ea103f425e5e2c9a60c52976d4c7544d34b04a7d44aaf07e705540e4c93c3eaea046f6c68b85feda7b90665265d167064f51c4160bead204bc70cbb0d0529321b7fb57295a4861bbfdf76cbad19613f27c1eec73015581f5b78f649769dd29f018d5ed7e70d9f292aef8b4ef9808de4d1905eee4cafc924e4b3a9047a8c6fd3988c366a09f384c75033e011acc5d3499f12b8953fda8770db8585ecf94d597657be65bd116c87ca7413bd177a28289ff616fbb9d937874893d4dce3041e06166278a6736b9ef9d02b1167febe34a49f63b9542f6c85394cd54523150edb0f88149209a726b28d3d713f06afb4685e52d69a813ccf405f77b212189bda14c3372dc67be1c2b0b426c06c54551084f12b8578eb4fde71f814822f856571360e139429c41a328b6e2f8f0adbc647e452af93284357688983618648cbf91a2cfc3ef444b66d1039318cefe1b5f7bf796cc2f3123c35a9c6d61a527a399ab5b471f6480230cc3ffe87cf538ea854f9c764f602b9e78ca1165f1f0604d58476696a3e9008f7971de5996c336506608a778c795c11049c5b59ce8c168e8ba97447ffa97ef4f6d691d35d069f1d3b6624ef278583dda1482943cad7bc773e37401621719b7f3e2db83d30b3dcc01bc047b999667e27b51fd3ab1e2f8eb2869935d8ba5202524fc42fa43a7c707a8593a6059cac75c597a7e59f0b814ac634eabef769fa0ede012af537c37879d0cb21d438211ac8c63f56fd79d3cb30310b93b5775710f093a3ae12a63a8e174b93faa0ef7d0e2173674f8a3125231ab4375e1561baf5c47d66f4e474f9a850112bf059d0e1970921e2b5cf1c9d2a228a848cc18bf4cf164a1ea2f92bab508cbae3e015cf00eb62299160f9eeb6b0b6f88e657ee627f79dad5800ed45c9040848a2538013ce06c155e98496bf21f839b1240db0b3a22c578ddebee5499f360bffc0b5072fd0a7324d1c5acd84591c85c9d2cbbfbc903a8a6d2c8a4efa5b9c20b0afa9110b153172c94e8d81ad8623fcda81c744ecc9dbb515b0e99e3fb9ee0684725a3436a40f1bede7af446698afbc05ff798617c92c8815118383a0e927d408cee3bd089be83211d50d1aa537994e7b880c3fe8f8814070b3e05c22ea6204741120bed5f11ad035b3385fea4fbd2bd1251e1665a619495ae391192d0207a32aa5d469f0842dbacd5e001df713f5970b5dce5d6b14a2df0a0f6609d761df71c14c4b1905d052a2504484d31d11b2495899d568a7da37ea148c72fc0d70e8f9eaea2af99984d393e82d52dfb095463ca86832053acb674ab185856093db4df438e9cd1fc6fbade65340436029dac8b0f57bd36d995f684892141949bc5e158e7a86eb61eedc826256eed0eb133293f267e9383cc49637beaf1fc1dd9c01de2d18e6e4c0f675db25443efcae0c87656c82a217066ae1d9677cfafc6f301681046520663e00c0d2f9b7f73d5249ae43de5bf62aad291971d8144deef5a998ce078f65a5e6de3868f2d77fcc1aeebd622c06d836d4a4a65668d887a075d4495fc08dba45737b17e19f9cfd02d8f464da450d309ad824de6f472467b768dbad6eb88d2f77684925c239188542dec82996be7505bd1d3586b3755179db40aaf697af277afa5bab75d6070221ba360ff287a4ecf92e915c70108705116d8e9e698e3682746b8093ea264b181d3f114d9b1c9e5d51eb0d8e2c17db7d6bfb6e9eeb1363c1e4c1563463321ffc069f426adf16639f4bc1ef2fe912a91db0f7070d75b79df26f62598494ccae43fb2a7298901fa14e05a65c99307b4b67fdbe384e2b0ee48ebd13d79fbafd282f0d650b1f7c23a762f1061f01548107c7af0121263e80658e404128026da68cb13f161488109adbece97c9989f9b41d3d9fc33e875337e5e2f71132fae271dc48d7a66697b77fc615c2e67c2b67d7e4da1cbc534a44b34494bb140e83223f12b1c09689d16dccedc4a07e829783953bc4b93ae9915efab3408cb8516e8f40323d4bf7e4a496c38f1bf5890308c51dc727e2e4a1fd5b50b86c96f5f17e3d4853a13d65bd0e37231082c8cd235a768a538e6beb12049cb9b722e9e9476eee3b4c360c087d4265bec0a07aaf31f10d1c986a9255378a53901a9ed574f537c6bb169c8e6514cce019edd322c5b0952b91f64480d35271fc7ff234d21d7345961071bf22d0fe3e11ea4059365ea9c4b0020146f08647e539bb1f36b554d201215653322abb4a8d42c004b298b7d583165038c436aa7ac04d4e7897e0d2b7adfdcc6b1f7babc364bd94870790755c28543723e2352cf3bbd6b8a4d5e871be37f646913ed3d0e6fadcb24d21e9cf0900ed12de0331e3e229a5ddcb3998ae275b212a2aaf4ba66599f6ca4ea6b794b5de0d854d309f5cb95f94f79906cac7e0025d17cea9d4fbec6d24140c37d25cd0d0a11aa2b3354bb556b0b5a9bb729b70f4e8c6fa9d600ce351e971d4f10923e466e59a057dc8c6799b4930129f68c20d4c0c77b4245731be57bd246006691947d0f3425d89565b07933c5ef3166cf5071a84d50de0fef8d9bade6a6241bdae6556cfc2d1d0746ea16939a67d54f7fad9eb1c4dbb0737aaec1b33f8b21d850a4d4f87ca856207e92a955ef2a0c739d3b3166241a4f685768ef41fd144ba86bbc8cb86e2273e7036fa2363c2f4fa32bba7d8f9f752f78ba14aec3e9a8d01e75ff6d063c5943e5c5161443b820231694ff9ce6b3b653018811993294bf649d2923de56c97ee0db6174403106697e89be94f6b8c3fe35556dac5db628bc6352d7ebcee65253330f500c25fa2b0b2d18d5f38a604a55a909a32bc3dd1626b49709a7b05664803a202b69689f0c5bfd4cc12aacea031fd34f6968d6ca0c486ebccdea84f6539afe7ed5996f17810de174eed1f982d3b762cac9402c8c7b6f8590205ba755be5be59c56678ded05a9557c3311cbb582330bb8d754c8b33611334260530513293131f6ea47c13df19a6b56ba2a34f2ba6681aa1615b42178ef3c47cf7a6ced4befd36c49a0f198b8224628dd59c0aaa23417a372cfe6b1735fa83ed8e7c6ab09f0699522fb8e835182975d3eda1d84fcf954ee88df040a8a4ae325eec23ae853e0607289674e333ec7db2c14f187d9ba6d858f45e4a44831780acaed228e7c125b288047188c141dced7b54298ab2a898eb23b85a782ca7c323c46ddfa81a1e7cad96eba3e4ceea3a29fa8f37d09bb7d19b8bc2ddf589edfb999b17f6827481f893bfef44aa46adc82758138bd21b4a18b6430406eafa0969d551638f3a2eaac5308f967377b38cf20b79271cdc9d26fde8a5d6e47db2e33a7b71351731be52d29710474b56f9e0240f30d917efd72fed3f496663a97428ea2ea7263a37e4b718f6a5f0a29844c54a002ef1333c4d61e3adb8751a3ffe"
            ),
        ),
    ]

    UNBLIND_OUTPUTS = [
        proto.LiquidUnblindOutput(
            blinded=BLINDED_OUTPUTS[0],
            ecdh_privkey=bytes.fromhex(
                "8ba892ac8508abb576daab4f966c3ed3832cc4284b4632749c1ee496d9dfe6db"
            ),
        ),
        proto.LiquidUnblindOutput(
            blinded=BLINDED_OUTPUTS[1],
            ecdh_privkey=bytes.fromhex(
                "6527f295b57d3788edbfca7a911da6d62e1238946736d47ae04c714502b409d2"
            ),
        ),
    ]

    def test_blind(self):
        self.setup_mnemonic_nopin_nopassphrase()

        blinded = liquid.blind_tx(
            self.client, inputs=self.INPUT_AMOUNTS, outputs=self.BLIND_OUTPUTS
        )
        assert blinded == self.BLINDED_OUTPUTS
        for i, blinded_output in enumerate(blinded):
            _verify_range_proof(blinded_output)
            _verify_surjection_proof(blinded_output, inputs=self.INPUT_AMOUNTS)

        _verify_balance(
            inputs=list(map(_blind_amount, self.INPUT_AMOUNTS)),
            outputs=(self.EXPLICIT_AMOUNTS + blinded),
        )

    def test_unblind(self):
        self.setup_mnemonic_nopin_nopassphrase()

        unblinded_amounts = []
        for i, unblind_output in enumerate(self.UNBLIND_OUTPUTS):
            unblinded = liquid.unblind_output(self.client, unblind_output)
            amount = self.OUTPUT_AMOUNTS[i]
            assert unblinded.value == amount.value
            assert unblinded.asset == amount.asset
            assert unblinded.asset_blind == amount.asset_blind
            if i != len(self.BLINDED_OUTPUTS) - 1:
                # Last value_blind is updated for balancing the commitments
                assert unblinded.value_blind == amount.value_blind
            unblinded_amounts.append(unblinded)

        for i, unblinded_amount in enumerate(unblinded_amounts):
            c = _blind_amount(unblinded_amount)
            assert c.conf_value == self.BLINDED_OUTPUTS[i].conf_value

    def test_unblind_for_me(self):
        self.setup_mnemonic_nopin_nopassphrase()

        unblind_output = proto.LiquidUnblindOutput(
            blinded=proto.LiquidBlindedOutput(
                conf_value=bytes.fromhex(
                    "09b28ea8c906ee2ad38f5bc761f0a7e3d9415e2d65f982ae56cbb2f0785c37c03b"
                ),
                conf_asset=bytes.fromhex(
                    "0a0f32794e865d649de7190109c93fb784c4197ca0ec14d80deb7f45839c889949"
                ),
                ecdh_pubkey=bytes.fromhex(
                    "026f2ceaf0187c894c69d30809252f597da1c59270d2a0ddb2f7528dacaa5762fa"
                ),
                script_pubkey=bytes.fromhex("76a9143a56a008ea50c69036f345a8b274b35bb156329288ac"),
                surjection_proof=None,
                range_proof=bytes.fromhex(
                    "60230000000000000001bd7300558aba88fa8c9191af365570da78f3b308a506d62c044210072fe37cefbd723cdc4159f9e927119b8e9276fac238f737f9ab994159bf0a5530a50225272edd79d19afba9fc833cf2037eec925b69bafd187d2593480037d5cc145cdb5933f1b8e362b8fed30c46ddde57c7b8913d2c1538cbedf1ec2465fc401dbd973a4cfee4f5282d2c059ccb0df8198f92054012122036d19f005a2078bfa7c7219d6a270db55ad23c26403db81afc5c35b69e1a1f62be1753f8d0681f4168ba301f1806302fa78244a32f00ef9d062910c434472fdfe5560b60dc1a50103a9f77fe9dd2dd7e43181a99cba959c1f8e9dccb348f23f349ed08a0e0bfd439ac61191b11f4aaa18762a8a4154c0a7a278cb080e7e70e3dcd299e2e431d83d656f45437284827ecf4ccd92ef830a84fc7d7a9c4a167b665a700e0a13533e4ef78a6586518a3298ce31897cf537988fa8e7dd3931ae9f6fa4045a45eff9d631c18a97d0fb8522a0a9c5b530f4bfaa4bbb4feab397ff0c09aebd2650f8753f43c5b6bf75350f345171c51348f5a2453cbe787b50ac9efa319334a474f19c0492c0851139da054fb65c7006eb5828002b1185babd215abea33ec95fa9ffba38b6abb7022995787f30c36ffca9e738dd1fdc406e56878611819d1fdd63b78646550b3e9045b50aa2d09a76fcc8cd4769d3c666db87b86fd107ea5feae5ff0e5987f65632e4d046afd7889657ac6fdc527e8440cc96917dea13c87136c320da46fcfc935396894f93f6fdfb9d7857c8331ec1fb4bdab197b1c7356969ff6675db2a3eacd07b30d940a7a5cd150e25d3a0f4cb353b62fbe07018d9af36be0c1bb1c1e8a149cda8d497e83c0e2d76e235c563e73a8a8953fe031a56590f8c0032536f69d16dca55c75819aa3d6cb8923f77ef8d816a00370602668f81c40ab28ea23de26a1fd35e34820b1a4c4e7fe78b2aa85d52644f67ba0a6cdc94158012a340f591484e9b03ecf01352c89a266ac74114e322f1a084e026dc8989e05885150e932a1d2d122afc9d05a92a5728fe6d7d6889dbdd8a1c6030f6fc1226a0f64e3228280ed69ffed74e8f1bccd484622f52e15f1810c624e7af226ee37203be9427a76de048aa4c65d8c2d1c19928f5f9ff1cbbe176b8a12980197bddbd89da00ca18d5b6336d87673b42a49308c01219faa40fb1064ad7167a4c53a8ce3705fdaa10457d29ed6d8f713ddca2a5a74a46d31b2b0d9b2977744fab09144da33cc6d5afff0acc37d2737b42250180a1514f3704ab761f635cb0ba80584e771edc701ab4e6a111995f307767111adbfbbd40afbf8b338934c309ec432d58ab43d1bba6a04086abe3a709a7f131b647434d47d71662d799690b81de570e4c8820d7a8716bd5ac5dee7020f7e4b754e68a55be00b3c4cb4dc6834fd0d6b1606fdba818195344ce1309645b9da4c15ea533501421d3011ceb369655ce6a7f231a5ff61847634577813ac6bf0d3392686c7cf64ce423ab24b5bb0f0f83d749516d8984b2e7b6511be76169299b5b6ff2b9887c3a3fd2ceea9c26c4b5b399d814ed1fc07dca178ce3424e9779f9a00450ddeab82c3862dbd7551e68e3596b0cec65a395ed60375f93eb6ff695e9a42e9dc0dedbb6fa90736a83dfb00557e7fe4123d0c44fe9c7a2d93752a5ef0e49021cd2b34fb359d7a791766ca7f430df4ca9fed20869361e3f540364437529adb7366af4d09cf6b230860dc9793bd3f379cd4eed774572df15bd92522a81c1d93447d504e0f7dc0fdcb3303c75174a72829c5273470897fbe1d7387d4f382161ca264ac57cba85c517936de575c54d594b875227bb51e7fd932aee8f3490dc8f2c07766ed7a35735b8ec537ccb278bb32308615420f987b3f21504c683f082c780fdae69b33156e66fbe2a2aeed0e4bad9d1a731d618158f26d154f084f409f86cc144e14f5ce273e24465ebf8ea613e0fdf282caa2a0e9bfa1c0dd47868144aaea4345d3a0e28420f47e877ccf7ad1922121d0479db804269fd571245fd99531f6fda2ae91b6cf0510e73746c4335aa92f06687ed9014b9e4d0d94fc02f704fd366c7001e9621ad3376052f01f1f85d92570fc4cceaafe90e9b169311f32f5981abe26267495a9800406d57d30517d743ac3cfa9185f5145d67eb3e1a4a3cf805e141d30cf895ee7b7d69e267e001a64006e77e52bd6c327d552cdcdada89a4fd74066f592e27ac07a0143d5610d884818bb75deadf43633ecfa35f847b0ff8cd7290a2ecae3412792477ee285b487e74e9da70b627b21afcabb039ea4c4eb41b3fcceffea517389a0fb52aeb72f085dbe43307b5cfbf2f9793e4ff3e1455b60e27c589aff5db95f2881c14c12e8b2e8ee20f486fae9adcb8f9cb7f1bf772ec202d5c599fc6b93d7e480e9f3d9fd3749104fbb4c2ef1e54e34ee152fdf4f5231f51ba1d6d06f716650b03b8e6f3c4698987e36e55cc82be3e02222accbafe67894ece4f0d093e84e6a81f5d0014397e723f221f4b92994006507466576b9a94d2947b8fab799e0e307d09802826b05788fb18cf13df2722fe1473994815960640d265b943d91914a4718f020c8a8f347f19c032414177110ee76f42b36e5e85cca19404c1d2faed7a26e80708720ad19a330bacf2a7d1bf777addf5e9138534f3a0a7586ac99d2dd261d39b4a949c39752e0a8f9a01ccf08b1de25b460f02e3e9c35075d7721ec49540f71d804ca11970444815e858218d09b19269609e225082638cb319eb32a8954c81d17c6b7bf2e9367771da582659a9a7040cbbe59f4679be9dcf670722f47cd0ac6a3b88b1cc92a5fe8fc63898930f32359e01311b9018ef05448c8fe60b42f416f2d45ba85d7dd2169e33b4af877860382af1910132bc9a1098bcb0fdcce5ec21db54cae52be7ef0b3babe32f44cbb4ba381e83476ab2e1810dfe74f5a0aac280e6fc6511c09c9e578a4736a2cd2a1b727048a3611dd5e9595f0ec9b128331d9fd93439ecd92dbc4b92065bdc1c0198d88bf46efd389977eac133c3d04477fed528dbb25c4eb0cbf5fce6bcb524748d6e9a426bdfa5355e9af3534b75c1022bb1adc005206d781b8234e80564f1ef2d99aa3e385a8939671ff0b22abd67408b3a85e86348287f2e9db64bf344881905c99e816074bf4472d7ed9f0c9c109b6795693ee71d27c6dd1281f7d8d210f203785578f350f8e7a6691cf7f1c6c08c5015eca5538b4a35f61641b5fa7e1db13a1edda55b55e3e068705cb23e649b600fd0bb7161f7831f55b44629abb40c434791c600fa51a41ff291fd061496f23b9791af1772cd8dcd62ac863bd2017b1befabf8d16462f00969ddc13a3d9502ddc2c96609a15e0c6fc3ab6fa236d8d39796517cab31835caf49284e9ccae627b042f22dacbb68e738099bd8a415082fd5dcdc4ceba70b342d25fe07b36e4445ebbd2c390db7dea0b0e52d878b766689f3544516ec294abcf9520b74f76f86628673fcf94bba95f809ba24ca4295b9bb6c8fac4e65c9871335f5097ef025d5a6ca69b6fb5f74dbe9a58ae08e3250456f94b245be68e5559a972cb8e16d476fb1d5cdf5a227eca3637829b86e9da01d62448e27253b8844db59beb3624daede185163310cf91aa54350fe3a5cafd23725e7680d33e4452e3f749990aafccc6f67b4af626f0431dcb5a2ddc78a7e7355b25307c5cbb21dd2eb4c30c42535f80899f9291a1fd66b479d89f660c23ddfb75896454ad8b2d3a2b90316b6600dc978d3a3f277c1f7eb27eb783a39334a2c05cbe09869f0570cb9b3fbb0c630527baf69cdbbc81fa774d2436c77d9ca1e2b0f7e952471f70a97108f37bd794b601a0f1a9a34a603dfbd932c977fc703e21120bb1411b69833434f393afcf547c11d72d2714cece04efb3dbf02bfafe677d4e7727ca01c4e4629ada78970bd597cfb6838ac8fe6774a60436bf3371917783fcb21a06bec89beb2866f468f63536b2f1afdd93f07ef94085492e42385a8d59c2c817ce5e1bcc8a14625fe529eec799d1cf6f7d75f59e1a229bea9cb082b203ab7117bd1f9efa27bdac"
                ),
            ),
            ecdh_privkey=None,
        )
        unblinded = liquid.unblind_output(self.client, unblind_output)
        assert unblinded == proto.LiquidAmount(
            value=10020000,
            value_blind=bytes.fromhex("58cbf3aeee7976e0b1933a6ac063635aec60a4e7c8de141b8e83f325e82e40e2"),
            asset=bytes.fromhex("230f4f5d4b7c6fa845806ee4f67713459e1b69e8e60fcee2e4940c7a0d5de1b2"),
            asset_blind=bytes.fromhex("6b501a727daac45b0d130b6044348c6cc8d55c1dc0da8b51bea13a3131548860"))


    def test_get_blinded_address_pkh(self):
        self.setup_mnemonic_nopin_nopassphrase()
        addr = liquid.get_blinded_address(
            self.client,
            n=parse_path("m/44'/1'/0'/0/0"),
            coin_name="Elements",
            script_type=proto.InputScriptType.SPENDADDRESS,
        )
        assert (
            addr
            == "CTEoGBnb8SmWgM5tgyfWMqbReCQZNXHubYoVtMbYMDb4u5vBMbPoAhcWgJty5kPsygDYTJZR1nkDSHa1"
        )

    def test_get_blinded_address_p2sh(self):
        self.setup_mnemonic_nopin_nopassphrase()
        addr = liquid.get_blinded_address(
            self.client,
            n=parse_path("m/49'/1'/0'/0/0"),
            coin_name="Elements",
            script_type=proto.InputScriptType.SPENDP2SHWITNESS,
        )
        assert (
            addr
            == "AzpvjySCSPyqppx1FFTFWZF9X7gJmxNfXv1z3W8mQgZYHw9qucPJhgXJjjBzLr3h2ejDTjpYUG2G86kH"
        )

    # TODO: check output surjection using libsecp256k1
    def test_sign_tx(self):
        self.setup_mnemonic_nopin_nopassphrase()
        sign_inputs = [
            proto.LiquidSignTxInput(
                prev_hash=bytes.fromhex(
                    "110a761d119f0919c3c60e223a477948c6c6c4a020a46b818fa05a53201e11bf"
                ),
                prev_index=1,
                sequence=0xFFFFFFFD,
                issuance=b"",
                value=bytes.fromhex(
                    "08178bd3991e333107346f26b52a27f441b43b70f45e8f8cdf20df59897cfc077b"
                ),
                script_code=bytes.fromhex(
                    "76a914ec1d316f5b03870be2dda1df3c15876c414c958988ac"
                ),  # -> derive on-device
                sign_privkey=bytes.fromhex(
                    "aa902fc9df6a07f330dcbb2d303544a91e58d88a5d1760599b4b72719d240e22"
                ),
            )  # -> derive on-device
        ]
        sign_outputs = [
            proto.LiquidSignTxOutput(
                asset=bytes.fromhex(
                    "0a85e434f59be44088e971c1e732c646e3acf6201d4306087e2745eec2d69c4714"
                ),
                value=bytes.fromhex(
                    "0880b90389f41f30152a8c6478dbebcb174f0040af3c2ada1d3bb18e3e9d4e5a8a"
                ),
                nonce=bytes.fromhex(
                    "02ebbcfb668fcfbf91d8c505236dbfb28a24baf7fef42138f4109d47912b9f7f19"
                ),
                script_pubkey=bytes.fromhex(
                    "a914568171b717ea909b9d64bf6c96bf77d4be47ec6887"
                ),
            ),
            proto.LiquidSignTxOutput(
                asset=bytes.fromhex(
                    "0ab6f751be3ba9b69fcd94907a41c24d2700b910a3292deeb91ca17dd0a851d112"
                ),
                value=bytes.fromhex(
                    "091d571f498f3865ef359b8ab6d9133d5152d8db0087c3bee995b7c56fcff3496e"
                ),
                nonce=bytes.fromhex(
                    "0225765310adc82c37c9552815a5cbc8f2a4e200c32be579167d953a5ff187edc3"
                ),
                script_pubkey=bytes.fromhex(
                    "a914092edbd0a602e8464ce37b97b74a0151f01ab57a87"
                ),
            ),
            proto.LiquidSignTxOutput(
                asset=bytes.fromhex(
                    "01230f4f5d4b7c6fa845806ee4f67713459e1b69e8e60fcee2e4940c7a0d5de1b2"
                ),
                value=bytes.fromhex("01000000000000aa50"),
                nonce=bytes.fromhex("00"),
                script_pubkey=bytes.fromhex(""),
            ),
        ]
        req = proto.LiquidSignTx(
            version=2,
            inputs=sign_inputs,
            outputs=sign_outputs,
            lock_time=303,
            hash_type=1,
        )
        res = liquid.sign_tx(self.client, req)
        sigs = [
            proto.LiquidSignature(
                digest=bytes.fromhex(
                    "dbcdc4287f3ffeaf33dfe8d7238383502bbafd702d3b41b92fdc47e83982ff0c"
                ),
                sigder=bytes.fromhex(
                    "30440220292cf66c5ea9e7efb39a396f90ad6b638adc3e34e68f8af2ede74f6fb7cf76bf02203610c1040f380f226619d059cdc64e4f74d5b7b19ff36ef3e1072df29caa91e0"
                ),
                pubkey=bytes.fromhex(
                    "02d1fc4a3a9c00e1b17b9f4af071aa8331e97218d96a44ed0069c224a054fd85cc"
                ),
            )
        ]
        assert res == proto.LiquidSignedTx(sigs=sigs)
        for sig in res.sigs:
            ecdsa_verify(sig)


# Build by:
# $ cd vendor/secp256k1-zkp/
# $ ./autogen.sh
# $ ./configure \
#       --enable-experimental \
#       --enable-module-generator \
#       --enable-module-rangeproof \
#       --enable-module-surjectionproof \
#       --enable-module-ecdh \
#       --enable-module-recovery
# $ make


ctx = lib.secp256k1_blind_context


def ecdsa_verify(sig):
    # Parse serialized public key
    pubkey = ctypes.create_string_buffer(64)
    assert (
        lib.secp256k1.secp256k1_ec_pubkey_parse(
            ctx, pubkey, sig.pubkey, len(sig.pubkey)
        )
        == 1
    )
    # Parse DER-serialized ECDSA signature
    rawsig = ctypes.create_string_buffer(64)
    assert (
        lib.secp256k1.secp256k1_ecdsa_signature_parse_der(
            ctx, rawsig, sig.sigder, len(sig.sigder)
        )
        == 1
    )
    # Verify ECDSA signature on given digest
    assert lib.secp256k1.secp256k1_ecdsa_verify(ctx, rawsig, sig.digest, pubkey) == 1


def _verify_range_proof(blinded_output):
    conf_value = ctypes.create_string_buffer(lib.SECP256K1_PEDERSEN_COMMITMENT_SIZE)
    assert (
        lib.secp256k1.secp256k1_pedersen_commitment_parse(
            ctx, conf_value, blinded_output.conf_value
        )
        == 1
    )
    conf_asset = ctypes.create_string_buffer(lib.SECP256K1_GENERATOR_SIZE)
    assert (
        lib.secp256k1.secp256k1_generator_parse(
            ctx, conf_asset, blinded_output.conf_asset
        )
        == 1
    )

    min_value = ctypes.c_uint64(0)
    max_value = ctypes.c_uint64(0)
    extra_commit = blinded_output.script_pubkey
    res = lib.secp256k1.secp256k1_rangeproof_verify(
        ctx,
        ctypes.byref(min_value),
        ctypes.byref(max_value),
        conf_value,
        blinded_output.range_proof,
        len(blinded_output.range_proof),
        extra_commit,
        len(extra_commit),
        conf_asset,
    )
    assert res == 1

    # TODO: free allocated memory

    min_value = min_value.value
    max_value = max_value.value
    assert min_value < max_value
    assert min_value >= 1
    assert max_value <= 2 ** 51


def _blind_amount(a: proto.LiquidAmount):
    generator = ctypes.create_string_buffer(lib.SECP256K1_GENERATOR_SIZE)
    assert (
        lib.secp256k1.secp256k1_generator_generate_blinded(
            ctx, generator, a.asset, a.asset_blind
        )
        == 1
    )

    commit = ctypes.create_string_buffer(lib.SECP256K1_PEDERSEN_COMMITMENT_SIZE)
    assert (
        lib.secp256k1.secp256k1_pedersen_commit(
            ctx, commit, a.value_blind, a.value, generator
        )
        == 1
    )

    serialized = ctypes.create_string_buffer(33)
    assert (
        lib.secp256k1.secp256k1_pedersen_commitment_serialize(ctx, serialized, commit)
        == 1
    )

    return proto.LiquidBlindedOutput(conf_value=bytes(serialized))


def _get_commitment(v):
    """v may be an explicit proto.LiquidAmount or BlindedOutput"""
    if isinstance(v, proto.LiquidAmount):
        zero_blinder = b"\x00" * 32
        generator = ctypes.create_string_buffer(lib.SECP256K1_GENERATOR_SIZE)
        assert lib.secp256k1.secp256k1_generator_generate(ctx, generator, v.asset) == 1

        commit = ctypes.create_string_buffer(lib.SECP256K1_PEDERSEN_COMMITMENT_SIZE)
        assert (
            lib.secp256k1.secp256k1_pedersen_commit(
                ctx, commit, zero_blinder, v.value, generator
            )
            == 1
        )
        return commit

    if isinstance(v, proto.LiquidBlindedOutput):
        conf_value = ctypes.create_string_buffer(lib.SECP256K1_PEDERSEN_COMMITMENT_SIZE)
        assert (
            lib.secp256k1.secp256k1_pedersen_commitment_parse(
                ctx, conf_value, v.conf_value
            )
            == 1
        )
        return conf_value

    raise ValueError(v)


def _get_blinded_generator(v):
    if isinstance(v, proto.LiquidAmount):
        generator = ctypes.create_string_buffer(lib.SECP256K1_GENERATOR_SIZE)
        assert (
            lib.secp256k1.secp256k1_generator_generate_blinded(
                ctx, generator, v.asset, v.asset_blind
            )
            == 1
        )
        return generator

    if isinstance(v, proto.LiquidBlindedOutput):
        conf_asset = ctypes.create_string_buffer(lib.SECP256K1_GENERATOR_SIZE)
        assert (
            lib.secp256k1.secp256k1_generator_parse(ctx, conf_asset, v.conf_asset) == 1
        )
        return conf_asset

    raise ValueError(v)


def _collect_commits(values):
    commits = list(map(_get_commitment, values))
    # Return array of pointers to commitments
    result = (ctypes.c_char_p * len(commits))()
    for i, commit in enumerate(commits):
        result[i] = ctypes.cast(commit, ctypes.c_char_p)
    return result


def _verify_balance(inputs, outputs):
    input_commits = _collect_commits(inputs)
    output_commits = _collect_commits(outputs)
    res = lib.secp256k1.secp256k1_pedersen_verify_tally(
        ctx, input_commits, len(input_commits), output_commits, len(output_commits)
    )
    assert res == 1


def _verify_surjection_proof(blinded_output, inputs):
    output_generator = _get_blinded_generator(blinded_output)
    input_generators = list(map(_get_blinded_generator, inputs))
    assert len(output_generator) == lib.SECP256K1_GENERATOR_SIZE
    for g in input_generators:
        assert len(g) == lib.SECP256K1_GENERATOR_SIZE

    n_input_generators = len(input_generators)
    input_generators = b"".join(input_generators)
    assert len(input_generators) == n_input_generators * lib.SECP256K1_GENERATOR_SIZE

    proof = ctypes.create_string_buffer(
        10_000
    )  # TODO: use sizeof(secp256k1_surjectionproof)
    assert (
        lib.secp256k1.secp256k1_surjectionproof_parse(
            ctx,
            proof,
            blinded_output.surjection_proof,
            len(blinded_output.surjection_proof),
        )
        == 1
    )

    assert (
        lib.secp256k1.secp256k1_surjectionproof_verify(
            ctx, proof, input_generators, n_input_generators, output_generator
        )
        == 1
    )
