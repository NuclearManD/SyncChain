import os, time
from sync_chain import nbcrypt

# chaindb.py

# module to store a blockchain


# name of the file that stores the length of the chain
DIR_LENFILE = "db.len"
# name of the file storing the genesis block
GENESIS_FILE = "0.blk"

class BlockchainStorage:
    def __init__(self, path, genesis=None):
        self.path = path
        if genesis==None:
            if (not os.path.isdir(path)) or (not os.path.isfile(os.path.join(path,DIR_LENFILE))):
                raise FileNotFoundError("No blockchain database exists at '"+path+"'")
            # load the database
            with open(os.path.join(path,DIR_LENFILE)) as f:
                self.length = int(f.read())
            # loaded
        else:
            if type(genesis)!=bytes:
                raise ValueError("genesis parameter should be None or a bytes object")
            if os.path.isdir(path) and os.path.isfile(os.path.join(path,DIR_LENFILE)):
                with open(os.path.join(path,DIR_LENFILE)) as f:
                    self.length = int(f.read())
                    if self.length>0:
                        # the genesis block should exist
                        if not os.isFile(os.path.join(path,GENESIS_FILE)):
                            # but it doesn't?
                            raise Exception("Invalid existing database, not overwriting")
                        else:
                            # load and compare
                            with open(os.path.join(path,GENESIS_FILE), 'rb') as f:
                                # Is the genesis block the same?
                                if f.read()!=genesis:
                                    # Nope; incompatible chain.
                                    raise ValueError("Existing blockchain database is incompatible")
                                else:
                                    # yep; we can just load.
                                    pass
                    else:
                        # existing db is empty?
                        raise Exception("Empty existing database, not overwriting")
            # if we made it here then we are creating a new database
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path,DIR_LENFILE), 'w') as f:
                f.write('1')
            with open(os.path.join(path,GENESIS_FILE), 'wb') as f:
                f.write(genesis)
            # make sure to initialize with one block
            self.length = 1
    def getLength(self):
        return self.length
    def getBlockData(self, blocknum):
        if blocknum>=self.length:
            raise ValueError("Blocknumber is higher than database size")
        with open(os.path.join(self.path,str(blocknum)+".blk"), 'rb') as f:
            return f.read()
    def writeBlock(self, blocknum, data, overwrite_ok=False):
        if (not overwrite_ok) and blocknum<self.length:
            raise ValueError("Cannot overwrite block (not enabled)")
        if blocknum>self.length:
            raise ValueError("Cannot add blocks into the future")
        if type(data)!=bytes:
            raise ValueError("data parameter must be a bytes object")
        with open(os.path.join(self.path,str(blocknum)+".blk"), 'wb') as f:
            f.write(data)
        self.length+=1
        with open(os.path.join(path,DIR_LENFILE), 'w') as f:
            f.write(str(self.length))
class Transaction:
    # decode() will convert Transaction->bytes
    # decode(bytes) will convert bytes->Transaction
    def decode(data):
        if type(data)==Transaction:
            return data.pub+data.sig+data.type+len(self.payload).to_bytes(3, 'little')+self.payload
        if type(data)!=bytes:
            raise ValueError("Must give this function a bytes object.")
        if(len(data)<132):
            raise ValueError("Transaction cannot be less than 132 bytes.")

        # Extract the block's properties first
        public_key  = data[0:64]
        signature   = data[64:128]

        the_rest    = data[128:]
        
        # check the transaction signature first to make sure it's legit
        if(not nbcrypt.verify(the_rest, public_key, signature)):
            return None  # It's bullshit!

        t_type = data[128]
        size = int.from_bytes(data[129:132], 'little')

        if size+132!=len(data):
            return None # wrong length!

        return Transaction(public_key, signature, t_type, data[132:size+132])
    def sign(payload, type_t, prikey, pubkey):
        if type(payload)!=bytes:
            raise ValueError("Must give this function a bytes object.")
        if len(payload)>2**24:
            raise ValueError("Payload is too big!")
        data = bytes([type_t])+len(payload).to_bytes(3, 'little')+payload
        sig = nbcrypt.sign(data, prikey)
        return Transaction(pubkey, sig, type_t, payload)
    def __init__(self, pub, sig, t_type, payload):
        if type(payload)!=bytes:
            raise ValueError("Must give this function a bytes object.")
        if len(payload)>2**24:
            raise ValueError("Payload is too big!")
        self.payload = payload
        self.pub = pub
        self.sig = sig
        self.type = t_type
        
        
class Block:
    def decode(data):
        if type(data)!=bytes:
            raise ValueError("Must give this function a bytes object.")
        if(len(data)<264):
            raise ValueError("Block cannot be less than 264 bytes.")

        # Extract the block's properties first
        public_key  = data[0:64]
        signature   = data[64:128]

        the_rest    = data[128:]
        
        # check the block signature first to make sure it's legit
        if(not nbcrypt.verify(the_rest, public_key, signature)):
            return None  # It's bullshit!
        
        last_sig    = data[128:192]
        extra       = data[192:256]
        timestamp   = int.from_bytes(data[256:264], 'little')
        
        
        result = Block(public_key, signature, last_sig, extra, timestamp, transactions)
    def __init__(self, pub_key, sig, last_block_signature, extra = bytes(64), timestamp = None, transactions = []):
        if timestamp==None:
            timestamp=int(time.time())
        self.timestamp = timestamp
        self.pub = pub_key
        self.ls_s = last_block_signature
        self.extra = extra
        self.transactions = transactions
