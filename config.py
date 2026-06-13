# ================= CONFIG =================
CONFIDENCE = 0.8
INTERVAL = 1
IMAGE_CACHE = {}
VISIT_TIMEOUT = 300  # 5 minutes
BROWSER = "Chromium"  # Change to "Google-chrome" or "Brave-browser" if needed

# ================= URL RULES =================
# Define actions to take when certain URLs are detected
# Actions:
# - cancel_xdg: Press Enter to close system dialogs (like Telegram opening)
# - surfe_video_view: Specific click for surfe videos
# - multiple_redirects, breaks_extension, no_reward, unable_to_play: Report and close
RULES_URL_ACTIONS = [
    {"action": "cancel_xdg", "patterns": ["https://t.me/"]},
    {"action": "surfe_video_view", "patterns": ["https://surfe.be/video/view/"]},
    {
        "action": "multiple_redirects",
        "patterns": [
            "https://politeconomics.org/",
            "https://supesolar.com/",
            "https://instukzia.com/",
            "https://stroihome.net/",
        ],
    },
    # Removed placeholder example.com patterns
]
