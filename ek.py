#!/usr/bin/python2
# encoding: utf-8
"""Encyclopedia Kerbonautica

Launch library and vehicle/stage/engine database."""

from datetime import date

class EngineFamily(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty temporary hack for testing

class Engine(object):
    def __init__(self, name, family, description=None):
        self.name = name
        self.family = family
        self._description = description
    @property
    def description(self):
        if self._description is None and self.family is not None:
            return self.family.description
        return self._description
    @description.setter
    def description(self, value):
        self._description = value
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty

class StageFamily(object):
    def __init__(self, name, ef, description, engine_count=1):
        self.name = name
        self.engine = ef
        self.description = description
        self.engine_count = engine_count
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty

class Stage(object):
    def __init__(self, name, family, engine=None, description=None, engine_count=None):
        self.name = name
        self.family = family
        self._engine = engine
        self._description = description
        self._engine_count = engine_count
    @property
    def engine(self):
        if self._engine is None and self.family is not None:
            return self.family.engine
        return self._engine
    @engine.setter
    def engine(self, value):
        self._engine = value
    @property
    def description(self):
        if self._description is None and self.family is not None:
            return self.family.description
        return self._description
    @description.setter
    def description(self, value):
        self._description = value
    @property
    def engine_count(self):
        if self._engine_count is None and self.family is not None:
            return self.family.engine_count
        return self._engine_count
    @engine.setter
    def engine_count(self, value):
        self._engine_count = value
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty

class LVFamily(object):
    def __init__(self, name, description, *sf):
        self.name = name
        self.description = description
        self.stages = sf
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty

class LV(object):
    def __init__(self, name, family, description=None, *stages):
        self.name = name
        self.family = family
        self._description = description
        self._stages = stages
    @property
    def stages(self):
        if self._stages is None and self.family is not None:
            return self.family.stages
        return self._stages
    @stages.setter
    def stages(self, value):
        self._stages = value
    @property
    def description(self):
        if self._description is None and self.family is not None:
            return self.family.description
        return self._description
    @description.setter
    def description(self, value):
        self._description = value
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty

class Destination(object):
    def __init__(self, name, abbr, description, category=None):
        self.name = name
        self.abbr = abbr
        self.description = description
        self.category = category
    def __str__(self):
        return self.abbr
    __repr__ = __str__ # XXX naughty

SO = Destination("Sub-orbital", "SO", "Any ballistic trajectory which clears Earth's atmosphere (apogee beyond the Kármán line, 100km) but does not reach orbit.")
EO = Destination("Earth orbit", "EO", "Any orbit around Earth, excluding Lunar transfers.")
EPO = Destination("Earth polar orbit", "EPO", "Orbit around Earth with inclination close to 90°.")
SSO = Destination("Sun-synchronous orbit", "SSO", "Orbit around Earth with inclination close to 98°.")
LEO = Destination("Low earth orbit", "LEO", "Orbit around Earth with apogee below 2,000km.", EO)
MEO = Destination("Medium earth orbit", "MEO", "Near-circular Earth orbit with apogee above 2,000km but below the ~35,800km of GEO.", EO)
GEO = Destination("Geostationary orbit", "GEO", "Circular equatorial Earth orbit with period of one sidereal day.  Altitude is about 35,800km.", EO)
HEO = Destination("High elliptical orbit", "HEO", "High-eccentricity Earth orbit with apogee above the ~35,800km of GEO, typically Molniya or Tundra.", EO)
Moon = Destination("Moon", "L", "Earth's main natural satellite.")
LF = Destination("Lunar fly-by", "LF", "Trajectory which passes near to the Moon but does not capture into orbit or reach the lunar surface.", Moon)
LI = Destination("Lunar impact", "LI", "Hard impact with the Moon, destroying the vessel.", LF)
LO = Destination("Lunar orbit", "LO", "Any orbit around the Moon.", Moon)
LS = Destination("Lunar surface", "LS", "Soft landing on the Moon's surface.", LO)
LSR = Destination("Lunar surface return", "LSR", "Soft landing on the Moon's surface, followed by return to Earth and recovery.", LS)
HO = Destination("Heliocentric orbit", "HO", "Any mission which escapes Earth's gravity.")
IP = Destination("Interplanetary", "IP", "Any mission to a solar-system body beyond the Earth-Moon system.", HO)
Venus = Destination("Venus", "V", "The second planet of the Solar System, a rocky world with a thick atmosphere and a runaway greenhouse effect.", IP)
VF = Destination("Venus fly-by", "VF", "Trajectory which visits Venus but does not capture or enter the atmosphere.", Venus)

class Payload(object):
    def __init__(self, name, paren=None, description=None):
        self._name = name
        self.paren = paren
        self.description = description
    @property
    def name(self):
        if self._name is None and self.paren is not None:
            return '[%s]' % (self.paren,)
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

class Launch(object):
    def __init__(self, name, when, lv, payload, dest, result):
        """Result semantics:
        
        -1 = Mission failure (all stages worked but design error killed mission)
        0 = Success
        positive = number of failing stage"""
        self.name = name
        self.date = when
        self.lv = lv
        self.payload = payload
        self.dest = dest
        self.result = result

class Database(object):
    def __init__(self, launches):
        self.launches = launches
        self.update()
    def add_lv(self, lv):
        self.lvs.setdefault(lv.name, {'lv': lv, 'success': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}})
        if lv.name not in self.lv_tree:
            self.lv_tree[lv.name] = {}
        fam = getattr(lv, "family", None)
        if fam:
            self.add_lv(fam)[lv.name] = self.lv_tree[lv.name]
        return self.lv_tree[lv.name]
    def add_stage(self, stage):
        self.add_engine(stage.engine)
        self.stages.setdefault(stage.name, {'stage': stage, 'success': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}})
        if stage.name not in self.stage_tree:
            self.stage_tree[stage.name] = {}
        fam = getattr(stage, "family", None)
        if fam:
            self.add_stage(fam)[stage.name] = self.stage_tree[stage.name]
        return self.stage_tree[stage.name]
    def add_engine(self, eng):
        self.engines.setdefault(eng.name, {'engine': eng, 'success': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}})
        if eng.name not in self.engine_tree:
            self.engine_tree[eng.name] = {}
        fam = getattr(eng, "family", None)
        if fam:
            self.add_engine(fam)[eng.name] = self.engine_tree[eng.name]
        return self.engine_tree[eng.name]
    def update(self):
        self.engines = {}
        self.engine_tree = {}
        self.stages = {}
        self.stage_tree = {}
        self.lvs = {}
        self.lv_tree = {}
        for launch in self.launches:
            self.add_lv(launch.lv)
            lv = self.lvs[launch.lv.name]
            lv['first'] = min(lv.get('first', launch.date), launch.date)
            lv['last'] = max(lv.get('last', launch.date), launch.date)
            if launch.result == 0:
                lv['success'] += 1
            elif launch.result < 0:
                lv['mission_failure'] += 1
            else:
                lv['failure'] += 1
            lv['dest'][launch.dest] = lv['dest'].get(launch.dest, 0) + 1
            for i,stage in enumerate(launch.lv.stages):
                self.add_stage(stage)
                st = self.stages[stage.name]
                en = self.engines[stage.engine.name]
                st['first'] = min(st.get('first', launch.date), launch.date)
                en['first'] = min(en.get('first', launch.date), launch.date)
                st['last'] = max(st.get('last', launch.date), launch.date)
                en['last'] = max(en.get('last', launch.date), launch.date)
                if launch.result == 0:
                    st['success'] += 1
                    en['success'] += 1
                elif launch.result < 0 or launch.result > i + 1:
                    st['mission_failure'] += 1
                    en['mission_failure'] += 1
                else:
                    st['failure'] += 1
                    en['failure'] += 1
                st['dest'][launch.dest] = st['dest'].get(launch.dest, 0) + 1
                en['dest'][launch.dest] = en['dest'].get(launch.dest, 0) + 1
    @classmethod
    def flatten_tree(cls, tree):
        l = tree.keys()
        for v in tree.values():
            l.extend(cls.flatten_tree(v))
        return l
    @property
    def lv_family_tree(self):
        return dict((k,v) for k,v in self.lv_tree.items() if isinstance(self.lvs[k]['lv'], LVFamily))
    @property
    def stage_family_tree(self):
        return dict((k,v) for k,v in self.stage_tree.items() if isinstance(self.stages[k]['stage'], StageFamily))
    @property
    def engine_family_tree(self):
        return dict((k,v) for k,v in self.engine_tree.items() if isinstance(self.engines[k]['engine'], EngineFamily))
    @classmethod
    def roll_family(cls, d, e):
        for k in ('success', 'failure', 'mission_failure'):
            d[k] += e[k]
        if 'first' in d:
            d['first'] = min(d['first'], e.get('first', d['first']))
        elif 'first' in e:
            d['first'] = e['first']
        if 'last' in d:
            d['last'] = max(d['last'], e.get('last', d['last']))
        elif 'last' in e:
            d['last'] = e['last']
        for k in e['dest'].keys():
            d['dest'][k] = d['dest'].get(k, 0) + e['dest'][k]
    def lv_family(self, name):
        fam = self.flatten_tree(self.lv_tree[name])
        d = {'lv': self.lvs[name]['lv'], 'success': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}}
        for n in [name] + fam:
            self.roll_family(d, self.lvs[n])
        return d
    def stage_family(self, name):
        fam = self.flatten_tree(self.stage_tree[name])
        d = {'stage': self.stages[name]['stage'], 'success': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}}
        for n in [name] + fam:
            self.roll_family(d, self.stages[n])
        return d
    def engine_family(self, name):
        fam = self.flatten_tree(self.engine_tree[name])
        d = {'engine': self.engines[name]['engine'], 'success': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}}
        for n in [name] + fam:
            self.roll_family(d, self.engines[n])
        return d

