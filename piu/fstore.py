'''File-based storage

See ``FStore`` documentation for details
'''

import gzip
import collections
import os, os.path as op

import tnetstring


class FStore(object):
    '''Storage, based on tnetstrings stored in gzipped files

    Usage::

      >>> s = Fstore('path')
      >>> i = s.new()
      >>> i['something'] = 'text'
      >>> i.save()
      >>> print i.id
      0
      >>> print i.path
      0/0.piu.gz
    '''
    def __init__(self, base, create=False):
        self.base = op.expandvars(op.expanduser(base))
        if not op.exists(self.base):
            if create:
                os.mkdir(self.base)
            else:
                raise ValueError('%s does not exist' % base)

        if not op.isdir(self.base):
            raise ValueError('%s is not a directory' % base)

        try:
            self.index = tnetstring.loads(self.open('index.gz').read())
        except IOError:
            self.index = {}

    # API methods

    def __getitem__(self, key):
        if key not in self.index:
            raise KeyError('%s does not exist' % key)
        return Item(key, self, self.index[key])

    def keys(self):
        return self.index.keys()

    def new(self, **kwargs):
        try:
            key = max(self.index.keys()) + 1
        except ValueError:
            key = 0
        item = Item(key, self, self.itempath(key))
        for k, v in kwargs.iteritems():
            item[k] = v
        self.index[key] = item.path
        return item

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.save()

    # service methods

    def open(self, path, mode='r', createdirs=False):
        if createdirs:
            try:
                os.makedirs(op.join(self.base, op.dirname(path)))
            except OSError:
                pass
        return gzip.open(op.join(self.base, path), mode)

    def itempath(self, key):
        return op.join(str(key // 1000), str(key) + '.piu.gz')

    def save(self):
        self.open('index.gz', 'w').write(tnetstring.dumps(self.index))

    def rebuildindex(self):
        for path, dirs, files in os.walk(self.base):
            basepath = path[len(self.base):].lstrip('/\\')
            if not basepath.isdigit():
                continue
            for fn in files:
                # 7 = len('.piu.gz')
                if fn.endswith('.piu.gz') and fn[:-7].isdigit():
                    self.index[int(fn[:-7])] = op.join(basepath, fn)
        self.save()


class Item(collections.MutableMapping):
    def __init__(self, key, fstore, path):
        self.id = key
        self.store = fstore
        self.path = path
        try:
            self.data = tnetstring.loads(fstore.open(path).read())
        except IOError:
            self.data = {}

    # implemented abstract methods

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        value = self.data[key]
        if isinstance(value, str):
            return value.decode('utf-8')
        return value

    def __setitem__(self, key, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    # other API

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.save()

    def save(self):
        (self.store.open(self.path, 'w', createdirs=True)
         .write(tnetstring.dumps(self.data)))
        self.store.save()
