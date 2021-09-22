from flask import Flask, render_template, request, jsonify, Markup
import json
import sqlite3
import markdown
import os
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


# 人口


####################################################
# 连接数据库
db = sqlite3.connect('HISTORY_DATABASE')
print("数据库连接成功")
cur = db.cursor()
"""
人口信息：
"""
####################################################
Dynastys = ['刘宋', '东魏', '隋代', '唐', '北宋', '金', '元', '明', '清']  # 各朝代列表
Countys = []  # 各朝所含郡县
Countynum = []  # 各朝所含郡县数量
CountyHouseholds = []  # 各朝代各郡县户数
CountyPopulations = []  # 各朝代各郡县人口数
CountyFamilies = []  # 各朝代各郡县人每户数
Households = []  # 各朝代总户数
Populations = []  # 各朝代总人口总数
Families = []  # 各朝代人每户数量
Household_dict = {}  # 户数字典
Population_dict = {}  # 人口字典
Familie_dict = {}  # 人每户字典
form_time = []  # 前端返回的名字
dynasty = []  # 朝代时间
####################################################
for dynasty in Dynastys:
    num1, num2, num3, num4 = 0, 0, 0, 0  # 户数,口数,人每户,郡县数
    countys = []  # 单个朝代的所有郡县名称
    CountyHousehold = []  # 当前朝代各郡县户数
    CountyPopulation = []  # 当前朝代各郡县人口数
    CountyFamilie = []  # 当前朝代各郡县人每户数
    data_people = cur.execute("select * from people where 朝代='{}'".format(dynasty))
    for row in data_people:
        num1 += int(row[3])
        num2 += int(row[4])
        num3 += float(row[5])
        num4 += 1
        countys.append(str(row[2]))
        CountyHousehold.append(int(row[3]))
        CountyPopulation.append(int(row[4]))
        CountyFamilie.append(int(row[5]))
    Households.append(num1)
    Populations.append(num2)
    Families.append(float('%.2f' % float(num3 / num4)))  # 结果保留一位小数
    Countynum.append(num4)
    Countys.append(countys)
    CountyHouseholds.append(CountyHousehold)
    CountyPopulations.append(CountyPopulation)
    CountyFamilies.append(CountyFamilie)
    print("{}人口信息计算成功".format(dynasty))
Household_dict = dict(list(zip(Dynastys, Households)))
Population_dict = dict(list(zip(Dynastys, Populations)))
Familie_dict = dict(list(zip(Dynastys, Families)))
####################################################

"""
人物信息展示：
"""
####################################################
CelebrityDynasty = ['春秋', '战国', '秦', '西汉', '东汉', '三国', '西晋', '东晋', '南北朝', '隋', '唐', '后梁', '北宋', '金', '元', '明', '清']
CelebrityNames = []  # 人物姓名
CelebrityInfos = []  # 人物信息
CelebrityPlaces = []  # 人物地点
CelebrityAttributes = []  # 人物属性
####################################################
for dynasty in CelebrityDynasty:
    names = []
    infos = []
    places = []
    attributes = []
    data_celebrity = cur.execute("select * from renwu where 朝代='{}'".format(dynasty))
    for row in data_celebrity:
        names.append(str(row[1]))
        infos.append(str(row[2]))
        places.append(str(row[3]))
        attributes.append(str(row[5]))
    CelebrityNames.append(names)
    CelebrityInfos.append(infos)
    CelebrityPlaces.append(places)
    CelebrityAttributes.append(attributes)
    print("{}人物信息统计完成".format(dynasty))
####################################################
db.close()  # 关闭数据库连接。


####################################################

