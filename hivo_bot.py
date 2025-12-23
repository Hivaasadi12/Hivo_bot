from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import re
import random
import asyncio
import datetime
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import os
import subprocess

console = Console()

# ==== تنظیمات ====
API_ID = 27996365
API_HASH = "458b1583f49640ea3a4ba8227f6d9b3a"
PHONE = "+989925203884"

BOT_TOKEN = "8527657678:AAHAZQ2QSc4OQ-tJIhpEvQMeFD4tjg8inUs"

SOURCE_CHANNEL = "@ConfigsHUB"
DEST_CHANNEL = "@Hivo_Configs7"

processed_links = set()

# تشخیص کشور قوی
def get_flag_from_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode", timeout=6)
        if response.status_code == 200:
            code = response.json().get("countryCode")
            flags = {"IR": "🇮🇷", "DE": "🇩🇪", "US": "🇺🇸", "NL": "🇳🇱", "FR": "🇫🇷", "GB": "🇬🇧", "CA": "🇨🇦", "JP": "🇯🇵", "SG": "🇸🇬", "RU": "🇷🇺"}
            return flags.get(code, "🌍")
    except:
        pass
    return "🌍"

IP_PATTERN = re.compile(r'@([a-zA-Z0-9.-]+)')
CONFIG_PATTERN = re.compile(r'(vless|vmess|trojan|ss|shadowsocks|hysteria|hysteria2|hy2|tuic|reality)://[^\s\"\'<>\n]+', re.IGNORECASE)

