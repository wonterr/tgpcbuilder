import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask, request

TOKEN = "7040613432:AAHAIt7MJuMwRS_U7cbIZdaUU7rk2gsIcjE"
bot = telebot.TeleBot(TOKEN)
#bot.set_webhook(url="https://<tgpcbuilder>.onrender.com/")

def get_price_kaspi(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        meta_tag = soup.find("meta", attrs={"property": "product:price:amount"})
        if meta_tag:
            return int(meta_tag.get("content"))
        else:
            return None
    except Exception:
        return None

def get_price(url):
    if "kaspi.kz" in url:
        return get_price_kaspi(url)
    return None

build_300_parts = [
    {
        "name": "Процессор: Intel Core i3-12100F",
        "url": "https://kaspi.kz/shop/p/intel-core-i3-12100f-oem-103650823/?c=750000000"
    },
    {
        "name": "Материнская плата: MSI H610M-E",
        "url": "https://kaspi.kz/shop/p/msi-pro-h610m-e-ddr4-108405271/?srsltid=AfmBOoprJNRFnCK7cJ0vaAIwoo8ehPnYLlZseAWGVQcO4sALNkQf0_GG"
    },
    {
        "name": "Оперативная память: GSkill 16GB DDR4",
        "url": "https://kaspi.kz/shop/p/g-skill-aegis-f4-3200c16d-16gis-16-gb-100052885/?c=750000000"
    },
    {
        "name": "Кулер: ID-COOLING SE-214-XT BASIC",
        "url": "https://kaspi.kz/shop/p/kuler-id-cooling-se-214-xt-basic-113735702/?c=750000000"
    },
    {
        "name": "Видеокарта: MSI RTX 3050 Ventus 2X 6G OC",
        "url": "https://kaspi.kz/shop/p/msi-rtx-3050-ventus-2x-6g-oc-6-gb-118168135/?c=750000000"
    },
    {
        "name": "Блок питания: Deepcool PF550",
        "url": "https://kaspi.kz/shop/p/deepcool-pf550-r-pf550d-ha0b-eu-550-vt-104151899/?c=750000000"
    },
    {
        "name": "Корпус: Zalman T7",
        "url": "https://kaspi.kz/shop/p/zalman-t7-chernyi-101085497/?c=750000000"
    },
    {
        "name": "SSD: Kingston SNV3S 500 GB",
        "url": "https://kaspi.kz/shop/p/ssd-kingston-snv3s-500g-500-gb-124121199/?c=750000000"
    },
    {
        "name": "HDD: Seagate Barracuda 1TB",
        "url": "https://kaspi.kz/shop/p/hdd-seagate-st1000dm010-1000-gb-6800526/?c=750000000"
    }
]

intel_cpu_mobo = [
    {
        "name": "Процессор: Intel Core i5-12400F",
        "url": "https://kaspi.kz/shop/p/intel-core-i5-12400f-oem-103698110/?c=750000000"
    },
    {
        "name": "Материнская плата: ASRock H610M-HDV/M.2 R2.0",
        "url": "https://kaspi.kz/shop/p/asrock-h610m-hdv-m-2-r-2-0-113833607/?c=750000000"
    }
]

amd_cpu_mobo = [
    {
        "name": "Процессор: AMD Ryzen 5 5600",
        "url": "https://kaspi.kz/shop/p/amd-ryzen-5-5600-oem-105933939/?c=750000000"
    },
    {
        "name": "Материнская плата: GIGABYTE B550M K",
        "url": "https://kaspi.kz/shop/p/gigabyte-b550m-k-109791474/?c=750000000"
    }
]
common_400_parts = [
    {
        "name": "Оперативная память: GSkill 16GB DDR4",
        "url": "https://kaspi.kz/shop/p/g-skill-aegis-f4-3200c16d-16gis-16-gb-100052885/?c=750000000"
    },
    {
        "name": "Кулер: ID-COOLING SE-214-XT BASIC",
        "url": "https://kaspi.kz/shop/p/kuler-id-cooling-se-214-xt-basic-113735702/?c=750000000"
    },
    {
        "name": "Видеокарта: RTX 4060 Infinity 2 OC",
        "url": "https://kaspi.kz/shop/p/palit-rtx-4060-infinity-2-oc-ne64060s19p1-1070l-8-gb-118167758/?c=750000000"
    },
    {
        "name": "Блок питания: MSI MAG A650BN 650 Вт",
        "url": "https://kaspi.kz/shop/p/msi-mag-a650bn-650-vt-105630268/?c=750000000"
    },
    {
        "name": "Корпус: Zalman T7",
        "url": "https://kaspi.kz/shop/p/zalman-t7-chernyi-101085497/?c=750000000"
    },
    {
        "name": "SSD: Kingston SNV3S 500 GB",
        "url": "https://kaspi.kz/shop/p/ssd-kingston-snv3s-500g-500-gb-124121199/?c=750000000"
    },
    {
        "name": "HDD: Seagate Barracuda 1TB",
        "url": "https://kaspi.kz/shop/p/hdd-seagate-st1000dm010-1000-gb-6800526/?c=750000000"
    }
]

def generate_build_response(parts):
    result = "🛠 Ваша сборка:\n\n"
    total_price = 0
    for part in parts:
        price = get_price(part["url"])
        if price is not None:
            total_price += price
            price_str = f"{price:,} ₸".replace(",", " ")
        else:
            price_str = "Ошибка при получении цены"
        result += f"- {part['name']} — <a href=\"{part['url']}\">Kaspi</a>\n  💰 Цена: {price_str}\n\n"
    result += f"<b>💵 Итоговая стоимость:</b> {total_price:,} ₸".replace(",", " ")
    return result

@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup()
    print("Получена команда /start")
    markup.add(InlineKeyboardButton("Сборка за ~300 000₸", callback_data="build_300"))
    markup.add(InlineKeyboardButton("Сборка за ~400 000₸", callback_data="build_400"))
    bot.send_message(message.chat.id, "Выбери бюджет сборки:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "build_300")
def handle_build(call):
    response = generate_build_response(build_300_parts)
    bot.send_message(call.message.chat.id, response, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "build_400")
def handle_400_choice(call):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔵 Intel", callback_data="build_400_intel"),
        InlineKeyboardButton("🟠 AMD", callback_data="build_400_amd")
    )
    bot.send_message(call.message.chat.id, "Выберите платформу:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "build_400_intel")
def handle_build_400_intel(call):
    full_build = intel_cpu_mobo + common_400_parts
    response = generate_build_response(full_build)
    bot.send_message(call.message.chat.id, response, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "build_400_amd")
def handle_build_400_amd(call):
    full_build = amd_cpu_mobo + common_400_parts
    response = generate_build_response(full_build)
    bot.send_message(call.message.chat.id, response, parse_mode="HTML")

# --- Flask + webhook ---
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    return '', 403

@app.route('/', methods=['GET'])
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
