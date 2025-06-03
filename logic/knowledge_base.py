class KnowledgeBase:
    def __init__(self):
        self.facts = []

    def tell(self, fact):
        self.facts.append(fact)

    def ask(self, query):
        # Stub: return False by default
        return False
