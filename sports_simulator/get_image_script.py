from bs4 import BeautifulSoup
import requests




if __name__ == "__main__":
    url = "https://stats.nba.com/player/"+str(201935)
    response = requests.get(url)

    data = response.text
    #print(data)
    soup = BeautifulSoup(data,features='html.parser')

    img = soup.findAll('img')#, {'class': 'player_img'})
    for i in img:
        print(i)
    #img_url = img['src']
    #print(img_url)