# -*- coding: utf-8 -8_

# config file format:
# [main] #program options section
# option_name = value
# ...
# [123456] # eve-api key section. section name is api keyID 6 digits
# vCode = string # eve-api verification code for api keyID specified in section name
# charIDs = integer # comma-separated character IDs
# charNames = string # comma-separated character Names.
#
# number of eve-api key sections unlimited. each api key must have own section 
#
import ConfigParser,os,re
class Config(ConfigParser.RawConfigParser):
    def __init__(self,filename="eve-iw.conf"):
        ConfigParser.RawConfigParser.__init__(self)
        self.reg = re.compile("^[0-9]{6}$")
        if os.path.exists(filename):
            self.read(filename)
            if len(self.sections()) == 0:
                self.createDefaultConfig(filename)
        else:
            self.createDefaultConfig(filename)
    def createDefaultConfig(self,filename):
        self.add_section("main")
        self.set("main", "minimize_on_close", "True")
        self.writeConfig(filename)
    def getApiData(self):
        result = list()
        apis = self.apiList()
        for api in apis:
            ids = self.get(api, "charIDs").split(",")
            names = self.get(api, "charNames").split(",")
            vCode = self.get(api,"vCode")
            if not len(ids) == len(names):
                continue
            result.append(dict(api=api,vCode=vCode,charNames=names,charIDs=ids))
        return result
    def apiList(self):
        sections = self.sections()
        apis = list()
        for section in sections:
            if self.reg.match(section):
                apis.append(section)
        return apis
    def writeConfig(self,filename):
        fp = open(filename,"wb")
        self.write(fp)
        fp.close()