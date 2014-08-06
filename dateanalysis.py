import urllib.request
import json
import os
import shutil
import copy

################################################################################
mode = input('Enter computer: ')
today = input('Enter today\'s date: ')
skipcities = input('Enter any city/cities the program should skip: ')

if mode == 'HASEE':
    dir = 'C:/Users/William/Dropbox/YGW/Airbnb/dates'
    backupdir = 'C:/Users/William/Dropbox/YGW/Airbnb/backup'
if mode == 'SURFACE':
    dir = 'C:/Users/william22/Dropbox/YGW/Airbnb/dates'
    backupdir = 'C:/Users/william22/Dropbox/YGW/Airbnb/backup'

todayday1 = int(today[4:5])
todayday2 = int(today[3:4])
if todayday1 == 0:
    yesterday = '08-' + str(todayday2 - 1) + '9'
else:
    yesterday = '08-' + str(todayday2) + str(todayday1 - 1)

os.chdir(dir)

success = {
    'sf_id.txt': False,
    'nyc_id.txt': False,
    'la_id.txt': False,
    'seattle_id.txt': False,
    'cha_id.txt': False,
    'seoul_id.txt': False
}

skipidx = []
skiplist = skipcities.split()
for i in range(0, len(skiplist)):
    if skiplist[i] == 'sf':
        success['sf_id.txt'] = True
        skipidx.append(0)
    if skiplist[i] == 'nyc':
        success['nyc_id.txt'] = True
        skipidx.append(1)
    if skiplist[i] == 'la':
        success['la_id.txt'] = True
        skipidx.append(2)
    if skiplist[i] == 'seattle':
        success['seattle_id.txt'] = True
        skipidx.append(3)
    if skiplist[i] == 'cha':
        success['cha_id.txt'] = True
        skipidx.append(4)
    if skiplist[i] == 'seoul':
        success['seoul_id.txt'] = True
        skipidx.append(5)

idfilenamelist = ['sf_id.txt', 'nyc_id.txt', 'la_id.txt', 'seattle_id.txt', 'cha_id.txt', 'seoul_id.txt']
cityfilenamelist = ['sf', 'nyc', 'la', 'seattle', 'cha', 'seoul']


