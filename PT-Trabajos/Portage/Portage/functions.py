import datetime
import arcpy
import arcgisscripting
import time

'''
getMidPoint : computation of the mid point from gps data.
parameters: None
return:
    - x_mid : mid point x coordinate .
    - y_mid : mid point y coordinate .
'''
def getMidPoint(gpsDict):
    sum_x,sum_y = 0.,0.
    for dictPoint in gpsDict.values():
        sum_x += dictPoint["gpsPoint"][0]
        sum_y += dictPoint["gpsPoint"][1]
    n = len(gpsDict)
    return sum_x/n,sum_y/n

'''
utc2datetime : conversion from utcdate and utctime to datetime
parameters:
    - utcdate: a date (y,m,d) in datetime format.
    - strTime: a time (h,m,s) in string.
return:
    - a cambination of date and time in datetime format.
'''
def str2datetime(strTime):
    type_time = strTime[-2:]
    strTime = strTime[:-3]
    h,m,s = map(int,strTime.split(':'))
    if type_time == 'PM': h += 12
    return datetime.datetime(1,1,1,h,m,s)

'''
gpsDataDict: generate a dictionary from geo processing data.
parameters: None
return: None
'''
def gpsDataDict(gpsData):
    gpsDict = {}
    #dspeed y speed puede variar (traducir)      ||        change speed or dspeed if the set needs it
    with arcpy.da.SearchCursor(gpsData,["OBJECTID","X","Y","Time","Speed","NEAR_FID"]) as gpsCursor:
        for gpsRow in gpsCursor:
            gpsDict[gpsRow[0]] = {"gpsPoint":(gpsRow[1],gpsRow[2]),"time":str2datetime(gpsRow[3]),
                                  "dSpeed":gpsRow[4],"near_fid":gpsRow[5]}
    del gpsCursor
    return gpsDict

'''
route_solver : computing the route between two points.
parameters :
    - gpsDict : gps points dictionary.
    - snap_i  : current k_i point.
    - snap_j  : current k_j point.
    - i       : point index.
    - j       : point index.
return :
    - distance between snap points.
    - speed between snap points.
    - average speed between gps points.
'''
def route_solver(snap_i,snap_j,i,j,snapData,networkDataSet,currentRoute,currentRouteSearch,gpsDict,gp):
    upCursor = arcpy.da.UpdateCursor(snapData,"SHAPE@XY")
    ## current snap point k_i
    row = upCursor.next()
    row[0] = (snap_i[0],snap_i[1])
    upCursor.updateRow(row)
    ## current snap point k_j
    row = upCursor.next()
    row[0] = (snap_j[0],snap_j[1])
    upCursor.updateRow(row)
    del upCursor

    ## generating route k_i --> k_j
    routeLayer = gp.MakeRouteLayer_na(networkDataSet, currentRoute, "LENGTH").getOutput(0)
    gp.AddLocations_na(routeLayer, "Stops", snapData)
    ## solving route k_i --> k_j.
    gp.Solve_na(routeLayer)
    ## distance k_i --> k_j
    cursor = arcpy.da.SearchCursor(currentRouteSearch,["Total_Length"])
    row = cursor.next()
    distance = round(row[0],3)/1000. ## meters to km
    ## utcdate + utctime for k_i and k_j. 
    time_i = gpsDict[i]["time"]
    time_j = gpsDict[j]["time"]
    ## k_i and k_j speed.
    speed_i = gpsDict[i]["dSpeed"]
    speed_j = gpsDict[j]["dSpeed"]
    ## delta time k_i --> k_j.
    deltaTime = time_j - time_i
    ## travel speed k_i --> k_j.
    speedSnap = round(3600*distance/deltaTime.total_seconds(),3) ## km/sec is converted to km/hr
    ## average speed.
    averageSpeed = round(.5*(speed_i + speed_j),3)

    return distance,speedSnap,averageSpeed

'''
near_segments : search all segments which are inside of a determined radius.
parameters:
    - i           : point index.
    - snapDict    : dictionary of snap points.
    - gpsDict     : gps points dictionary.
return:
    - snapDict modified, where the near segments and corresponding snap
    points for the gps point i has been added.
'''
def near_segments(index,tempData,roadway,tempTable,searchRadius,gpsDict,snapDict):
    nearList = []
    upCursor = arcpy.da.UpdateCursor(tempData,"SHAPE@XY")
    row = upCursor.next()
    row[0] = (gpsDict[index]["gpsPoint"][0],gpsDict[index]["gpsPoint"][1])
    upCursor.updateRow(row)
    del upCursor

    arcpy.GenerateNearTable_analysis(tempData,roadway,tempTable,searchRadius,"LOCATION","ANGLE","ALL")
    with arcpy.da.SearchCursor(tempTable,["NEAR_DIST","NEAR_FID","NEAR_X","NEAR_Y"]) as tempCursor:
        for row in tempCursor:
            nearList.append(row)
    nearList.sort()
    ## print "id:{} -- point:{} -- nearList:{}".format(index,gpsDict[index]["gpsPoint"],nearList)
    del tempCursor
    
    #if nearList == []:
    #    nearList = near_segments(index,tempData,roadway,tempTable,searchRadius+1,gpsDict,snapDict)
    #else:
    #    snapDict[index] = nearList
    #    return snapDict

    snapDict[index] = nearList
    return snapDict


