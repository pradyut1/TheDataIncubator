from flask import Flask, render_template, request, redirect,jsonify
import quandl
import operator

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/show_data')
def show_data():
  return render_template('show_data.html')
  
@app.route('/getdata')
def getdata():
	ticker = request.args.get('ticker')
	quandl.ApiConfig.api_key = '8qE_gvSFKhn9k4zfBLeE'
	data = quandl.get("WIKI/"+ticker,rows=30,returns="numpy")
	de=dict(enumerate(data))
	jsonfile={}
	for key in de:
		jsonfile[de[key][0].strftime("%Y-%m-%d %H:%M:%S")]=de[key][4]
	listofdict=[]
	for key in jsonfile:
	    listofdict.append({"label":key,"y":jsonfile[key]})
	listofdict.sort(key=operator.itemgetter('label'))
	return jsonify(listofdict)
	
if __name__ == '__main__':
  app.run()
