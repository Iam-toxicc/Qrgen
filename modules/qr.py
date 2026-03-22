# Toxicqrbot QR Module

import io
import qrcode

from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import app
from database.mongo import db
import config

print("📦 QR MODULE LOADED")
def create_qr(amount, upi, name="Payment"):
    upi_link = f"upi://pay?pa={upi}&pn={name}&am={amount}&cu=INR"

    qr = qrcode.QRCode(box_size=12, border=2)
    qr.add_data(upi_link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#0f172a", back_color="white").convert("RGB")

    # LOGO CENTER
    try:
        logo = Image.open("assets/logo.png")
        logo_size = int(img.size[0] / 4)
        logo = logo.resize((logo_size, logo_size))

        pos = (
            (img.size[0] - logo_size) // 2,
            (img.size[1] - logo_size) // 2
        )
        img.paste(logo, pos)
    except:
        pass

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    draw.text((20, img.size[1] - 100), name, fill="black", font=font)
    draw.text((20, img.size[1] - 50), "@ZyroqrGenbot", fill="gray", font=font)

    bio = io.BytesIO()
    bio.name = "qr.png"
    img.save(bio, "PNG")
    bio.seek(0)

    return bio


@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(f"""
⚡ Welcome Toxic!

1. Save UPI:
/add user@upi

2. Generate QR:
/gen 500
OR
/gen 500 user@upi

Inline:
@{config.BOT_USERNAME} 500
""")


@app.on_message(filters.command("add"))
async def add_upi(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: /add user@upi")

    await db.users.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"upi": message.command[1]}},
        upsert=True
    )

    await message.reply_text("✅ UPI Saved")


@app.on_message(filters.command("del"))
async def del_upi(client, message):
    await db.users.delete_one({"user_id": message.from_user.id})
    await message.reply_text("🗑 Deleted")


@app.on_message(filters.command("myupi"))
async def myupi(client, message):
    user = await db.users.find_one({"user_id": message.from_user.id})
    if not user:
        return await message.reply_text("❌ No UPI saved")

    await message.reply_text(f"💳 {user['upi']}")


@app.on_message(filters.command("gen"))
async def gen_qr(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: /gen amount")

    amount = message.command[1]

    if len(message.command) >= 3:
        upi = message.command[2]
    else:
        user = await db.users.find_one({"user_id": message.from_user.id})
        if not user:
            return await message.reply_text("❌ Save UPI first")
        upi = user["upi"]

    qr = create_qr(amount, upi, message.from_user.first_name)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Share", switch_inline_query=amount)]
    ])

    await message.reply_photo(
        qr,
        caption=f"💰 ₹{amount}\n💳 {upi}",
        reply_markup=buttons
    )


@app.on_inline_query()
async def inline(client, query):
    await query.answer(
        results=[],
        switch_pm_text="Generate QR",
        switch_pm_parameter="start"
    )