# کپشن‌های کامل حرفه‌ای
captions = [
    "✨ **کانفیگ جدید Hivo Configs** ✨\n\nروی لینک کلیک کن تا اتوماتیک کپی بشه 🚀\nسرعت بالا | پینگ عالی | اتصال پایدار\n\nبهترین انتخاب برای اینترنت آزاد 🌍\n@Hivo_Configs7",
    "⚡ **آپدیت تازه رسید!** ⚡\n\nکلیک = کپی فوری 🔥\nسرورهای به‌روز | بدون قطعی | تست‌شده\n\nبا Hivo همیشه متصل باش ❤️\n@Hivo_Configs7",
    "🔔 **کانفیگ پرمیوم جدید** 🔔\n\nفقط یک کلیک تا آزادی اینترنت 💎\nپینگ پایین | حجم نامحدود | امنیت بالا\n\nعضو شو و لذت ببر 👑\n@Hivo_Configs7",
    "🔥 **جواهر جدید Hivo Configs** 🔥\n\nروی کانفیگ بزن → کپی شد! 🌟\nسرورهای اختصاصی | اتصال آنی\n\nبهترین کانفیگ‌های ایران همین‌جاست 💪\n@Hivo_Configs7",
    "🚀 **کانفیگ خفن تازه وارد شد!** 🚀\n\nکپی با یک کلیک ساده 😎\nسرعت نور | پایداری بالا | بدون لگ\n\nHivo = کیفیت تضمینی\n@Hivo_Configs7",
    "💎 **کانفیگ اختصاصی Hivo** 💎\n\nکلیک کن و کپی شو!\nسرورهای پرمیوم | پینگ ایده‌آل\n\nدیگه جایی نرو، بهترین‌ها اینجان 🔥\n@Hivo_Configs7",
    "🌟 **به‌روزرسانی لحظه‌ای Hivo Configs** 🌟\n\nروی لینک بزن → آماده استفاده!\nاتصال پایدار حتی در پیک ترافیک\n\nعشقولانه‌ترین کانفیگ‌ها ❤️\n@Hivo_Configs7",
    "⚡️ **سرعت و قدرت با Hivo** ⚡️\n\nکپی اتوماتیک با کلیک\nبهترین سرورهای جهانی | تست‌شده\n\nهمین الان امتحان کن 😉\n@Hivo_Configs7",
    "🛡️ **کانفیگ امن و سریع** 🛡️\n\nکلیک = کپی شد!\nرمزنگاری قوی | بدون قطعی\n\nبا Hivo همیشه در امانی 👌\n@Hivo_Configs7",
    "🎯 **دقیقاً همونی که می‌خوای!** 🎯\n\nکانفیگ جدید با یک کلیک کپی\nپینگ عالی برای گیم و استریم\n\nبه خانواده Hivo بپیوند 🏆\n@Hivo_Configs7",
    "🔰 **کانفیگ حرفه‌ای Hivo** 🔰\n\nفقط کافیه کلیک کنی!\nسرورهای به‌روز | اتصال آنی\n\nکیفیت رو با Hivo حس کن 🌍\n@Hivo_Configs7",
    "💨 **سریع‌تر از همیشه** 💨\n\nکپی با یک لمس\nحجم نامحدود | سرعت بالا\n\nHivo انتخاب هوشمندانه‌ست 😏\n@Hivo_Configs7",
    "🌍 **کانفیگ جهانی Hivo** 🌍\n\nکلیک کن و برو پرواز!\nسرورهای متعدد | پینگ پایین\n\nهمیشه همراهتیم ❤️\n@Hivo_Configs7",
    "🏅 **بهترین کانفیگ روز** 🏅\n\nروی لینک بزن → کپی شد!\nتست‌شده | پایدار | پرسرعت\n\nHivo برنده است!\n@Hivo_Configs7",
    "✈️ **آماده پرواز با Hivo** ✈️\n\nکپی اتوماتیک | اتصال سریع\nدیگه منتظر نمونی 🔥\n\nعضو شو و تفاوت رو ببین\n@Hivo_Configs7",
    "🔥 **داغ‌ترین کانفیگ Hivo** 🔥\n\nکلیک = کپی فوری\nسرورهای آتشین | سرعت دیوانه‌کننده\n\nبهترین جا برای کانفیگ خوبه!\n@Hivo_Configs7",
    "💪 **قدرتمند و مطمئن** 💪\n\nروی کانفیگ کلیک کن\nاتصال قوی | بدون محدودیت\n\nHivo همیشه بهترینه\n@Hivo_Configs7",
    "🌙 **کانفیگ شبانه Hivo** 🌙\n\nحتی شب‌ها هم آپدیت داریم!\nکپی با یک کلیک\n\nخواب راحت با اتصال پایدار 😴\n@Hivo_Configs7",
    "☀️ **صبح بخیر با کانفیگ جدید!** ☀️\n\nشروع روز با Hivo\nکلیک کن و کپی شو\n\nروزت رو آزاد شروع کن 🌞\n@Hivo_Configs7",
    "🎉 **جشن آپدیت Hivo Configs** 🎉\n\nکانفیگ تازه رسید!\nکپی آسان | استفاده راحت\n\nبیا جشن بگیریم با اتصال عالی!\n@Hivo_Configs7",
    "❤️ **با عشق از Hivo** ❤️\n\nکانفیگ جدید تقدیم شما\nکلیک = کپی\n\nما عاشق رضایت شماییم\n@Hivo_Configs7"
]

