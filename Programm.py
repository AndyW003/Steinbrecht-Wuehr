import asyncio
from asyncua import Client, ua
from flask import Flask, jsonify, request, render_template_string, redirect, session
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.secret_key = "super_secret_key_change_me"
USERNAME = "Benutzer"
PASSWORD = "SPS"
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
            return {
                "analog": float(await analog_node.read_value()),
                "magazin": bool(await magazin_node.read_value()),
                "zylinder": bool(await zylinder_node.read_value())
            }
        except Exception as e:
            print("FEHLER:", e)
            return {"analog": 0, "magazin": False, "zylinder": False}
# -------------------------------
# SPS SCHREIBEN
# -------------------------------
async def write_sps(node_string):
    try:
        async with Client(url=SPS_URL) as client:
            node = client.get_node(node_string)
            await node.write_attribute(
                ua.AttributeIds.Value,
                ua.DataValue(ua.Variant(True))
            )
            await asyncio.sleep(0.5)
            await node.write_attribute(
                ua.AttributeIds.Value,
                ua.DataValue(ua.Variant(False))
            )
    except Exception as e:
        print("FEHLER:", e)
# -------------------------------
# LOGIN
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == USERNAME and request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            session["fresh_login"] = True
            return redirect("/")
        return "Login fehlgeschlagen", 401
    return """
    <html>
    <body style="font-family:Arial;background:#1e1e1e;color:white;text-align:center;">
        <h2>Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button>Login</button>
        </form>
    </body>
    </html>
    """
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
def login_required():
    return session.get("logged_in", False)
# -------------------------------
# API
# -------------------------------
@app.route("/api/tags")
def tags():
    if not login_required():
        return jsonify({"error": "not logged in"}), 403
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return jsonify(loop.run_until_complete(read_sps()))
@app.route("/api/control", methods=["POST"])
def control():
    if not login_required():
        return jsonify({"error": "not logged in"}), 403
    cmd = request.json["cmd"]
    nodes = {
        "start": 'ns=3;s="RPI_verknuepfung"."SFEProjekt.Taster_Start"',
        "stop":  'ns=3;s="RPI_verknuepfung"."SFEProjekt.Taster_Stopp"',
        "reset": 'ns=3;s="RPI_verknuepfung"."SFEProjekt.Taster_Reset"'
    }
    if cmd not in nodes:
        return jsonify({"status": "unknown"})
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(write_sps(nodes[cmd]))
    return jsonify({"status": "ok"})