def DynastyAllData(num):
    # 返回当前朝代所有数据，需要参数num:当前朝代在列表中的索引，从0开始。如：刘宋为0，东魏为1。
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    CurrentHouseholds = []  # 当前朝代各郡县总户数
    CurrentPopulations = []  # 当前朝代各郡县人口数
    CurrentFamilies = []  # 当前朝代各郡县户口数
    CurrentCountyName = Countys[num]  # 当前朝代各郡县名称
    CurrentHouseholdValue = CountyHouseholds[num]  # 当前朝代各郡县户数值
    CurrentPopulationValue = CountyPopulations[num]  # 各朝代各郡县人口数值
    CurrentPopulationMin = int(min(CurrentPopulationValue) - 1000)  # 当前朝代各郡县人口最小值
    CurrentPopulationMax = int(max(CurrentPopulationValue) + 1000)  # 当前朝代各郡县人口最大值
    CurrentFamiliesValue = CountyFamilies[num]  # 各朝代各郡县户口数值
    CurrentHousehold_dict = dict(list(zip(CurrentCountyName, CurrentHouseholdValue)))
    CurrentHousehold_dict_sort = dict(sorted(CurrentHousehold_dict.items(), key=lambda item: item[1]))  # 各朝代总人口从高到低排序
    CurrentCountyName_sort = list(CurrentHousehold_dict_sort.keys())  # 排序后的郡县名称列表
    CurrentHousehold_sort = list(CurrentHousehold_dict_sort.values())  # 排序后的各郡县总户数
    for i in range(len(CurrentHouseholdValue)):
        each_dict = {'value': CurrentHouseholdValue[i], 'name': CurrentCountyName[i]}
        CurrentHouseholds.append(each_dict)
    for i in range(len(CurrentHouseholdValue)):
        each_dict = {'value': CurrentPopulationValue[i], 'name': CurrentCountyName[i]}
        CurrentPopulations.append(each_dict)
    for i in range(len(CurrentHouseholdValue)):
        each_dict = {'value': CurrentFamiliesValue[i], 'name': CurrentCountyName[i]}
        CurrentFamilies.append(each_dict)
    CurrentAlldata = [CurrentCountyName_sort,
                      CurrentHousehold_sort,
                      CurrentHouseholds,
                      CurrentPopulations,
                      CurrentFamilies,
                      CurrentPopulationMin,
                      CurrentPopulationMax]
    return CurrentAlldata  # 返回当前朝代数据
    # 数据目录：
    # 当前朝代按照户数排序后的各郡县名称CurrentCountyName_sort
    # 当前朝代各郡县总户数排序CurrentHousehold_sort
    # 当前朝代各郡县总户数CurrentHouseholds
    # 当前朝代各郡县总人口排序CurrentPopulations
    # 当前朝代各郡县户口数排序CurrentFamilies
    # 当前朝代各郡县人口最小值CurrentPopulationMin
    # 当前朝代各郡县人口最小值CurrentPopulationMax


def CelebrityAllData(num):
    CurrentName = CelebrityNames[num]  # 当前人物姓名
    CurrentInfo = CelebrityInfos[num]  # 当前人物信息
    CurrentPlace = CelebrityPlaces[num]  # 当前人物地点
    CurrentAttribute = CelebrityAttributes[num]  # 当前人物属性
    CurrentAlldata = [CurrentName,
                      CurrentInfo,
                      CurrentPlace,
                      CurrentAttribute]
    return CurrentAlldata  # 返回当前朝代人物信息数据


# @app.route('/people_all')
# def people_all():
#     Populationlabel = Populations# 各朝代总人口总数
#     Dynastylabel = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']# 各朝代列表
#     Householdlabel = Households# 各朝代总户数
#     Familylabel = Families[:-1]# 各朝代人每户
#     Populationlabelweight = list(map(lambda x:x/1000000,Populationlabel))# 总人口加权除以1000000后的结果
#     Householdlabelweight = list(map(lambda x:x/1000000,Householdlabel))# 总户数加权除以1000000后的结果
#     Population_dict_sort = dict(sorted(Population_dict.items(),key=lambda item:item[1]))# 各朝代总人口从高到低排序
#     Dynasty_sort = list(Population_dict_sort.keys())# 排序后的朝代列表
#     Population_sort = list(Population_dict_sort.values())# 排序后的各朝代总人口数
#     return render_template("people_all.html",
#                             Dynasty_sort=Dynasty_sort,
#                             Population_sort=Population_sort,
#                             Populationlabel=Populationlabel,
#                             Populationlabelweight=Populationlabelweight,
#                             Dynastylabel=Dynastylabel,
#                             Familylabel=Familylabel,
#                             Householdlabel=Householdlabel,
#                             Householdlabelweight=Householdlabelweight)

