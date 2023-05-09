from datetime import datetime
import json
import pickle
from click import Path
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    #return "Hello World"

#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,12)
    THIS_FOLDER = Path(__file__).parent.resolve()
    my_model_file = THIS_FOLDER / "model.pkl"    
    loaded_model = pickle.load(open(my_model_file,"rb"))
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        if len(request.form) != 0:
            to_predict_list = request.form.to_dict()
        elif len(request.data) != 0:
            to_predict_list = json.loads(request.data)
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        
        if int(result)==1:
            prediction='Income more than 50K'
        else:
            prediction='Income less that 50K'

        if len(request.form) != 0 :
            return render_template("result.html",prediction=prediction)
        else:
            return  prediction

# @app.route('/')
# def index():
#    print('Request for index page received')
#    return render_template('index.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/hello', methods=['POST'])
# def hello():
#    name = request.form.get('name')

#    if name:
#        print('Request for hello page received with name=%s' % name)
#        return render_template('hello.html', name = name)
#    else:
#        print('Request for hello page received with no name or blank name -- redirecting')
#        return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug=True)