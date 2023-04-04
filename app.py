# import flask
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("agg")
app = Flask(__name__)

# route("/url") maps to only /url but route("/url/") maps to both /url & /url/


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        try:
            if request.form["ID"] == "course_id":
                course = request.form["id_value"]
                f = open("data.csv")
                l, total, n, maxi = [], 0, 0, -1
                for line in f:
                    line = [x.strip() for x in line.strip().split(",")]
                    if line[1] == course:
                        cur = int(line[2])
                        l.append(cur)
                        total += cur
                        n += 1
                        if cur > maxi:
                            maxi = cur
                avg = total / n
                plt.hist(l)
                plt.xlabel("Marks")
                plt.ylabel("Frequency")
                plt.savefig("static/plot.png")
                f.close()
                if l:
                    return render_template("course.html", highest=maxi, average=avg)
                else:
                    return render_template("default.html")
            elif request.form["ID"] == "student_id":
                f = open("data.csv")
                l, total = [], 0
                stu_id = request.form["id_value"]
                for line in f:
                    line = [x.strip() for x in line.strip().split(",")]
                    if line[0] == stu_id:
                        l.append({"student": line[0], "course": line[1], "marks": line[2]})
                        total += int(line[2])
                f.close()
                if l:
                    return render_template("student.html", lis=l, tot=total)
                else:
                    return render_template("default.html")
        except:
            return render_template("default.html")


if __name__ == "__main__":
    # but now start the server through python3 app.py...so that this function executes or else debugger mode isn't gonna activate
    app.run(debug=True)  # debug=True implements hot reload for the server
