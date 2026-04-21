# ================= CONFIG =================
CONFIDENCE = 0.8
INTERVAL = 1
IMAGE_CACHE = {}
VISIT_TIMEOUT = 300
BROWSER = "Chromium"

RULES_URL_ACTIONS = [
    {
        "action": "cancel_xdg",
        "patterns": ["https://t.me/"]
    },
    {
        "action": "surfe_video_view",
        "patterns": ["https://surfe.be/video/view/"]
    },
    {
        "action": "multiple_redirects",
        "patterns": [
            "https://politeconomics.org/",
            "https://supesolar.com/"
        ]
    },
    {
        "action": "breaks_extension",
        "patterns": ["https://example.com/"]
    },
    {
        "action": "no_reward",
        "patterns": ["https://example.com/"]
    },
    {
        "action": "unable_to_play",
        "patterns": ["https://example.com/"]
    },
]