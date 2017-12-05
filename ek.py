#!/usr/bin/python2
# encoding: utf-8
"""Encyclopedia Kerbonautica

Launch library and vehicle/stage/engine database."""

from datetime import date

class EngineFamily(object):
    def __init__(self, name, description, vac=False):
        self.name = name
        self.description = description
        self.vac = vac
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty temporary hack for testing

class Engine(object):
    def __init__(self, name, family, description=None, vac=None):
        self.name = name
        self.family = family
        self._description = description
        self._vac = vac
    @property
    def description(self):
        if self._description is None and self.family is not None:
            return self.family.description
        return self._description
    @description.setter
    def description(self, value):
        self._description = value
    @property
    def vac(self):
        if self._vac is None and self.family is not None:
            return self.family.vac
        return self._vac
    @vac.setter
    def vac(self, value):
        self._vac = value
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty

class StageFamily(object):
    def __init__(self, name, ef, description, engine_count=1, vac=False):
        self.name = name
        self.engine = ef
        self.description = description
        self.engine_count = engine_count
        self.vac = vac
    def __str__(self):
        return self.name
    __repr__ = __str__ # XXX naughty

class Stage(object):
    def __init__(self, name, family, engine=None, description=None, engine_count=None, vac=None):
        self.name = name
        self.family = family
        self._engine = engine
        self._description = description
        self._engine_count = engine_count
        self._vac = vac
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
    @engine_count.setter
    def engine_count(self, value):
        self._engine_count = value
    @property
    def vac(self):
        if self._vac is None and self.family is not None:
            return self.family.vac
        return self._vac
    @vac.setter
    def vac(self, value):
        self._vac = value
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
        if not self._stages and self.family is not None:
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

_destination_sort = 0
class Destination(object):
    def __init__(self, name, abbr, description, category=None):
        self.name = name
        self.abbr = abbr
        self.description = description
        self.category = category
        global _destination_sort
        self.sort = _destination_sort
        _destination_sort += 1
        self._depth = 0
    @property
    def depth(self):
        if self.category is None:
            return self._depth
        return self.category.depth + 1
    @depth.setter
    def depth(self, value):
        self._depth = value
    def member(self, other):
        if self == other:
            return True
        if self.category:
            return self.category.member(other)
        return False
    def __str__(self):
        return self.abbr
    __repr__ = __str__ # XXX naughty

SO = Destination("Sub-orbital", "SO", "Any ballistic trajectory which clears Earth's atmosphere (apogee beyond the Kármán line, 100km) but does not reach orbit.")
EO = Destination("Earth orbit", "EO", "Any orbit around Earth, excluding Lunar transfers.")
EO.depth = 1
EPO = Destination("Earth polar orbit", "EPO", "Orbit around Earth with inclination close to 90°.", EO)
SSO = Destination("Sun-synchronous orbit", "SSO", "Orbit around Earth with inclination close to 98°.", EO)
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
IP = Destination("Interplanetary", "IP", "Any mission to a solar-system body beyond the Earth-Moon system.")
Venus = Destination("Venus", "V", "The second planet of the Solar System, a rocky world with a thick atmosphere and a runaway greenhouse effect.", IP)
VF = Destination("Venus fly-by", "VF", "Trajectory which visits Venus but does not capture or enter the atmosphere.", Venus)

class Payload(object):
    def __init__(self, name, description=None, paren=None):
        self._name = name
        self.description = description
        self.paren = paren
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
        self.stages.setdefault(stage.name, {'stage': stage, 'success': 0, 'mission_failure': 0, 'lower_failure': 0, 'failure': 0, 'dest': {}})
        if stage.name not in self.stage_tree:
            self.stage_tree[stage.name] = {}
        fam = getattr(stage, "family", None)
        if fam:
            self.add_stage(fam)[stage.name] = self.stage_tree[stage.name]
        return self.stage_tree[stage.name]
    def add_engine(self, eng):
        self.engines.setdefault(eng.name, {'engine': eng, 'success': 0, 'mission_failure': 0, 'lower_failure': 0, 'failure': 0, 'dest': {}})
        if eng.name not in self.engine_tree:
            self.engine_tree[eng.name] = {}
        fam = getattr(eng, "family", None)
        if fam:
            self.add_engine(fam)[eng.name] = self.engine_tree[eng.name]
        return self.engine_tree[eng.name]
    def add_dest(self, dest):
        d = {}
        if dest not in self.dest_tree:
            self.dest_tree[dest] = d
        fam = dest.category
        if fam:
            self.add_dest(fam)[dest.name] = d
        return d
    def update(self):
        self.engines = {}
        self.engine_tree = {}
        self.stages = {}
        self.stage_tree = {}
        self.lvs = {}
        self.lv_tree = {}
        self.dest_tree = {}
        self.launches_by_year = {}
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
                    en['success'] += stage.engine_count
                elif launch.result < 0 or launch.result > i + 1:
                    st['mission_failure'] += 1
                    en['mission_failure'] += stage.engine_count
                elif launch.result < i + 1:
                    st['lower_failure'] += 1
                    en['lower_failure'] += stage.engine_count
                else:
                    st['failure'] += 1
                    en['failure'] += 1
                    en['mission_failure'] += stage.engine_count - 1
                st['dest'][launch.dest] = st['dest'].get(launch.dest, 0) + 1
                en['dest'][launch.dest] = en['dest'].get(launch.dest, 0) + stage.engine_count
            self.add_dest(launch.dest)
            self.launches_by_year.setdefault(launch.date.year, []).append(launch)
    @classmethod
    def flatten_tree(cls, tree):
        l = tree.keys()
        for v in tree.values():
            l.extend(cls.flatten_tree(v))
        return l
    @classmethod
    def counted_flatten_tree(cls, tree, data):
        l = []
        for c,v in sorted(tree.items(), key=lambda (k,i): data[k]['first']):
            l.append((c, 0))
            chld = cls.counted_flatten_tree(v, data)
            if len(chld) > 1:
                l.extend((k, i+1) for (k, i) in chld)
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
        for k in ('success', 'failure', 'mission_failure', 'lower_failure'):
            if k in e:
                d[k] = d.get(k, 0) + e[k]
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
    def coalesce_dests(self, items, maxdepth):
        count = {}
        for item in items:
            for k,v in item['dest'].items():
                count[k] = count.get(k, 0) + v
        leaves = set(k for k in count if count[k])
        changes = True
        while changes:
            changes = False
            for leaf in list(leaves):
                siblings = set(k for k in leaves if k.category == leaf.category) if leaf.category else set()
                if leaf.depth > maxdepth or (len(siblings) == 1 and not count.get(leaf.category)):
                    count[leaf.category] = count.get(leaf.category, 0) + count[leaf]
                    leaves = set(l for l in leaves if not l.member(leaf.category))
                    leaves.add(leaf.category)
                    changes = True
        return sorted(leaves, key=lambda d:d.sort)

