from sync_chain import nbcrypt
from sync_chain.chaindb import Block, Transaction, BlockchainStorage

DEFAULT_GENESIS_BLOCK = Block(bytes(64), "genesis_block", 1561672701

class BlockchainManager:
    def __init__(self, path, genesis = DEFAULT_GENESIS_BLOCK):
        
