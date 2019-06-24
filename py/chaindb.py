import os

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
            if (not os.isDir(path)) or (not os.isFile(os.path.join(path,DIR_LENFILE))):
                raise FileNotFoundError("No blockchain database exists at '"+path+"'")
            # load the database
            with open(os.path.join(path,DIR_LENFILE)) as f:
                self.length = int(f.read())
            # loaded
        else:
            if type(genesis)!=bytes:
                raise ValueError("genesis parameter should be None or a bytes object")
            if os.isDir(path) and os.isFile(os.path.join(path,DIR_LENFILE)):
                with open(os.path.join(path,DIR_LENFILE)) as f:
                    self.length = int(f.read())
                    if self.length>0:
                        # the genesis block should exist
                        if !os.isFile(os.path.join(path,GENESIS_FILE)):
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
                                    
                    else:
                        # existing db is empty?
                        raise Exception("Empty existing database, not overwriting")
            # if we made it here then we are creating a new database
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path,DIR_LENFILE), 'w') as f:
                f.write('1')
            with open(os.path.join(path,GENESIS_FILE), 'wb') as f:
                f.write(genesis)
    def getLength(self):
        return self.length
    def getBlockData(self, blocknum):
        if blocknum>=self.length:
            raise ValueError("Blocknumber is higher than database size")
        with open(os.path.join(path,str(blocknum)+".blk"), 'rb') as f:
            return f.read()
    def writeBlock(self, blocknum, data, overwrite_ok=False):
        if (not overwrite_ok) and blocknum<self.length:
            raise ValueError("Cannot overwrite block (not enabled)")
        if blocknum>self.length:
            raise ValueError("Cannot add blocks into the future")
        if type(data)!=bytes:
            raise ValueError("data parameter must be a bytes object")
        with open(os.path.join(path,str(blocknum)+".blk"), 'wb') as f:
            f.write(data)
