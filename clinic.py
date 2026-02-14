from flask import Flask, request
import json
import jdatetime

app = Flask(__name__)

FILE = "appointments.json"
SLOTS_FILE = "slots.json"


# ---------- مدیریت فایل‌ها ----------

def load():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_slots():
    try:
        with open(SLOTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_slots(slots):
    with open(SLOTS_FILE, "w", encoding="utf-8") as f:
        json.dump(slots, f, ensure_ascii=False, indent=2)


# ---------- تبدیل تاریخ میلادی به شمسی ----------

def gregorian_to_jalali(g_date):
    y,m,d = map(int, g_date.split("-"))
    return str(jdatetime.date.fromgregorian(year=y,month=m,day=d))


# ---------- صفحه اصلی ----------

@app.route("/", methods=["GET", "POST"])
def home():

    slots = load_slots()
    appointments = load()

    booked = [(a["date"], a["time"]) for a in appointments]

    available = []

    for s in slots:

        g_date = s["date"]
        time = s["time"]

        if (g_date, time) not in booked:

            j_date = gregorian_to_jalali(g_date)

            available.append({
                "g_date": g_date,
                "j_date": j_date,
                "time": time
            })

    options = ""

    for s in available:

        options += f'<option value="{s["g_date"]}|{s["time"]}">{s["j_date"]} ساعت {s["time"]}</option>'


    if request.method == "POST":

        name = request.form.get("name")
        lastname = request.form.get("lastname")
        birthdate = request.form.get("birthdate")
        national_id = request.form.get("national_id")
        phone = request.form.get("phone")
        slot = request.form.get("slot")
        service = request.form.get("service")

        if not slot:
            return "<h3>لطفاً وقت را انتخاب کنید</h3><a href='/'>بازگشت</a>"

        date, time = slot.split("|")

        discount = "15%" if service == "زیبایی" else "20%"

        data = load()

        data.append({

            "name": name,
            "lastname": lastname,
            "birthdate": birthdate,
            "national_id": national_id,
            "phone": phone,
            "date": date,
            "time": time,
            "service": service,
            "discount": discount

        })

        save(data)

        j_date = gregorian_to_jalali(date)

        return f"""
        <div style='font-family:tahoma;direction:rtl;text-align:center;margin-top:100px'>
        <h2 style='color:green'>رزرو ثبت شد ✅</h2>
        <p>{name} {lastname}</p>
        <p>{j_date} ساعت {time}</p>
        <p>تخفیف: {discount}</p>
        <br>
        <a href="/">بازگشت</a>
        </div>
        """


    return f'''
<html>
<head>

<meta charset="UTF-8">

<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;600&display=swap" rel="stylesheet">

<style>

body {{

    font-family: 'Vazirmatn', Tahoma;
    direction: rtl;

    background-image: url("https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=1500&q=80");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    margin:0;
    padding:0;
}}

.overlay {{

    background: rgba(255,255,255,0.85);
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;

}}

.form-box {{

    background: rgba(255,255,255,0.95);
    padding:30px;
    border-radius:15px;
    width:350px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);

}}

h2 {{

    text-align:center;
    color:#2a7fba;
    margin-bottom:20px;

}}

input, select {{

    width:100%;
    padding:10px;
    margin:5px 0 15px 0;
    border-radius:8px;
    border:1px solid #ccc;
    font-family:'Vazirmatn';

}}

input:focus, select:focus {{

    outline:none;
    border:1px solid #2a7fba;

}}

button {{

    width:100%;
    padding:12px;
    background:#2a7fba;
    color:white;
    border:none;
    border-radius:8px;
    font-size:16px;
    cursor:pointer;

}}

button:hover {{

    background:#1b5f8a;

}}

.error {{

    color:red;
    font-size:12px;
    display:none;

}}

</style>

<script>

function validateForm(){{

let ok=true

let fields=["name","lastname","birthdate","national_id","phone","slot"]

fields.forEach(function(f){{

let input=document.getElementById(f)
let error=document.getElementById(f+"_error")

if(!input.value){{

input.style.border="2px solid red"
error.style.display="block"
ok=false

}}
else{{

input.style.border=""
error.style.display="none"

}}

}})

return ok

}}

</script>

</head>

<body>

<div class="overlay">

<div class="form-box">

<h2>رزرو آنلاین<br>دندان‌پزشکی مادیا دنتال</h2>

<form method="post" onsubmit="return validateForm()">

نام
<input id="name" name="name">
<div id="name_error" class="error">پر کردن این مرحله الزامی است</div>

نام خانوادگی
<input id="lastname" name="lastname">
<div id="lastname_error" class="error">پر کردن این مرحله الزامی است</div>

تاریخ تولد
<input id="birthdate" name="birthdate" type="date">
<div id="birthdate_error" class="error">پر کردن این مرحله الزامی است</div>

کد ملی
<input id="national_id" name="national_id">
<div id="national_id_error" class="error">پر کردن این مرحله الزامی است</div>

شماره تماس
<input id="phone" name="phone">
<div id="phone_error" class="error">پر کردن این مرحله الزامی است</div>

انتخاب وقت
<select id="slot" name="slot">
<option value="">انتخاب کنید</option>
{options}
</select>
<div id="slot_error" class="error">پر کردن این مرحله الزامی است</div>

نوع خدمات
<select name="service">
<option>زیبایی</option>
<option>درمانی</option>
</select>

<br>

<button type="submit">ثبت نوبت</button>

</form>

</div>

</div>

</body>
</html>
'''


# ---------- پنل منشی ----------

@app.route("/secretary", methods=["GET","POST"])
def secretary():

    slots=load_slots()
    appointments=load()

    today=jdatetime.date.today()

    today_g = today.togregorian().strftime("%Y-%m-%d")

    today_res=""

    for a in appointments:

        if a["date"]==today_g:

            today_res+=f"<li>{a['name']} {a['lastname']} ساعت {a['time']}</li>"


    if request.method=="POST":

        date=request.form["date"]
        time=request.form["time"]

        if not any(s["date"]==date and s["time"]==time for s in slots):

            slots.append({"date":date,"time":time})

            save_slots(slots)


    slot_list=""

    for s in slots:

        j_date=gregorian_to_jalali(s["date"])

        slot_list+=f"<li>{j_date} ساعت {s['time']}</li>"


    return f"""

    <h2>پنل منشی</h2>

    <form method='post'>

    تاریخ
    <input type='date' name='date' required>

    ساعت
    <input type='time' name='time' required>

    <button>افزودن</button>

    </form>

    <hr>

    <h3>وقت‌های ثبت شده</h3>

    {slot_list}

    <hr>

    <h3>رزروهای امروز</h3>

    {today_res if today_res else "رزروی نیست"}

    """


# ---------- اجرا ----------
# ---------- پنل ادمین ----------

# ---------- پنل ادمین ----------

@app.route("/admin")
def admin():

    appointments = load()

    result = "<h2>پنل ادمین - لیست همه بیماران</h2>"

    if not appointments:
        result += "<p>هیچ بیماری ثبت نشده</p>"
        return result

    for a in appointments:

        date = a.get("date")
        time = a.get("time")
        name = a.get("name", "")
        lastname = a.get("lastname", "")
        phone = a.get("phone", "")
        service = a.get("service", "")
        discount = a.get("discount", "")

        if not date or not time:
            continue

        try:
            j_date = gregorian_to_jalali(date)
        except:
            j_date = date

        result += f"""
        <hr>
        <b>نام:</b> {name} {lastname}<br>
        <b>تاریخ:</b> {j_date}<br>
        <b>ساعت:</b> {time}<br>
        <b>تلفن:</b> {phone}<br>
        <b>خدمات:</b> {service}<br>
        <b>تخفیف:</b> {discount}<br>
        """

    return result


app.run()