def updateDates(idfilename, cityfilename, today):
    print('Updating ' + cityfilename + '...')
    startdates = ['2014-07-01', '2014-11-01']
    enddates = ['2014-10-31', '2015-01-31']

    f = open(idfilename, 'r')
    idlist = f.readlines()
    for i in range(0, len(idlist)):
        idlist[i] = idlist[i].strip()
    f.close()
    newidlist = copy.deepcopy(idlist)

    jsfilename = 'date_' + cityfilename + '_' + today + 'js.json'
    g = open(jsfilename, 'w')
    odfilename = 'date_' + cityfilename + '_' + today + 'od.json'
    h = open(odfilename, 'w')

    for i in range(0, len(idlist)):
        if i % 100 == 0: print('Updated ' + str(i) + ' entries..')
        id = idlist[i]
        jscalurl = 'https://www.airbnb.com/api/v1/listings/' + str(id) + '/calendar?start_date=' + startdates[0] + '&end_date=' + enddates[0] + '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en'
        odcalurl = 'https://www.airbnb.com/api/v1/listings/' + str(id) + '/calendar?start_date=' + startdates[1] + '&end_date=' + enddates[1] + '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=en'

        try:
            jscalendar = json.loads(urllib.request.urlopen(jscalurl).read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.getcode() == 503:
                print('HTTP ERROR 503; terminating script and restoring idlist ' + idfilename)
                day1 = int(today[-1:])
                day2 = int(today[3:4])
                if day1 == 0:
                    yesday1 = 9
                else:
                    yesday1 = day1 - 1
                if day1 == 0:
                    yesday2 = day2 - 1
                else:
                    yesday2 = day2
                yesterday = today[:2] + '-' + str(yesday2) + str(yesday1)
                yesfilename = 'date_' + cityfilename + '_' + yesterday + 'js.json'
                x = open(yesfilename, 'r')
                y = open(idfilename, 'w')
                jlist = x.readlines()
                for j in range(0, len(jlist)):
                    listingid = str(json.loads(jlist[j])['calendar']['listing_id'])
                    y.write(listingid)
                    y.write('\n')
                x.close()
                y.close()
                g.close()
                h.close()
                os.remove(jsfilename)
                os.remove(odfilename)
                return
            else:
                print('Room id ' + str(id) + ' can no longer be retrieved; error ' + str(e.getcode()) + ' Deleting room id..')
                newidlist.remove(id)
                continue
        except:
            print('Room id ' + str(id) + ' can no longer be retrieved for error other than HTTPError; Deleting room id..')
            newidlist.remove(id)
            continue
        try:
            odcalendar = json.loads(urllib.request.urlopen(odcalurl).read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.getcode() == 503:
                print('HTTP ERROR 503; terminating script and restoring idlist ' + idfilename)
                day1 = int(today[-1:])
                day2 = int(today[3:4])
                if day1 == 0:
                    yesday1 = 9
                else:
                    yesday1 = day1 - 1
                if day1 == 0:
                    yesday2 = day2 - 1
                else:
                    yesday2 = day2
                yesterday = today[:2] + '-' + str(yesday2) + str(yesday1)
                yesfilename = 'date_' + cityfilename + '_' + yesterday + 'js.json'
                x = open(yesfilename, 'r')
                y = open(idfilename, 'w')
                jlist = x.readlines()
                for j in range(0, len(jlist)):
                    listingid = str(json.loads(jlist[j])['calendar']['listing_id'])
                    y.write(listingid)
                    y.write('\n')
                x.close()
                y.close()
                g.close()
                h.close()
                os.remove(jsfilename)
                os.remove(odfilename)
                return
            else:
                print('Room id ' + str(id) + ' can no longer be retrieved; error ' + str(e.getcode()) + ' Deleting room id..')
                newidlist.remove(id)
                continue
        except:
            print('Room id ' + str(id) + ' can no longer be retrieved for error other than HTTPError; Deleting room id..')
            newidlist.remove(id)
            continue

        json.dump(jscalendar, g)
        g.write('\n')
        json.dump(odcalendar, h)
        h.write('\n')

    g.close()
    h.close()

    os.remove(idfilename)
    z = open(idfilename, 'w')
    for i in range(0, len(newidlist)):
        z.write(newidlist[i])
        z.write('\n')
    z.close()
    shutil.copy2(dir + '/' + idfilename, backupdir + '/' + idfilename)

    print('Successfully updated ' + cityfilename)
    success[idfilename] = True
    print('Number of ID: ' + str(len(newidlist)))


def compareDates(cityfilename, today, yesterday):
    print('Comparing ' + cityfilename + '...')
    fjs = open('date_' + cityfilename + '_' + today + 'js.json', 'r')
    fod = open('date_' + cityfilename + '_' + today + 'od.json', 'r')
    gjs = open('date_' + cityfilename + '_' + yesterday + 'js.json', 'r')
    god = open('date_' + cityfilename + '_' + yesterday + 'od.json', 'r')
    todayjslist = fjs.readlines()
    todayodlist = fod.readlines()
    yesjslist = gjs.readlines()
    yesodlist = god.readlines()
    fjs.close()
    fod.close()
    gjs.close()
    god.close()

    h = open(cityfilename + '_id.txt', 'r')
    idlist = h.readlines()
    for i in range(0, len(idlist)):
        idlist[i] = idlist[i].strip()
    h.close()

    x = open('id_res_'+cityfilename+'_'+today+'_'+yesterday+'.txt', 'w')
    y = open('id_canc_'+cityfilename+'_'+today+'_'+yesterday+'.txt', 'w')
    z = open('id_'+cityfilename+'_change_log_' + today + '_' + yesterday + '.txt', 'w')

    for i in range(0, len(idlist)):
        becameReserved = []
        becameAvailable = []
        id = idlist[i]

        todayjscal = json.loads(todayjslist[i])['calendar']
        todayodcal = json.loads(todayodlist[i])['calendar']
        if todayjscal['listing_id'] != int(id):
            print('Check id ' + str(id) + ' at line ' + str(i + 1) + '; does not match todayjs')
            return
        if todayodcal['listing_id'] != int(id):
            print('Check id ' + str(id) + ' at line ' + str(i + 1) + '; does not match todayod')
            return

        yesidx = i
        while json.loads(yesjslist[yesidx])['calendar']['listing_id'] != int(id):
            yesidx += 1

        yesjscal = json.loads(yesjslist[yesidx])['calendar']
        yesodcal = json.loads(yesodlist[yesidx])['calendar']
        if yesjscal['listing_id'] != int(id):
            print('Check id ' + str(id) + ' at line ' + str(i + 1) + '; does not match yesjs')
            return
        if yesodcal['listing_id'] != int(id):
            print('Check id ' + str(id) + ' at line ' + str(i + 1) + '; does not match yesod')
            return

        day = int(today[-2:])
        startidx = day + 31 - 1

        for j in range(startidx, 123):
            todayavail = todayjscal['dates'][j]['available']
            yesavail = yesjscal['dates'][j]['available']
            if todayavail == True and yesavail == False:
                becameAvailable.append(todayjscal['dates'][j]['date'])
            if todayavail == False and yesavail == True:
                becameReserved.append(todayjscal['dates'][j]['date'])

        for j in range(0, 92):
            todayavail = todayodcal['dates'][j]['available']
            yesavail = yesodcal['dates'][j]['available']
            if todayavail == True and yesavail == False:
                becameAvailable.append(todayodcal['dates'][j]['date'])
            if todayavail == False and yesavail == True:
                becameReserved.append(todayodcal['dates'][j]['date'])

        if (len(becameReserved) != 0):
            x.write(id)
            x.write('\n')
            z.write('Room '+str(id)+' has '+str(len(becameReserved))+' new reservations for: ')
            z.write('\n')
            for j in range(0, len(becameReserved)):
                z.write(becameReserved[j])
                z.write('\n')

        if len(becameAvailable) != 0:
            y.write(id)
            y.write('\n')
            z.write('Room '+str(id)+' has '+str(len(becameAvailable))+' new cancellations for: ')
            z.write('\n')
            for j in range(0, len(becameAvailable)):
                z.write(becameAvailable[j])
                z.write('\n')

    x.close()
    y.close()
    z.close()
    print('Completed comparing ' + cityfilename + '---------------------------------------------')


for i in range(0, 6):
    if i in skipidx:
        print('Skipped city ' + cityfilenamelist[i])
        continue
    updateDates(idfilenamelist[i], cityfilenamelist[i], today)

if success[idfilenamelist[0]] and success[idfilenamelist[1]] and success[idfilenamelist[2]] and success[idfilenamelist[3]] and success[idfilenamelist[4]] and success[idfilenamelist[5]]:
    for i in range(0, 6):
        compareDates(cityfilenamelist[i], today, yesterday)
else:
    print('Update terminated unsuccessfully. Calendars not compared...')

print('--------------------Completed--------------------')
