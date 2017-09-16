import requests
from bs4 import BeautifulSoup
import mechanize
import numpy as np

def WxHist(forecaster,school='uic'):
    
    """
    
    This function retrieves the history of a forecaster throughout the WxChallenge history. Current functionallity allows the 
    same username to be found on multiple schools (to accomidate for their undergraduate and graduate institution. Example
    would be:
    
    data = WxHist('forecasterID',['UndergradSchool','GraduateSchool'])
    
    NOT SUPPORTED: A changing forecastID, will add in future versions
    
    """

    keys = ['06-07','07-08','08-09','09-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17']
    rank1_s = np.zeros(len(keys))
    rank2_s = np.zeros(len(keys))
    cuml_score_s = np.zeros(len(keys))
    score_list = {}

    if len(school) > 1:
        print('in more than one school loop')
        for k in school:
            it = -1
            for j in keys:
                it = it + 1
                url = 'http://wxchallenge.com/challenge/cumulative_results.php'
                br = mechanize.Browser()
                br.set_handle_robots(False) # ignore robots
                br.open(url)
                br.select_form(name='CumulativeScoresForm')
                br.form['year'] = [j,]
                br.form['school'] = [k,]
                res = br.submit()
                content = res.read()
                soup = BeautifulSoup(content,'lxml')
                table = soup.find('table', {"id":"cumulative_forecasters_scores"})
                
                try:
                    trs = table.find_all('tr')
                except:
                    rank1 = np.nan
                    rank2 = np.nan
                    cuml_score = np.nan
                    scores = np.nan
                    if rank1_s[it] == 0. :
                        rank1_s[it] = rank1
                        rank2_s[it] = rank2
                        cuml_score_s[it] = cuml_score
                        score_list[it] = scores
                    continue
                    
                
                a = table.find('td', text=forecaster)
                if a is None:
                    rank1 = np.nan
                    rank2 = np.nan
                    cuml_score = np.nan
                    scores = np.nan
                    if rank1_s[it] == 0. :
                        rank1_s[it] = rank1
                        rank2_s[it] = rank2
                        cuml_score_s[it] = cuml_score
                        score_list[it] = scores
                    continue

                row = a.findParent()
                tr = row.find_all('td')
                try:
                    rank1 = float(tr[1].get_text())
                except:
                    rank1 = np.nan

                try:
                    rank2 = float(tr[2].get_text())
                except:
                    rank2 = np.nan

                cuml_score = float(tr[len(tr)-6].get_text())
                scores = np.array([])
                for i in np.arange(9,len(tr)-6,2):
                    try:
                        s = float(tr[i].get_text())
                    except:
                        s = np.nan
                    scores = np.append(scores,s)

                if  rank1_s[it] == 0 or np.isnan(rank1_s[it]):
                    rank1_s[it] = rank1
                    rank2_s[it] = rank2
                    cuml_score_s[it] = cuml_score
                    score_list[it] = scores
                continue
                
    else:
        k = school[0]
        it = -1
        for j in keys:
            it = it + 1
            url = 'http://wxchallenge.com/challenge/cumulative_results.php'
            br = mechanize.Browser()
            br.set_handle_robots(False) # ignore robots
            br.open(url)
            br.select_form(name='CumulativeScoresForm')
            br.form['year'] = [j,]
            br.form['school'] = [k,]
            res = br.submit()
            content = res.read()
            soup = BeautifulSoup(content,'lxml')
            table = soup.find('table', {"id":"cumulative_forecasters_scores"})
            trs = table.find_all('tr')
            a = table.find('td', text=forecaster)
            if a is None:
                rank1 = np.nan
                rank2 = np.nan
                cuml_score = np.nan
                scores = np.nan
                rank1_s[it] = rank1
                rank2_s[it] = rank2
                cuml_score_s[it] = cuml_score
                score_list[it] = scores
                continue

            row = a.findParent()
            tr = row.find_all('td')
            try:
                rank1 = float(tr[1].get_text())
            except:
                rank1 = np.nan

            try:
                rank2 = float(tr[2].get_text())
            except:
                rank2 = np.nan

            cuml_score = float(tr[len(tr)-6].get_text())
            scores = np.array([])
            for i in np.arange(9,len(tr)-6,2):
                try:
                    s = float(tr[i].get_text())
                except:
                    s = np.nan
                scores = np.append(scores,s)

            rank1_s[it] = rank1
            rank2_s[it] = rank2
            cuml_score_s[it] = cuml_score
            score_list[it] = scores
        
    data = {}
    data['rank_all'] = rank1_s
    data['rank_year'] = rank2_s
    data['Cuml'] = cuml_score_s
    data['scores'] = score_list
    data['it'] = it
    return data


