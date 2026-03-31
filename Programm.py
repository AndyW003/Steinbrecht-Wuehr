#Marius Steinbrecht, Andreas Wühr
#SFE SA 2
#20.04.2026

import asyncio
from asyncua import Client
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
SPS_IP = "192.168.1.1"
SPS_URL = f"opc.tcp://{SPS_IP}:4840"
# -------------------------------
# SPS LESEN
# -------------------------------
async def read_sps():
    async with Client(url=SPS_URL) as client:
try:
            analog_node = client.get_node('ns=3;s="RPI_verknuepfung"."SFEProjekt.Analogwert"')
            magazin_node = client.get_node('ns=3;s="RPI_verknuepfung"."SFEProjekt.Magazin_voll"')
            zylinder_node = client.get_node('ns=3;s="RPI_verknuepfung"."SFEProjekt.Zylinder_ausfahren"')
analog = await analog_node.read_value()
            magazin = await magazin_node.read_value()
            zylinder = await zylinder_node.read_value()
return {
                "analog": float(analog),
                "magazin": bool(magazin),
                "zylinder": bool(zylinder)
            }
except Exception as e:
            print("FEHLER beim Lesen:", e)
            return {
                "analog": 0,
                "magazin": False,
                "zylinder": False
            }
# -------------------------------
# SPS SCHREIBEN
# -------------------------------
async def write_sps(node_string):
    async with Client(url=SPS_URL) as client:
        node = client.get_node(node_string)
        await node.write_value(True)
        await asyncio.sleep(0.2)
        await node.write_value(False)
# -------------------------------
# API
# -------------------------------
@app.route("/api/tags")
def tags():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return jsonify(loop.run_until_complete(read_sps()))
@app.route("/api/control", methods=["POST"])
def control():
cmd = request.json["cmd"]
if cmd == "start":
        node = 'ns=3;s="RPI_verknuepfung"."SFEProjekt.Taster_Start"'
elif cmd == "stop":
        node = 'ns=3;s="RPI_verknuepfung"."SFEProjekt.Taster_Stopp"'
elif cmd == "reset":
        node = 'ns=3;s="RPI_verknuepfung"."SFEProjekt.Taster_Reset"'
else:
        return jsonify({"status":"unknown"})
loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(write_sps(node))
return jsonify({"status":"ok"})
# -------------------------------
# WEBSEITE
# -------------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>SPS HMI</title>
<style>
body{
font-family:Arial;
background:#1e1e1e;
color:white;
text-align:center;
}
.card{
background:#2c2c2c;
padding:20px;
margin:20px auto;
width:350px;
border-radius:10px;
}
button{
padding:15px 25px;
font-size:16px;
margin:10px;
border:none;
border-radius:6px;
cursor:pointer;
}
.start{background:#27ae60;}
.stop{background:#c0392b;}
.reset{background:#f39c12;}
svg{
margin-top:10px;
}
</style>
</head>
<body>
<h1>SPS HMI</h1>
<div class="card">
<h2>Analogwert</h2>
<p id="analog">--</p>
</div>
<div class="card">
<h2>Zylinder</h2>
<p id="zylinder_text">--</p>
<div id="zylinder_svg"></div>
</div>
<div class="card">
<h2>Magazin</h2>
<p id="magazin_text">--</p>
<div id="magazin_svg"></div>
</div>
<div class="card">
<h2>Steuerung</h2>
<button class="start" onclick="start()">START</button>
<button class="stop" onclick="stop()">STOPP</button>
<button class="reset" onclick="reset()">RESET</button>
</div>
<script>
function getZylinderSVG(ausgefahren){
if(ausgefahren){
return `
<svg width="200" height="80">
<rect x="10" y="30" width="120" height="20" fill="#888"/>
<rect x="130" y="35" width="60" height="10" fill="#00ff00"/>
</svg>`
}else{
return `
<svg width="200" height="80">
<rect x="10" y="30" width="120" height="20" fill="#888"/>
<rect x="110" y="35" width="20" height="10" fill="#ff0000"/>
</svg>`
}
}
function getMagazinSVG(voll){
if(voll){
return `
<svg width="100" height="100">
<rect x="20" y="20" width="60" height="60" fill="#ff0000"/>
</svg>`
}else{
return `
<svg width="100" height="100">
<rect x="20" y="20" width="60" height="60" fill="#00ff00"/>
</svg>`
}
}
async function loadData(){
let res = await fetch("/api/tags")
let data = await res.json()
document.getElementById("analog").innerText = data.analog
// Zylinder
if(data.zylinder){
document.getElementById("zylinder_text").innerText = "AUSGEFAHREN"
}else{
document.getElementById("zylinder_text").innerText = "EINGEFAHREN"
}
document.getElementById("zylinder_svg").innerHTML = getZylinderSVG(data.zylinder)
// Magazin
if(data.magazin){
document.getElementById("magazin_text").innerText = "VOLL"
}else{
document.getElementById("magazin_text").innerText = "LEER"
}
document.getElementById("magazin_svg").innerHTML = getMagazinSVG(data.magazin)
}
async function start(){
await fetch("/api/control",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({cmd:"start"})})
}
async function stop(){
await fetch("/api/control",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({cmd:"stop"})})
}
async function reset(){
await fetch("/api/control",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({cmd:"reset"})})
}
setInterval(loadData,1000)
loadData()
</script>
</body>
</html>
"""
@app.route("/")
def index():
    return render_template_string(HTML_PAGE)
# -------------------------------
# START
# -------------------------------
if __name__ == "__main__":
    print("Server gestartet...")
    app.run(host="0.0.0.0", port=5000)

Aus <https://chatgpt.com/c/69b7d674-3980-8333-8997-cf4e4ea9208f> 
