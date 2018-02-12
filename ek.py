#!/usr/bin/python2
# encoding: utf-8
"""Encyclopædia Kerbonautica

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
Mercury = Destination("Mercury", "H", "Slow-rotating rocky innermost planet.  Lacking an atmosphere, temperatures on the day and night side reach opposite extremes.", IP) # 'H' for 'Hermes', to avoid confusion with Mars
HF = Destination("Mercury fly-by", "HF", "Trajectory which visits Mercury but does not capture into orbit or reach the surface.", Mercury)
Venus = Destination("Venus", "V", "The second planet of the Solar System, a rocky world with a thick atmosphere and a runaway greenhouse effect.", IP)
VF = Destination("Venus fly-by", "VF", "Trajectory which visits Venus but does not capture or enter the atmosphere.", Venus)
VO = Destination("Venus orbit", "VO", "Any orbit around Venus.", Venus)
VS = Destination("Venus surface", "VS", "Soft landing on the surface of Venus.", Venus)
Mars = Destination("Mars", "M", "Fourth rock from the Sun, the Red Planet has a thin but active atmosphere.", IP)
MF = Destination("Mars fly-by", "MF", "Trajectory which visits Mars but does not capture or enter the atmosphere.", Mars)
MO = Destination("Mars orbit", "MO", "Any orbit around Mars.", Mars)
Phobos = Destination("Phobos", "F", "Small potato orbiting Mars.", Mars) # 'F' for 'Fobos', to avoid confusion with Pluto
FF = Destination("Phobos fly-by", "FF", "Trajectory which passes near to Phobos but does not capture into orbit or reach the surface.", Phobos)
Jupiter = Destination("Jupiter", "J", "Largest planet of the solar system.  Gas giant.", IP)
JF = Destination("Jupiter fly-by", "JF", "Trajectory which visits Jupiter but does not capture or enter the atmosphere.", Jupiter)

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
                if isinstance(launch.result, tuple):
                    fails = len([r for r in launch.result if r == i + 1])
                    if fails:
                        st['failure'] += 1
                    if launch.result[0] == 0:
                        st['success'] += not fails
                        en['success'] += stage.engine_count - fails
                    elif launch.result[0] < 0 or launch.result[0] > i + 1:
                        st['mission_failure'] += not fails
                        en['mission_failure'] += stage.engine_count - fails
                    elif launch.result < i + 1:
                        st['lower_failure'] += not fails
                        en['lower_failure'] += stage.engine_count - fails
                    # else failure, handled already
                    en['failure'] += fails
                else:
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
                siblings = set(k for k in leaves if k.member(leaf.category)) if leaf.category else set()
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