def WxHist_Team(school=['uic']):
    
    """
    
    This function creates the past statistics through the history of the WxChallenge for the schools you provide.
    
    
    """
    
    keys = ['06-07','07-08','08-09','09-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17']


    ranks = {}
    scores = {}
    for k in school:
        it = -1
        rank_s = np.zeros(len(keys))
        score_s = np.zeros(len(keys))
        for j in keys:
            it = it + 1
            url = 'http://wxchallenge.com/challenge/cumulative_results.php'
            br = mechanize.Browser()
            br.set_handle_robots(False) # ignore robots
            br.open(url)
            br.select_form(name='CumulativeScoresForm')
            br.form['year'] = [j,]
            br.form['school'] = ['team',]
            res = br.submit()
            content = res.read()
            soup = BeautifulSoup(content,'lxml')
            table = soup.find('table', {"id":"cumulative_team_scores"})
            a = table.find('td', text=k)
            if a is None:
                rank = np.nan
                score = np.nan
                rank_s[it] = rank
                score_s[it] = score
                continue

            mom = a.find_parent()
            tds = mom.find_all('td')
            try:
                rank = float(tds[1].get_text())
            except:
                rank = np.nan

            try:
                score = float(tds[-2].get_text())
            except:
                score = np.nan

            rank_s[it] = rank
            score_s[it] = score

        ranks[k] = rank_s
        scores[k] = score_s
        
    data = {}
    data['rank'] = ranks
    data['score'] = scores
    return data


def Retrive_Error(forecaster,city_list,school,day):
    #FUNCTION
    frcstid = np.zeros([4,])
    day_list = np.ones(len(city_list),dtype=int)*8
    day_list[-1] = day
    it = -1
    for city in city_list:
        it = it + 1
        day = day_list[it]
        URLstr ='http://wxchallenge.com/history/results/'+season+'/'+city+'_results_'+school+'_day'       
        URLstr = URLstr + str(day) +'.html'
        HTML_Page = urllib.urlopen(URLstr).read()
        soup = BeautifulSoup(HTML_Page,"lxml")
        table = soup.find('table')
        tr = table.find('td', text=forecaster)
        td = tr.findAllNext('td')
        for i in np.arange(17,21,1):
            frcstid[i-17] = frcstid[i-17] + float(td[i].text)
    
    return frcstid

def Retrive_fcst(forecaster,city,school,day):
    #FUNCTION
    frcstid = np.zeros([4,])
    URLstr ='http://wxchallenge.com/history/results/'+season+'/'+city+'_results_'+school+'_day'       
    URLstr = URLstr + str(day) +'.html'
    HTML_Page = urllib.urlopen(URLstr).read()
    soup = BeautifulSoup(HTML_Page,"lxml")
    table = soup.find('table')
    tr = table.find('td', text=forecaster)
    td = tr.findAllNext('td')
    for i in np.arange(4,8,1):
        frcstid[i-4] = float(td[i].text)
    frcst_sc = np.array([float(td[24].text),float(td[25].text)])
    
    data = {}
    data['frcst'] = frcstid
    data['score'] = frcst_sc
    return data

def Retrive_score_array(forecaster,city,school,day):
    #FUNCTION
    city_score = np.zeros([day,])
    cuml_score =np.zeros([day,])
    rank = np.zeros([day,])
    for i in np.arange(0,day,1):
        URLstr ='http://wxchallenge.com/history/results/'+season+'/'+city+'_results_'+school+'_day'       
        URLstr = URLstr + str(i+1) +'.html'
        HTML_Page = urllib.urlopen(URLstr).read()
        soup = BeautifulSoup(HTML_Page,"lxml")
        table = soup.find('table')
        tr = table.find('td', text=forecaster)
        td = tr.findAllNext('td')
        city_score[i] = float(td[24].text)
        cuml_score[i] = float(td[25].text)
        rank[i] = float(td[26].text)
    
    data = {}
    data['city'] = city_score
    data['cuml'] = cuml_score
    data['rank'] = rank
    return data

def Retrive_consen(city,day):
    #FUNCTION
    school = 'bkp'
    frcstid = np.zeros([4,])
    URLstr ='http://wxchallenge.com/history/results/'+season+'/'+city+'_results_'+school+'_day'       
    URLstr = URLstr + str(day) +'.html'
    HTML_Page = urllib.urlopen(URLstr).read()
    soup = BeautifulSoup(HTML_Page,"lxml")
    table = soup.find('table')
    consen = table.find('td', text='CONSEN')
    td = consen.findAllNext('td')
    if td[0].text == 'bkp':
        td = td[34:]
    for i in np.arange(4,8,1):
        frcstid[i-4] = float(td[i].text)
    frcst_sc = np.array([float(td[24].text),float(td[25].text)])
    
    data = {}
    data['frcst'] = frcstid
    data['score'] = frcst_sc
    return data

