from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from numpy import linalg as geek
from scipy import linalg as la
import json
from json import JSONEncoder
import numpy as np
import copy
app = Flask(__name__)
app.config["DEBUG"] = True
@app.route('/todo/api/v1.0/rank', methods=['POST'])
def create_task():
    print("hi")
    if not request.json or not 'matrix' in request.json:
        abort(400)
    task = {
        'matrix': request.json['matrix'],
        'description': request.json['description'],
        'done': False,
        'l1': request.json['l1'],
        'l2': request.json['l2'],
        'l0': request.json['l0']
    }
    print(task['l0'])
    a=task['matrix']
    #a=[[1,0,0],[0,1,0],[0,0,1]]
    show=[]
    allmat=[]
    l=0
    if(len(a)<len(a[0])):
        l=len(a)
    else:
        l=len(a[0])
    i=0
    j=0
    while(i<l and j<l):
        if(a[i][j]==1):
            for m in range(i+1,len(a),1):
                b=a[m][j]
                str1="R"+str(m+1)+" = "+"R"+str(m+1)+" - ("+str(b)+"*"+"R"+str(i+1)+")"
                show.append(str1)
                for n in range(0,len(a[0]),1):
                    a[m][n]-=(b*a[i][n])
                    if(a[m][n]<0.00000000001 and -0.00000000001<a[m][n]):
                        a[m][n]=0.0
                for o in range(0,len(a),1):
                    a[o]=tuple(a[o])
                allmat.append(tuple(a))
                for o in range(0,len(a),1):
                    a[o]=list(a[o])
            i+=1
            j+=1
        
        else:
            if(a[i][j]==0):
                for m in range(i+1,len(a),1):
                    if(a[m][j]!=0):
                        print("Done")
                        str1="R"+str(i+1)+" <-> "+"R"+str(m+1)
                        show.append(str1)
                        for n in range(0,len(a[0]),1):
                            a[i][n],a[m][n]=a[m][n],a[i][n]
                        for o in range(0,len(a),1):
                            a[o]=tuple(a[o])
                        allmat.append(tuple(a))
                        for o in range(0,len(a),1):
                            a[o]=list(a[o])
                        break
                else:
                    j+=1
                if(i==l-1):
                    break
            else:
                for m in range(i+1,len(a),1):
                    b=a[m][j]
                    str1="R"+str(m+1)+" = "+"R"+str(m+1)+" - ("+str(b/a[i][j])+"*"+"R"+str(i+1)+")"
                    show.append(str1)
                    for n in range(0,len(a[0]),1):
                        a[m][n]-=((b/a[i][j])*a[i][n])
                        if(a[m][n]<0.00000000001 and -0.00000000001<a[m][n]):
                            a[m][n]=0.0
                    for o in range(0,len(a),1):
                        a[o]=tuple(a[o])
                    allmat.append(tuple(a))
                    for o in range(0,len(a),1):
                        a[o]=list(a[o])
                i+=1
                j+=1
    print(allmat)
    task['matrix']=allmat
    task['description']=show  
    task['l1']=len(allmat[0]) 
    task['l2']=len(show) 
    task['l0']=len(allmat[0][0])
    return jsonify({'task': task}), 201
CORS(app)
app.run()
