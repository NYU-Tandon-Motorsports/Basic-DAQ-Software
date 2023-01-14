# Sixfab - Reading GPS data with Python
# 2020


from time import sleep
import serial

portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"

def parseGPS(data):
    #print(data, end='') #prints raw data
    if data[0:6] != "$GPRMC":
        return None
    sdata = data.split(",")
    if sdata[2] == 'V':
        #print("\nNo satellite data available.\n")
        return (-1,-1,-1,-1,-1,-1)
    # print("-----Parsing GPRMC-----")
    time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
    lat = decode(sdata[3]) #latitude
    dirLat = sdata[4]      #latitude direction N/S
    lon = decode(sdata[5]) #longitute
    dirLon = sdata[6]      #longitude direction E/W
    speed = sdata[7]       #Speed in knots
    trCourse = sdata[8]    #True course
    date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6] #date
    variation = sdata[10]  #variation
    degreeChecksum = sdata[13] #Checksum
    dc = degreeChecksum.split("*")
    degree = dc[0]        #degree
    checksum = dc[1]      #checksum
    latitude = lat.split() # parsing latitude
    longitute = lon.split() # parsing longitute
    # print("\nLatitude: " + str(int(latitude[0]) + (float(latitude[2])/60)) + dirLat)
    # print("Longitute: " + str(int(longitute[0]) + (float(longitute[2])/60)) + dirLon)
    return (latitude, dirLat, longitute, dirLon, speed, time)
    # print("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s,True Course : %s, Date : %s, Magnetic Variation : %s(%s),Checksum : %s "%   (time,lat,dirLat,lon,dirLon,speed,trCourse,date,variation,degree,checksum))

  
def decode(coord):
    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

def testGPS():
    print("INFO: Connecting GPS Port..")
    try:
        serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1,rtscts=True, dsrdtr=True)
        serw.write('AT+QGPS=1\r'.encode())
        serw.close()
        sleep(1)
    except Exception as e:
        print("ERROR: Serial port connection failed.")
        print(e)

def set_candidates(candidates):
    global portwrite
    global port
    portwrite = candidates[2].device
    port = candidates[1].device