def test():
    # Some test data from my own RP-1 game
    Redstone = Engine("NAA-75-110", None, "Ethanol/LOx booster engine developed from German Aggregat 4.")
    DavyStage = StageFamily("Davy", Redstone, None)
    DavyShort = Stage("Davy 0/1", DavyStage, description="Short-stage booster to fit 20t pad.")
    DavyLong = Stage("Davy 2/3", DavyStage, description="Full-length Davy booster.")
    Aerobee = EngineFamily("Aerobee", "Early pressure-fed hypergolic (aniline/furfuryl/nitric) engine originally for sounding rockets.")
    XASR = Engine("XASR-1", Aerobee)
    Ten = Engine("AJ10-27", Aerobee, "Early pressure-fed hypergolic (aniline/furfuryl/nitric) upper stage engine.")
    AJ10 = EngineFamily("AJ10", "Pressure-fed hypergolic (UDMH/nitric) upper stage engine.")
    AJ10_37 = Engine("AJ10-37", AJ10)
    Blue = StageFamily("Blue", XASR, "Designation for generally unguided XASR-1 kick stages.")
    Davy = LVFamily("Davy", "The Agency's first large rockets, built around the booster stage of the same name.")
    Davy0 = LV("Davy 0", Davy, "Flying the Short-Stage Davy without an upper stage, either for booster development or as a heavy sounding rocket.", DavyShort)
    Davy0B = LV("Davy 0B", Davy, "Upper stage used for a boost-back maneuver to overfly land as a sounding rocket.", DavyShort, Blue)
    AbleStage = StageFamily("Able", AJ10, "Early pressure-fed hypergolic upper stage.")
    TwinTen = Stage("Twin-Ten", AbleStage, Ten, "Very early upper stage.", 2)
    Davy1 = LV("Davy 1/1A", Davy, "Two-stage sounding rocket for booster development.", DavyShort, TwinTen)
    Davy1B = LV("Davy 1B", Davy, "Three-stage sounding rocket for booster development.", DavyShort, TwinTen, Blue)
    TripleTen = Stage("Triple-Ten", AbleStage, Ten, "Very early upper stage.", 3)
    Davy2 = LV("Davy 2", Davy, "Very early orbital rocket for small payloads.", DavyLong, TripleTen, Blue)
    Davy2A = LV("Davy 2A", Davy2, "Very early orbital rocket for small payloads.  With two short Tens as strap-on boosters.")
    Davy2B = LV("Davy 2B", Davy2, "Very early orbital rocket for small payloads.  With four short Tens as strap-on boosters.")
    Davy3 = LV("Davy 3", Davy, "Similar to the Davy 2, but short-fuelled to reduce time-to-orbit at the cost of even tinier payload.", DavyLong, TripleTen, Blue)
    Davy3S = LV("Davy 3S", Davy, "Something of a misnomer, the Davy 3S uses the Short-Stage Davy to launch a tiny payload from a 20t pad.", DavyShort, TripleTen, Blue)
    Able0 = Stage("Able 0", AbleStage, AJ10_37)
    Davy3T = LV("Davy 3T", Davy, "Development of the Davy 3S using upgraded upper stages.", DavyShort, Able0, Blue)
    LR79 = EngineFamily("LR79", "Gas-generator kerolox booster engine.")
    S3 = Engine("S-3", LR79, "Prototype gas-generator kerolox booster engine.")
    NewtonStage = StageFamily("Newton", LR79, "Workhorse booster stage, Ø=2.4m.")
    Newton01 = Stage("Newton 0/1", NewtonStage, S3)
    Newton = LVFamily("Newton", "Workhorse launch vehicles based on the Newton family of booster stages", NewtonStage)
    Newton0 = LV("Newton 0", Newton, "Booster development flight", Newton01)
    Newton1 = LV("Newton 1", Newton, "Early Newton/Able workhorse.", Newton01, Able0)
    Newton1A = LV("Newton 1A", Newton, "Early Newton/Able with added kick stage.", Newton01, Able0, Blue)
    Able0Refresh = Stage("Able 0 Refresh", Able0, description="An improved version of the Able0 stage, with lighter tankage and better avionics; Ø=1.5m.")
    Newton1C = LV("Newton 1C", Newton1, None, Newton01, Able0Refresh)
    Castor = EngineFamily("Castor", "Solid-fuel strap-on booster.")
    CastorI = Engine("Castor I", Castor, "Early solid-fuel strap-on booster.")
    CastorStage = StageFamily("Castor", Castor, "Solid-fuel strap-on boosters.")
    CastorIx2 = Stage("Castor I ×2", CastorStage, CastorI, None, 2)
    Newton1D = LV("Newton 1D", Newton, "Augmented Newton/Able for lunar probes.", CastorIx2, Newton01, Able0Refresh, Blue)
    S3D = Engine("S-3D", LR79)
    Newton2Stage = Stage("Newton 2", NewtonStage, S3D)
    AJ10_42 = Engine("AJ10-42", AJ10)
    Able1 = Stage("Able 1", AbleStage, AJ10_42)
    Newton2 = LV("Newton 2", Newton, "Newton/Able workhorse.", Newton2Stage, Able1)
    Newton2A = LV("Newton 2A", Newton, "Augmented Newton/Able for lunar probes.", CastorIx2, Newton2Stage, Able1, Blue)
    Newton2C = LV("Newton 2C", Newton, "Newton/Able with added kick stage.", Newton2Stage, Able1, Blue)

    launches = []
    def launch(name, y, m, d, lv, payload, dest, result):
        launches.append(Launch(name, date(y, m, d), lv, payload, dest, result))
    def paren(text):
        return Payload(None, text, None)

    launch("Davy 0",        1952,  8, 23, Davy0,    None, SO, 0)
    launch("Davy 1",        1952, 10,  6, Davy1,    None, SO, 0)
    launch("Davy 1A",       1952, 11, 23, Davy1,    None, SO, 0)
    launch("Davy 1B",       1953,  1, 19, Davy1B,   None, SO, 0)
    launch("Davy 0A",       1953,  2, 28, Davy0,    paren("Early film camera"), SO, 0)
    launch("Davy 2",        1953,  4, 24, Davy2,    paren("60kg SR core"), EO, -1)
    launch("Davy 2A",       1953,  6, 24, Davy2A,   paren("60kg SR core"), EO, 3)
    launch("Davy 2B",       1953,  8, 27, Davy2B,   Payload("Kepler 0", "60kg SR core", "First satellite to orbit the Earth!"), EO, 0)
    launch("Davy 2B₂",      1953, 10, 29, Davy2B,   paren("60kg SR core"), SO, 0)
    launch("Davy 0B",       1953, 12, 10, Davy0B,   paren("Early film camera"), SO, 0)
    launch("Davy 3",        1954,  4, 30, Davy3,    Payload("Kepler 1", "Explorer-1"), EO, -1)
    launch("Davy 3S",       1954,  6, 23, Davy3S,   paren("Explorer-1"), EO, 2)
    launch("Davy 3",        1954,  8, 22, Davy3,    Payload("Kepler 2", "Explorer-1"), EO, 0)
    launch("Davy 3S₂",      1954, 10, 14, Davy3S,   Payload("Kepler 3", "Explorer-1"), EO, 0)
    launch("Davy 3A",       1954, 12, 14, Davy3,    Payload("Bernoulli 1", "Explorer-1", "Atmospheric analysis satellite."), EO, 0)
    launch("Newton 0",      1955,  1, 17, Newton0,  None, SO, -1)
    launch("Newton 0A",     1955,  3,  5, Newton1,  None, EO, 0)
    launch("Newton 1",      1955,  5,  7, Newton1,  paren("Scientific satellite"), EO, 1)
    launch("Davy 3SP",      1955,  6, 16, Davy3S,   paren("Explorer-1"), EPO, 2)
    launch("Newton 1A",     1955,  7,  8, Newton1A, Payload("Kepler 4", None, "Scientific satellite"), EO, 0)
    launch("Newton 1B",     1955,  9, 13, Newton1A, Payload("Kepler 5", None, "Scientific satellite"), HEO, 0)
    launch("Newton 1C",     1955, 12,  7, Newton1C, paren("Controllable weather satellite"), EO, 2)
    launch("Davy 3T",       1956,  2, 22, Davy3T,   Payload("Kepler 6", "Explorer-1", "First polar-orbit satellite."), EPO, 0)
    launch("Newton 1D",     1956,  3, 10, Newton1D, Payload("Tycho 1", None, "First lunar mission!  Does not carry lunar-range comms."), LI, 0)
    launch("Newton 1C₂",    1956,  5, 19, Newton1C, Payload("Bernoulli 2", None, "Controllable weather satellite."), LEO, 0)
    launch("Newton 1E",     1956,  9,  1, Newton1D, Payload("Tycho 2", None, "Prototype lunar probe."), LF, 0)
    launch("Newton 2",      1956, 10, 25, Newton2,  Payload("Bernoulli 3", None, "Weather satellite."), LEO, 0)
    launch("Newton 2A",     1957,  1, 11, Newton2A, Payload("Tycho 3", None, "Lunar probe with basic scientific instruments.  First pictures of lunar farside."), LF, 0)
    launch("Davy 3T₂",      1957,  1, 29, Davy3T,   Payload("Kepler 7", None, "Geodesy satellite."), SSO, 0)
    launch("Newton 2B",     1957,  2, 16, Newton2,  paren("Re-entry test vehicle; mass spectrometers"), LEO, 0)
    print "%d launches recorded" % (len(launches),)
    db = Database(launches)
    # Generate a few reports
    import pprint
    pprint.pprint(db.lv_family_tree)
    pprint.pprint(db.stage_family_tree)
    pprint.pprint(db.engine_family_tree)
    print
    pprint.pprint(db.lvs['Newton 1D'])
    pprint.pprint(db.stages['Davy 2/3'])
    pprint.pprint(db.engines['S-3'])
    print
    pprint.pprint(db.stage_family('Davy'))
    pprint.pprint(db.engine_family('LR79'))

if __name__ == '__main__':
    test()
