
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF

def _greeting(name: str):
    g = Graph()
    bob = URIRef("http://example.org/people/Bob")

    g.add((bob, FOAF.age, Literal(42)))
    # print(f"Bob is {g.value(bob, FOAF.age)}")
    # prints: Bob is 42

    g.set((bob, FOAF.age, Literal(43)))  # replaces 42 set above
    # print(f"Bob is now {g.value(bob, FOAF.age)}")
    # prints: Bob is now 43

    # message: str = "Hello " + name
    # return {"message": message}


    return g.serialize()
