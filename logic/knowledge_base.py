class KnowledgeBase:
    # todo: install prover9 or implement something similar with TELL and ASK interface
    def __init__(self):
        self.facts = []

    def tell(self, fact):
        self.facts.append(fact)

    def ask(self, query):
        return False
