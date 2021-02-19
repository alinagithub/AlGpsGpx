import os
import math
import datetime

def remove_prefix(prefix, text):
    return text[text.startswith(prefix) and len(prefix):]

class GpxSimpleType:

    def __init__(self, elementname, range=None):
        self.elementname=elementname
        self.range=range
        self.value=None

    def setValue(self, value):
        if self.range is not None:
            if value is not None:
                if value<self.range[0] or value>self.range[1]:
                    return False
        self.value = value
        return True

    def toString(self, elt_string, indent):
        if self.value is not None:
            elt_string.append("\t"*indent+"<"+str(self.elementname)+"> " + str(self.value) + " </"+str(self.elementname)+">")
            return 1
        return 0

class GpxComplexType:

    def __init__(self, elementname, attributs, subelements):
        self.elementname=elementname
        self.attributs=attributs
        self.subelements=subelements

    def setSubElt(self, key, value):
        self.subelements[key](value)

    def toString(self, elt_string, indent=0):
        subelt_nb=0

        elt_string.append("\t"*indent+"<"+str(self.elementname))
        for att in self.attributs:
            if self.attributs[att].value is not None:
                elt_string[-1]+=" "+self.attributs[att].elementname+"=\""+str(self.attributs[att].value)+"\""
        elt_string[-1]+=">"

        for subelt in self.subelements:
            subelt_nb+=self.subelements[subelt].toString(elt_string, indent+1)

        if subelt_nb>0:
            elt_string.append("\t"*indent+"</"+str(self.elementname)+">")
        else:
            del elt_string[-1]

        return subelt_nb

    def Load(self, namespace, root):
        for att in root.attrib:
            if remove_prefix(namespace,att) in self.attributs:
                self.attributs[remove_prefix(namespace,att)].value = root.attrib[att]

        for child in root:
            if remove_prefix(namespace,child.tag) in self.subelements:
                if isinstance(self.subelements[remove_prefix(namespace,child.tag)],GpxSimpleType):
                    self.subelements[remove_prefix(namespace,child.tag)].setValue(child.text)
                else:
                    self.subelements[remove_prefix(namespace,child.tag)].Load(namespace, child)

class copyrightType(GpxComplexType):
    def __init__(self):
        elementname = "copyright"
        attributs={"author":GpxSimpleType("author")}
        subelements={"year":GpxSimpleType("year"), 
                     "license":GpxSimpleType("license")}
        super().__init__(elementname, attributs, subelements)

class linkType(GpxComplexType):
    def __init__(self):
        elementname = "link"
        attributs={"href":GpxSimpleType("href")}
        subelements={"text":GpxSimpleType("text"), 
                     "type":GpxSimpleType("type")}
        super().__init__(elementname, attributs, subelements)

class emailType(GpxComplexType):
    def __init__(self):
        elementname = "email"
        attributs={"id":GpxSimpleType("id"), 
                   "domain":GpxSimpleType("domain")}
        super().__init__(elementname, attributs, ())

class personType(GpxComplexType):
    def __init__(self,eltname="person"):
        elementname = eltname
        subelements={"name":GpxSimpleType("name"), 
                     "email":emailType(), 
                     "link":linkType()}
        super().__init__(elementname, (), subelements)

class boundsType(GpxComplexType):
    def __init__(self):
        elementname = "bounds"
        attributs={"minlat":GpxSimpleType("minlat", [-90, +90]), 
                   "minlon":GpxSimpleType("minlon",[-180, +180]), 
                   "maxlat":GpxSimpleType("maxlat",[-90, +90]), 
                   "maxlon":GpxSimpleType("maxlon",[-180, +180])}
        super().__init__(elementname, attributs, ())

class extensionsType(GpxComplexType):
    def __init__(self):
        elementname = "extensions"
        super().__init__(elementname, (), ())

class fixType(GpxSimpleType):
    def __init__(self):
        super().__init__("fix")
    
    def setValue(value):
        if value not in ('none','2d','3d','dgps','pps'):
            return false
        self.val = value

import datetime
class timeType(GpxSimpleType):
    def __init__(self):
        super().__init__("time")

    def setTime(self, Year,Month,Day,Hour,Min,Sec):
        d = datetime.datetime(Year,Month,Day,Hour,Min,Sec)
        self.value = str(d).replace('+00:00', 'Z')

