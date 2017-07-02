import urllib2
from bs4 import BeautifulSoup
from matplotlib import dates
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import num2date,datestr2num
%matplotlib inline


def Scrape_Td(station,yearstart,yearend,daystart=1,dayend=32,monthstart=1,monthend=13,QC=True):

    td_tot = {}
    time_tot = {}
    it = -1
    for vYear in range(yearstart, yearend):
        print(vYear)
        it = it + 1
        td = np.array([])
        time = np.array([],dtype=object)
        for vMonth in range(monthstart,monthend):
            print(vMonth)   
            for vDay in range(daystart, dayend):
                # go to the next month, if it is a leap year and greater than the 29th or if it is not a leap year
                # and greater than the 28th
                if vYear % 4 == 0:
                    if vMonth == 2 and vDay > 29:
                        break
                else:
                    if vMonth == 2 and vDay > 28:
                        break
                # go to the next month, if it is april, june, september or november and greater than the 30th
                if vMonth in [4, 6, 9, 11] and vDay > 30:
                    break

                theDate = str(vYear) + "/" + str(vMonth) + "/" + str(vDay)
                urlstr = 'https://www.wunderground.com/history/airport/'+ station +'/' + theDate + '/DailyHistory.html'
                thepage = urllib2.urlopen(urlstr)
                soup = BeautifulSoup(thepage,'html.parser')
                weather_data  = soup.find(id='observations_details')


                try: 

                    a = weather_data.find_all('tr')

                    h1 = a[0]
                    h2 = h1.find_all('th')
                    headers = {}
                    for i in np.arange(0,len(h2),1):
                        headers[i] = h2[i].get_text()

                        if h2[i].get_text() == 'Dew Point':
                            index = i

                    for i in np.arange(1,len(a),1):
                        b = a[i]
                        c = b.find_all('td')

                        d = c[index].get_text()
                        if len(d) < 8:
                            td = np.append(td,np.nan)
                        elif len(d) > 8: 
                            td = np.append(td,float(d[0:5]))
                        elif len(d) == 8:
                            td = np.append(td,float(d[0:4]))

                        time = np.append(time,num2date(datestr2num(str(vYear)+'-'+str(vMonth)+'-'+str(vDay)+'-'+c[0].get_text())))

                except:
                    # If the web page is formatted improperly, signal that the page may need
                    # to be downloaded again.
                    try_again = True
                    if try_again:
                        print('Error with date {}'.format(theDate))
                        try_again = False
                    continue


        if QC:
            td[td == 32.0] = np.nan
            
        td_tot[it] = td
        time_tot[it] = time
    
    data = {}
    data['Td'] = td_tot
    data['time'] = time_tot
    
    return data
