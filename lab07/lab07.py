import random
from unittest import TestCase

################################################################################
# EXTENSIBLE HASHTABLE
################################################################################
class ExtensibleHashTable:

    def __init__(self, n_buckets=1000, fillfactor=0.5):
        self.n_buckets = n_buckets
        self.fillfactor = fillfactor
        self.buckets = [None] * n_buckets
        self.nitems = 0

    def find_bucket(self, key, buckets, n_buckets):
        # BEGIN_SOLUTION
        h = hash(key) % n_buckets
        index = 0
        #print(f"This is h: {h}")
        while buckets[h] and buckets[h][0] != key:
            index += 1
            h = (hash(key) + index) % n_buckets
        #print(f"This is new h: {h}")
        return h
        # END_SOLUTION

    def extend(self):
        newdata = [None] * 2 * self.n_buckets
        for el in self.buckets:
            if el:
                hnew = self.find_bucket(el[0], newdata, self.n_buckets*2)
                #print(f"This is the new hash: {hnew} and this is the old hash: {el[0]}")
                newdata[hnew] = (el[0], el[1])
                #print(f"This is the new bucket: {newdata[hnew]}")
        #print(newdata)
        self.n_buckets *= 2
        self.buckets = newdata

    def __getitem__(self,  key):
        # BEGIN_SOLUTION
        h = self.find_bucket(key, self.buckets, self.n_buckets)
        if self.buckets[h]:
            return self.buckets[h][1]
        else:
            raise KeyError
        # END_SOLUTION

    def __setitem__(self, key, value):
        # BEGIN_SOLUTION
        h = self.find_bucket(key, self.buckets, self.n_buckets)
        #print(f"This is the key: {key} and this is the value being paired with it: {value}")
        if self.nitems >= self.n_buckets * self.fillfactor:
            self.extend()
            h = self.find_bucket(key,self.buckets, self.n_buckets)
        self.buckets[h] = (key, value)
        #print(f"This is the bucket being set: {self.buckets[h]} and this is its hash: {h}")
        self.nitems += 1
        # END_SOLUTION

    def __delitem__(self, key):
        # BEGIN SOLUTION
        h = self.find_bucket(key, self.buckets, self.n_buckets)
        if self.buckets[h] and self.buckets[h][0] == key:
            self.buckets[h] = None
            self.nitems += -1

        # END SOLUTION

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except:
            return False

    def __len__(self):
        return self.nitems

    def __bool__(self):
        return self.__len__() != 0

    def __iter__(self):
        ### BEGIN SOLUTION
        i = 0
        while i < len(self.buckets):
            if self.buckets[i]:
                yield self.buckets[i][0]
            i += 1
        ### END SOLUTION

    def keys(self):
        return iter(self)

    def values(self):
        ### BEGIN SOLUTION
        i = 0
        while i < len(self.buckets):
            if self.buckets[i]:
                yield self.buckets[i][1]
            i += 1
        pass
        ### END SOLUTION

    def items(self):
        ### BEGIN SOLUTION
        i = 0
        while i < len(self.buckets):
            if self.buckets[i]:
                yield self.buckets[i]
            i += 1
        pass
        ### END SOLUTION

    def __str__(self):
        return '{ ' + ', '.join(str(k) + ': ' + str(v) for k, v in self.items()) + ' }'

    def __repr__(self):
        return str(self)

################################################################################
# TEST CASES
################################################################################
# points: 20
def test_insert():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100000)

    for i in range(1,10000):
        h[i] = i
        tc.assertEqual(h[i], i)
        tc.assertEqual(len(h), i)


    random.seed(1234)
    for i in range(1000):
        k = random.randint(0,1000000)
        h[k] = k
        tc.assertEqual(h[k], k)

    for i in range(1000):
        k = random.randint(0,1000000)
        h[k] = "testing"
        tc.assertEqual(h[k], "testing")

# points: 10
def test_getitem():
    tc = TestCase()
    h = ExtensibleHashTable()

    for i in range(0,100):
        h[i] = i * 2

    with tc.assertRaises(KeyError):
        h[200]


# points: 10
def test_iteration():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100)
    entries = [ (random.randint(0,10000), i) for i in range(100) ]
    keys = [ k for k, v in entries ]
    values = [ v for k, v in entries ]


    for k, v in entries:
        h[k] = v

    for k, v in entries:
        tc.assertEqual(h[k], v)

    tc.assertEqual(set(keys), set(h.keys()))
    tc.assertEqual(set(values), set(h.values()))
    tc.assertEqual(set(entries), set(h.items()))

# points: 20
def test_modification():
    tc = TestCase()
    h = ExtensibleHashTable()
    random.seed(1234)
    keys = [ random.randint(0,10000000) for i in range(100) ]

    for i in keys:
        h[i] = 0

    for i in range(10):
        for i in keys:
            h[i] = h[i] + 1

    for k in keys:
        tc.assertEqual(h[k], 10)

# points: 20
def test_extension():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100,fillfactor=0.5)
    nitems = 10000
    for i in range(nitems):
        h[i] = i

    tc.assertEqual(len(h), nitems)
    tc.assertEqual(h.n_buckets, 25600)

    for i in range(nitems):
        tc.assertEqual(h[i], i)


# points: 20
def test_deletion():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100000)
    random.seed(1234)
    keys = [ random.randint(0,1000000) for i in range(10) ]
    for k in keys:
        h[k] = 1

    for k in keys:
        del h[k]

    tc.assertEqual(len(h), 0)
    with tc.assertRaises(KeyError):
        h[keys[0]]

    with tc.assertRaises(KeyError):
        h[keys[3]]

    with tc.assertRaises(KeyError):
        h[keys[5]]

################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "*" + "\n" + f.__name__)

def say_success():
    print("SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_insert,
              test_iteration,
              test_getitem,
              test_modification,
              test_deletion,
              test_extension]:
        say_test(t)
        t()
        say_success()

if __name__ == '__main__':
    main()