'''
acceptSnapPoints : generate a feature class with the accepted snap points.
parameters:
    - acceptDict: dictionary with the accepted snap points.
return: None
'''
def acceptSnapPoints(n,finalData,acceptDict,spatial_reference):
    arcpy.CreateFeatureclass_management(arcpy.env.workspace, finalData, "POINT", "", "DISABLED", "DISABLED", spatial_reference)
    finalCursor = arcpy.da.InsertCursor(finalData,["SHAPE@XY"])
    i = 1
    while i <= n:
        finalCursor.insertRow([acceptDict[i][0]])
        i += 1
    del finalCursor
    
    arcpy.AddField_management(finalData, "FID", "LONG")
    i = 1
    with arcpy.da.UpdateCursor(finalData,["FID"]) as finalCursor:
        for finalRow in finalCursor:
            finalRow[0] = acceptDict[i][1]
            finalCursor.updateRow(finalRow)
            i += 1
    del finalCursor

'''
clean : clean the feature classes used.
parameters: None
return: None
'''
def clean(snapData,tempData,assignData,tempTable,assignTable):
    if arcpy.Exists(snapData):
        arcpy.Delete_management(snapData)
    if arcpy.Exists(tempData):
        arcpy.Delete_management(tempData)
    if arcpy.Exists(tempTable):
        arcpy.Delete_management(tempTable)
    if arcpy.Exists(assignData):
        arcpy.Delete_management(assignData)
    if arcpy.Exists(assignTable):
        arcpy.Delete_management(assignTable)

'''
mapMatch : 
parameters:
    - j: id number of point.
return: None
'''

def solverForIAndJ(i,j,pointsToCheck,snapDict,acceptDict,tol_rs,snapData,networkDataSet,currentRoute,currentRouteSearch,gpsDict,gp,tempData,roadway,tempTable,searchRadius,n):
    
    forward = False

    print "Input i: " + str(i)
    print "Input j: " + str(j)

    fid_i = acceptDict[i][1] 
    snap_i = acceptDict[i][0] 

    if(j >= n):
        j = n
 
    while pointsToCheck > 0:
        if(len(snapDict[j]) > 0):
            # Revisar i -> street[j]
            if i < 1: #In case of being close to 1, without this if the program brakes because of boundries.
                    print "no more i for iterations" # going for j now
                    break 
            fid_i = acceptDict[i][1] 
            snap_i = acceptDict[i][0] 
            if fid_i > 0:
                #print "entro el j alt"
                print "Searching for alt j (" + str(j) + ")"
                for street in snapDict[j]:
                    fid_j = street[1]
                    snap_j = (street[2],street[3])
                    dist,snapSpeed,avSpeed = route_solver(snap_i,snap_j,i,j,snapData,networkDataSet,currentRoute,currentRouteSearch,gpsDict,gp)
                    if snapSpeed - tol_rs <= avSpeed <= snapSpeed + tol_rs:   
                        print "solution found!"
                        print "i: " +str(i)+ "  &   j: " +str(j)
                        return True, (snap_i, fid_i), (snap_j,fid_j), i, j

            # Revisar street[i] -> j
            if( i > 1):
                snap_im = acceptDict[i-1][0]
                fid_j = snapDict[j][0][1]
                snap_j = (snapDict[j][0][2],snapDict[j][0][3])
                set_FID_i = {fid_i}
                print "Searching for alt i (" + str(i) + ")"
                for street in snapDict[i]:
                    fid_i = street[1]
                    if(fid_i not in set_FID_i):
                        snap_i = (street[2],street[3])
                        dist_A,snapSpeed_A,avSpeed_A = route_solver(snap_im,snap_i,i - 1,i,snapData,networkDataSet,currentRoute,currentRouteSearch,gpsDict,gp)
                        dist_B,snapSpeed_B,avSpeed_B = route_solver(snap_i,snap_j,i,j,snapData,networkDataSet,currentRoute,currentRouteSearch,gpsDict,gp)
                        if (snapSpeed_A - tol_rs <= avSpeed_A <= snapSpeed_A + tol_rs) and (snapSpeed_B - tol_rs <= avSpeed_B <= snapSpeed_B + tol_rs):
                            print "solution found!"
                            print "i: " +str(i)+ "  &   j: " +str(j)
                            return True, (snap_i, fid_i), (snap_j,fid_j), i, j
                        



            if(not(forward)):
                i -= 1
                pointsToCheck -= 1          
                if i < 1: #In case of being close to 1, without this if the program brakes because of boundries.
                    print "no more i for iterations" # going for j now
                    break
                forward = True
            else:      
                j += 1
                if j >= n:
                    print "no more j for itereation, final point"
                    return False, (snap_i, fid_i), (gpsDict[n]['gpsPoint'],0), i, n
                pointsToCheck -= 1
                if j not in snapDict:
                    snapDict = near_segments(j,tempData,roadway,tempTable,searchRadius,gpsDict,snapDict)
                forward = False

        else:    
            movinPos = "j"
            j += 1
            if j >= n:
                print "no more j for itereation, final point"
                return False, (snap_i, fid_i), (gpsDict[n]['gpsPoint'],0), i, n
            pointsToCheck -= 1
            if j not in snapDict:
                snapDict = near_segments(j,tempData,roadway,tempTable,searchRadius,gpsDict,snapDict)
            forward = False

    print "didn't find matching i or j"
    return False, (snap_i, fid_i), (gpsDict[n]['gpsPoint'],0), i, j
                