async def main():
    while True:
        user_client = TelegramClient('hivo_session', API_ID, API_HASH)
        bot_client = TelegramClient('hivo_bot', API_ID, API_HASH)

        try:
            await bot_client.start(bot_token=BOT_TOKEN)
            await user_client.start(phone=PHONE)

            # گرافیک فوق‌العاده لوکس در ترموکس (رنگ‌های استاندارد)
            os.system("clear")
            try:
                subprocess.run(["figlet", "-f", "big", "HIVO CONFIGS"], check=True)
                subprocess.run(["figlet", "-f", "digital", "LUXE EDITION"], check=True)
            except:
                console.print("[bold magenta]██╗  ██╗██╗██╗   ██╗ ██████╗ [/]")
                console.print("[bold cyan]██║  ██║██║██║   ██║██╔═══██╗[/]")
                console.print("[bold green]███████║██║██║   ██║██║   ██║[/]")
                console.print("[bold yellow]██╔══██║██║╚██╗ ██╔╝██║   ██║[/]")
                console.print("[bold red]██║  ██║██║ ╚████╔╝ ╚██████╔╝[/]")
                console.print("[bold blue]╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═════╝ [/]")
            console.print(Panel.fit("[bold white on blue] ربات Hivo با گرافیک لوکس فعال شد! [/]\n[bold green]در حال رصد @ConfigsHUB...[/]", title="[rainbow]HIVO PREMIUM BOT[/]", border_style="yellow", box=box.HEAVY))

            @user_client.on(events.NewMessage(chats=SOURCE_CHANNEL, incoming=True))
            async def handler(event):
                try:
                    text = event.message.message or ""
                    if not text:
                        return

                    matches = list(CONFIG_PATTERN.finditer(text))
                    if not matches:
                        return

                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    new_parts = []

                    for match in matches:
                        original_link = match.group(0)
                        if original_link in processed_links:
                            continue
                        processed_links.add(original_link)

                        flag = "🌍"
                        if "#[" in original_link:
                            try:
                                flag = original_link.split("#[")[1].split("]")[0]
                                flag = f"[{flag}]"
                            except:
                                flag = "🌍"
                        elif "#" in original_link:
                            name = original_link.split("#")[1]
                            for f in "🇮🇷🇩🇪🇺🇸🇳🇱🇫🇷🇬🇧🇨🇦🇯🇵🇸🇬🇷🇺":
                                if f in name:
                                    flag = f
                                    break

                        if flag == "🌍":
                            ip_match = IP_PATTERN.search(original_link)
                            if ip_match:
                                ip = ip_match.group(1)
                                flag = get_flag_from_ip(ip)

                        new_name = f"{flag} Hivo Configs"
                        encoded_name = new_name.replace(" ", "%20")

                        if "#" in original_link:
                            new_link = original_link.rsplit("#", 1)[0] + "#" + encoded_name
                        else:
                            new_link = original_link + "#" + encoded_name

                        # گرافیک لوکس، واضح و مینیمال (الماس کم)
                        card = f"╔══════════════════════════════════════════╗\n"
                        card += f"║  {flag}      **{flag} Hivo Configs**      ║\n"
                        card += f"║                                          ║\n"
                        card += f"║   ⚡ سرعت بالا • پینگ عالی            ║\n"
                        card += f"║   🔒 امن • پایدار • تست‌شده          ║\n"
                        card += f"║                                          ║\n"
                        card += f"╚══════════════════════════════════════════╝\n"
                        card += f"`{new_link}`\n\n"

                        new_parts.append(card)

                    if not new_parts:
                        return

                    header = "💎 💎 💎  H I V O   C O N F I G S  💎 💎 💎\n"
                    header += "                PREMIUM LUXE EDITION                \n"
                    header += "💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎\n\n"

                    configs_text = "".join(new_parts)
                    footer = "💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎 💎\n\n" + random.choice(captions)

                    final_text = header + configs_text + footer

                    await asyncio.sleep(3)
                    await bot_client.send_message(DEST_CHANNEL, final_text, parse_mode='md')

                    # لاگ لوکس در ترموکس
                    table = Table(title=f"[bold yellow]ارسال موفق {len(new_parts)} کانفیگ[/]", box=box.DOUBLE, border_style="yellow")
                    table.add_column("زمان", style="cyan", justify="center")
                    table.add_column("تعداد", style="magenta", justify="center")
                    table.add_column("منبع", style="bright_white", justify="center")
                    table.add_row(now, str(len(new_parts)), SOURCE_CHANNEL)
                    console.print(table)

                except Exception as e:
                    console.print(Panel(f"[bold red]ارور: {str(e)}[/]", title="خطا", box=box.HEAVY, border_style="red"))

            await user_client.run_until_disconnected()

        except Exception as e:
            console.print(Panel(f"[bold yellow]قطع ارتباط: {str(e)} | دوباره تلاش...[/]", title="اتصال", box=box.HEAVY, border_style="yellow"))
            await asyncio.sleep(30)
        finally:
            try:
                await user_client.disconnect()
                await bot_client.disconnect()
            except:
                pass

asyncio.run(main())