class metadataType(GpxComplexType):
    def __init__(self):
        elementname = "metadata"
        subelements={"name":GpxSimpleType("name"), 
                     "desc":GpxSimpleType("desc"), 
                     "author":personType("author"),
                     "copyright":copyrightType(),
                     "link":linkType(),
                     "time":timeType(),
                     "keywords":GpxSimpleType("keywords"),
                     "bounds":boundsType(),
                     "extensions":extensionsType()}
        super().__init__(elementname, (), subelements)

class ptType(GpxComplexType):
    def __init__(self):
        elementname = "pt"
        attributs={"lat":GpxSimpleType("lat",0), 
                   "lon":GpxSimpleType("lon",0)}
        subelements={"ele":GpxSimpleType("ele"), 
                     "time":timeType()}
        super().__init__(elementname, attributs, subelements)

class wptType(GpxComplexType):
    def __init__(self, wpt=None):
        elementname = "wpt"
        attributs={"lat":GpxSimpleType("lat",[-90,+90]), 
                   "lon":GpxSimpleType("lon",[-180,+180])}
        subelements={"ele":GpxSimpleType("ele"), 
                     "time":timeType(),
                     "magvar":GpxSimpleType("magvar", [0, 360]),
                     "geoidheight":GpxSimpleType("geoidheight"),
                     "name":GpxSimpleType("name"),
                     "cmt":GpxSimpleType("cmt"),
                     "desc":GpxSimpleType("desc"),
                     "src":GpxSimpleType("src"),
                     "link":linkType(),
                     "sym":GpxSimpleType("sym"),
                     "type":GpxSimpleType("type"),
                     "fix":fixType(),
                     "sat":GpxSimpleType("sat"),
                     "hdop":GpxSimpleType("hdop"),
                     "vdop":GpxSimpleType("vdop"),
                     "pdop":GpxSimpleType("pdop"),
                     "ageofdgpsdata":GpxSimpleType("ageofdgpsdata"),
                     "dgpsid":GpxSimpleType("dgpsid",[0, 1023]),
                     "extensions":extensionsType()}
        super().__init__(elementname, attributs, subelements)
        self.copy(wpt)

    def copy(self, wpt):
        if wpt is not None:
            self.attributs = wpt.attributs.copy()
            self.subelements = wpt.subelements.copy()

class rteptType(wptType):
    def __init__(self, wpt=None):
        super().__init__()
        self.elementname = "rtept"
        self.copy(wpt)

class trkptType(wptType):
    def __init__(self, wpt=None):
        super().__init__()
        self.elementname = "trkpt"
        self.copy(wpt)

class elementCollection():
    def __init__(self):
        self.List=[]

    def toString(self, elt_string, indent):
        subelt_nb=0
        for item in self.List:
            subelt_nb+=item.toString(elt_string, indent)
        return subelt_nb

class waypointsType(elementCollection):
    def __init__(self):
        super().__init__()

class rtepointsType(elementCollection):
    def __init__(self):
        super().__init__()

class trkpointsType(elementCollection):
    def __init__(self):
        super().__init__()

class routeType(GpxComplexType):
    def __init__(self):
        elementname = "rte"
        subelements={"ele":GpxSimpleType("ele"), 
                     "name":GpxSimpleType("name"),
                     "cmt":GpxSimpleType("cmt"),
                     "desc":GpxSimpleType("desc"),
                     "src":GpxSimpleType("src"),
                     "link":linkType(),
                     "number":GpxSimpleType("number"),
                     "type":GpxSimpleType("type"),
                     "extensions":extensionsType(),
                     "routepoints":rtepointsType()}
        super().__init__(elementname, (), subelements)

    def Load(self, namespace, root):
        super().Load(namespace, root)

        for child in root:
            if remove_prefix(namespace,child.tag) == "rtept":
                self.subelements["routepoints"].List.append(rteptType())
                self.subelements["routepoints"].List[-1].Load(namespace, child)


class tracksegmentType(GpxComplexType):
    def __init__(self):
        elementname = "trkseg"
        subelements={"trackpoints":trkpointsType(), 
                     "extensions":extensionsType()}
        super().__init__(elementname, (), subelements)

    def Load(self, namespace, root):
        super().Load(namespace, root)

        for child in root:
            if remove_prefix(namespace,child.tag) == "trkpt":
                self.subelements["trackpoints"].List.append(rteptType())
                self.subelements["trackpoints"].List[-1].Load(namespace, child)