def mapMatch(i,j,tol_rs,snapData,tempData,assignData,tempTable,assignTable,searchRadius,currentRoute,currentRouteSearch,networkDataSet,roadway,gpsDict,snapDict,acceptDict,gp,n_points,n):
    ## searching near segments for gps_j

    it = i

    realI = i
    realJ = j
    
    if j not in snapDict:
        snapDict = near_segments(j,tempData,roadway,tempTable,searchRadius,gpsDict,snapDict)
    
    # Here starts the routing   
    pointsToCheck = n_points

    solution, resultado_i, resultado_j, i, j = solverForIAndJ(i,j,pointsToCheck,snapDict,acceptDict,tol_rs,snapData,networkDataSet,currentRoute,currentRouteSearch,gpsDict,gp,tempData,roadway,tempTable,searchRadius,n)
        
    if(j == n and resultado_j[1] == 0):
        acceptDict[n] = resultado_j
    if solution:
        acceptDict[j] = resultado_j
        acceptDict[i] = resultado_i
        if j - i > 1:
            print "Routing..."
            assignList = []
            arcpy.MakeFeatureLayer_management(currentRouteSearch, "routeIn")
            arcpy.MakeFeatureLayer_management(roadway, "roadway")
            arcpy.SelectLayerByLocation_management("roadway", 'SHARE_A_LINE_SEGMENT_WITH', "routeIn")
            #arcpy.SelectLayerByLocation_management("roadway", 'SHARE_A_LINE_SEGMENT_WITH', "routeIn")   REVISAR

            for row in arcpy.da.SearchCursor("roadway",["OBJECTID"]):
                assignList.append(row[0])
            arcpy.SelectLayerByAttribute_management("roadway", "CLEAR_SELECTION")
            print "{}-->{} - Assign List:{}".format(i,j,assignList)
            for oid in range(i + 1,j):
                print "i:{} - j:{}".format(i,j)
                ## if the point is already in the snap dictionary,
                ## the closer point is assigned.
                oidIsAssign = False
                if oid in snapDict:
                    print "{} - near: {}".format(oid,snapDict[oid])
                    if len(snapDict[oid]) > 0:
                        fid_oid = snapDict[oid][0][1]
                    else:
                        fid_oid = 0
                    if fid_oid in assignList:
                        snap_oid = (snapDict[oid][0][2],snapDict[oid][0][3])
                        acceptDict[oid] = (snap_oid,fid_oid)
                        oidIsAssign = True
                    else:
                        oidIsAssign = False
                            
                ## if the point is not in the snap dictionary,
                ## from the fid in the route, the closer one is assigned.
                if not oidIsAssign:
                    upCursor = arcpy.da.UpdateCursor(assignData,"SHAPE@XY")
                    row = upCursor.next()
                    print oid
                    row[0] = (gpsDict[oid]["gpsPoint"][0],gpsDict[oid]["gpsPoint"][1])
                        
                    upCursor.updateRow(row)
                    del upCursor
                    arcpy.GenerateNearTable_analysis(assignData,"roadway",assignTable,"","LOCATION","NO_ANGLE","CLOSEST")# aqui busco la calle mas cercana
                    with arcpy.da.SearchCursor(assignTable,["NEAR_DIST","NEAR_FID","NEAR_X","NEAR_Y"]) as assignCursor:
                        row = assignCursor.next()
                        print row
                        acceptDict[oid] = ((row[2],row[3]),row[1]) 
            
    return acceptDict, realI, realJ, solution
                                                                                    
def compareFID(n,finalData,gpsDict):
    mmList = []
    with arcpy.da.SearchCursor(finalData,["FID"]) as finalCursor:
        for finalRow in finalCursor:
            mmList.append(finalRow[0])
    del finalCursor
    
    realList = []
    for i in range(1,n + 1):
        realList.append(gpsDict[i]["near_fid"] + 1)

    matchList = [i for i,j in zip(mmList,realList) if i == j]
    
    return len(matchList)