class Renderer(object):
    def __init__(self, db):
        self.db = db
    def render_lv_families(self):
        raise NotImplementedError()

class TextRenderer(Renderer):
    def table(self, cols, rows):
        for c in cols:
            c['width'] = len(c['head'])
        def fmt(r, c):
            return c.get('formatter', str)(r[c['key']])
        for r in rows:
            for c in cols:
                if c['key'] in r:
                    c['width'] = max(c['width'], len(fmt(r, c)))
        head = ''
        for c in cols:
            head += ' %s |' % (c['head'].ljust(c['width']),)
        body = ''
        rows = rows + ['=']
        for r in rows:
            body += '\n'
            for c in cols:
                if isinstance(r, str):
                    field = r * (c['width'] + 2)
                    body += '%s|' % (field,)
                else:
                    field = fmt(r, c).ljust(c['width'])
                    body += ' %s |' % (field,)
        return head + body
    def render_lv_families(self, maxdepth, maxdest):
        dests = self.db.coalesce_dests(self.db.lvs.values(), maxdest)
        def render_dest(dest):
            def render_d(d):
                c = sum(dest.get(n, 0) for n in self.db.dest_tree.keys() if n.member(d) and (n == d or n not in dests))
                s = str(c) if c else '-'
                return s.rjust(max(len(d.abbr), 2))
            return ' '.join(map(render_d, dests))
        desthead = ' '.join(d.abbr.rjust(2) for d in dests)
        cols = [{'head': 'Name', 'key': 'name'},
                {'head': 'First', 'key': 'first', 'formatter': date.isoformat},
                {'head': 'Last', 'key': 'last', 'formatter': date.isoformat},
                {'head': 'Succ', 'key': 'success'},
                {'head': 'fSta', 'key': 'failure'},
                {'head': 'fMis', 'key': 'mission_failure'},
                {'head': desthead, 'key': 'dest', 'formatter': render_dest}]
        tree = self.db.lv_family_tree
        rows = []
        lv = dict((name, self.db.lv_family(name)) for name in self.db.lvs)
        odepth = 0
        for name, depth in self.db.counted_flatten_tree(tree, lv):
            if depth < maxdepth:
                if not depth:
                    rows.append('=')
                elif not odepth:
                    rows.append('-')
                row = dict(lv[name])
                row['name'] = ' ' * depth + row['lv'].name
                rows.append(row)
                odepth = depth
        return self.table(cols, rows)
    def render_stage_families(self, maxdepth, maxdest, vac=None):
        dests = self.db.coalesce_dests(self.db.stages.values(), maxdest)
        def render_dest(dest):
            def render_d(d):
                c = sum(dest.get(n, 0) for n in self.db.dest_tree.keys() if n.member(d) and (n == d or n not in dests))
                s = str(c) if c else '-'
                return s.rjust(max(len(d.abbr), 2))
            return ' '.join(map(render_d, dests))
        def render_engine(st):
            if st.engine_count > 1:
                return '%dx %s' % (st.engine_count, st.engine)
            return str(st.engine)
        desthead = ' '.join(d.abbr.rjust(2) for d in dests)
        cols = [{'head': 'Name', 'key': 'name'},
                {'head': 'Engine', 'key': 'stage', 'formatter': render_engine},
                {'head': 'First', 'key': 'first', 'formatter': date.isoformat},
                {'head': 'Last', 'key': 'last', 'formatter': date.isoformat},
                {'head': 'Succ', 'key': 'success'},
                {'head': 'fSta', 'key': 'failure'},
                {'head': 'fLwr', 'key': 'lower_failure'},
                {'head': 'fMis', 'key': 'mission_failure'},
                {'head': desthead, 'key': 'dest', 'formatter': render_dest}]
        tree = self.db.stage_family_tree
        rows = []
        st = dict((name, self.db.stage_family(name)) for name in self.db.stages)
        odepth = 0
        if maxdepth <= 1:
            rows.append('=')
        for name, depth in self.db.counted_flatten_tree(tree, st):
            if depth < maxdepth and (vac is None or st[name]['stage'].vac == vac):
                if maxdepth > 1:
                    if not depth:
                        rows.append('=')
                    elif not odepth:
                        rows.append('-')
                row = dict(st[name])
                row['name'] = ' ' * depth + row['stage'].name
                rows.append(row)
                odepth = depth
        return self.table(cols, rows)
    def render_engine_families(self, maxdepth, maxdest, vac=None):
        dests = self.db.coalesce_dests(self.db.engines.values(), maxdest)
        def render_dest(dest):
            def render_d(d):
                c = sum(dest.get(n, 0) for n in self.db.dest_tree.keys() if n.member(d) and (n == d or n not in dests))
                s = str(c) if c else '-'
                return s.rjust(max(len(d.abbr), 2))
            return ' '.join(map(render_d, dests))
        desthead = ' '.join(d.abbr.rjust(2) for d in dests)
        cols = [{'head': 'Name', 'key': 'name'},
                {'head': 'First', 'key': 'first', 'formatter': date.isoformat},
                {'head': 'Last', 'key': 'last', 'formatter': date.isoformat},
                {'head': 'Succ', 'key': 'success'},
                {'head': 'fSta', 'key': 'failure'},
                {'head': 'fLwr', 'key': 'lower_failure'},
                {'head': 'fMis', 'key': 'mission_failure'},
                {'head': desthead, 'key': 'dest', 'formatter': render_dest}]
        tree = self.db.engine_family_tree
        rows = []
        en = dict((name, self.db.engine_family(name)) for name in self.db.engines)
        odepth = 0
        if maxdepth <= 1:
            rows.append('=')
        for name, depth in self.db.counted_flatten_tree(tree, en):
            if depth < maxdepth and (vac is None or en[name]['engine'].vac == vac):
                if maxdepth > 1:
                    if not depth:
                        rows.append('=')
                    elif not odepth:
                        rows.append('-')
                row = dict(en[name])
                row['name'] = ' ' * depth + row['engine'].name
                rows.append(row)
                odepth = depth
        return self.table(cols, rows)
    def render_launches_per_year(self, maxdest):
        dests = self.db.coalesce_dests(self.db.lvs.values(), maxdest)
        def render_dest(dest):
            def render_d(d):
                c = sum(dest.get(n, 0) for n in self.db.dest_tree.keys() if n.member(d) and (n == d or n not in dests))
                s = str(c) if c else '-'
                return s.rjust(max(len(d.abbr), 2))
            return ' '.join(map(render_d, dests))
        desthead = ' '.join(d.abbr.rjust(2) for d in dests)
        cols = [{'head': 'Year', 'key': 'year'},
                {'head': 'Launches', 'key': 'count'},
                {'head': desthead, 'key': 'dest', 'formatter': render_dest}]
        rows = ['=']
        for year, launches in sorted(self.db.launches_by_year.items()):
            row = {'year': year, 'count': len(launches), 'dest': {}}
            for launch in launches:
                row['dest'][launch.dest] = row['dest'].get(launch.dest, 0) + 1
            rows.append(row)
        return self.table(cols, rows)

