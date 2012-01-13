# -*- coding: utf-8 -*-
import os,eveapi,time,zlib,cPickle

class CacheHandler(object):
    def __init__(self,debug=False):
        self.debug = debug
        self.count = 0
        self.cache = {}
        self.cachedir = "./cache/" # TODO: move cache dir to user homedir
        self.logfile = self.cachedir+"log.txt"
        if not os.path.exists(self.cachedir):
            os.makedirs(self.cachedir)
    def log(self,text):
        fp = open(self.logfile,"a")
        fp.write(text)
        fp.close
    def retrieve(self, host, path, params):
        key = hash((host, path, frozenset(params.items())))
        self.count += 1
        cached = self.cache.get(key, None)
        if cached:
            cacheFile = None
        else:
            cacheFile = self.cachedir + str(key) + ".cache"
            if os.path.exists(cacheFile):
                self.log("%s: retrieving from disk" % path)
                f = open(cacheFile, "rb")
                cached = self.cache[key] = cPickle.loads(zlib.decompress(f.read()))
                f.close()

        if cached:
            if time.time() < cached[0]:
                self.log("%s: returning cached document" % path)
                return cached[1]

            self.log("%s: cache expired, purging!" % path)
            del self.cache[key]
            if cacheFile:
                os.remove(cacheFile)

        self.log("%s: not cached, fetching from server..." % path)
        return None

    def store(self, host, path, params, doc, obj):
        key = hash((host, path, frozenset(params.items())))

        cachedFor = obj.cachedUntil - obj.currentTime
        if cachedFor:
            self.log("%s: cached (%d seconds)" % (path, cachedFor))

            cachedUntil = time.time() + cachedFor

            cached = self.cache[key] = (cachedUntil, doc)

            cacheFile = self.cachedir + str(key) + ".cache"
            print "cache file %s, cacheDir %s, str(key) %s" % (cacheFile,self.cachedir,str(key))
            f = open(cacheFile, "wb")
            f.write(zlib.compress(cPickle.dumps(cached, -1)))
            f.close()
class Eapi(object):
    def __init__(self):
        self.eapi = eveapi.EVEAPIConnection(cacheHandler=CacheHandler(debug=True))
    def getCharacterSheet(self,keyID,vCode,charID):
        auth = self.eapi.auth(keyID=keyID,vCode=vCode)
        result = auth.char.CharacterSheet(characterID=charID)
        return result