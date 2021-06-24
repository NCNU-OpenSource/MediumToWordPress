from flask import Flask, request, make_response, redirect, session, render_template, send_file, send_from_directory
import os
import json
import LSA

app = Flask(__name__)
@app.route("/download/<filename>", methods=['POST'])
def download(filename):
    dirpath = os.path.join(app.root_path, 'download')  # 這個資料夾是要讓別人下載檔案的資料夾
    # 透過flask內建的send_from_directory
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要寫，不然會變開啟，不是下載


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/downloadPage")
def downloadPage():
    return render_template("download.html")


@app.route("/input", methods=['POST'])
def input():
    LSA.start(request.form["url"],request.form["nickname"])
    print(request.form.get("username"))
    return redirect("/downloadPage")



# @app.route("/sauce")
# def sauce():
#     return send_file(__file__, mimetype="text/plain")


if __name__ == '__main__':
    app.run(threaded=True, debug=True)