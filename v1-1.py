from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.style import Style
from rich.spinner import Spinner
import time
import requests
import uuid

# إعداد وحدة التحكم
console = Console()

# عرض كلمة "Dexter" بتنسيق جميل
def display_dexter():
    dexter_text = Text()
    dexter_text.append("D", style="bold red")
    dexter_text.append("e", style="bold yellow")
    dexter_text.append("x", style="bold green")
    dexter_text.append("t", style="bold blue")
    dexter_text.append("e", style="bold magenta")
    dexter_text.append("r", style="bold cyan")
    
    dexter_panel = Panel(
        dexter_text,
        title="[bold white]Automation Tool[/bold white]",
        subtitle="[italic white]Mine $SSLX and Collect Gold Eagle Coins![/italic white]",
        border_style="bold white",
        padding=(1, 2),
        width=50  # تحديد عرض الإطار
    )
    
    console.print(dexter_panel, justify="center")

# عرض وصف الأداة
def display_tool_description():
    description = Text()
    description.append("$SSLX Miner & Gold Eagle Bot\n\n", style="bold white")
    description.append("An automated tool for mining $SSLX and collecting Gold Eagle coins.\n", style="bold cyan")
    description.append("Simply run the bot and let it handle the rest!\n", style="italic green")
    
    description_panel = Panel(
        description,
        title="[bold white]Description[/bold white]",
        border_style="bold white",
        padding=(1, 2),
        width=50  # تحديد عرض الإطار
    )
    
    console.print(description_panel, justify="center")

# عرض معرف التليجرام بشكل مميز
def display_telegram_username():
    telegram_text = Text()
    telegram_text.append("📩 Telegram: ", style="bold white")
    telegram_text.append("@IFJOB", style="bold cyan")
    
    telegram_panel = Panel(
        telegram_text,
        title="[bold white]Contact Me[/bold white]",
        border_style="bold white",
        padding=(1, 2),
        width=50  # تحديد عرض الإطار
    )
    
    console.print(telegram_panel, justify="center")

# إعداد البيانات اللازمة
url_tap = "https://gold-eagle-api.fly.dev/tap"
url_wallet = "https://gold-eagle-api.fly.dev/wallet/my"
url_progress = "https://gold-eagle-api.fly.dev/user/me/progress"

# إعداد الرؤوس (headers) مع إضافة التوكين
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoiODJmOTE1OTMtYTk4YS00ODZiLTg3MzMtOGU5ODIyMDJjNDE3IiwiZmlyc3RfbmFtZSI6ItmF2Y_YrdmF2K8g8J-QjSIsInVzZXJuYW1lIjoiSUZKT0IifSwic2Vzc2lvbl9pZCI6NzA4NjU0LCJzdWIiOiI4MmY5MTU5My1hOThhLTQ4NmItODczMy04ZTk4MjIwMmM0MTciLCJleHAiOjE3Mzg2NjQwMzF9.d3RPeKkpf2vA6vt0rFyQRVF4mpzihQVA_zSn3n3t6Ic",
    "content-type": "application/json",
}

# دالة للحصول على بيانات المحفظة
def get_wallet_data():
    try:
        response = requests.get(url_wallet, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            console.print(f"❌ Failed to fetch wallet data: {response.status_code}", style="bold red")
            return None
    except Exception as e:
        console.print(f"❌ An error occurred while fetching wallet data: {e}", style="bold red")
        return None

# دالة للحصول على بيانات التقدم
def get_progress_data():
    try:
        response = requests.get(url_progress, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            console.print(f"❌ Failed to fetch progress data: {response.status_code}", style="bold red")
            return None
    except Exception as e:
        console.print(f"❌ An error occurred while fetching progress data: {e}", style="bold red")
        return None

# دالة لجمع العملات باستخدام الطاقة المتاحة
def collect_coins_using_energy(energy):
    try:
        if energy > 0:
            timestamp = int(time.time())
            salt = str(uuid.uuid4())  # استخدام UUID كـ salt فريد
            
            body = {
                "available_taps": energy,
                "count": energy,  # عدد النقرات بناءً على الطاقة المتاحة
                "timestamp": timestamp,
                "salt": salt,
            }
            
            response = requests.post(url_tap, json=body, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'coins_amount' in data:
                    console.print(f"\n✅ Successfully collected coins! Total coins now: {data['coins_amount']}", style="bold green")
                else:
                    console.print("❌ Failed to collect coins. Invalid data received.", style="bold red")
            else:
                console.print(f"❌ Failed to collect coins: {response.status_code}", style="bold red")
        else:
            console.print("⚠️ Not enough energy to collect coins. Waiting for energy to recharge...", style="bold yellow")
    except Exception as e:
        console.print(f"❌ An error occurred while collecting coins: {e}", style="bold red")

# دالة لانتظار استعادة الطاقة مع عرض علامة التحميل
def wait_for_energy(max_energy):
    try:
        energy_recharge_time = 16 * 60  # 16 دقيقة لإعادة شحن الطاقة بالكامل (بالثواني)
        console.print(f"⏳ Waiting for {energy_recharge_time / 60} minutes to recharge energy...", style="bold yellow")
        
        # عرض علامة التحميل أثناء الانتظار
        with console.status("[bold green]Recharging energy...[/bold green]", spinner="dots"):
            time.sleep(energy_recharge_time)  # الانتظار حتى تكتمل الطاقة
        
        console.print("✅ Energy fully recharged!", style="bold green")
    except Exception as e:
        console.print(f"❌ An error occurred while waiting: {e}", style="bold red")

# دالة لعرض المعلومات بشكل دوري
def display_info_periodically(interval_minutes=1):
    try:
        while True:
            # جلب بيانات التقدم لعرض الطاقة
            progress_data = get_progress_data()
            if progress_data:
                energy = progress_data["energy"]
                max_energy = progress_data["max_energy"]
                coins_amount = progress_data.get("coins_amount", 0)
                
                # عرض المعلومات بشكل احترافي ومنسق
                console.print("\n📊 Progress Data:", style="bold blue")
                console.print(f"💡 Current Energy: {energy}/{max_energy}", style="bold cyan")
                console.print(f"💰 Available Coins: {coins_amount}", style="bold green")
                console.print(f"⏳ Incomplete Tasks: {progress_data['not_completed_tasks_count']}", style="bold yellow")
                console.print(f"📅 Unregistered Events: {progress_data['not_registerd_events_count']}", style="bold magenta")
                
                # جمع العملات إذا كانت الطاقة كافية
                collect_coins_using_energy(energy)
                
            console.print(f"\n⏰ Waiting for {interval_minutes} minute(s) before the next attempt...", style="bold blue")
            
            # عرض علامة التحميل أثناء الانتظار
            with console.status("[bold blue]Waiting...[/bold blue]", spinner="dots"):
                time.sleep(interval_minutes * 60)  # الانتظار لمدة المحددة بالدقائق
    except KeyboardInterrupt:
        console.print("⛔ Automated coin collection stopped successfully.", style="bold red")
    except Exception as e:
        console.print(f"❌ An error occurred during periodic display: {e}", style="bold red")

# بدء جمع العملات التلقائي مع عرض البيانات بشكل دوري
if __name__ == "__main__":
    display_dexter()
    display_tool_description()
    display_telegram_username()
    display_info_periodically(interval_minutes=1)  # تعيين الفترة الزمنية بين عرض المعلومات إلى دقيقة واحدة