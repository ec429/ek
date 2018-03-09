#!/usr/bin/python2
# encoding: utf-8
"""Encyclopædia Kerbonautica

Launch library and vehicle/stage/engine database."""

from datetime import date
from nevow import tags as t
from nevow.flat import flatten
import nevow.entities
import urllib

class EngineFamily(object):
    def __init__(self, name, description, vac=False):
        self.name = name
        self.description = description
        self.vac = vac
        self.family = None
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
        self.family = None
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
        self.family = None
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

EA = Destination("Earth Atmosphere", "EA", "Ballistic trajectory which does not reach the Kármán line.")
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
HC = Destination("Heliocentric orbit", "HC", "Orbit around the Sun not encountering any other bodies.")
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

class Picture(object):
    def __init__(self, path, alt, caption=None):
        self.path = path
        self.alt = alt
        self._caption = caption
    @property
    def caption(self):
        if self._caption is None:
            return self.alt
        return self._caption
    @caption.setter
    def caption(self, value):
        self._caption = value

class Payload(object):
    def __init__(self, name, description=None, paren=None, pics=[]):
        self._name = name
        self.description = description
        self.paren = paren
        self.pics = pics
        self.launch = None
    @property
    def name(self):
        if self._name is None and self.paren is not None:
            return '[%s]' % (self.paren,)
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    def add_pic(self, pic):
        self.pics.append(pic)
    @property
    def launch_pic(self):
        if self.launch:
            return self.launch.launch_pic
        return None

class Launch(object):
    def __init__(self, name, when, lv, payload, dest, result, comments=None, pics=[]):
        """Result semantics:
        
        -2 = Scrub at T-0 (i.e., failure before launch clamps released)
        -1 = Mission failure (all stages worked but design error killed mission)
        0 = Success
        positive = number of failing stage
        tuple: [0] as above, remainder are further failing stages"""
        self.name = name
        self.date = when
        self.lv = lv
        self.payload = payload
        if self.payload and result != -2:
            self.payload.launch = self
        self.dest = dest
        self.result = result
        self.comments = comments
        self.pics = pics
    def add_pic(self, pic):
        self.pics.append(pic)
    @property
    def launch_pic(self):
        if self.pics:
            return self.pics[0]
        return None

class Database(object):
    def __init__(self, launches):
        self.launches = launches
        self.update()
    def add_lv(self, lv):
        self.lvs.setdefault(lv.name, {'lv': lv, 'success': 0, 'scrub': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}})
        if lv.name not in self.lv_tree:
            self.lv_tree[lv.name] = {}
        fam = getattr(lv, "family", None)
        if fam:
            self.add_lv(fam)[lv.name] = self.lv_tree[lv.name]
        return self.lv_tree[lv.name]
    def add_stage(self, stage):
        self.add_engine(stage.engine)
        self.stages.setdefault(stage.name, {'stage': stage, 'success': 0, 'scrub': 0, 'mission_failure': 0, 'lower_failure': 0, 'failure': 0, 'dest': {}})
        if stage.name not in self.stage_tree:
            self.stage_tree[stage.name] = {}
        fam = getattr(stage, "family", None)
        if fam:
            self.add_stage(fam)[stage.name] = self.stage_tree[stage.name]
        return self.stage_tree[stage.name]
    def add_engine(self, eng):
        self.engines.setdefault(eng.name, {'engine': eng, 'success': 0, 'scrub': 0, 'mission_failure': 0, 'lower_failure': 0, 'failure': 0, 'dest': {}})
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
            elif launch.result == -2:
                lv['scrub'] += 1
            elif launch.result < 0:
                lv['mission_failure'] += 1
            else:
                lv['failure'] += 1
            if launch.result != -2:
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
                    elif launch.result[0] == -2:
                        if not i:
                            st['scrub'] += not fails
                            en['scrub'] += stage.engine_count - fails
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
                    elif launch.result == -2:
                        if not i:
                            st['scrub'] += 1
                            en['scrub'] += stage.engine_count
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
                if launch.result != -2:
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
        for k in ('success', 'scrub', 'failure', 'mission_failure', 'lower_failure'):
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
        d = {'lv': self.lvs[name]['lv'], 'success': 0, 'scrub': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}}
        for n in [name] + fam:
            self.roll_family(d, self.lvs[n])
        return d
    def stage_family(self, name):
        fam = self.flatten_tree(self.stage_tree[name])
        d = {'stage': self.stages[name]['stage'], 'success': 0, 'scrub': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}}
        for n in [name] + fam:
            self.roll_family(d, self.stages[n])
        return d
    def engine_family(self, name):
        fam = self.flatten_tree(self.engine_tree[name])
        d = {'engine': self.engines[name]['engine'], 'success': 0, 'scrub': 0, 'mission_failure': 0, 'failure': 0, 'dest': {}}
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
        leaves = [l for l in leaves if count[l]]
        return sorted(leaves, key=lambda d:d.sort)
    def filter_launches(self, lv=None, stage=None, engine=None, year=None):
        lvf = self.flatten_tree({lv: self.lv_tree[lv]}) if lv else None
        stf = self.flatten_tree({stage: self.stage_tree[stage]}) if stage else None
        enf = self.flatten_tree({engine: self.engine_tree[engine]}) if engine else None
        def do_filter(l):
            if lvf is not None and l.lv.name not in lvf:
                return False
            if stf is not None and not any(st in [s.name for s in l.lv.stages] for st in stf):
                return False
            if enf is not None and not any(en in [s.engine.name for s in l.lv.stages] for en in enf):
                return False
            if year is not None and l.date.year != year:
                return False
            return True
        return filter(do_filter, self.launches)

