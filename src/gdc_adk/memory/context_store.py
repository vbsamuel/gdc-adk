_CONTEXT = []

def add(block):
    _CONTEXT.append(block)

def search(query):
    return [b for b in _CONTEXT if query.lower() in str(b).lower()]
