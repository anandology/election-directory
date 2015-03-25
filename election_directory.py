"""Python Library to interact with the election directory.
"""
__author__ = "Anand Chitipothu <anandology@gmail.com>"
__version__ = "0.1"

"""change notes:
0.1: first usable version
"""

import os

def _read_tsv(filename):
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    return (line.strip("\r\n").split("\t") for line in open(path))

def first(seq):
    for x in seq:
        if x:
            return x

class State(object):
    __slots__ = ["code", "name"]

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def get_districts(self):
        """Returns all districts in this state.
        """
        return [District(self, code, name) for state, code, name in _read_tsv("districts.tsv") if state==self.code]

    def get_acs(self):
        """Returns all assembly constituencies in this state.
        """
        districts = {d.code: d for d in self.get_districts()}
        return [AssemblyConstituency(districts.get(district), code, name) 
                    for state, district, code, name in _read_tsv("assembly-constituencies.tsv") 
                    if state==self.code]

    def get_ac(self, ac_code):
        return first(ac for ac in self.get_acs() if ac.code == ac_code)

    @classmethod
    def find(cls, code):
        return first(s for s in cls.all())

    @classmethod
    def all(cls):
        return [State(code, name) for code, name in _read_tsv("states.tsv")]

class District(object):
    __slots__ = ["state", "code", "name"]

    def __init__(self, state, code, name):
        self.state = state
        self.code = code
        self.name = name

    def get_acs(self):
        """Returns list of assembly constituencies in this state.
        """
        return [AssemblyConstituency(self, code, name) 
                for state, district, code, name in _read_tsv("assembly-constituencies.tsv")
                if self.state.code == state and self.code == district]

class AssemblyConstituency(object):
    __slots__ = ["district", "code", "name"]

    def __init__(self, district, code, name):
        self.district = district
        self.code = code
        self.name = name

    @property
    def state(self):
        return self.district.state

    @classmethod
    def find(cls, state_code, ac_num):
        state = State.find(state_code)
        return state.get_ac(ac_num)

def test():
    assert len(State.all()) == 36
    assert 'Andhra Pradesh' in [state.name for state in State.all()]

    ap = State.find("S01")
    assert ap.name == 'Andhra Pradesh'
    assert '216-Narasaraopet' in [ac.name for ac in ap.get_acs()]

    nrt = ap.get_ac("216")
    assert nrt is not None
    assert nrt.district.code == "17"

    nrt = AssemblyConstituency.find("S01", "216")
    assert nrt is not None
    assert nrt.name == "216-Narasaraopet"
    assert nrt.district.code == "17"

if __name__ == '__main__':
    test()