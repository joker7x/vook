import time
import requests
import uuid

# إعداد البيانات اللازمة
url_tap = "https://gold-eagle-api.fly.dev/tap"
url_progress = "https://gold-eagle-api.fly.dev/user/me/progress"

headers = {
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoiODJmOTE1OTMtYTk4YS00ODZiLTg3MzMtOGU5ODIyMDJjNDE3IiwiZmlyc3RfbmFtZSI6ItmF2Y_YrdmF2K8iLCJ1c2VybmFtZSI6IklGSk9CIn0sInNlc3Npb25faWQiOjY1MTU3NSwic3ViIjoiODJmOTE1OTMtYTk4YS00ODZiLTg3MzMtOGU5ODIyMDJjNDE3IiwiZXhwIjoxNzM4NTM5MTQ0fQ.CTUes6cz0YJqa0snl12FT29AZb7Y5mIk9mQyV0DE_OE",
}

# عرض اسم الأداة
def display_dexter():
    print("=" * 50)
    print("Dexter Bot".center(50))
    print("Automated Tool for Mining $SSLX".center(50))
    print("=" * 50)

# عرض وصف الأداة
def display_description():
    print("\nDescription:")
    print("-" * 50)
    print("An automated tool for mining $SSLX and collecting Gold Eagle coins.")
    print("Simply run the bot and let it handle the rest!")
    print("-" * 50)

# دالة لجلب بيانات التقدم
def get_progress_data():
    try:
        response = requests.get(url_progress, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    return None

# دالة لجمع العملات
def collect_coins(energy):
    if energy <= 0:
        print("⚠️ Not enough energy!")
        return
    try:
        body = {
            "available_taps": energy,
            "count": energy,
            "timestamp": int(time.time()),
            "salt": str(uuid.uuid4()),
        }
        response = requests.post(url_tap, json=body, headers=headers)
        if response.status_code == 200:
            coins = response.json().get("coins_amount", 0)
            print(f"✅ Collected coins! Total: {coins}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")

# دالة عرض البيانات بشكل دوري
def start_bot(interval_minutes=1):
    try:
        while True:
            data = get_progress_data()
            if data:
                energy = data.get("energy", 0)
                max_energy = data.get("max_energy", 0)
                coins = data.get("coins_amount", 0)

                print("\n📊 Progress Data:")
                print(f"💡 Energy: {energy}/{max_energy}")
                print(f"💰 Coins: {coins}")

                collect_coins(energy)

            print(f"\n⏳ Waiting {interval_minutes} min...")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        print("⛔ Bot stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")

# تشغيل الأداة
if __name__ == "__main__":
    display_dexter()
    display_description()
    start_bot(interval_minutes=0.5)  # الانتظار 30 ثانية