@app.route('/Dynasty')
def Dynasty():
    Populationlabel = Populations  # 各朝代总人口总数
    Dynastylabel = ['刘宋', '东魏', '隋代', '唐', '北宋', '金', '元', '明', '清']  # 各朝代列表
    Householdlabel = Households  # 各朝代总户数
    Familylabel = Families[:-1]  # 各朝代人每户
    Populationlabelweight = list(map(lambda x: x / 1000000, Populationlabel))  # 总人口加权除以1000000后的结果
    Householdlabelweight = list(map(lambda x: x / 1000000, Householdlabel))  # 总户数加权除以1000000后的结果
    Population_dict_sort = dict(sorted(Population_dict.items(), key=lambda item: item[1]))  # 各朝代总人口从高到低排序
    Dynasty_sort = list(Population_dict_sort.keys())  # 排序后的朝代列表
    Population_sort = list(Population_dict_sort.values())  # 排序后的各朝代总人口数
    return render_template("people.html",
                           Dynasty_sort=Dynasty_sort,
                           Population_sort=Population_sort,
                           Populationlabel=Populationlabel,
                           Populationlabelweight=Populationlabelweight,
                           Dynastylabel=Dynastylabel,
                           Familylabel=Familylabel,
                           Householdlabel=Householdlabel,
                           Householdlabelweight=Householdlabelweight)


@app.route('/Dynasty/liusong', methods=['POST'])
def liusong():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 0  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    return jsonify(alldata)


@app.route('/Dynasty/dongwei', methods=['POST'])
def dongwei():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 1  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    print(123)
    return jsonify(alldata)


@app.route('/Dynasty/sui', methods=['POST'])
def sui():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 2  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    return jsonify(alldata)


@app.route('/Dynasty/tang', methods=['POST'])
def tang():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 3  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    return jsonify(alldata)


@app.route('/Dynasty/beisong', methods=['POST'])
def beisong():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 4  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    return jsonify(alldata)


@app.route('/Dynasty/jin', methods=['POST'])
def jin():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 5  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    return jsonify(alldata)


@app.route('/Dynasty/yuan', methods=['POST'])
def yuan():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 6  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    return jsonify(alldata)


@app.route('/Dynasty/ming', methods=['POST'])
def ming():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 7  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    return jsonify(alldata)


@app.route('/Dynasty/qing', methods=['POST'])
def qing():
    # Dynastys = ['刘宋','东魏','隋代','唐','北宋','金','元','明','清']
    num = 8  # 当前朝代的索引值
    alldata = DynastyAllData(num)
    return jsonify(alldata)


#  帝王巡视
def diwangshujuku():
    秦始皇 = []
    乾隆帝 = []
    康熙帝 = []
    汉武帝 = []
    con = sqlite3.connect("HISTORY_DATABASE")
    cur = con.cursor()
    sql = "select 参与人物,朝时间,介绍,历经地点,坐标,地点介绍 from tour WHERE 参与人物='秦始皇'"
    data = cur.execute(sql)
    for item in data:
        秦始皇.append(item)
    sql = "select 参与人物,朝时间,介绍,历经地点,坐标 ,地点介绍 from tour WHERE 参与人物='乾隆帝'"
    data = cur.execute(sql)
    for item in data:
        乾隆帝.append(item)
    sql = "select 参与人物,朝时间,介绍,历经地点,坐标 ,地点介绍 from tour WHERE 参与人物='康熙帝'"
    data = cur.execute(sql)
    for item in data:
        康熙帝.append(item)
    sql = "select 参与人物,朝时间,介绍,历经地点,坐标 ,地点介绍 from tour WHERE 参与人物='汉武帝'"
    data = cur.execute(sql)
    for item in data:
        汉武帝.append(item)
    cur.close()
    con.close()
    return 秦始皇, 乾隆帝, 康熙帝, 汉武帝


@app.route('/diwang')
def diwang():
    return render_template("diwang.html")


