
from flask import Flask, render_template, request, session, Response, jsonify
import sqlite3, json, cv2, requests
from datetime import datetime
from inference import detect_pest

app = Flask(__name__)
app.secret_key = "secret123"

# load pest info
with open("pest_info.json") as f:
    pest_data = json.load(f)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (user TEXT, pest TEXT, confidence REAL, date TEXT, lat TEXT, lon TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_location():
    try:
        res = requests.get("https://ipinfo.io/json", timeout=3).json()
        loc = res.get("loc","0,0").split(",")
        return loc[0], loc[1]
    except:
        return "0","0"

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        filepath = "static/" + file.filename
        file.save(filepath)

        pest, conf = detect_pest(filepath)
        lat, lon = get_location()

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO history VALUES (?, ?, ?, ?, ?, ?)",
                  (session.get("user","guest"), pest, conf, str(datetime.now()), lat, lon))
        conn.commit()
        conn.close()

        info = pest_data.get(pest, {})
        return render_template("index.html", pest=pest, conf=conf, info=info, img=filepath)

    return render_template("index.html")

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            temp_path = "static/frame.jpg"
            cv2.imwrite(temp_path, frame)

            pest, conf = detect_pest(temp_path)
            label = f"{pest} ({conf})"

            # draw label
            cv2.putText(frame, label, (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

            # save detection with location if pest found
            if pest != "No Pest":
                lat, lon = get_location()
                conn = sqlite3.connect("database.db")
                c = conn.cursor()
                c.execute("INSERT INTO history VALUES (?, ?, ?, ?, ?, ?)",
                          (session.get("user","guest"), pest, conf, str(datetime.now()), lat, lon))
                conn.commit()
                conn.close()

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route("/video")
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT pest, COUNT(*) FROM history GROUP BY pest")
    counts = c.fetchall()
    c.execute("SELECT lat, lon FROM history WHERE lat!='0' AND lon!='0' ORDER BY date DESC LIMIT 50")
    coords = c.fetchall()
    conn.close()
    return render_template("dashboard.html", data=counts, coords=coords)

@app.route("/api/last")
def api_last():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT pest, confidence, date, lat, lon FROM history ORDER BY date DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({"pest":row[0], "conf":row[1], "date":row[2], "lat":row[3], "lon":row[4]})
    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)
