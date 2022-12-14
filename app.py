from flask import Flask, send_from_directory, request, send_file, Response, jsonify, make_response
from flask_restful import Api
from flask_cors import CORS, cross_origin
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import requests
from bs4 import BeautifulSoup
import csv
import cleantext
import os
from os.path import exists
import anaylzeCSV as ancsv


app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
api = Api(app)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/image/<svgFile>') 
def serve_image(svgFile):
    return send_file(svgFile, mimetype='image/svg+xml')

@app.route('/filterupdate', methods=['GET','POST'])
def filterupdate():
    if (not exists("analyzed_data.csv")):
        response = make_response(jsonify({'message': "Image is being created. Please be patient."}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    if (exists("analyzed_histogram.svg")):
        os.remove("analyzed_histogram.svg")
    if (exists("analyzed_heatmap.svg")):
        os.remove("analyzed_heatmap.svg")
    try:
        month = request.json["month"]
    except:
        month = "";
    try:
        location = request.json["location"]
    except:
        location = ""
    if (location == "" and month == ""):
        ancsv.createHistogram('analyzed_data.csv',[[]])
        ancsv.createHeatMap('analyzed_data.csv',[[]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    elif (location == ""):
        ancsv.createHistogram('analyzed_data.csv',[['month', month]])
        ancsv.createHeatMap('analyzed_data.csv',[['month', month]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    elif (month == ""):
        ancsv.createHistogram('analyzed_data.csv',[['location', location]])
        ancsv.createHeatMap('analyzed_data.csv',[['location', location]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        ancsv.createHistogram('analyzed_data.csv',[['location', location], ['month', month]])
        ancsv.createHeatMap('analyzed_data.csv',[['location', location], ['month', month]])
        ancsv.plotClose()
        response = make_response(jsonify({'message': "Success"}), 200,)
        response.headers["Content-Type"] = "application/json"
        return response

@app.route("/remove", methods=['GET'])
@cross_origin()
def remove():
    if (exists("tutorial.csv")):
            os.remove("tutorial.csv")
    if (exists("analyzed_data.csv")):
            os.remove("analyzed_data.csv")
    if (exists("analyzed_histogram.svg")):
            os.remove("analyzed_histogram.svg")
    if (exists("analyzed_heatmap.svg")):
        os.remove("analyzed_heatmap.svg")
    return Response("Success", status=200, mimetype='application/text')

@app.route("/url", methods=['GET','POST'])
@cross_origin()
def setURL():

    # Declaration
    global comments, locations, months, amazonID, headers

    comments = []
    locations = []
    months = []
    headers = {  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", }

    # If the url is invalid, returns message
    URL = request.json["url"]

    if (URL.rfind("/dp/") == -1):
        if(URL==""):
            response = make_response(jsonify({"message": "Please enter a url."}), 200,)
        else:
            response = make_response(jsonify({"message": "The link is invalid. Please try another link."}), 200, )
    else:
        # Gives the Amazon ID
        amazonID = URL.split("/dp/")[1][0:10]
        response = make_response(jsonify({"message": "Collecting data from the US sites."}), 200, )
    response.headers["Content-Type"] = "application/json"
    return response

#
#   Web Scraping Begins Here
#

@app.route("/us-scraping", methods=['GET','POST'])       
@cross_origin()
def usScraping():
    def printPage(item):
        urlBeginning = "https://amazon.com/product-reviews/" + amazonID + "/ref=cm_cr_arp_d_paging_btm_next_"
        urlEnd = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urlBeginning +str(item)+ urlEnd + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            comments.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            locations.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            months.append(splitter[1].split('on')[-1])
    
    for page in range(50):
        printPage(page+1)

    response = make_response(jsonify({"message": "Collecting data from the Australian sites."}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/au-scraping", methods=['GET','POST'])       
@cross_origin()
def auScraping():
    def printPageAu(item):
        urlBeginning = "https://amazon.com.au/product-reviews/" + amazonID + "/ref=cm_cr_arp_d_paging_btm_next_"
        urlEnd = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urlBeginning +str(item)+ urlEnd + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
            
        for i in reviews:
            comments.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            locations.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            months.append(splitter[1].split('on')[-1])
    
    for page2 in range(2):
        printPageAu(page2+1)

    response = make_response(jsonify({"message": "Collecting data from the Canadian sites."}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/ca-scraping", methods=['GET','POST'])       
@cross_origin()
def caScraping():
    def printPageCA(item):
        urlBeginning = "https://amazon.ca/product-reviews/" + amazonID + "/ref=cm_cr_arp_d_paging_btm_next_"
        urlEnd = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urlBeginning +str(item)+ urlEnd + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            comments.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            locations.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            months.append(splitter[1].split('on')[-1])

    for page3 in range(50):
        printPageCA(page3+1)

    response = make_response(jsonify({"message": "Collecting data from the India sites."}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response
            
@app.route("/in-scraping", methods=['GET','POST'])       
@cross_origin()
def inScraping():
    def printPageIN(item):
        urlBeginning = "https://amazon.in/product-reviews/" + amazonID + "/ref=cm_cr_arp_d_paging_btm_next_"
        urlEnd = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urlBeginning +str(item)+ urlEnd + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            comments.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split('in')     
            locations.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True)) 
            months.append(splitter[1].split('on')[-1])
        
    for page4 in range(2):
        printPageIN(page4+1)

    response = make_response(jsonify({"message": "Collecting data from the UK sites."}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/uk-scraping", methods=['GET','POST'])       
@cross_origin()
def ukScraping():
    def printpageUK(item):
        urlBeginning = "https://amazon.co.uk/product-reviews/" + amazonID + "/ref=cm_cr_arp_d_paging_btm_next_"
        urlEnd = "?ie=UTF8&reviewerType=all_reviews&pageNumber="
        url =  (urlBeginning +str(item)+ urlEnd + str(item))
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        for i in reviews:
            comments.append(cleantext.clean(i.find('span', {'data-hook' : 'review-body'}).text, no_emoji=True))
            splitter = i.find('span', {'data-hook' : 'review-date'}).text.split(' in')    
            locations.append(cleantext.clean(splitter[1].split('on')[0], no_emoji=True))             
            months.append(splitter[1].split('on ')[-1])
    
    for page5 in range(10):
        printpageUK(page5+1)
    
    response = make_response(jsonify({"message": "Compiling all the site information into one location."}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response
    
# Creates the tutorial csv
@app.route("/tutorial-csv", methods=['GET','POST'])       
@cross_origin()
def tutorialCSV():
    with open('tutorial.csv', 'w', newline ='') as csvfile:
        fieldnames = ['number', 'entry', 'location', 'month']
        
        thewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        thewriter.writeheader()
        
        #DEBUG
        # print('DEBUG:',len(c))
        # print('DEBUG:',len(b))
        # print('DEBUG',len(d))
        num = 0
        for location in locations:
            num+=1
            
            #DEBUG
            # print('DEBUG:',num)
            # print('DEBUG',b[num-1])
            locations[num-1]
            month = months[num-1].split(" ")[1]   #splits the date and returns the month
            thewriter.writerow({'number':num, 'entry':comments[num-1], 'location':location, 'month':month  })
        
    response = make_response(jsonify({"message": "Analyzing the data and creating the graphs."}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

# Creates ONLY the anaylzed csv
@app.route("/analyzed-csv", methods=['GET','POST'])       
@cross_origin()
def analyzedCSV():
    ancsv.analyzeCSV([[]])
    ancsv.plotClose()

    response = make_response(jsonify({"message": "Complete!"}), 200,)
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run()