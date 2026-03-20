_CONTINUITY = {}

def save(id, state):
    _CONTINUITY[id] = state

def load(id):
    return _CONTINUITY.get(id)
