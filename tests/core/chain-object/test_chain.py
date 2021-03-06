import pytest
import rlp

from eth_utils import decode_hex

from evm import constants
from evm.chains.mainnet import MAINNET_GENESIS_HEADER
from evm.chains.ropsten import ROPSTEN_GENESIS_HEADER
from evm.exceptions import (
    TransactionNotFound,
)
from evm.vm.forks.frontier.blocks import FrontierBlock

from tests.core.fixtures import valid_block_rlp
from tests.core.helpers import new_transaction


@pytest.fixture()
def tx(chain):
    recipient = decode_hex('0xa94f5374fce5edbc8e2a8697c15331677e6ebf0c')
    amount = 100
    vm = chain.get_vm()
    from_ = chain.funded_address
    return new_transaction(vm, from_, recipient, amount, chain.funded_address_private_key)


def test_import_block_validation(valid_chain):
    block = rlp.decode(valid_block_rlp, sedes=FrontierBlock)
    imported_block = valid_chain.import_block(block)
    assert len(imported_block.transactions) == 1
    tx = imported_block.transactions[0]
    assert tx.value == 10
    vm = valid_chain.get_vm()
    with vm.state.state_db(read_only=True) as state_db:
        assert state_db.get_balance(
            decode_hex("095e7baea6a6c7c4c2dfeb977efac326af552d87")) == tx.value
        tx_gas = tx.gas_price * constants.GAS_TX
        assert state_db.get_balance(valid_chain.funded_address) == (
            valid_chain.funded_address_initial_balance - tx.value - tx_gas)


def test_import_block(chain, tx):
    vm = chain.get_vm()
    computation, _ = vm.apply_transaction(tx)
    assert not computation.is_error

    # add pending so that we can confirm it gets removed when imported to a block
    chain.add_pending_transaction(tx)

    block = chain.import_block(vm.block)
    assert block.transactions == [tx]
    assert chain.get_block_by_hash(block.hash) == block
    assert chain.get_canonical_block_by_number(block.number) == block
    assert chain.get_canonical_transaction(tx.hash) == tx

    with pytest.raises(TransactionNotFound):
        # after mining, the transaction shouldn't be in the pending set anymore
        chain.get_pending_transaction(tx.hash)


def test_get_pending_transaction(chain, tx):
    chain.add_pending_transaction(tx)
    assert chain.get_pending_transaction(tx.hash) == tx


def test_empty_transaction_lookups(chain):

    with pytest.raises(TransactionNotFound):
        chain.get_canonical_transaction(b'\0' * 32)

    with pytest.raises(TransactionNotFound):
        chain.get_pending_transaction(b'\0' * 32)


def test_canonical_chain(valid_chain):
    genesis_header = valid_chain.chaindb.get_canonical_block_header_by_number(
        constants.GENESIS_BLOCK_NUMBER)

    # Our chain fixture is created with only the genesis header, so initially that's the head of
    # the canonical chain.
    assert valid_chain.get_canonical_head() == genesis_header

    block = rlp.decode(valid_block_rlp, sedes=FrontierBlock)
    valid_chain.chaindb.persist_header_to_db(block.header)

    assert valid_chain.get_canonical_head() == block.header
    canonical_block_1 = valid_chain.chaindb.get_canonical_block_header_by_number(
        constants.GENESIS_BLOCK_NUMBER + 1)
    assert canonical_block_1 == block.header


def test_mainnet_genesis_hash():
    assert MAINNET_GENESIS_HEADER.hash == decode_hex(
        b'0xd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3')


def test_ropsten_genesis_hash():
    assert ROPSTEN_GENESIS_HEADER.hash == decode_hex(
        b'0x41941023680923e0fe4d74a34bdac8141f2540e3ae90623718e47d66d1ca4a2d')