@app.route('/diwang/qa', methods=['POST'])
def qa():
    秦始皇, 乾隆帝, 康熙帝, 汉武帝 = diwangshujuku()
    d = {'秦始皇': 秦始皇, '乾隆帝': 乾隆帝, '康熙帝': 康熙帝, '汉武帝': 汉武帝, }
    res = request.form['data']
    res1 = []
    for key, vau in d.items():
        if res == key:
            res1 = vau
    dataall = []
    for i in range(len(res1)):
        coor = []
        key = str(res1[i][3]).split("&")
        vau = str(res1[i][4]).split("&", )
        info = str(res1[i][5]).split("&", )
        for j in range(len(key)):
            v = str(vau[j]).split(",")
            coor_each = {
                "name": key[j],
                "lon": v[0],
                "lat": v[1],
                "info_place": info[j]
            }
            coor.append(coor_each)
        coor = json.dumps(coor, ensure_ascii=False)

        data = {
            'name': res,
            'time': res1[i][1],
            'info': res1[i][2],
            'where': coor
        }
        dataall.append(data)

    return jsonify(dataall)


# 文字发源
@app.route('/wenzi')
def wenzi():
    dataneed = []
    con = sqlite3.connect("HISTORY_DATABASE")
    cur = con.cursor()
    sql = "select 遗址名称,描述,link,遗址出土年代,遗址地点,遗址坐标,遗址类型 from words_origin "
    data = cur.execute(sql)
    for item in data:
        dataneed.append(item)
    cur.close()
    con.close()
    print(dataneed)
    return render_template("wenzi.html", data=dataneed)


@app.route('/wenzi/GetSiteData', methods=['POST'])
def GetSiteData():
    data = dict(request.form)
    conn = sqlite3.connect('HISTORY_DATABASE')
    sql = "insert into words_origin (遗址名称,遗址出土年代,遗址地点,描述,遗址类型)  values('{}', '{}', '{}', '{}', '{}')".format(
        data['name'], data['time'], data['loc'], data['info'], data['type'])
    conn.execute(sql)
    conn.commit()
    conn.close()
    return "收到消息"


def coor_all():
    coor = []
    con = sqlite3.connect("HISTORY_DATABASE")
    cur = con.cursor()
    sql = "select name,info,地点,朝代,人物属性,经度,纬度 from renwu "
    data = cur.execute(sql)
    for item in data:
        coor_each = {
            "name": item[0].replace("\n", ""),
            "info": item[1].replace("\n", ""),
            "place": item[2].replace("\n", ""),
            "chaodai": item[3].replace("\n", ""),
            "shuxing": item[4].replace("\n", ""),
            "lon": item[5],
            "lat": item[6],
        }
        coor.append(coor_each)
    coor = json.dumps(coor, ensure_ascii=False)
    cur.close()
    con.close()
    # print(coor)
    return coor


@app.route("/time_map")
def time_map():
    coor = coor_all()

    return render_template("time_map.html", coor=coor)


@app.route("/trace", methods=['POST'])
def trace():
    res = request.form["name"]  # 点击时空轨迹传回后端的name
    con = sqlite3.connect("HISTORY_DATABASE")
    cur = con.cursor()
    sql = "select  name,time,Biao_place,C_place,info,lon,lat from trace where name=" + '"' + res + '"'
    data = cur.execute(sql)
    all_trace = [];
    for item in data:
        time = str(item[1]).split("-")
        title = str(item[2]).split("-")
        c_place = str(item[3]).split("-")
        info = str(item[4]).split("-")
        lon = str(item[5]).split("-")
        lat = str(item[6]).split("-")
        for i in range(len(time)):
            data_each = {
                "name": item[0],
                'time': time[i],
                'title': title[i],
                'c_place': c_place[i],
                'info': info[i],
                'lon': lon[i],
                'lat': lat[i],
            }
            print(data_each)
            all_trace.append(data_each)
    print(all_trace)
    all_trace = json.dumps(all_trace, ensure_ascii=False)
    return render_template("time_trace.html", all_trace=all_trace)