class Renderer(object):
    def __init__(self, db):
        self.db = db
    def render_lv_families(self):
        raise NotImplementedError()
    def render_stage_families(self, maxdepth, maxdest, vac=None):
        raise NotImplementedError()
    def render_engine_families(self, maxdepth, maxdest, vac=None):
        raise NotImplementedError()
    def render_launches_per_year(self, maxdest):
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

class HtmlRenderer(Renderer):
    stylesheet = """
        table { border-collapse: collapse; border: 2px solid black; }
        th { border-top: 2px solid black; }
        td, th { border: 1px solid black; }
        td.num, th.num { text-align: right; }
        td.date { font-family: monospace; }
        .major { font-weight: bold; border-top: 2px solid black; }
    """
    def wrap_page(self, title, body):
        page = t.html[t.head[t.title[title + ' - Encyclopædia Kerbonautica'], t.style[self.stylesheet]],
                      t.body[t.h1[title], body]]
        return flatten(page)
    def show_dest(self, dest):
        return t.acronym(title="%s: %s" % (dest.name, dest.description))[dest.abbr]
    def show_payload(self, payload):
        if not payload:
            return 'None'
        if not payload.description:
            return str(payload.name)
        return t.acronym(title=payload.description)[payload.name]
    def table_lv_families(self, maxdepth, maxdest, root=None):
        if root:
            tree = {root: self.db.lv_tree[root]}
        else:
            tree = self.db.lv_family_tree
        lvs = dict((name, self.db.lv_family(name)) for name in self.db.lvs)
        dests = self.db.coalesce_dests(map(self.db.lv_family, self.db.flatten_tree(tree)), maxdest)
        head1 = t.tr[t.th(rowspan=2)["Name"], t.th(colspan=2)["Flight dates"], t.th(rowspan=2)["Success"], t.th(colspan=2)["Failed"], t.th(rowspan=2)["T-0 Scrub"], t.th(colspan=len(dests))["Destinations"]]
        head2 = t.tr[t.th["First"], t.th["Last"], t.th["Stage"], t.th["Mission"], [t.th(Class='num')[self.show_dest(d)] for d in dests]]
        rows = []
        for name, depth in self.db.counted_flatten_tree(tree, lvs):
            if depth < maxdepth:
                lv = lvs[name]
                def render_d(d):
                    c = sum(lv['dest'].get(n, 0) for n in self.db.dest_tree.keys() if n.member(d) and (n == d or n not in dests))
                    return str(c) if c else '-'
                name = lv['lv'].name
                rows.append(t.tr(Class='' if depth else 'major')[
                        t.td[[nevow.entities.nbsp] * depth, t.a(href='lv?name='+urllib.quote(name))[name]],
                        t.td(Class='date')[lv['first'].isoformat()],
                        t.td(Class='date')[lv['last'].isoformat()],
                        t.td(Class='num')[str(lv['success'] or '-')],
                        t.td(Class='num')[str(lv['failure'] or '-')],
                        t.td(Class='num')[str(lv['mission_failure'] or '-')],
                        t.td(Class='num')[str(lv['scrub'] or '-')],
                        [t.td(Class='num')[render_d(d)] for d in dests],
                        ])
        return t.table[head1, head2, rows]
    def render_lv_families(self, maxdepth, maxdest):
        return self.wrap_page("LV families", self.table_lv_families(maxdepth, maxdest))
    def table_stage_families(self, maxdepth, maxdest, vac=None, root=None):
        if root:
            tree = {root: self.db.stage_tree[root]}
        else:
            tree = self.db.stage_family_tree
        dests = self.db.coalesce_dests(map(self.db.stage_family, self.db.flatten_tree(tree)), maxdest)
        head1 = t.tr[t.th(rowspan=2)["Name"], t.th(rowspan=2)["Engine"], t.th(colspan=2)["Flight dates"], t.th(rowspan=2)["Success"], t.th(colspan=3)["Failed"], t.th(colspan=len(dests))["Destinations"]]
        head2 = t.tr[t.th["First"], t.th["Last"], t.th["Stage"], t.th["Lower"], t.th["Mission"], [t.th(Class='num')[self.show_dest(d)] for d in dests]]
        rows = []
        stages = dict((name, self.db.stage_family(name)) for name in self.db.stages)
        def render_engine(st):
            eng = t.a(href='engine?name='+urllib.quote(st.engine.name))[st.engine.name]
            if st.engine_count > 1:
                eng = ['%dx ' % (st.engine_count,), eng]
            return eng
        for name, depth in self.db.counted_flatten_tree(tree, stages):
            st = stages[name]
            if depth < maxdepth and (vac is None or st['stage'].vac == vac):
                def render_d(d):
                    c = sum(st['dest'].get(n, 0) for n in self.db.dest_tree.keys() if n.member(d) and (n == d or n not in dests))
                    return str(c or '-')
                name = st['stage'].name
                rows.append(t.tr(Class='' if depth else 'major')[
                        t.td[[nevow.entities.nbsp] * depth, t.a(href='stage?name='+urllib.quote(name))[name]],
                        t.td[render_engine(st['stage'])],
                        t.td(Class='date')[st['first'].isoformat()],
                        t.td(Class='date')[st['last'].isoformat()],
                        t.td(Class='num')[str(st['success'] or '-')],
                        t.td(Class='num')[str(st['failure'] or '-')],
                        t.td(Class='num')[str(st['lower_failure'] or '-')],
                        t.td(Class='num')[str(st['mission_failure'] or '-')],
                        [t.td(Class='num')[render_d(d)] for d in dests],
                        ])
        return t.table[head1, head2, rows]
    def render_stage_families(self, maxdepth, maxdest, vac=None):
        title = {None: "Stage families", False: "Booster stages", True: "Upper stages"}.get(vac)
        return self.wrap_page(title, self.table_stage_families(maxdepth, maxdest, vac=vac))
    def table_engine_families(self, maxdepth, maxdest, vac=None, root=None):
        if root:
            tree = {root: self.db.engine_tree[root]}
        else:
            tree = self.db.engine_family_tree
        dests = self.db.coalesce_dests(map(self.db.engine_family, self.db.flatten_tree(tree)), maxdest)
        head1 = t.tr[t.th(rowspan=2)["Name"], t.th(colspan=2)["Flight dates"], t.th(rowspan=2)["Success"], t.th(colspan=3)["Failed"], t.th(colspan=len(dests))["Destinations"]]
        head2 = t.tr[t.th["First"], t.th["Last"], t.th["Stage"], t.th["Lower"], t.th["Mission"], [t.th(Class='num')[self.show_dest(d)] for d in dests]]
        rows = []
        engines = dict((name, self.db.engine_family(name)) for name in self.db.engines)
        for name, depth in self.db.counted_flatten_tree(tree, engines):
            en = engines[name]
            if depth < maxdepth and (vac is None or en['engine'].vac == vac):
                def render_d(d):
                    c = sum(en['dest'].get(n, 0) for n in self.db.dest_tree.keys() if n.member(d) and (n == d or n not in dests))
                    return str(c) if c else '-'
                name = en['engine'].name
                rows.append(t.tr(Class='' if depth else 'major')[
                        t.td[[nevow.entities.nbsp] * depth, t.a(href='engine?name='+urllib.quote(name))[name]],
                        t.td(Class='date')[en['first'].isoformat()],
                        t.td(Class='date')[en['last'].isoformat()],
                        t.td(Class='num')[str(en['success'] or '-')],
                        t.td(Class='num')[str(en['failure'] or '-')],
                        t.td(Class='num')[str(en['lower_failure'] or '-')],
                        t.td(Class='num')[str(en['mission_failure'] or '-')],
                        [t.td(Class='num')[render_d(d)] for d in dests],
                        ])
        return t.table[head1, head2, rows]
    def render_engine_families(self, maxdepth, maxdest, vac=None):
        title = {None: "Engine families", False: "Atmospheric engines", True: "Vacuum engines"}.get(vac)
        return self.wrap_page(title, self.table_engine_families(maxdepth, maxdest, vac=vac))
    def render_launches_per_year(self, maxdest):
        dests = self.db.coalesce_dests(self.db.lvs.values(), maxdest)
        head1 = t.tr[t.th(rowspan=2)["Year"], t.th(rowspan=2)["Launches"], t.th(colspan=len(dests))["By destination"]]
        head2 = t.tr[[t.th[self.show_dest(d)] for d in dests]]
        rows = []
        for year, launches in sorted(self.db.launches_by_year.items()):
            by_dest = {}
            launches = [l for l in launches if l.result != -2]
            for launch in launches:
                by_dest[launch.dest] = by_dest.get(launch.dest, 0) + 1
            def render_d(d):
                c = sum(by_dest.get(n, 0) for n in self.db.dest_tree.keys() if n.member(d) and (n == d or n not in dests))
                return str(c) if c else '-'
            rows.append(t.tr[t.td(Class='date')[t.a(href='year?year=%d'%(year,))[year]], t.td(Class='num')[len(launches)], [t.td(Class='num')[render_d(d)] for d in dests]])
        tbl = t.table[head1, head2, rows]
        return self.wrap_page("Launches per year", tbl)
    def table_launch_history(self, **kwargs):
        head = t.tr[t.th["Name"], t.th["Date"], t.th["LV"], t.th["Payload"], t.th["Destination"], t.th["Result"]]
        rows = []
        for launch in self.db.filter_launches(**kwargs):
            def render_result(result):
                if isinstance(result, tuple):
                    return [render_result(result[0]), ' + stage %s failure' % (', '.join(map(str, result[1:])),)]
                if result == 0:
                    return 'Success'
                if result == -2:
                    return t.acronym(title="A failure occurred before launch clamps were released, so the launch attempt was abandoned and the vehicle rolled back.")['T-0 Scrub']
                if result < 0:
                    return 'Mission Failure'
                return 'Stage %d Failure' % (result,)
            rows.append(t.tr[t.td[launch.name],
                             t.td(Class='date')[launch.date.isoformat()],
                             t.td[t.a(href='lv?name='+urllib.quote(launch.lv.name))[launch.lv.name]],
                             t.td[self.show_payload(launch.payload)],
                             t.td[t.acronym(title=launch.dest.description)[launch.dest.name]],
                             t.td[render_result(launch.result)],
                             ])
        return t.table[head, rows]
    def launches_for_year(self, year=None):
        if year is None:
            raise Exception("No year specified")
        year = int(year)
        title = "Launches for %d" % (year,)
        body = [t.p[t.a(href='year?year=%d'%(year - 1,))['%d <'%(year - 1,)], ' ',
                    t.a(href='year?year=%d'%(year + 1,))['> %d'%(year + 1,)]],
                self.table_launch_history(year=year)]
        return self.wrap_page(title, body)
    def render_lv_info(self, name=None):
        if name not in self.db.lvs:
            raise Exception("No such LV '%s'"%(name,))
        lv = self.db.lvs[name]['lv']
        lvs = dict((name, self.db.lv_family(name)) for name in self.db.lvs)
        title = "LV '%s'"%(lv.name,)
        blocks = []
        if lv.family:
            blocks.append(t.p["Family: ", t.a(href='lv?name='+urllib.quote(lv.family.name))[lv.family.name]])
        blocks.append(t.p[lv.description])
        blocks.append(t.h2["Stages"])
        blocks.append(t.ol[[t.li[t.a(href='stage?name='+urllib.quote(stage.name))[stage.name]] for stage in lv.stages]])
        blocks.append(t.h2["Summary of Launches"])
        blocks.append(self.table_lv_families(2, 1, root=name))
        blocks.append(t.h2["Full Launch History"])
        blocks.append(self.table_launch_history(lv=name))
        return self.wrap_page(title, blocks)
    def render_stage_info(self, name=None):
        if name not in self.db.stages:
            raise Exception("No such stage '%s'"%(name,))
        st = self.db.stages[name]['stage']
        sts = dict((name, self.db.stage_family(name)) for name in self.db.stages)
        title = "Stage '%s'"%(st.name,)
        blocks = []
        if st.family:
            blocks.append(t.p["Family: ", t.a(href='stage?name='+urllib.quote(st.family.name))[st.family.name]])
        blocks.append(t.p["Upper stage." if st.vac else "Booster stage."])
        blocks.append(t.p[st.description])
        blocks.append(t.h2["Engine"])
        eng = t.a(href='engine?name='+urllib.quote(st.engine.name))[st.engine.name]
        if st.engine_count > 1:
            eng = ['%d× ' % (st.engine_count,), eng]
        blocks.append(t.p[eng])
        blocks.append(t.h2["Summary of Launches"])
        blocks.append(self.table_stage_families(2, 1, root=name))
        blocks.append(t.h2["Full Launch History"])
        blocks.append(self.table_launch_history(stage=name))
        return self.wrap_page(title, blocks)
    def render_engine_info(self, name=None):
        if name not in self.db.engines:
            raise Exception("No such engine '%s'"%(name,))
        en = self.db.engines[name]['engine']
        ens = dict((name, self.db.engine_family(name)) for name in self.db.engines)
        title = "Engine '%s'"%(en.name,)
        blocks = []
        if en.family:
            blocks.append(t.p["Family: ", t.a(href='engine?name='+urllib.quote(en.family.name))[en.family.name]])
        blocks.append(t.p["Vacuum engine." if en.vac else "Atmospheric engine."])
        blocks.append(t.p[en.description])
        blocks.append(t.h2["Used in the following stages:"])
        stages = [k for k,v in self.db.stages.items() if v['stage'].engine == en]
        blocks.append(t.ul[[t.li[t.a(href='stage?name='+urllib.quote(st))[st]] for st in stages]])
        blocks.append(t.h2["Summary of Launches"])
        blocks.append(self.table_engine_families(2, 1, root=name))
        blocks.append(t.h2["Full Launch History"])
        blocks.append(self.table_launch_history(engine=name))
        return self.wrap_page(title, blocks)

