# Toxicqrbot
# Copyright (c) 2026 Gyanesh Patel
# All rights reserved.

from app import app

print("🔥 Bot Starting...")

# Import modules AFTER app init
try:
    import modules.qr
    print("📦 QR MODULE LOADED")
except Exception as e:
    print("❌ Module Import Error:", e)

print("✅ Modules Loaded")

# Run bot
app.run()
