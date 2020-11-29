from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")


table = soup.find('div', attrs={'class':'lister list detail sub-list'}) 
row = table.find_all('div',attrs={'class':'lister-item mode-advanced'})


temp = [] #initiating a tuple

for i in range(0, len(row)):
    
    row = table.find_all('div',attrs={'class':'lister-item mode-advanced'})[i]

    
    judul = row.find('h3', attrs={'class':'lister-item-header'}).find('a').text
    
    if row.find('div', attrs={'class':'inline-block ratings-metascore'}) is None:
        metascores = '0'
    elif row.find('div', attrs={'class':'inline-block ratings-metascore'}).find('span').text:
        metascores = row.find('div', attrs={'class':'inline-block ratings-metascore'}).find('span').text.strip()
    
    rating = row.find('div', attrs={'class':'inline-block ratings-imdb-rating'}).find('strong').text
    
    votes = row.find('p', attrs={'class':'sort-num_votes-visible'}).find('span', attrs={'name':'nv'}).text
    
    temp.append((judul, rating, metascores, votes))
    
temp 


#change into dataframe
imdb = pd.DataFrame(temp, columns= ('Title', 'Ratings', 'Metascores', 'Votes'))

#insert data wrangling here
imdb = imdb.set_index('Title')
imdb[['Ratings','Metascores']] = imdb[['Ratings','Metascores']].astype('float64')
imdb['Votes'] = imdb['Votes'].str.replace(',', '')
imdb['Votes'] = imdb['Votes'].astype('int')

imdb7 = imdb.head(7).copy()
imdb7 = imdb7[::-1]

plt.style.use('seaborn-dark-palette')

#end of data wranggling 

@app.route("/")
def index(): 
	
	

	# generate plot1
	top7_r = imdb7['Ratings'].plot.barh(figsize = (11,2))
	top7_r.set_xlabel('Ratings Counts')
	top7_r.set_ylabel('Title Name')
	
	# Rendering plot1
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]
	
	# generate plot2
	top7_rm = imdb7[['Ratings','Metascores']].plot.barh(figsize = (11,2))
	top7_rm.set_ylabel('Title Name')
	
	# Rendering plot2
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_baru = str(figdata_png)[2:-1]
	
	# generate plot3
	top7_v = imdb7['Votes'].plot.barh(figsize = (11,2))
	top7_v.set_xlabel('Voters Counts')
	top7_v.set_ylabel('Title Name')
	
	# Rendering plot3
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_ketiga = str(figdata_png)[2:-1]    
	
	# render to html
	return render_template('index.html',
		#card_data = card_data, 
		plot_result=plot_result,
        plot_baru=plot_baru,
		plot_ketiga=plot_ketiga
		)


if __name__ == "__main__": 
    app.run(debug=True)