class tracksegmentsType(elementCollection):
    def __init__(self):
        super().__init__()

class trackType(GpxComplexType):
    def __init__(self):
        elementname = "trk"
        subelements={"name":GpxSimpleType("name"),
                     "cmt":GpxSimpleType("cmt"),
                     "desc":GpxSimpleType("desc"),
                     "src":GpxSimpleType("src"),
                     "link":linkType(),
                     "number":GpxSimpleType("number"),
                     "type":GpxSimpleType("type"),
                     "extensions":extensionsType(),
                     "tracksegments":tracksegmentsType()}
        super().__init__(elementname, (), subelements)

    def Load(self, namespace, root):
        super().Load(namespace, root)

        for child in root:
            if remove_prefix(namespace,child.tag) == "trkseg":
                self.subelements["tracksegments"].List.append(rteptType())
                self.subelements["tracksegments"].List[-1].Load(namespace, child)

class routesType(elementCollection):
    def __init__(self):
        super().__init__()

class tracksType(elementCollection):
    def __init__(self):
        super().__init__()


class GpxObject(GpxComplexType):

    def __init__(self):
        elementname = "gpx"
        attributs={"version":GpxSimpleType("version"), 
                   "creator":GpxSimpleType("creator")}
        subelements={"metadata":metadataType(), 
                     "waypoints":waypointsType(), 
                     "routes":routesType(), 
                     "tracks":tracksType(), 
                     "extensions":extensionsType()}
        attributs["version"].setValue("1.1 [1]")
        attributs["creator"].setValue("AlGpx_1.0")
        super().__init__(elementname, attributs, subelements)

    def Load(self, namespace, root):
        for child in root:
            if remove_prefix(namespace,child.tag) == "metadata":
                self.subelements["metadata"].Load(namespace, child)
            if remove_prefix(namespace,child.tag) == "wpt":
                self.subelements["waypoints"].List.append(wptType())
                self.subelements["waypoints"].List[-1].Load(namespace, child)
            elif remove_prefix(namespace,child.tag) == "rte":
                self.subelements["routes"].List.append(routeType())
                self.subelements["routes"].List[-1].Load(namespace, child)
            elif remove_prefix(namespace,child.tag) == "trk":
                self.subelements["tracks"].List.append(trackType())
                self.subelements["tracks"].List[-1].Load(namespace, child)

class GpsGpx():

    def __init__(self):
        self.gpx = GpxObject()

    def Reset(self):
        self.gpx = GpxObject()

    ########################################################
    # waypoints operations
    ########################################################

    #  get, set, get tag, add, copy

    ########################################################
    # route operations
    ########################################################
    #def NbRoutes(self):
    #    return len(self.gpx.subelements["waypoints"].List)

    # del, find, add, set name,... ou set tag (advanced)
    # distance, nb trpe points, find a way point or closest in route
    # replace, insert, move up/down/first/last
    # make from waypoint
    # make from track
    # make from waypoints at track locations
    # make from trackpoint closest to way point within max dist


    ########################################################
    # track operations
    ########################################################
    #def NbTracks(self):
    #    return len(self.gpx.subelements["waypoints"].List)

    # del, find, add, set name,... ou set tag (advanced)
    # distance, nb trpe points, find a way point or closest in route
    # replace, insert, move up/down/first/last
    # sparse 1,2,3 recipes, curvature based..., make from points close to waypoints


    ########################################################
    # util
    ########################################################
    def Print(self):
        # TO BE DONE
        a=0

    def Load(self, filename):
        import xml.etree.ElementTree as ET
        tree = ET.parse(filename)
        root = tree.getroot()
        namespace=""
        if len(root.tag.split('}'))>1:
            namespace = "{"+root.tag.split('}')[0].strip('{')+"}"
        if root.tag == namespace+"gpx":
            self.gpx.Load(namespace, root)

    def Save_as(self, filename):
        gpx_str = []
        self.gpx.toString(gpx_str)
        f = open(filename, "w")
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "\n")
        for l in gpx_str:
            f.write(l + "\n")
        f.close()

## DRAW?