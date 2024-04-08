from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/getdata')
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data_all.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

@app.route('/')
def index():
    return render_template('index.html')

from collections import defaultdict

@app.route('/data')
def get_data():
    with open('data_all.json', 'r') as f:
        all_data = json.load(f)

    # เรียงลำดับข้อมูลตามเวลา
    all_data.sort(key=lambda x: x['@timestamp'])

    # นับจำนวนแพ็คเกจที่ยิงเข้ามาทุกๆ 1 นาที
    # นับจำนวนแพ็คเกจที่ยิงเข้ามาทุกๆ 1 นาที
    count_packets = defaultdict(int)
    for item in all_data:
        timestamp = item['@timestamp']
        minute = timestamp.split(':')[1]  # แยกนาทีออกมาจาก timestamp
        count_packets[minute] += 1

    # แปลง dictionary เป็น list เพื่อให้สามารถส่งไปยัง JSON ได้
    timestamps = list(count_packets.keys())
    packet_counts = list(count_packets.values())

    return jsonify({'timestamps': timestamps, 'count_packets': packet_counts})

if __name__ == '__main__':
    app.run(debug=True, port=4500)  # เปลี่ยน port ตามต้องการ