# -------------------------------
# HTML
# -------------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Förderband HMI</title>
<style>
body{
font-family:Arial;
background:#0f0f0f;
color:white;
text-align:center;
margin:0;
}
.container{
display:flex;
justify-content:center;
gap:15px;
flex-wrap:wrap;
margin-top:15px;
}
.card{
background:#1c1c1c;
padding:10px;
border-radius:10px;
width:160px;
font-size:13px;
transition:0.3s;
}
/* Magazin Status */
.card.ok{
background:#1e6b2d;
box-shadow:0 0 10px rgba(0,255,0,0.3);
}
.card.bad{
background:#7a1e1e;
box-shadow:0 0 10px rgba(255,0,0,0.3);
}
.belt{
position:relative;
width:900px;
height:160px;
margin:20px auto;
background:#2a2a2a;
border-radius:12px;
overflow:hidden;
border:2px solid #444;
}
.cylinder{
position:absolute;
top:35px;
left:60px;
width:120px;
height:40px;
background:#666;
border-radius:8px;
}
.piston{
position:absolute;
top:8px;
left:10px;
width:20px;
height:22px;
background:#00ff00;
}
.out .piston{left:90px;background:red;}
.puck{
position:absolute;
top:105px;
left:260px;
width:40px;
height:40px;
background:orange;
border-radius:50%;
opacity:0;
transition:opacity 0.2s;
}
/* CONTROL BAR */
.control-bar{
position:fixed;
bottom:20px;
left:50%;
transform:translateX(-50%);
display:flex;
gap:15px;
background:#1c1c1c;
padding:12px 18px;
border-radius:14px;
border:1px solid #333;
box-shadow:0 5px 20px rgba(0,0,0,0.6);
}
.control-bar button{
padding:12px 22px;
border:none;
border-radius:10px;
font-size:14px;
font-weight:bold;
cursor:pointer;
transition:0.2s;
min-width:110px;
}
.control-bar button:hover{
transform:scale(1.05);
opacity:0.9;
}
.start{background:#28a745;color:white;}
.stop{background:#dc3545;color:white;}
.reset{background:#ff9800;color:white;}
</style>
</head>
<body>
<h1>Förderband</h1>
<div class="belt">
    <div id="cylinder" class="cylinder">
        <div class="piston"></div>
    </div>
    <div id="puck" class="puck"></div>
</div>
<div class="container">
    <div class="card" id="magazin_card">
        <h3>Magazin</h3>
        <p id="magazin_text">--</p>
    </div>
    <div class="card">
        <h3>Zylinder</h3>
        <p id="zylinder_text">--</p>
    </div>
    <div class="card">
        <h3>Analog</h3>
        <p id="analog">--</p>
    </div>
</div>
<div class="control-bar">
    <button class="start" onclick="start()">▶ START</button>
    <button class="stop" onclick="stop()">⏹ STOP</button>
    <button class="reset" onclick="reset()">↺ RESET</button>
</div>
<script>
let running = false;
let lastZylinder = false;
let startTime = null;
let duration = 5000;
let startPos = 260;
let endPos = 660;
async function loadData(){
let res = await fetch("/api/tags",{credentials:"include"})
let data = await res.json()
if(data.error){
location.href="/login"
return
}
document.getElementById("analog").innerText = data.analog.toFixed(2) + " Volt";
// -------------------------
// MAGAZIN STATUS
// -------------------------
let magazinCard = document.getElementById("magazin_card");
if(data.magazin){
document.getElementById("magazin_text").innerText = "VOLL";
magazinCard.classList.add("ok");
magazinCard.classList.remove("bad");
}else{
document.getElementById("magazin_text").innerText = "LEER";
magazinCard.classList.add("bad");
magazinCard.classList.remove("ok");
}
// -------------------------
let cyl = document.getElementById("cylinder");
if(data.zylinder){
cyl.classList.add("out");
document.getElementById("zylinder_text").innerText = "AUSGEFAHREN";
if(data.zylinder && !lastZylinder && running){
startMaterial();
}
}else{
cyl.classList.remove("out");
document.getElementById("zylinder_text").innerText = "EINGEFAHREN";
}
lastZylinder = data.zylinder;
moveMaterial();
}
function startMaterial(){
let puck = document.getElementById("puck");
startTime = performance.now();
puck.style.opacity = "1";
puck.style.left = startPos + "px";
}
function moveMaterial(){
if(startTime === null || !running) return;
let puck = document.getElementById("puck");
let now = performance.now();
let progress = (now - startTime) / duration;
if(progress >= 1){
puck.style.left = endPos + "px";
puck.style.opacity = "0";
startTime = null;
return;
}
let pos = startPos + (endPos - startPos) * progress;
puck.style.left = pos + "px";
}
async function start(){
running = true;
await fetch("/api/control",{method:"POST",
headers:{"Content-Type":"application/json"},
credentials:"include",
body:JSON.stringify({cmd:"start"})
});
}
async function stop(){
running = false;
await fetch("/api/control",{method:"POST",
headers:{"Content-Type":"application/json"},
credentials:"include",
body:JSON.stringify({cmd:"stop"})
});
}
async function reset(){
running = false;
startTime = null;
lastZylinder = false;
document.getElementById("puck").style.opacity = "0";
await fetch("/api/control",{method:"POST",
headers:{"Content-Type":"application/json"},
credentials:"include",
body:JSON.stringify({cmd:"reset"})
});
}
setInterval(loadData,200);
loadData();
</script>
</body>
</html>
"""
# -------------------------------
# ROUTES
# -------------------------------
@app.route("/")
def index():
    if not login_required():
        return redirect("/login")
    # 🔥 Logout bei Reload erzwingen
    if not session.get("fresh_login"):
        session.clear()
        return redirect("/login")
    session.pop("fresh_login", None)
    return render_template_string(HTML_PAGE)
if __name__ == "__main__":
    print("Server gestartet...")
    app.run(host="0.0.0.0", port=5000)
