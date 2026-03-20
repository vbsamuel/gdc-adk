class MemoryStore:
    def get(self, key: str): raise NotImplementedError
    def set(self, key: str, value): raise NotImplementedError

class ContextStore:
    def get_blocks(self, query: str): raise NotImplementedError
    def add_block(self, block): raise NotImplementedError

class ContinuityStore:
    def snapshot(self, state): raise NotImplementedError
    def load(self, id: str): raise NotImplementedError