@app.route("/RelationshipGraph", methods=['POST'])
def RelationshipGraph():
    RootName = ''  # 根节点
    Nodes_list = []  # 子节点列表
    LinkName_list = []  # 节点关系列表
    InDB_list = []  # 判断子节点是否在数据库中的列表
    res = request.form["name"]  # 前端传回的数据
    db = sqlite3.connect('HISTORY_DATABASE')
    print("关系图谱数据库连接成功")
    cur = db.cursor()
    sql = "select * from relationship where RootName='{}'".format(res)
    data = cur.execute(sql)
    RootName = res
    for row in data:
        # 每个人只有一条记录，所以只循环一遍
        Nodes_list += str(row[2]).split('-')
        LinkName_list += str(row[3]).split('-')
        InDB_list += str(row[4]).split('-')
    Nodes = [{'name': RootName, 'symbolSize': 50, 'category': 0}]
    Links = []
    for i in range(len(Nodes_list)):
        if int(InDB_list[i]) == 1:
            # 子节点在数据库中
            node = {'name': Nodes_list[i], 'symbolSize': 50, 'category': 1}
            link = {'source': RootName, 'target': Nodes_list[i], 'name': LinkName_list[i]}
        else:
            # 子节点不在数据库中
            node = {'name': Nodes_list[i], 'symbolSize': 50, 'category': 2}
            link = {'source': RootName, 'target': Nodes_list[i], 'name': LinkName_list[i]}
        Nodes.append(node)
        Links.append(link)
    return render_template('relationship.html', Nodes=Nodes, Links=Links)


# 留言板
@app.route("/comment")
def comment():
    return render_template('comment.html')


# 将md转html
def MDToHTML(filename):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']
    mdcontent = ""
    with open(filename, 'r', encoding='utf-8') as f:
        mdcontent = f.read()
    html = markdown.markdown(mdcontent, extensions=exts)
    content = Markup(html)
    return content


@app.route("/article", methods=['POST'])
def article():
    article_name = str(request.form["name"])
    root_path = str(os.path.realpath('static/asster/doc'))  # 获取/static/asster/doc文件夹的真实路径
    filepath = root_path.replace('\\', '/') + '/' + article_name + '.md'
    content = MDToHTML(filepath)  # markdown文件的路径
    return render_template('article.html', content=content, article_name=article_name)


# 关系图谱
@app.route("/relationship_tackle", methods=['POST'])
def relationalship_tackle():
    res = request.form['name']
    print(res)
    con = sqlite3.connect("HISTORY_DATABASE")
    cur = con.cursor()
    sql = "select * from renwu WHERE name='{}'".format(res)
    print(sql)
    data = cur.execute(sql)
    dataneed = {}
    for item in data:
        dataneed = {
            'name': item[1],
            'dynasty': item[4],
            'info': item[2],
            'now_where': item[3],
            'coordinate': {
                "lat": item[5],
                "lon": item[6]
            }
        }
    print(dataneed)
    return jsonify(dataneed)


@app.route("/rel_timemap", methods=['POST'])
def rel_timemap():
    res = request.form["in_name"]  # 点击传回后端的name
    coor = coor_all()
    dyn = []
    con = sqlite3.connect("HISTORY_DATABASE")
    cur = con.cursor()
    sql = "select * from renwu WHERE name='{}'".format(str(res))
    data = cur.execute(sql)
    for item in data:
        dyn = item[4]
    return render_template("form_time_map.html", name=res, coor=coor, form_dynasty=dyn)


# 人物信息展示
@app.route("/celebrity")
def celebrity():
    return render_template('celebrity.html')


@app.route('/celebrity/chunqiu_celebrity', methods=['POST'])
def chunqiu_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 0  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/zhanguo_celebrity', methods=['POST'])
def zhanguo_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 1  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/qin_celebrity', methods=['POST'])
def qin_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 2  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/xihan_celebrity', methods=['POST'])
def xihan_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 3  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/donghan_celebrity', methods=['POST'])
def donghan_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 4  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/sanguo_celebrity', methods=['POST'])
def sanguo_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 5  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/xijin_celebrity', methods=['POST'])
def xijin_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 6  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/dongjin_celebrity', methods=['POST'])
def dongjin_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 7  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/nanbeichao_celebrity', methods=['POST'])
def nanbeichao_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 8  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/sui_celebrity', methods=['POST'])
def sui_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 9  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/tang_celebrity', methods=['POST'])
def tang_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 10  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/houliang_celebrity', methods=['POST'])
def houliang_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 11  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/beisong_celebrity', methods=['POST'])
def beisong_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 12  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/jin_celebrity', methods=['POST'])
def jin_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 13  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/yuan_celebrity', methods=['POST'])
def yuan_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 14  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/ming_celebrity', methods=['POST'])
def ming_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 15  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/qing_celebrity', methods=['POST'])
def qing_celebrity():
    # CelebrityDynasty = ['春秋','战国','秦','西汉','东汉','三国','西晋','东晋','南北朝','隋','唐','后梁','北宋','金','元','明','清']
    num = 16  # 当前朝代的索引值
    alldata = CelebrityAllData(num)
    return jsonify(alldata)


