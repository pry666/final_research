from flask import Flask,render_template
from flask import redirect
from flask import url_for
from flask import request
import os
import subprocess

#utf-8
app = Flask(__name__)

master_ip = '0.0.0.0'

@app.route('/')
def begin():
    return render_template("begin.html")

@app.route('/mainboard',methods=['GET','POST'])
def mainboard():
    filedir = '/root/'
    if request.method=='POST':
       configfile = request.files['podconfigfile']
       configfile.save(os.path.join(filedir, configfile.filename))
       podpath = "/root/" + configfile.filename
       result = subprocess.getstatusoutput("kubectl apply -f" + podpath)
       status = result[0]
       message = result[1]
       if(status == 0 ):
           return render_template('board.html',message = "部署成功")
       else:
           return render_template('board.html',message = "部署失败，错误信息为: "+ message)
    return render_template('board.html')

@app.route('/gettoken')
def gettoken():
    gettoken = subprocess.getstatusoutput("kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')")
    message_t = gettoken[1]
    return render_template('gettoken.html', tokenmessage = message_t)

@app.route('/docker')
def docker():
    return redirect("http://106.75.100.186:3000")

@app.route('/kubernetes')
def kubernetes():
    return redirect("https://106.75.100.186:30001")

if __name__=="__main__":
    app.run()
