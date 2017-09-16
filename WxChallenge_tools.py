import requests
from bs4 import BeautifulSoup
import mechanize
import numpy as np

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