@app.route('/celebrity/CelebrityGoToMap', methods=['POST'])
def CelebrityGoToMap():
    global form_time
    global dynasty
    form_time = request.form["name"]

    con = sqlite3.connect("HISTORY_DATABASE")
    cur = con.cursor()
    sql = "select * from renwu WHERE name='{}'".format(str(form_time))
    data = cur.execute(sql)
    for item in data:
        dynasty = item[4]
    return jsonify(form_time)


@app.route('/form_time_map_tackle')
def form_time_map_tackle():
    coor = coor_all()
    form_dynasty = dynasty
    return render_template("form_time_map.html", name=form_time, coor=coor, form_dynasty=form_dynasty)


# 空间查询返回后端处理函数
@app.route('/search_tackle', methods=['POST'])
def search_tackle():
    res = request.form['name']
    name=res.split(',')

    con = sqlite3.connect("HISTORY_DATABASE")
    cur = con.cursor()
    data_all_name=[]
    for item1 in name:
        sql = "select * from renwu WHERE name='{}'".format(item1)
        print(sql)
        data = cur.execute(sql)
        dataneed = {}
        for item in data:
            dataneed = {
                'name': item[1],
                'dynasty': item[4],
                'info': item[2],
                'now_where': item[3],
                'coordinate': {
                    "lat": item[5],
                    "lon": item[6]
                }
            }
        data_all_name.append(dataneed)
    print(data_all_name)
    return jsonify(data_all_name)




#人物添加
def get_location(location):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    param = {
        'address': location,
        'ak': 'PT2uN1tyKMWrkCZsB3Y86TuNiwxXaDOn',
        'output': 'json'
    }
    lon = None
    lat = None
    try:
        response = requests.get(url, param)
        answer = json.loads(response.text)
        lon = round(float(answer['result']['location']['lng']), 6)
        lat = round(float(answer['result']['location']['lat']), 6)
        ordinate = [lon, lat]
    except:
        ordinate = '未查询到结果'
    return ordinate
@app.route('/time_map/GetFigureData', methods=['POST'])
def GetFigureData():
    data = json.loads(request.form.get('data'))
    figure_ = data['figure']
    relation_ = data['relation']
    trace_ = data['trace']

    conn = sqlite3.connect('HISTORY_DATABASE')
    cur = conn.cursor()
    lon, lat = get_location(figure_['loc'])
    sql = "insert into renwu (name,朝代,地点,人物属性,info,经度,纬度)  values('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        figure_['name'], figure_['dynasty'], figure_['loc'], figure_['type'], figure_['info'], lon, lat)
    cur.execute(sql)

    for index, item in enumerate(trace_):
        lon_, lat_ = get_location(item['Location'])
        trace_[index]['lon'] = lon_
        trace_[index]['lat'] = lat_
    new_trace = connect_item(trace_)
    sql = "insert into trace (name,time,Biao_place,C_place,info,lon,lat)  values('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        figure_['name'], new_trace['Time'], new_trace['Brief'], new_trace['Location'], new_trace['Info'],
        new_trace['lon'], new_trace['lat'])
    cur.execute(sql)

    for index, item in enumerate(relation_):
        sql = "SELECT IFNULL((Select 1 from renwu where name='{}' limit 1), 0)".format(item['this_name'])
        cur.execute(sql)
        relation_[index]['YoN'] = cur.fetchone()[0] + 1
    new_relation = connect_item(relation_)
    sql = "insert into relationship (RootName,Nodes,LinkName, InDB) values('{}', '{}', '{}', '{}')".format(
        figure_['name'], new_relation['this_name'], new_relation['relation'], new_relation['YoN']
    )
    cur.execute(sql)

    conn.commit()
    conn.close()
    return "收到消息"

def connect_item(data):
    new_data = {}
    keys_ = list(data[0].keys())
    for key in keys_:
        new_data[key] = ''
    for d in data:
        for key, item in d.items():
            if item == '':
                item = ' '
            new_data[key] += (str(item) + '-')
    for key in new_data.keys():
        new_data[key] = new_data[key].rstrip('-')
    return new_data

# 文章历史页面
@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)
