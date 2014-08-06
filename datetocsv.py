import os
import re
from bs4 import BeautifulSoup
import csv

def getResId(today):
    os.chdir('C:/Users/william22/Dropbox/YGW/Airbnb/dates')

    resid = []
    filelist = os.listdir()

    for i in range(0, len(filelist)):
        if re.match('id_res_\w+_' + today, filelist[i]):
            f = open(filelist[i], 'r')
            idlist = f.readlines()
            for j in range(0, len(idlist)):
                id = idlist[j]
                if id not in resid:
                    resid.append(idlist[j].strip())
            f.close()

    return resid


def getCancId(today):
    os.chdir('C:/Users/william22/Dropbox/YGW/Airbnb/dates')

    cancid = []
    filelist = os.listdir()

    for i in range(0, len(filelist)):

        if re.match('id_canc_\w+_' + today, filelist[i]):
            f = open(filelist[i], 'r')
            idlist = f.readlines()
            for j in range(0, len(idlist)):
                id = idlist[j]
                if id not in cancid:
                    cancid.append(idlist[j].strip())
            f.close()

    return cancid


def checkAmen(amenstr, namenstr, name):
    return int((amenstr.find(name) >= 0) and (not namenstr.find(name) >= 0))


def getRoomFromId(idlist, today, updatetype):
    data = []
    features = ['id', 'name', 'type', 'address', 'review num', 'reference num', 'price', 'photo num', 'room type',
                'bed type', 'accom', 'bedroom num', 'bathroom num', 'bed num', 'extra price', 'min stay', 'weekly price',
                'monthly price', 'location', 'cancellation', 'cleaning fee', 'deposit', 'user id', 'member since',
                'resp rate', 'resp time', 'kitchen', 'internet', 'tv', 'essentials', 'heating', 'ac', 'washer', 'dryer',
                'parking', 'wifi', 'cable tv', 'breakfast', 'pets', 'pets live', 'fam friendly', 'events', 'smoking',
                'wheelchair', 'elevator', 'fireplace', 'intercom', 'doorman', 'shampoo', 'pool', 'hot tub', 'gym',
                'smoke detector', 'co detector', 'first aid', 'safety card', 'fire extinguisher', 'overall score',
                'accuracy score', 'communication score', 'cleanliness score', 'location score', 'check in score',
                'value score']

    os.chdir('C:/Users/william22/Desktop/YGW/Airbnb/htmls')
    filename = updatetype + '_data_' + today + '.csv'
    completefilename = os.path.join('C:/Users/william22/Dropbox/YGW/Airbnb/', filename)
    f = open(completefilename, 'w', newline='')
    dictwriter = csv.DictWriter(f, features)
    dictwriter.writeheader()

    for i in range(0, len(idlist)):
        id = idlist[i]
        htmlfilename = str(id) + '_html.txt'
        htmlfile = open(htmlfilename, 'rb')
        soup = BeautifulSoup(htmlfile)
        htmlfile.close()

        if soup.find('div', {'class':'subnav'}):
            if soup.title.string.find('Airbnb') >= 0:
                print('Check id ' + str(id) + ' HTML WEIRDD')
                continue
            listing = {}
            listing['id'] = id
            listing['name'] = soup.find('h1', {'itemprop': 'name'}).string.strip()
            try:
                for elem in soup(text=re.compile(r'Property type: ')):
                    listing['type'] = elem.parent.find('strong').text
            except:
                listing['type'] = ''
            listing['address'] = soup.findAll('div', {'id': 'hover-card'})[0].text.strip()
            try:
                listing['review num'] = soup.findAll('span', {'class': 'badge-pill-count'})[0].text
            except:
                listing['review num'] = 0
            try:
                listing['reference num'] = soup.findAll('span', {'class': 'badge-pill-count'})[1].text
            except:
                listing['reference num'] = 0
            listing['price'] = soup.find('div', {'id': 'price_amount'}).string.strip()
            try:
                listing['photo num'] = len(
                    soup.find('ul', {'class': 'slideshow-thumbnails thumbnails-slide-panel'}).find_all('li'))
            except:
                listing['photo num'] = 0
            listing['room type'] = soup.findAll('div', {'class': 'row row-condensed text-muted text-center'})[1].contents[1].text.strip()

            try:
                for elem in soup(text=re.compile(r'Bed type: ')):
                    listing['bed type'] = elem.parent.find('strong').text
            except:
                listing['bed type'] = ''

            try:
                for elem in soup(text=re.compile(r'Accommodates: ')):
                    listing['accom'] = elem.parent.find('strong').text
            except:
                listing['accom'] = ''

            try:
                for elem in soup(text=re.compile(r'Bedrooms: ')):
                    listing['bedroom num'] = elem.parent.find('strong').text
            except:
                listing['bedroom num'] = ''

            try:
                for elem in soup(text=re.compile(r'Bathrooms: ')):
                    listing['bathroom num'] = elem.parent.find('strong').text
            except:
                listing['bathroom num'] = ''

            try:
                for elem in soup(text=re.compile(r'Beds: ')):
                    listing['bed num'] = elem.parent.find('strong').text
            except:
                listing['bed num'] = ''

            try:
                for elem in soup(text=re.compile(r'Extra people: ')):
                    listing['extra price'] = elem.parent.find('strong').text
            except:
                listing['extra price'] = ''

            try:
                for elem in soup(text=re.compile(r'Minimum Stay: ')):
                    listing['min stay'] = elem.parent.find('strong').text
            except:
                listing['min stay'] = ''

            try:
                for elem in soup(text=re.compile(r'Weekly Price: ')):
                    listing['weekly price'] = elem.parent.find('strong').text
            except:
                listing['weekly price'] = ''

            try:
                for elem in soup(text=re.compile(r'Monthly Price: ')):
                    listing['monthly price'] = elem.parent.find('strong').text
            except:
                listing['monthly price'] = ''

            listing['location'] = soup.find('div', {'id': 'display-address'}).find('a').text.strip()

            try:
                for elem in soup(text=re.compile(r'Cancellation: ')):
                    listing['cancellation'] = elem.parent.find('strong').text
            except:
                listing['cancellation'] = ''

            try:
                for elem in soup(text=re.compile(r'Cleaning Fee: ')):
                    listing['cleaning fee'] = elem.parent.find('strong').text
            except:
                listing['cleaning fee'] = ''

            try:
                for elem in soup(text=re.compile(r'Security Deposit: ')):
                    listing['deposit'] = elem.parent.find('strong').text
            except:
                listing['deposit'] = ''

            try:
                for elem in soup(text=re.compile(r'View full profile')):
                    listing['user id'] = elem.parent.parent['href']
            except:
                listing['user id'] = ''
            listing['member since'] = \
                soup.find('div', {'class': 'row row-condensed row-space-2'}).contents[1].contents[3].text.strip()
            try:
                listing['resp rate'] = \
                    soup.find('div', {'class': 'row row-condensed row-space-2'}).contents[3].contents[1].contents[
                        1].text.strip()
            except:
                listing['resp rate'] = ''
            try:
                listing['resp time'] = \
                    soup.find('div', {'class': 'row row-condensed row-space-2'}).contents[3].contents[3].contents[
                        1].text.strip()
            except:
                listing['resp time'] = ''

            amen = soup.find('div', {'class': 'long-version'})
            amenstr = str.join(u'\n', map(str, amen))
            namen = amen.findAll('del')
            namenstr = str.join(u'\n', map(str, namen))
            listing['kitchen'] = checkAmen(amenstr, namenstr, 'Kitchen')
            listing['internet'] = checkAmen(amenstr, namenstr, 'Internet')
            listing['tv'] = checkAmen(amenstr, namenstr, 'TV')
            listing['essentials'] = checkAmen(amenstr, namenstr, 'Essentials')
            listing['heating'] = checkAmen(amenstr, namenstr, 'Heating')
            listing['ac'] = checkAmen(amenstr, namenstr, 'Air Conditioning')
            listing['washer'] = checkAmen(amenstr, namenstr, 'Washer')
            listing['dryer'] = checkAmen(amenstr, namenstr, 'Dryer')
            listing['parking'] = checkAmen(amenstr, namenstr, 'Free Parking on Premises')
            listing['wifi'] = checkAmen(amenstr, namenstr, 'Wireless Internet')
            listing['cable tv'] = checkAmen(amenstr, namenstr, 'Cable TV')
            listing['breakfast'] = checkAmen(amenstr, namenstr, 'Breakfast')
            listing['pets'] = checkAmen(amenstr, namenstr, 'Pets Allowed')
            listing['pets live'] = checkAmen(amenstr, namenstr, 'Pets live on this property')
            listing['fam friendly'] = checkAmen(amenstr, namenstr, 'Family/Kid Friendly')
            listing['events'] = checkAmen(amenstr, namenstr, 'Suitable for Events')
            listing['smoking'] = checkAmen(amenstr, namenstr, 'Smoking Allowed')
            listing['wheelchair'] = checkAmen(amenstr, namenstr, 'Wheelchair Accessible')
            listing['elevator'] = checkAmen(amenstr, namenstr, 'Elevator in Building')
            listing['fireplace'] = checkAmen(amenstr, namenstr, 'Indoor Fireplace')
            listing['intercom'] = checkAmen(amenstr, namenstr, 'Buzzer/Wireless Intercom')
            listing['doorman'] = checkAmen(amenstr, namenstr, 'Doorman')
            listing['shampoo'] = checkAmen(amenstr, namenstr, 'Shampoo')
            listing['pool'] = checkAmen(amenstr, namenstr, 'Pool')
            listing['hot tub'] = checkAmen(amenstr, namenstr, 'Hot Tub')
            listing['gym'] = checkAmen(amenstr, namenstr, 'Gym')
            listing['smoke detector'] = checkAmen(amenstr, namenstr, 'Smoke Detector')
            listing['co detector'] = checkAmen(amenstr, namenstr, 'Carbon Monoxide Detector')
            listing['first aid'] = checkAmen(amenstr, namenstr, 'First Aid Kit')
            listing['safety card'] = checkAmen(amenstr, namenstr, 'Safety Card')
            listing['fire extinguisher'] = checkAmen(amenstr, namenstr, 'Fire Extinguisher')

            try:
                stars = soup.find('div', {'id': 'reviews'}).findAll('div', {'class': 'foreground'})
                scores = [0, 0, 0, 0, 0, 0, 0]
                k = 0
                for star in stars:
                    score = 0
                    fullstar = star.findAll('i', {'class': 'icon icon-pink icon-beach icon-star'})
                    halfstar = star.findAll('i', {'class': 'icon icon-pink icon-beach icon-star-half'})
                    for s in fullstar:
                        score += 1
                    for s in halfstar:
                        score += 0.5
                    scores[k] = score
                    k += 1
            except:
                scores = [0, 0, 0, 0, 0, 0, 0]

            listing['overall score'] = scores[0]
            listing['accuracy score'] = scores[1]
            listing['communication score'] = scores[2]
            listing['cleanliness score'] = scores[3]
            listing['location score'] = scores[4]
            listing['check in score'] = scores[5]
            listing['value score'] = scores[6]

            data.append(listing)
            try:
                dictwriter.writerow(listing)
            except UnicodeEncodeError:
                try:
                    for key, value in listing.items():
                        if (isinstance(value, str)):
                            value = value.encode('utf-8')
                    dictwriter.writerow(listing)
                except UnicodeEncodeError:
                    pass
            if (len(data) % 100 == 0): print(len(data))

        else:
            if (soup.title.string.find('Airbnb') >= 0):
                print('Check id ' + str(id) + ' HTML WEIRDD')
                continue
            listing = {}
            listing['id'] = id
            listing['name'] = soup.find('div', {'id': 'listing_name'}).string.strip()
            try:
                listing['type'] = soup.find('a', {'class': 'property-type text-normal'}).string.strip()
            except:
                listing['type'] = ''
            listing['address'] = soup.find('span', {'id': 'display-address'}).string.strip()
            listing['review num'] = soup.find('span', {'class': 'badge-pill-count'}).string.strip()
            listing['reference num'] = ''
            listing['price'] = soup.find('div', {'id': 'price_amount'}).string.strip()
            try:
                listing['photo num'] = len(
                    soup.find('ul', {'class': 'slideshow-thumbnails thumbnails-slide-panel'}).findAll('li'))
            except:
                listing['photo num'] = 0

            try:
                for elem in soup(text=re.compile(r'Room type:')):
                    listing['room type'] = elem.parent.parent.contents[3].text
            except:
                listing['room type'] = ''

            try:
                for elem in soup(text=re.compile(r'Bed type:')):
                    listing['bed type'] = elem.parent.parent.contents[3].text
            except:
                listing['bed type'] = ''

            try:
                for elem in soup(text=re.compile(r'Accommodates:')):
                    listing['accom'] = elem.parent.parent.contents[3].text
            except:
                listing['accom'] = ''

            try:
                for elem in soup(text=re.compile(r'Bedrooms:')):
                    listing['bedroom num'] = elem.parent.parent.contents[3].text
            except:
                listing['bedroom num'] = ''

            try:
                for elem in soup(text=re.compile(r'Bathrooms:')):
                    listing['bathroom num'] = elem.parent.parent.contents[3].text
            except:
                listing['bathroom num'] = ''

            try:
                for elem in soup(text=re.compile(r'Beds:')):
                    listing['bed num'] = elem.parent.parent.contents[3].text
            except:
                listing['bed num'] = ''

            try:
                for elem in soup(text=re.compile(r'Extra people:')):
                    listing['extra price'] = elem.parent.parent.contents[3].text
            except:
                listing['extra price'] = ''

            try:
                for elem in soup(text=re.compile(r'Minimum Stay:')):
                    listing['min stay'] = elem.parent.parent.contents[3].text
            except:
                listing['min stay'] = ''

            try:
                for elem in soup(text=re.compile(r'Weekly Price:')):
                    listing['weekly price'] = elem.parent.parent.contents[3].text
            except:
                listing['weekly price'] = ''

            try:
                for elem in soup(text=re.compile(r'Monthly Price:')):
                    listing['monthly price'] = elem.parent.parent.contents[3].text
            except:
                listing['monthly price'] = ''

            try:
                for elem in soup(text=re.compile(r'Country:')):
                    country = elem.parent.parent.contents[3].text
            except:
                country = ''

            try:
                for elem in soup(text=re.compile(r'City:')):
                    city = elem.parent.parent.contents[3].text
            except:
                city = ''

            if (country == '' and city == ''):
                loc = ''
            elif (country == ''):
                loc = city
            elif (city == ''):
                loc = country
            else:
                loc = city + ',' + country
            listing['location'] = loc

            try:
                for elem in soup(text=re.compile(r'Cancellation:')):
                    listing['cancellation'] = elem.parent.parent.contents[3].text
            except:
                listing['cancellation'] = ''

            listing['cleaning fee'] = ''
            listing['deposit'] = ''

            listing['user id'] = soup.find('div', {'class': 'h2 text-special row-space-1'}).contents[1]['href']
            listing['member since'] = ''
            try:
                listing['resp rate'] = \
                    soup.findAll('div', {'class': 'row row-space-2'})[1].findAll('span', {'class': 'h3'})[1].string.strip()
            except:
                listing['resp rate'] = ''
            try:
                listing['resp time'] = \
                    soup.findAll('div', {'class': 'row row-space-2'})[2].findAll('span', {'class': 'h3'})[1].string.strip()
            except:
                listing['resp time'] = ''

            amen = soup.find('div', {'id': 'amenities-panel'})
            amenstr = str.join(u'\n', map(str, amen))
            namen = amen.findAll('span', {'class': 'text-muted'})
            namenstr = str.join(u'\n', map(str, namen))
            listing['kitchen'] = checkAmen(amenstr, namenstr, 'Kitchen')
            listing['internet'] = checkAmen(amenstr, namenstr, 'Internet')
            listing['tv'] = checkAmen(amenstr, namenstr, 'TV')
            listing['essentials'] = checkAmen(amenstr, namenstr, 'Essentials')
            listing['heating'] = checkAmen(amenstr, namenstr, 'Heating')
            listing['ac'] = checkAmen(amenstr, namenstr, 'Air Conditioning')
            listing['washer'] = checkAmen(amenstr, namenstr, 'Washer')
            listing['dryer'] = checkAmen(amenstr, namenstr, 'Dryer')
            listing['parking'] = checkAmen(amenstr, namenstr, 'Free Parking on Premises')
            listing['wifi'] = checkAmen(amenstr, namenstr, 'Wireless Internet')
            listing['cable tv'] = checkAmen(amenstr, namenstr, 'Cable TV')
            listing['breakfast'] = checkAmen(amenstr, namenstr, 'Breakfast')
            listing['pets'] = checkAmen(amenstr, namenstr, 'Pets Allowed')
            listing['pets live'] = checkAmen(amenstr, namenstr, 'Pets live on this property')
            listing['fam friendly'] = checkAmen(amenstr, namenstr, 'Family/Kid Friendly')
            listing['events'] = checkAmen(amenstr, namenstr, 'Suitable for Events')
            listing['smoking'] = checkAmen(amenstr, namenstr, 'Smoking Allowed')
            listing['wheelchair'] = checkAmen(amenstr, namenstr, 'Wheelchair Accessible')
            listing['elevator'] = checkAmen(amenstr, namenstr, 'Elevator in Building')
            listing['fireplace'] = checkAmen(amenstr, namenstr, 'Indoor Fireplace')
            listing['intercom'] = checkAmen(amenstr, namenstr, 'Buzzer/Wireless Intercom')
            listing['doorman'] = checkAmen(amenstr, namenstr, 'Doorman')
            listing['shampoo'] = checkAmen(amenstr, namenstr, 'Shampoo')
            listing['pool'] = checkAmen(amenstr, namenstr, 'Pool')
            listing['hot tub'] = checkAmen(amenstr, namenstr, 'Hot Tub')
            listing['gym'] = checkAmen(amenstr, namenstr, 'Gym')
            listing['smoke detector'] = checkAmen(amenstr, namenstr, 'Smoke Detector')
            listing['co detector'] = checkAmen(amenstr, namenstr, 'Carbon Monoxide Detector')
            listing['first aid'] = checkAmen(amenstr, namenstr, 'First Aid Kit')
            listing['safety card'] = checkAmen(amenstr, namenstr, 'Safety Card')
            listing['fire extinguisher'] = checkAmen(amenstr, namenstr, 'Fire Extinguisher')

            try:
                stars = soup.find('div', {'id': 'review-summary'}).findAll('div', {'class': 'foreground'})
                scores = [0, 0, 0, 0, 0, 0, 0]
                k = 0
                for star in stars:
                    score = 0
                    fullstar = star.findAll('i', {'class': 'icon icon-pink icon-beach icon-star'})
                    halfstar = star.findAll('i', {'class': 'icon icon-pink icon-beach icon-star-half'})
                    for s in fullstar:
                        score += 1
                    for s in halfstar:
                        score += 0.5
                    scores[k] = score
                    k += 1
            except:
                scores = [0, 0, 0, 0, 0, 0, 0]
            listing['overall score'] = scores[0]
            listing['accuracy score'] = scores[1]
            listing['communication score'] = scores[2]
            listing['cleanliness score'] = scores[3]
            listing['location score'] = scores[4]
            listing['check in score'] = scores[5]
            listing['value score'] = scores[6]

            data.append(listing)
            try:
                dictwriter.writerow(listing)
            except UnicodeEncodeError:
                try:
                    for key, value in listing.items():
                        if (isinstance(value, str)):
                            value = value.encode('utf-8')
                    dictwriter.writerow(listing)
                except UnicodeEncodeError:
                    pass
            if (len(data) % 100 == 0): print(len(data))

    print('Completed processing ' + filename + ', number of rooms: ' + str(len(data)))
    f.close()


today = input('Enter today\'s date: ')

getRoomFromId(getResId(today), today, 'res')
print('------------------Completed res data')
getRoomFromId(getCancId(today), today, 'canc')
print('------------------Completed canc data')
