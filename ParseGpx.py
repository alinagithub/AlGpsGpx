import sys
sys.path.insert(0, ".\gpsgpx")

from pygpx import *
import sys

def main():
    
    gpgp = GpsGpx()

    mygo = gpgp.gpx

    meta = mygo.subelements["metadata"]
    meta.subelements["name"].value="G. Weiffenbach and W. Guier"

    w1 = wptType()
    w1.attributs["lat"].value=45.514597
    w1.attributs["lon"].value=-73.592006
    w1.subelements["name"].value="1_wp"
    w1.subelements["type"].value="start"

    w2 = wptType()
    w2.attributs["lat"].value=48.251606
    w2.attributs["lon"].value=-69.640205
    w2.subelements["name"].value="2_wp"
    w2.subelements["type"].value="via"

    w3 = wptType()
    w3.attributs["lat"].value=49.406049
    w3.attributs["lon"].value=-67.413502
    w3.subelements["name"].value="3_wp"
    w3.subelements["type"].value="via"

    w4 = wptType()
    w4.attributs["lat"].value=50.196662
    w4.attributs["lon"].value=-66.376715
    w4.subelements["name"].value="4_wp"
    w4.subelements["type"].value="destination"

    wpt_list = mygo.subelements["waypoints"].List
    wpt_list.append(w2)
    wpt_list.append(w1)
    wpt_list.append(w4)
    wpt_list.append(w3)

    rw1 = rteptType(w1)
    rw2 = rteptType(w2)
    rw3 = rteptType(w3)
    rw4 = rteptType(w4)

    r1 = routeType()
    r1.subelements["name"].value="ma route 1"
    r1.subelements["routepoints"].List.append(rw1)
    r1.subelements["routepoints"].List.append(rw2)

    r2 = routeType()
    r2.subelements["name"].value="ma route 2"
    r2.subelements["routepoints"].List.append(rw3)
    r2.subelements["routepoints"].List.append(rw4)

    rte_list = mygo.subelements["routes"].List
    rte_list.append(r1)
    rte_list.append(r2)

    tw1 = trkptType(w1)
    tw2 = trkptType(w2)
    tw3 = trkptType(w3)
    tw4 = trkptType(w4)

    ts1 = tracksegmentType()
    ts1.subelements["trackpoints"].List.append(tw1)
    ts1.subelements["trackpoints"].List.append(tw2)
    
    ts2 = tracksegmentType()
    ts2.subelements["trackpoints"].List.append(tw3)
    ts2.subelements["trackpoints"].List.append(tw4)

    t1 = trackType()
    t1.subelements["name"].value="ma track 1"
    t1.subelements["tracksegments"].List.append(ts1)
    t1.subelements["tracksegments"].List.append(ts2)

    trk_list = mygo.subelements["tracks"].List
    trk_list.append(t1)

    GpxString = []
    mygo.toString(GpxString)

    print(GpxString)

    f = open("test.gpx", "w")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "\n")
    for l in GpxString:
        f.write(l + "\n")
    f.close()


    gpgpbis = GpsGpx()
    gpgpbis.Load("test.gpx")

    gpgptris = GpsGpx()
    gpgptris.Load("D:\\GPS\\PyGpx\\PyGpx\\tests\\test_data\\Cote-Nord.gpx")
    gpgptris.Save_as("D:\\GPS\\PyGpx\\PyGpx\\tests\\test_data\\Cote-Nord_TESTSAVE.gpx")

if __name__ == "__main__":
    main()
