from bs4 import BeautifulSoup
import xlsxwriter


def loadSeason(season):
    ecj_data = open(season,'r').read()
    soup = BeautifulSoup(ecj_data)
    
    list_of_teams_temp = soup.findAll("span", { "class" : "padl" })
    results_temp = soup.findAll("td", { "class" : "cell_sa score  bold" })
    
    list_of_teams = []
    for team in list_of_teams_temp:
        x = team.get_text();
        list_of_teams.append(x.encode("utf-8"))
    
    results = []
    for result in results_temp:
        if result.get_text()=="-":
            home_team_score = 0
            away_team_score = 0
        else:
            home_team_score,away_team_score = result.get_text().split(':')
        
        results.append(int(home_team_score))
        results.append(int(away_team_score))

    list_of_teams = list_of_teams[::-1] #reverses the order of columns because in the HTML file games were written from 34-th round to 1-st round
    results = results[::-1]
    
    return list_of_teams,results
    
    
def writeSeasonInExcel(file_name,list_of_teams,results):
    book = xlsxwriter.Workbook(file_name)
    sh = book.add_worksheet("Sheet 1")
    
    all_star_finished = 0
    for i in range(0,len(list_of_teams),2):
        if ("Germany" in list_of_teams[i+1]) or ("Bundesliga Stars" in list_of_teams[i]): # because the HTML file contains information about ALL-STAR game
            all_star_finished = all_star_finished + 2
            continue
        sh.write((i-all_star_finished)/2,0,list_of_teams[i+1])
        sh.write((i-all_star_finished)/2,1,list_of_teams[i])
        sh.write((i-all_star_finished)/2,2,results[i+1])
        sh.write((i-all_star_finished)/2,3,results[i])
    
    book.close()
    return