def test():
    # Some test data from my own RP-1 game
    Redstone = EngineFamily("NAA-75-110", "Ethanol/LOx booster engine developed from German Aggregat 4.")
    DavyStage = StageFamily("Davy", Redstone, None)
    DavyShort = Stage("Davy 0/1", DavyStage, description="Short-stage booster to fit 20t pad.")
    DavyLong = Stage("Davy 2/3", DavyStage, description="Full-length Davy booster.")
    Aerobee = EngineFamily("Aerobee", "Early pressure-fed hypergolic (aniline/furfuryl/nitric) engine originally for sounding rockets.", vac=True)
    XASR = Engine("XASR-1", Aerobee)
    Ten = Engine("AJ10-27", Aerobee, "Early pressure-fed hypergolic (aniline/furfuryl/nitric) upper stage engine.")
    AJ10 = EngineFamily("AJ10", "Pressure-fed hypergolic (UDMH/nitric) upper stage engine.", vac=True)
    AJ10_37 = Engine("AJ10-37", AJ10)
    Blue = StageFamily("Blue", XASR, "Designation for generally unguided XASR-1 kick stages.", vac=True)
    Davy = LVFamily("Davy", "The Agency's first large rockets, built around the booster stage of the same name.")
    Davy01Family = LV("Davy 0/1", Davy, "Early model Davy rockets, lacking orbital capability.")
    Davy0 = LV("Davy 0", Davy01Family, "Flying the Short-Stage Davy without an upper stage, either for booster development or as a heavy sounding rocket.", DavyShort)
    Davy0B = LV("Davy 0B", Davy01Family, "Upper stage used for a boost-back maneuver to overfly land as a sounding rocket.", DavyShort, Blue)
    AbleStage = StageFamily("Able", AJ10, "Early pressure-fed hypergolic upper stage.", vac=True)
    TwinTen = Stage("Twin-Ten", AbleStage, Ten, "Very early upper stage.", 2)
    Davy1 = LV("Davy 1/1A", Davy01Family, "Two-stage sounding rocket for booster development.", DavyShort, TwinTen)
    Davy1B = LV("Davy 1B", Davy01Family, "Three-stage sounding rocket for booster development.", DavyShort, TwinTen, Blue)
    TripleTen = Stage("Triple-Ten", AbleStage, Ten, "Very early upper stage.", 3)
    Davy2Family = LV("Davy 2x", Davy, "Very early orbital rocket for small payloads.", DavyLong, TripleTen, Blue)
    Davy2 = LV("Davy 2", Davy2Family, "Very early orbital rocket for small payloads.", DavyLong, TripleTen, Blue)
    Davy2A = LV("Davy 2A", Davy2Family, "Very early orbital rocket for small payloads.  With two short Tens as strap-on boosters.")
    Davy2B = LV("Davy 2B", Davy2Family, "Very early orbital rocket for small payloads.  With four short Tens as strap-on boosters.")
    Davy3 = LV("Davy 3", Davy, "Similar to the Davy 2, but short-fuelled to reduce time-to-orbit at the cost of even tinier payload.", DavyLong, TripleTen, Blue)
    Davy3ST = LV("Davy 3S/T", Davy)
    Davy3S = LV("Davy 3S", Davy3ST, "Something of a misnomer, the Davy 3S uses the Short-Stage Davy to launch a tiny payload from a 20t pad.", DavyShort, TripleTen, Blue)
    Able0 = Stage("Able 0", AbleStage, AJ10_37)
    Davy3T = LV("Davy 3T", Davy3ST, "Development of the Davy 3S using upgraded upper stages.", DavyShort, Able0, Blue)
    LR79 = EngineFamily("LR79", "Gas-generator kerolox booster engine.")
    S3 = Engine("S-3", LR79, "Prototype gas-generator kerolox booster engine.")
    NewtonStage = StageFamily("Newton", LR79, "Workhorse booster stage, Ø=2.4m.")
    Newton01 = Stage("Newton 0/1", NewtonStage, S3)
    Newton = LVFamily("Newton", "Workhorse launch vehicles based on the Newton family of booster stages", NewtonStage)
    Newton0 = LV("Newton 0", Newton, "Booster development flight", Newton01)
    NewtonAx = LV("Newton Ax", Newton, "Newton/Able workhorse SLLV.", Newton, AbleStage)
    Newton1Family = LV("Newton 1x", NewtonAx, "Early Newton/Able workhorse.", Newton01, Able0)
    Newton1 = LV("Newton 1", Newton1Family)
    Newton1A = LV("Newton 1A", Newton1Family, "Early Newton/Able with added kick stage.", Newton01, Able0, Blue)
    Able0Refresh = Stage("Able 0 Refresh", Able0, description="An improved version of the Able0 stage, with lighter tankage and better avionics; Ø=1.5m.")
    Newton1C = LV("Newton 1C", Newton1Family, None, Newton01, Able0Refresh)
    Castor = EngineFamily("Castor", "Solid-fuel strap-on booster.")
    CastorI = Engine("Castor I", Castor, "Early solid-fuel strap-on booster.")
    CastorStage = StageFamily("Castor", Castor, "Solid-fuel strap-on boosters.")
    CastorIx2 = Stage("Castor I x2", CastorStage, CastorI, None, 2)
    Newton1D = LV("Newton 1D", Newton1Family, "Augmented Newton/Able for lunar probes.", CastorIx2, Newton01, Able0Refresh, Blue)
    S3D = Engine("S-3D", LR79)
    Newton2Stage = Stage("Newton 2", NewtonStage, S3D)
    AJ10_42 = Engine("AJ10-42", AJ10)
    Able1 = Stage("Able 1", AbleStage, AJ10_42)
    NewtonA2Family = LV("Newton A2x", NewtonAx, "Newton/Able workhorse.", Newton2Stage, Able1)
    Newton2 = LV("Newton 2", NewtonA2Family, "Newton/Able workhorse.", Newton2Stage, Able1)
    Newton2A = LV("Newton 2A", NewtonA2Family, "Augmented Newton/Able for lunar probes.", CastorIx2, Newton2Stage, Able1, Blue)
    Newton2C = LV("Newton 2C", NewtonA2Family, "Newton/Able with added kick stage.", Newton2Stage, Able1, Blue)
    XLR81 = EngineFamily("XLR81", "Bell Agena vacuum engine, gas-generator, UDMH/nitric.", vac=True)
    XLR81BA5 = Engine("XLR81-BA-5", XLR81, "Early hypergolic gas-generator upper-stage engine; rated for 2m burn.")
    Agena = StageFamily("Agena", XLR81, "Versatile upper stage using hypergolic propellants.", vac=True)
    AgenaA = Stage("Agena A", Agena, XLR81BA5)
    NewtonBx = LV("Newton Bx", Newton, "Newton/Agena small-medium lift workhorse.", Newton, Agena)
    NewtonB2 = LV("Newton B2", NewtonBx, "Prototype Newton/Agena.", Newton2Stage, AgenaA, Blue)
    MB31 = Engine("MB-3-1", LR79, "Production gas-generator kerolox booster engine.")
    Newton3Stage = Stage("Newton 3", NewtonStage, MB31)
    NewtonB3 = LV("Newton B3", NewtonBx, "Newton/Agena workhorse.", Newton3Stage, AgenaA)
    AJ10_101A = Engine("AJ10-101A", AJ10)
    Able2 = Stage("Able 2", AbleStage, AJ10_101A)
    NewtonA3 = LV("Newton A3", NewtonAx, "Newton/Able workhorse.", Newton3Stage, Able2)
    NewtonA3A = LV("Newton A3A", NewtonA3, "Newton/Able with added kick stage.", Newton3Stage, Able2, Blue)
    NewtonB3A = LV("Newton B3A", NewtonB3, "Newton/Agena with added kick stage.", Newton3Stage, AgenaA, Blue)
    LR105 = EngineFamily("LR105", "Kerolox gas-generator sustainer engine, rated for nearly six minutes burn time.")
    LR105NA3 = Engine("LR105-NA-3", LR105, "Prototype kerolox gas-generator sustainer engine.")
    TartagliaStage = StageFamily("Tartaglia", LR105, "Kerolox sustainer stage, Ø=2.4m.")
    TartagliaA = Stage("Tartaglia A", TartagliaStage, LR105NA3)
    Tartaglia = LVFamily("Tartaglia", "Suborbital development flights of the Tartaglia sustainer stage.", TartagliaStage)
    Tartaglia0 = LV("Tartaglia 0", Tartaglia, "Suborbital test flight of Tartaglia A sustainer stage.", TartagliaA)
    LeibnitzBooster = StageFamily("Leibnitz LFB", LR79, "Newton-derived liquid-fuel boosters.", 2)
    LeibnitzAStage = Stage("Leibnitz A LFB", LeibnitzBooster, MB31, "Liquid fuel boosters based on Newton 3.")
    Leibnitz = LVFamily("Leibnitz", "Parallel-staged kerolox LV for medium lift, GLOM up to 150t.", LeibnitzBooster, TartagliaStage)
    LeibnitzA = LV("Leibnitz A", Leibnitz, "Prototype parallel-staged kerolox LV.", LeibnitzAStage, TartagliaA)
    LeibnitzAB = LV("Leibnitz AB", LeibnitzA, "Prototype Leibnitz/Agena.", LeibnitzAStage, TartagliaA, AgenaA)
    Napier = StageFamily("Napier", XLR81, "Spaceplane with one-man crew.", vac=True)
    NapierA = Stage("Napier (1958)", Napier, XLR81BA5, "Initial configuration of Napier spaceplane; first manned spaceflights.")
    LeibnitzAH = LV("Leibnitz AH", LeibnitzA, "Prototype Leibnitz/Napier.", LeibnitzAStage, TartagliaA, NapierA)
    MB32 = Engine("MB-3-2", LR79, "Upgraded gas-generator kerolox booster engine.")
    Newton4Stage = Stage("Newton 4/5/6", NewtonStage, MB32)
    AJ10_142 = Engine("AJ10-142", AJ10)
    Able3 = Stage("Able 3", AbleStage, AJ10_142, "Ultimate refined version of Able upper stage; for later related development see Delta.")
    NewtonA4 = LV("Newton A4", NewtonAx, "Final variant of the venerable Newton/Able workhorse.", Newton4Stage, Able3)
    NewtonB4 = LV("Newton B4", NewtonBx, "Newton/Agena workhorse.", Newton4Stage, AgenaA)
    NewtonB4Blue = LV("Newton B4+", NewtonB4, "Newton/Agena workhorse with kick stage.", Newton4Stage, AgenaA, Blue)
    LeibnitzBStage = Stage("Leibnitz B LFB", LeibnitzBooster, MB32, "Liquid fuel boosters based on Newton 4.")
    LR105NA5 = Engine("LR105-NA-5", LR105)
    TartagliaB = Stage("Tartaglia B", TartagliaStage, LR105NA5)
    LeibnitzB = LV("Leibnitz B", Leibnitz, None, LeibnitzBStage, TartagliaB)
    LeibnitzBH1 = LV("Leibnitz BH1", LeibnitzB, "Early Leibnitz/Napier with upgraded kerolox engines.", LeibnitzBStage, TartagliaB, NapierA)
    XLR81BA7 = Engine("XLR81-BA-7", XLR81, "Restartable hypergolic gas-generator upper-stage engine; rated for two burns totalling up to four minutes.")
    AgenaB = Stage("Agena B", Agena, XLR81BA7, "First upper stage with relight capability; generally unprecedented performance.")
    NewtonB5 = LV("Newton B5", NewtonBx, "Newton/Agena workhorse, introduced restartable Agena B.", Newton4Stage, AgenaB)
    AJ10_104 = Engine("AJ10-104", AJ10, "First 'Delta' variant of the AJ10; unlimited restarts.")
    Delta = StageFamily("Delta", AJ10, "Restartable pressure-fed hypergolic upper stage.", vac=True)
    DeltaD = Stage("Delta D", Delta, AJ10_104)
    NewtonD4 = LV("Newton D4", Newton, "Prototype Newton/Delta.", Newton4Stage, DeltaD)
    NapierB = Stage("Napier (1959)", Napier, XLR81BA7, "Upgraded configuration of Napier spaceplane; increased reliability.")
    LeibnitzBH2 = LV("Leibnitz BH2", LeibnitzB, "1959-standard Leibnitz/Napier.", LeibnitzBStage, TartagliaB, NapierB)
    LeibnitzBB = LV("Leibnitz BB", LeibnitzB, "Leibnitz/Agena medium-lift LV.", LeibnitzBStage, TartagliaB, AgenaB)
    XLR81BA11 = Engine("XLR81-BA-11", XLR81, "Adds propellant sumps and slightly increased Isp.")
    AgenaD = Stage("Agena D", Agena, XLR81BA11)
    LeibnitzBB4 = LV("Leibnitz BB4", LeibnitzBB, "Leibnitz/Agena medium-lift LV.", LeibnitzBStage, TartagliaB, AgenaD)
    NewtonB6 = LV("Newton B6", NewtonBx, "A further slight upgrade to the Newton/Agena workhorse.", Newton4Stage, AgenaD)
    H1Family = EngineFamily("H-1", "Gas-generator kerolox engine, a simplified and uprated development of LR79 technology.")
    H1 = Engine("H-1 A", H1Family)
    LockeStage = StageFamily("Locke", H1Family, "Workhorse booster stage (based on Newton).")
    Locke01 = Stage("Locke 0/1", LockeStage, H1)
    Locke = LVFamily("Locke", "Workhorse launch vehicles based on the Locke family of booster stages (developed from, and replacing, the Newton family).", LockeStage)
    Locke0 = LV("Locke 0", Locke, "Booster development flight of prototype Locke stage with dummy upper stage.", Locke01)
    Locke1B = LV("Locke 1B", Locke, "Locke/Agena workhorse, replacement for Newton Bx series.", Locke01, AgenaD)
    LR105NA6 = Engine("LR105-NA-6", LR105)
    TartagliaC = Stage("Tartaglia C", TartagliaStage, LR105NA6)
    TartagliaC0 = LV("Tartaglia C0", Tartaglia, "Suborbital test flights of Tartaglia C sustainer stage.", CastorIx2, TartagliaC)
    LeibnitzCStage = Stage("Leibnitz C LFB", LeibnitzBooster, H1, "Liquid fuel boosters based on Locke 1.")
    LeibnitzC = LV("Leibnitz C", Leibnitz, "Revamped Leibnitz using Locke-1-derived boosters.", LeibnitzCStage, TartagliaC)
    LeibnitzCB = LV("Leibnitz CB", LeibnitzC, "Leibnitz/Agena medium-lift LV.", LeibnitzCStage, TartagliaC, AgenaD)
    LeibnitzCB1 = LV("Leibnitz CB1", LeibnitzCB, "Leibnitz/Agena medium-lift LV with added retro stage.", LeibnitzCStage, TartagliaC, AgenaD, Blue)
    TartagliaCA0 = LV("Tartaglia CA0", TartagliaC0, "Suborbital test flight of Tartaglia C sustainer (with Able 3 upper stage).", CastorIx2, TartagliaC, Able3)
    LeibnitzCD = LV("Leibnitz CD", LeibnitzC, "Leibnitz/Delta, for direct GEO insertion of small payloads.", LeibnitzCStage, TartagliaC, DeltaD)
    RL10 = EngineFamily("RL10", "Expander cycle hydrolox engine.", vac=True)
    RL10A1 = Engine("RL10A-1", RL10, "Prototype hydrolox engine.")
    Centaur = StageFamily("Centaur", RL10, "High-energy hydrolox upper stage.", vac=True)
    CentaurA = Stage("CentaurA", Centaur, RL10A1, "Prototype hydrolox upper stage.")
    Locke1C = LV("Locke 1C", Locke, "Locke/Centaur medium-lift LV.", Locke01, CentaurA)
    LeibnitzCC = LV("Leibnitz CC", LeibnitzC, "Leibnitz/Centaur, for high-energy launches.", LeibnitzCStage, TartagliaC, CentaurA)
    GrotiusBooster = StageFamily("Grotius LFB", "Locke-derived liquid-fuel boosters.", H1Family, 3)
    Grotius1Stage = Stage("Grotius 1 LFB", GrotiusBooster, None, H1)
    GrotiusFamily = LVFamily("Grotius", "Like Leibnitz but with more than two LFBs.", GrotiusBooster, TartagliaStage)
    Grotius1 = LV("Grotius 1", GrotiusFamily, "Hotch-potch LV to place heavy comsat in GEO.", Grotius1Stage, TartagliaC, CentaurA, DeltaD)
    NapierD = Stage("Napier (1960)", Napier, XLR81BA11, "1960 configuration of Napier spaceplane; increased on-orbit endurance.")
    LeibnitzCH = LV("Leibnitz CH", LeibnitzC, "1960-standard Leibnitz/Napier.", LeibnitzCStage, TartagliaC, NapierD)

    launches = []
    def launch(name, y, m, d, lv, payload, dest, result):
        launches.append(Launch(name, date(y, m, d), lv, payload, dest, result))
    def paren(text):
        return Payload(None, None, text)

    launch("Davy 0",        1952,  8, 23, Davy0,        None, SO, 0)
    launch("Davy 1",        1952, 10,  6, Davy1,        None, SO, 0)
    launch("Davy 1A",       1952, 11, 23, Davy1,        None, SO, 0)
    launch("Davy 1B",       1953,  1, 19, Davy1B,       None, SO, 0)
    launch("Davy 0A",       1953,  2, 28, Davy0,        paren("Early film camera"), SO, 0)
    launch("Davy 2",        1953,  4, 24, Davy2,        paren("60kg SR core"), EO, -1)
    launch("Davy 2A",       1953,  6, 24, Davy2A,       paren("60kg SR core"), EO, 3)
    launch("Davy 2B",       1953,  8, 27, Davy2B,       Payload("Kepler 0", "First satellite to orbit the Earth!", "60kg SR core"), EO, 0)
    launch("Davy 2B₂",      1953, 10, 29, Davy2B,       paren("60kg SR core"), SO, 0)
    launch("Davy 0B",       1953, 12, 10, Davy0B,       paren("Early film camera"), SO, 0)
    launch("Davy 3",        1954,  4, 30, Davy3,        Payload("Kepler 1", None, "Explorer-1"), EO, -1)
    launch("Davy 3S",       1954,  6, 23, Davy3S,       paren("Explorer-1"), EO, 2)
    launch("Davy 3",        1954,  8, 22, Davy3,        Payload("Kepler 2", None, "Explorer-1"), EO, 0)
    launch("Davy 3S₂",      1954, 10, 14, Davy3S,       Payload("Kepler 3", None, "Explorer-1"), EO, 0)
    launch("Davy 3A",       1954, 12, 14, Davy3,        Payload("Bernoulli 1", "Atmospheric analysis satellite.", "Explorer-1"), EO, 0)
    launch("Newton 0",      1955,  1, 17, Newton0,      None, SO, -1)
    launch("Newton 0A",     1955,  3,  5, Newton1,      None, EO, 0)
    launch("Newton A1",     1955,  5,  7, Newton1,      paren("Scientific satellite"), EO, 1)
    launch("Davy 3SP",      1955,  6, 16, Davy3S,       paren("Explorer-1"), EPO, 2)
    launch("Newton A1A",    1955,  7,  8, Newton1A,     Payload("Kepler 4", "Scientific satellite"), EO, 0)
    launch("Newton A1B",    1955,  9, 13, Newton1A,     Payload("Kepler 5", "Scientific satellite"), HEO, 0)
    launch("Newton A1C",    1955, 12,  7, Newton1C,     paren("Controllable weather satellite"), EO, 2)
    launch("Davy 3T",       1956,  2, 22, Davy3T,       Payload("Kepler 6", "First polar-orbit satellite.", "Explorer-1"), EPO, 0)
    launch("Newton A1D",    1956,  3, 10, Newton1D,     Payload("Tycho 1", "First lunar mission!  Does not carry lunar-range comms."), LI, 0)
    launch("Newton A1C₂",   1956,  5, 19, Newton1C,     Payload("Bernoulli 2", "Controllable weather satellite."), LEO, 0)
    launch("Newton A1E",    1956,  9,  1, Newton1D,     Payload("Tycho 2", "Prototype lunar probe."), LF, 0)
    launch("Newton A2",     1956, 10, 25, Newton2,      Payload("Bernoulli 3", "Weather satellite."), LEO, 0)
    launch("Newton A2A",    1957,  1, 11, Newton2A,     Payload("Tycho 3", "Lunar probe with basic scientific instruments.  First pictures of lunar farside."), LF, 0)
    launch("Davy 3T₂",      1957,  1, 29, Davy3T,       Payload("Kepler 7", "Geodesy satellite."), SSO, 0)
    launch("Newton A2B",    1957,  2, 16, Newton2,      paren("Re-entry test vehicle; mass spectrometers"), LEO, 0)
    launch("Newton A2C",    1957,  3,  9, Newton2C,     Payload("Tycho 4"), LI, 0)
    launch("Newton A2D",    1957,  4,  9, Newton2,      paren("Photographic satellite with film return capsule"), LEO, 0)
    launch("Newton B2",     1957,  5,  2, NewtonB2,     Payload("Tycho 5"), LI, 0)
    launch("Newton B3",     1957,  6,  1, NewtonB3,     paren("Photographic satellite with film return capsule"), LEO, 0)
    launch("Newton A3",     1957,  6, 26, NewtonA3,     Payload("Bernoulli 4", "Weather satellite + magnetometer."), LEO, 0)
    launch("Newton A3A",    1957,  7, 11, NewtonA3A,    paren("Communications satellite"), EO, 3)
    launch("Newton B3A",    1957,  8, 13, NewtonB3A,    Payload("Tycho 6", "First lunar orbiter; good science return."), LO, 0)
    launch("Newton A3B",    1957,  9,  3, NewtonA3,     Payload("Bernoulli 5", "Weather satellite."), LEO, 0)
    launch("Tartaglia 0",   1957,  9,  9, Tartaglia0,   None, SO, 0)
    launch("Leibnitz AB1",  1957, 10, 15, LeibnitzAB,   Payload("Fermat 1", "First communications satellite."), EO, 0)
    launch("Newton A3B₂",   1957, 11,  4, NewtonA3,     Payload("Bernoulli 6", "Weather satellite."), LEO, 0)
    launch("Leibnitz AH1",  1958,  2, 27, LeibnitzAH,   Payload("NPF-1", "Test flight of Napier", "unmanned"), LEO, 3)
    launch("Newton A3C",    1958,  3,  7, NewtonA3,     Payload("Bernoulli 7", "Weather satellite."), LEO, 0)
    launch("Leibnitz AH2",  1958,  5, 26, LeibnitzAH,   Payload("NPF-2", "First human spaceflight.", "Timur Vasilyevykh"), LEO, 0)
    launch("Newton A4",     1958,  6,  4, NewtonA4,     Payload("Bernoulli 8", "Weather satellite."), LEO, 0)
    launch("Newton B4",     1958,  7,  3, NewtonB4Blue, Payload("Tycho 7", "Lunar magnetometry probe."), LO, 0)
    launch("Leibnitz BH1",  1958, 10, 25, LeibnitzBH1,  Payload("NEF-1", "Planned EVA mission; transatlantic abort due to Tartaglia failure.", "Vasily Sungatulin"), LEO, 2)
    launch("Newton B5",     1958, 10, 31, NewtonB5,     Payload("Fermat 2", "Communications satellite."), EO, 0)
    launch("Newton D4",     1958, 11, 11, NewtonD4,     paren("600kg lead ballast"), EO, 0)
    launch("Newton B4A",    1958, 12, 29, NewtonB4,     Payload("Pascal 1", "Second-generation weather satellite."), SSO, 0)
    launch("Leibnitz BH2",  1959,  2,  4, LeibnitzBH2,  Payload("NEF-1a", "EVA; 24 hours on orbit.", "Timur Vasilyevykh"), LEO, 0)
    launch("Newton B5B",    1959,  2, 10, NewtonB5,     Payload("Fermat 3", "Communications test satellite."), EO, 0)
    launch("Newton B5A",    1959,  4,  9, NewtonB5,     Payload("Pascal 2", "Second-generation weather satellite."), SSO, 0)
    launch("Leibnitz BB2",  1959,  6,  3, LeibnitzBB,   Payload("Copernicus 1", "First interplanetary probe."), VF, 0)
    launch("Leibnitz BH3",  1959,  7, 20, LeibnitzBH2,  Payload("NEF-2", "Rendezvous with Bernoulli 2.", "Vasily Sungatulin"), LEO, 0)
    launch("Newton B5C",    1959,  7, 28, NewtonB5,     paren("Photographic satellite with film return capsule"), LEO, 0)
    launch("Newton B5D",    1959,  8,  2, NewtonB5,     Payload("Mersenne 1", "Start of four-satellite comms network."), MEO, 0)
    launch("Leibnitz BB3",  1959,  9, 17, LeibnitzBB,   Payload("Fermat 4", "First comsat in Molniya orbit."), HEO, 0)
    launch("Newton D4A",    1959, 10,  4, NewtonD4,     Payload("Descartes 1", "RADAR mapping satellite."), EPO, 0)
    launch("Newton B5E",    1959, 10,  9, NewtonB5,     Payload("Mersenne 2", "Communications satellite, part of four-sat network."), MEO, 0)
    launch("Newton B5E₂",   1959, 11,  4, NewtonB5,     Payload("Mersenne 3", "Communications satellite, part of four-sat network."), MEO, 0)
    launch("Newton B5A",    1959, 11, 21, NewtonB5,     Payload("Pascal 3", "Second-generation weather satellite."), SSO, 0)
    launch("Newton B5E₃",   1959, 11, 24, NewtonB5,     paren("Mersenne communications satellite for four-sat network"), MEO, 2)
    launch("Locke 0",       1959, 12, 10, Locke0,       paren("8 tons lead ballast"), SO, 0)
    launch("Newton B6A",    1959, 12, 15, NewtonB6,     Payload("Mersenne 4", "Communications satellite, completes four-sat network."), MEO, 0)
    launch("Locke 1B1",     1959, 12, 27, Locke1B,      Payload("Fermat 5", "Communications test satellite."), EO, 0)
    launch("Newton B6",     1959, 12, 28, NewtonB6,     Payload("Pascal 4", "Second-generation weather satellite."), SSO, 0)
    launch("Tartaglia C0",  1960,  1,  5, TartagliaC0,  None, SO, -1)
    launch("Leibnitz BB4",  1960,  1, 21, LeibnitzBB4,  Payload("Tycho 8", "Lunar RADAR mapping."), LO, 0)
    launch("Tartaglia CA0", 1960,  1, 27, TartagliaCA0, None, SO, 0)
    launch("Leibnitz CB1",  1960,  2,  1, LeibnitzCB1,  Payload("Tycho 9", "Lunar film-return probe."), LF, 0)
    launch("Locke 1B2",     1960,  2,  3, Locke1B,      Payload("Boyle 1", "Sun-synchronous weather satellite."), SSO, 0)
    launch("Locke 1B3",     1960,  2, 10, Locke1B,      Payload("Kepler 8", "Scientific satellite."), LEO, 0)
    launch("Leibnitz CD1",  1960,  2, 19, LeibnitzCD,   Payload("Fermat 6", "First geostationary satellite; prototype comsat."), GEO, 0)
    launch("Locke 1B5",     1960,  2, 28, Locke1B,      paren("Communications test satellite."), EO, 2)
    launch("Leibnitz CB2",  1960,  3,  8, LeibnitzCB,   Payload("Fermat 7", "First comsat in Tundra orbit."), HEO, 0)
    launch("Locke 1B5₂",    1960,  3,  9, Locke1B,      Payload("Fermat 8", "Communications test satellite."), EO, 0)
    launch("Locke 1C0",     1960,  3, 31, Locke1C,      paren("1.5 tons lead ballast"), LEO, 0)
    launch("Leibnitz CB3",  1960,  4, 20, LeibnitzCB,   Payload("Tycho 9", "Lunar multispectral mapping."), LO, 0)
    launch("Locke 1B6",     1960,  4, 28, Locke1B,      Payload("Fermat 9", "Communications test satellite."), EO, 0)
    launch("Locke 1B7",     1960,  5, 13, Locke1B,      Payload("IRSat", "Scientific satellite."), HEO, 0)
    launch("Leibnitz CC1",  1960,  5, 14, LeibnitzCC,   Payload("Laplace 1", "First softlanding lunar probe.  Very limited science payload."), LS, 0)
    launch("Locke 1B4",     1960,  6,  7, Locke1B,      Payload("Descartes 2", "Biome mapping satellite."), EPO, 0)

    print "%d launches recorded" % (len(launches),)
    db = Database(launches)
    # Render text tables
    rend = TextRenderer(db)
    print rend.render_launches_per_year(1)
    print
    print rend.render_lv_families(2, 1)
    print
    print "Booster stages:"
    print rend.render_stage_families(2, 1, False)
    print
    print "Upper stages:"
    print rend.render_stage_families(2, 1, True)
    print
    print "Atmospheric engines:"
    print rend.render_engine_families(2, 1, False)
    print
    print "Vacuum engines:"
    print rend.render_engine_families(2, 1, True)

if __name__ == '__main__':
    test()
