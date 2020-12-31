from flask import Flask, request, abort,send_from_directory, make_response
from flask_pymongo import PyMongo
import json
import os
import shutil
import datetime
from TestDataProcess import Main
from MutantSetReduce import MSRMain

# 实例化app
application = Flask(import_name=__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db


def request_parse(req_data):
    '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST' or req_data.method == 'OPTIONS':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data

def getData(results,page,filename):
    startId=(page-1)*results
    endId=startId+results
    with open(filename, 'r') as f:
        data = json.load(f)
        res=data['results']
        if endId-1>len(res):
            endId=len(res)
        jsondic = {}
        newres=[]
        for i in range(startId,endId):
            newres.append(res[i])
        jsondic['results']=newres
        jsondic['length']=len(res)
        return json.dumps(jsondic, ensure_ascii=False)

# 模型获取
@application.route('/api/model/query', methods=["GET", "POST"])
def query():
    data = request_parse(request)
    res={}
    username = data.get("username")
    # 指定查询
    myquery = {"username": username}
    mydoc=db.usersites.find(myquery)
    models=[]
    for x in mydoc:
        models=x['models']
        break
    res['models']=models
    rst = make_response(json.dumps(res, ensure_ascii=False))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Content-Type'] = 'application/json'
    return rst, 201

BASE_DIR=os.path.abspath(os.path.dirname(__file__))
# zip文件上传，解压缩文件
@application.route("/api/upload", methods=["GET", "POST","OPTIONS"])
def upload():
    print(request.method)
    obj = request.files.get("file")
    if obj is None:
        rst = make_response("no content")
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
        allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        rst.headers['Access-Control-Allow-Credentials'] = 'true'
        return rst, 204
    print(obj)  # POST /upload HTTP/1.1<FileStorage: 'test.zip' ('application/x-zip-compressed')>
    print(obj.filename)  # test.zip
    print(obj.stream)  # <tempfile.SpooledTemporaryFile object at 0x0000000004135160>
    # 检查上传文件的后缀名是否为zip
    ret_list = obj.filename.rsplit(".", maxsplit=1)
    if len(ret_list) != 2 or ret_list[1]!="zip":
        rst = make_response("please upload zip file")
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
        allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        rst.headers['Access-Control-Allow-Credentials'] = 'true'
        return rst, 400
    target_path = os.path.join(BASE_DIR, "sourcecode")
    shutil._unpack_zipfile(obj.stream, target_path)

    rst = make_response("upload success")
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
    allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Access-Control-Allow-Credentials'] = 'true'
    return rst, 201
# 初始化项目，变异体生成，特征提取，返回变异体总数
@application.route('/api/mutant/generate', methods=["GET", "POST"])
def generate():
    starttime = datetime.datetime.now()
    data = request_parse(request)
    dic = {}
    dic['length'] = 0
    dic['error']=''
    try:
        projectId = data.get("projectId")
        projectName=projectId+"Project"
        projectdir = os.path.join(BASE_DIR, "sourcecode",projectName)
        pitdir=os.path.join(projectdir,'target/pit-reports')
        coberturadir = os.path.join(projectdir, 'target/site/cobertura')
        # # 为了性能测试
        # dirs = 'D:/mutationtestingReduction/MSReduction/sourcecode/exp4j/'
        # if os.path.exists(dirs):
        #     shutil.rmtree(dirs)
        # print(projectId,projectdir,pitdir,coberturadir)
        Main.main(projectId, projectdir, pitdir, coberturadir)
        filename=os.path.join( BASE_DIR, "sourcecode",projectId,"mutantInfo.json")

        with open(filename, 'r') as f:
            data = json.load(f)
            res=data['results']
            dic['length']=len(res)
    except Exception as e:
        dic['error'] = str(e)
    # # 测量运行时间
    endtime = datetime.datetime.now()
    print('Time of Feature Extracting Elapsed:(S)', (endtime - starttime).seconds)
    rst = make_response(json.dumps(dic, ensure_ascii=False))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Content-Type'] = 'application/json'
    return rst, 201

@application.route('/api/login', methods=["GET", "POST","OPTIONS"])
def login():
    data = request_parse(request)
    if data is None:
        rst = make_response("no content")
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
        allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        rst.headers['Access-Control-Allow-Credentials'] = 'true'
        return rst, 204
    res={}
    username = data.get("username")
    password = data.get("password")
    # 指定查询
    myquery = {"username": username}
    mydoc = db.usersites.find(myquery)
    pwd=0
    for x in mydoc:
        pwd = x['password']
        break
    if pwd==0:
        res['state']=0
        res['reason']='username does not exists'
    elif pwd!=password:
        res['state']=1
        res['reason']='password is wrong'
    else:
        res['state']=2
        res['reason'] = 'success'
    rst = make_response(json.dumps(res, ensure_ascii=False))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
    allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Access-Control-Allow-Credentials'] = 'true'
    return rst, 201

@application.route('/api/register', methods=["GET", "POST","OPTIONS"])
def register():
    data = request_parse(request)
    if data is None:
        rst = make_response("no content")
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
        allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        rst.headers['Access-Control-Allow-Credentials'] = 'true'
        return rst, 204
    res={}
    username = data.get("username")
    password = data.get("password")
    # 指定查询
    myquery = {"username": username}
    mydoc = db.usersites.find(myquery)
    pwd=0
    for x in mydoc:
        pwd = x['password']
        break
    if pwd!=0:
        res['state']=0
        res['reason']='username does exists'
    else:
        db.usersites.insert_one({"username": username, "password": password, "models": []})
        res['state'] = 1
        res['reason'] = 'success'
    rst = make_response(json.dumps(res, ensure_ascii=False))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
    allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Access-Control-Allow-Credentials'] = 'true'
    return rst, 201

@application.route('/api/mutant/show/all', methods=['GET', 'POST'])
def all():
    data = request_parse(request)
    results = int(data.get("results"))
    # 短路运算逻辑
    page=data.get("page") or 1
    page=int(page)
    projectId=data.get("projectId")
    # dirpath=os.getcwd()
    file = os.path.join(BASE_DIR, 'sourcecode',projectId,'mutantInfo.json')
    # file_object = open(file)
    # try:
    #     result_text = file_object.read()
    # finally:
    #     file_object.close()
    result_text=getData(results,page,file)

    rst = make_response(result_text)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Content-Type']='application/json'
    return rst, 201

# 变异体集合约简
@application.route('/api/mutant/reduce', methods=["GET", "POST"])
def reduce():
    starttime = datetime.datetime.now()
    data = request_parse(request)
    projectId = data.get("projectId")
    hasModel = data.get("hasModel")
    print(hasModel)
    rangeS = int(data.get("rangeS"))
    rangeE = int(data.get("rangeE"))
    range=[rangeS//10,rangeE//10]
    print(range)
    mutantSize, mscore,testSize=MSRMain.main(projectId,hasModel,range)
    # # 测量运行时间
    endtime = datetime.datetime.now()
    print('Time of Mutant Reduction Elapsed:(S)', (endtime - starttime).seconds)
    dic={}
    dic['mutantSize']=mutantSize
    dic['mscore']=round(mscore,4)
    dic['testSize']=testSize

    rst = make_response(json.dumps(dic, ensure_ascii=False))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Content-Type'] = 'application/json'
    return rst, 201

# 约简结果展示
@application.route('/api/mutant/show/part', methods=['GET', 'POST'])
def part():
    data = request_parse(request)
    results = int(data.get("results"))
    # 短路运算逻辑
    page=data.get("page") or 1
    page=int(page)
    projectName='mutantreduce_'+data.get("projectId")+'.json'
    # dirpath=os.getcwd()
    file = os.path.join(BASE_DIR, 'output',projectName)
    result_text=getData(results,page,file)

    rst = make_response(result_text)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Content-Type']='application/json'
    return rst, 201

# 测试结果展示
@application.route('/api/test/coverage', methods=['GET', 'POST'])
def coverage():
    data = request_parse(request)
    results = int(data.get("results"))
    # 短路运算逻辑
    page=data.get("page") or 1
    page=int(page)
    projectId=data.get("projectId")
    # dirpath=os.getcwd()
    file = os.path.join(BASE_DIR, 'sourcecode',projectId,'covtest.json')
    result_text=getData(results,page,file)

    rst = make_response(result_text)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
    allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Access-Control-Allow-Credentials']='true'
    rst.headers['Content-Type']='application/json'
    return rst, 201

# 模型保存
@application.route('/api/model/save', methods=["GET", "POST"])
def save():
    data = request_parse(request)
    projectId = data.get("projectId")
    username = data.get("username")
    # 指定查询
    myquery = {"username": username}
    mydoc = db.usersites.find(myquery)
    models=[]
    for x in mydoc:
        models=x['models']
        break
    if projectId not in models:
        models.append(projectId)
    myquery = {"username": username}
    newvalues = {"$set": {"models": models}}
    db.usersites.update_one(myquery, newvalues)
    rst = make_response("success")
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Content-Type'] = 'application/json'
    return rst, 201

# 下载结果
@application.route("/api/result/download", methods=['GET','POST','OPTIONS'])
def download_file():
    data = request_parse(request)
    projectId = data.get("projectId")
    filename="mutantreduce_"+projectId+".csv"
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    # dirpath = os.getcwd()
    directory= os.path.join(BASE_DIR, 'output')
    rst= send_from_directory(directory, filename, as_attachment=True)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = "GET,HEAD,OPTIONS,POST,PUT"
    allow_headers = "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    rst.headers['Access-Control-Allow-Credentials'] = 'true'
    return rst, 201

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)