def test_html(db):
    # Render HTML tables
    html = HtmlRenderer(db)
    import os
    if not os.path.isdir('html'):
        os.mkdir('html')
    with open('html/lpy.html', 'w') as lpy:
        lpy.write(html.render_launches_per_year(2))
    with open('html/lvf.html', 'w') as lvf:
        lvf.write(html.render_lv_families(2, 1))
    with open('html/bsf.html', 'w') as bsf:
        bsf.write(html.render_stage_families(2, 1, False))
    with open('html/vsf.html', 'w') as vsf:
        vsf.write(html.render_stage_families(2, 1, True))
    with open('html/bef.html', 'w') as bef:
        bef.write(html.render_engine_families(2, 1, False))
    with open('html/vef.html', 'w') as vef:
        vef.write(html.render_engine_families(2, 1, True))

def serve_web(db, port):
    from twisted.web import server, resource, static
    from twisted.internet import reactor, endpoints
    import os.path
    class Page(resource.Resource):
        """Abstract base class for HTML pages."""
        isLeaf = True

        def flatten_args(self, request):
            for k in request.args.keys():
                v = request.args[k]
                if isinstance(v, list):
                    l = len(v)
                    if l == 1:
                        request.args[k] = v[0]
                    elif not l:
                        del request.args[k]

        def error(self, msg):
            return t.html[t.head[t.title['Encyclopædia Kerbonautica']],
                          t.body[t.h1["Error"],
                                 t.h2[msg]]]

    def path_in(p1, p2):
        # returns true if p1 is in the tree rooted at p2.  Allows to follow symlinks.
        p2 = os.path.join(os.path.abspath(p2), '')
        p1 = os.path.abspath(p1)
        return os.path.commonprefix([p1, p2]) == p2

    class PictureResource(Page):
        def render_GET(self, request):
            try:
                self.flatten_args(request)
                path = request.args['path']
                size = request.args.get('size', None)
                if not path_in(path, '.'):
                    raise Exception("Bad path, reaches outside root")
                f = open(path, "rb")
                assert size is None, "size argument not supported yet"
                # XXX We should probably do a mime-type check on the file, but KSP screenshots are always PNGs so this should work
                request.setHeader("content-type", "image/png")
                # XXX Strictly speaking we should probably mess around with a twisted.internet.interfaces.IPullProducer, but this will do for now
                return f.read()
            except Exception as e:
                request.setHeader("content-type", "text/html; charset=utf-8")
                return flatten(self.error(e.message))

    class Index(Page):
        def render_GET(self, request):
            self.flatten_args(request)
            page = t.html[t.head[t.title['Encyclopædia Kerbonautica']],
                          t.body[t.h1['Encyclopædia Kerbonautica'],
                                 t.ul[t.li[t.a(href='lpy')['Launches per year']],
                                      t.li[t.a(href='lvf')['Launch-vehicle families']],
                                      t.li[t.a(href='bsf')['Booster stages']],
                                      t.li[t.a(href='vsf')['Upper stages']],
                                      t.li[t.a(href='bef')['Atmospheric engines']],
                                      t.li[t.a(href='vef')['Vacuum engines']],
                                      ]
                                 ]]
            request.setHeader("content-type", "text/html; charset=utf-8")
            return flatten(page)

    class Renderer(Page):
        def __init__(self, func, *args, **kwargs):
            self.func = func
            self.args = args
            self.kwargs = kwargs
        def render_GET(self, request):
            request.setHeader("content-type", "text/html; charset=utf-8")
            try:
                return flatten(self.func(*self.args, **self.kwargs))
            except Exception as e:
                return flatten(self.error(e.message))

    class PageWithArgs(Page):
        def content(self, **kwargs):
            raise NotImplementedError()
        def render_GET(self, request):
            request.setHeader("content-type", "text/html; charset=utf-8")
            self.flatten_args(request)
            debug = request.args.pop('debug', 0)
            try:
                page = self.content(**request.args)
            except Exception as e:
                if debug:
                    raise
                return flatten(self.error(e.message))
            return flatten(page)

    class RendererWithArgs(PageWithArgs):
        def __init__(self, func, *args, **kwargs):
            self.func = func
            self.args = args
            self.kwargs = kwargs
        def content(self, **kwargs):
            k = dict(kwargs)
            k.update(self.kwargs)
            return self.func(*self.args, **k)

    rend = HtmlRenderer(db)
    root = resource.Resource()
    root.putChild('', Index())
    root.putChild('lpy', Renderer(rend.render_launches_per_year, 2))
    root.putChild('lvf', Renderer(rend.render_lv_families, 2, 1))
    root.putChild('bsf', Renderer(rend.render_stage_families, 2, 1, vac=False))
    root.putChild('vsf', Renderer(rend.render_stage_families, 2, 1, vac=True))
    root.putChild('bef', Renderer(rend.render_engine_families, 2, 1, vac=False))
    root.putChild('vef', Renderer(rend.render_engine_families, 2, 1, vac=True))
    root.putChild('lv', RendererWithArgs(rend.render_lv_info))
    root.putChild('stage', RendererWithArgs(rend.render_stage_info))
    root.putChild('engine', RendererWithArgs(rend.render_engine_info))
    root.putChild('year', RendererWithArgs(rend.launches_for_year))
    root.putChild('pic', PictureResource())
    ep = "tcp:%d"%(port,)
    endpoints.serverFromString(reactor, ep).listen(server.Site(root))
    reactor.run()

def test_text(db):
    # Render text tables
    rend = TextRenderer(db)
    print rend.render_launches_per_year(2)
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
