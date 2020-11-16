from flask import Flask,render_template,request,redirect,url_for,send_from_directory,session
from models.azure import Azure
import pandas as pd
import csv
import os
pic_count = 0

toeic_words = pd.read_csv("static/toeic_words.csv")

app = Flask(__name__)


@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/part1',methods =["get"])
def part1():
    return render_template("part1.html")

@app.route('/part1',methods =["post"])
def part1_post():
    img_file = request.files['member_image']
    result = Azure.detect_objects(img_file)
    result_di = list()
    for eng_word in list(result.tags):
        temp_di = dict()
        temp_di["eng_word"] = eng_word
        temp_di["jap_word"] = Azure.trans_word(eng_word,"en","ja")
        result_di.append(temp_di)
    return render_template("part1_result.html",words =(result_di))

@app.route("/important",methods=["get"])
def important():
    return render_template("important.html")

@app.route('/important',methods =["post"])
def important_post():
    img_file = request.files['member_image']
    result = Azure.read(img_file)#文字読み込み
    sen_jap = list()
    words = list()
    for sen in result["sentences"]:
        sen_jap.append(Azure.trans_sentence(sen,"ja"))
    for eng_word in result["words"]:
        df = toeic_words[toeic_words["eng"]==eng_word]
        #print(df)
        if df.empty:  # 重要単語でないのなら飛ばす
            continue
        temp_di = dict()
        temp_di["eng_word"] = eng_word
        temp_di["jap_word"] = df.iloc[len(df)-1,1]
        words.append(temp_di)

    #print(words)
    return render_template("important_result.html",
                           sentences = result["sentences"],#英語文章のlist
                           sen_japs = sen_jap,#日本語訳
                           words = words,#ワード
                           )

@app.route("/wordbook",methods=["get"])
def wordbook():
    return render_template("wordbook.html")




@app.route("/wordbook",methods=["post"])
def wordbook_post():
    img_file = request.files['member_image']
    result = Azure.read(img_file)#文字読み込み
    sen_jap = list()
    for sen in result["sentences"]:
        sen_jap.append(Azure.trans_sentence(sen,"ja"))

    with open('static/toeic_words.csv', 'a') as f:
        writer = csv.writer(f)
        for i in range(len(sen_jap)):
            writer.writerow([result["sentences"][i],sen_jap[i]])



    return render_template("wordbook_result.html",
                           word_ens = result["sentences"],
                           word_japs = sen_jap)



if __name__ == '__main__':

    app.run(debug=True)
