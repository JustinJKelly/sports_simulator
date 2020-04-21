from bs4 import BeautifulSoup
import requests    


def find_games():
    current = 20200312
    last = 20200415
    f = open('unplayed_games.txt', 'w')

    while current <= last:
        url = "https://www.cbssports.com/nba/schedule/"+str(current)
        response = requests.get(url)

        data = response.text
        soup = BeautifulSoup(data,features='html.parser')
        team_names = []
        games = []

        str_current = str(current)
        print("%s/%s/%s\n" % (str_current[4:6],str_current[6:],str_current[0:4]))
        f.write("%s/%s/%s\n" % (str_current[4:6],str_current[6:],str_current[0:4]))

        for span_tag in soup.findAll('span', {'class': 'TeamName'}):
            team_names.append((span_tag.find('a')).string)

        for i in range(0,len(team_names),2):
            team1 = team_names[i]
            team2 = team_names[i+1]
            game = [team1,team2]
            games.append(game)
            f.write("Away: %s  Home: %s\n" % (team1,team2))

        for game in games:
            print(game)

        f.write('\n')
        print('\n\n')
        
        if current == 20200331:
            current = 20200401
        else:
            current += 1

    f.close()


if __name__ == "__main__":
    find_games()
    


