import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import threading
import asyncio
import os
import tempfile
import time

# ============================================================
# KALYANAM ENNA? AI™
# Kerala's Most Unnecessary AI
#
# Educational / entertainment project.
# The "prediction" is fictional and NOT a real prediction.
# ============================================================


# ============================================================
# COLORS
# ============================================================

BG = "#05070b"
PANEL = "#0b1018"
PANEL2 = "#111824"
RED = "#ff1738"
RED_DARK = "#8e0018"
GOLD = "#ffd447"
WHITE = "#f5f7fa"
MUTED = "#788291"
GREEN = "#39ff88"
CYAN = "#29dfff"


# ============================================================
# QUESTIONS
# ============================================================

QUESTIONS = [
    {
        "question": "ചായയോ കാപ്പിയോ?",
        "english": "Tea or Coffee?",
        "options": ["☕ ചായ", "☕ കാപ്പി", "രണ്ടും", "ഒന്നും വേണ്ട"],
    },
    {
        "question": "Sunday എത്ര മണിക്ക് എഴുന്നേൽക്കും?",
        "english": "What time do you wake up on Sunday?",
        "options": ["6 AM-ന് മുമ്പ്", "6–9 AM", "9–12 PM", "ഉച്ച കഴിഞ്ഞ് 😴"],
    },
    {
        "question": "വീട്ടിൽ ആരെയാണ് കൂടുതൽ പേടിക്കുന്നത്?",
        "english": "Who are you most scared of at home?",
        "options": ["അമ്മ", "അച്ഛൻ", "രണ്ടുപേരെയും", "ആരെയും പേടിയില്ല 😎"],
    },
    {
        "question": "വിവാഹത്തിന് ശേഷം എവിടെ താമസിക്കണം?",
        "english": "Where would you live after marriage?",
        "options": ["Kerala", "Gulf 🌴", "മറ്റൊരു state", "എവിടെയായാലും Wi-Fi വേണം"],
    },
    {
        "question": "നിനക്ക് ഏറ്റവും പ്രധാനപ്പെട്ടത്?",
        "english": "What matters most to you?",
        "options": ["ജോലി 💼", "പണം 💰", "സമാധാനം 😌", "സ്വാതന്ത്ര്യം 🚀"],
    },
]


# ============================================================
# RESULT MESSAGES
# ============================================================

VERDICTS = [
    "മോനെ... ആദ്യം ജോലി നോക്ക്.",
    "വീട്ടിൽ അന്വേഷണം തുടങ്ങിയിട്ടുണ്ട്.",
    "അടുത്ത ഞായറാഴ്ച പെണ്ണുകാണൽ സാധ്യത.",
    "കല്യാണത്തെക്കുറിച്ച് അധികം ചിന്തിക്കണ്ട... ഇപ്പോൾ.",
    "നിന്റെ കാര്യത്തിൽ AI പോലും confused ആണ്.",
    "ചായ കുടിച്ച് ആലോചിക്കാം.",
    "അമ്മയോട് ചോദിച്ചിട്ട് final decision എടുക്കുക.",
    "നിന്റെ future-നെക്കുറിച്ച് പറയാൻ ഞങ്ങൾക്കും പേടിയാണ്.",
]

AMMA_LINES = [
    "ചോറ് കഴിച്ചോ മോനെ?",
    "എന്തായാലും നല്ല കുട്ടിയാ നോക്കേണ്ടത്.",
    "ജോലി ഉണ്ടല്ലോ?",
    "Gulf ആണെങ്കിൽ നല്ലതാ.",
    "നന്നായി പഠിക്ക്... ബാക്കി പിന്നെ നോക്കാം.",
    "Phone ഒന്ന് താഴെ വെക്ക് മോനെ.",
]

AMMAVAN_LINES = [
    "ഇപ്പോഴത്തെ പിള്ളേർക്ക് കല്യാണം വേണ്ടത്രേ!",
    "ഞങ്ങളുടെ കാലത്ത് ഇതൊന്നുമില്ലായിരുന്നു.",
    "ജോലി എന്താ?",
    "Government job ആണോ?",
    "Gulf പോകുന്നുണ്ടോ?",
    "ശരി ശരി... ഞങ്ങൾ അന്വേഷിക്കാം.",
]


# ============================================================
# GLOBALS
# ============================================================

camera = None
camera_running = False
camera_frame = None

face_cascade = None

answers = []
current_question = 0
scan_complete = False
face_detected = False

speech_enabled = True
last_speech = 0


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak_async(text):
    """
    Uses Microsoft Edge TTS.
    Malayalam support depends on the available voice.
    """

    if not speech_enabled:
        return

    def worker():
        try:
            import edge_tts

            async def make_audio():
                communicate = edge_tts.Communicate(
                    text,
                    "ml-IN-SobhanaNeural"
                )

                temp_file = os.path.join(
                    tempfile.gettempdir(),
                    "kalyanam_ai_voice.mp3"
                )

                await communicate.save(temp_file)

                try:
                    import pygame

                    pygame.mixer.init()
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()

                    while pygame.mixer.music.get_busy():
                        time.sleep(0.05)

                    pygame.mixer.quit()

                except Exception:
                    pass

            asyncio.run(make_audio())

        except Exception:
            pass

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


# ============================================================
# CAMERA
# ============================================================

def start_camera():
    global camera
    global camera_running

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        camera_running = False
        status_label.config(
            text="⚠ CAMERA NOT FOUND — DEMO MODE",
            fg=RED
        )
        return

    camera_running = True

    status_label.config(
        text="● CAMERA ONLINE",
        fg=GREEN
    )

    update_camera()


def update_camera():
    global camera_frame
    global face_detected

    if not camera_running:
        return

    ret, frame = camera.read()

    if not ret:
        root.after(30, update_camera)
        return

    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    face_detected = len(faces) > 0

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 23, 255),
            2
        )

        cv2.putText(
            frame,
            "HUMAN DETECTED",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 100),
            2
        )

    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    img = Image.fromarray(frame_rgb)

    # Keep camera preview reasonable
    img.thumbnail((700, 450))

    camera_frame = ImageTk.PhotoImage(img)

    camera_label.config(
        image=camera_frame
    )

    if face_detected:
        camera_status.config(
            text="● HUMAN DETECTED",
            fg=GREEN
        )
    else:
        camera_status.config(
            text="○ LOOK AT THE CAMERA",
            fg=GOLD
        )

    root.after(
        30,
        update_camera
    )


# ============================================================
# CAMERA STOP
# ============================================================

def stop_camera():
    global camera_running

    camera_running = False

    if camera is not None:
        camera.release()


# ============================================================
# UI HELPERS
# ============================================================

def clear_screen():

    for widget in main_frame.winfo_children():
        widget.destroy()


def title_label(parent, text, size=28, color=WHITE):

    label = tk.Label(
        parent,
        text=text,
        font=("Arial", size, "bold"),
        bg=BG,
        fg=color
    )

    return label


# ============================================================
# HOME SCREEN
# ============================================================

def show_home():

    clear_screen()

    global status_label

    # Logo
    tk.Label(
        main_frame,
        text="💍",
        font=("Arial", 70),
        bg=BG,
        fg=GOLD
    ).pack(
        pady=(30, 0)
    )

    tk.Label(
        main_frame,
        text="KALYANAM ENNA?",
        font=("Arial", 42, "bold"),
        bg=BG,
        fg=WHITE
    ).pack()

    tk.Label(
        main_frame,
        text="AI™",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=RED
    ).pack()

    tk.Label(
        main_frame,
        text="KERALA'S MOST UNNECESSARY AI",
        font=("Arial", 13, "bold"),
        bg=BG,
        fg=GOLD
    ).pack(
        pady=(8, 20)
    )

    tk.Label(
        main_frame,
        text=(
            "A completely fictional AI system that analyses you\n"
            "and attempts to answer Kerala's most dangerous question."
        ),
        font=("Arial", 13),
        bg=BG,
        fg=MUTED,
        justify="center"
    ).pack(
        pady=10
    )

    status_label = tk.Label(
        main_frame,
        text="● INITIALISING CAMERA...",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=GOLD
    )

    status_label.pack(
        pady=15
    )

    start_btn = tk.Button(
        main_frame,
        text="💍 START KALYANAM ANALYSIS",
        font=("Arial", 16, "bold"),
        bg=RED_DARK,
        fg=WHITE,
        activebackground=RED,
        activeforeground=WHITE,
        relief="flat",
        padx=35,
        pady=18,
        cursor="hand2",
        command=start_test
    )

    start_btn.pack(
        pady=20
    )

    tk.Label(
        main_frame,
        text="⚠ Entertainment / experimental project — not a real prediction",
        font=("Arial", 10),
        bg=BG,
        fg="#555d68"
    ).pack(
        pady=15
    )

    # Start camera once home is shown
    if not camera_running:
        root.after(
            500,
            start_camera
        )


# ============================================================
# START TEST
# ============================================================

def start_test():

    global answers
    global current_question
    global scan_complete

    answers = []
    current_question = 0
    scan_complete = False

    show_camera_scan()


# ============================================================
# CAMERA SCAN
# ============================================================

def show_camera_scan():

    clear_screen()

    tk.Label(
        main_frame,
        text="INITIALISING HUMAN SCAN",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(30, 10)
    )

    tk.Label(
        main_frame,
        text="Please look directly at the camera.",
        font=("Arial", 13),
        bg=BG,
        fg=MUTED
    ).pack(
        pady=5
    )

    global camera_label
    global camera_status

    camera_label = tk.Label(
        main_frame,
        bg="#000000",
        width=700,
        height=400
    )

    camera_label.pack(
        pady=20
    )

    camera_status = tk.Label(
        main_frame,
        text="SCANNING...",
        font=("Arial", 14, "bold"),
        bg=BG,
        fg=GOLD
    )

    camera_status.pack()

    root.after(
        3000,
        begin_questions
    )


# ============================================================
# QUESTIONS SCREEN
# ============================================================

def begin_questions():

    global current_question

    current_question = 0

    show_question()


def show_question():

    clear_screen()

    if current_question >= len(QUESTIONS):
        show_processing()
        return

    q = QUESTIONS[current_question]

    progress = (
        f"QUESTION {current_question + 1}"
        f" / "
        f"{len(QUESTIONS)}"
    )

    tk.Label(
        main_frame,
        text=progress,
        font=("Arial", 12, "bold"),
        bg=BG,
        fg=RED
    ).pack(
        pady=(30, 5)
    )

    tk.Label(
        main_frame,
        text=q["question"],
        font=("Arial", 30, "bold"),
        bg=BG,
        fg=WHITE,
        wraplength=900
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        main_frame,
        text=q["english"],
        font=("Arial", 13),
        bg=BG,
        fg=MUTED
    ).pack(
        pady=(0, 25)
    )

    button_frame = tk.Frame(
        main_frame,
        bg=BG
    )

    button_frame.pack(
        pady=10
    )

    for option in q["options"]:

        btn = tk.Button(
            button_frame,
            text=option,
            font=("Arial", 14, "bold"),
            bg=PANEL2,
            fg=WHITE,
            activebackground=RED_DARK,
            activeforeground=WHITE,
            relief="flat",
            width=32,
            pady=13,
            cursor="hand2",
            command=lambda x=option: answer_question(x)
        )

        btn.pack(
            pady=7
        )


# ============================================================
# ANSWER
# ============================================================

def answer_question(answer):

    global answers
    global current_question

    answers.append(answer)

    current_question += 1

    show_question()


# ============================================================
# PROCESSING
# ============================================================

def show_processing():

    clear_screen()

    tk.Label(
        main_frame,
        text="🤖",
        font=("Arial", 65),
        bg=BG
    ).pack(
        pady=(50, 10)
    )

    processing_label = tk.Label(
        main_frame,
        text="ANALYSING HUMAN...",
        font=("Arial", 27, "bold"),
        bg=BG,
        fg=GOLD
    )

    processing_label.pack(
        pady=10
    )

    detail = tk.Label(
        main_frame,
        text="",
        font=("Arial", 12),
        bg=BG,
        fg=MUTED
    )

    detail.pack(
        pady=15
    )

    messages = [
        "Analysing chaya dependency...",
        "Calculating Kerala factor...",
        "Checking family pressure...",
        "Measuring Sunday laziness...",
        "Consulting imaginary astrologer...",
        "Loading completely unnecessary AI...",
        "Asking AI Ammavan...",
    ]

    def animate(index=0):

        if index < len(messages):

            detail.config(
                text=messages[index]
            )

            root.after(
                650,
                lambda: animate(index + 1)
            )

        else:

            root.after(
                500,
                show_reveal
            )

    animate()


# ============================================================
# CALCULATE RESULT
# ============================================================

def calculate_result():

    # Completely fictional scoring system.
    # This is intentionally entertainment-only.

    score = random.randint(
        35,
        92
    )

    # Add a little variation based on answers
    for answer in answers:

        if "അമ്മ" in answer:
            score += 3

        if "Gulf" in answer:
            score += 4

        if "ഉച്ച" in answer:
            score += 2

        if "രണ്ടും" in answer:
            score += 1

    score = max(
        1,
        min(
            score,
            99
        )
    )

    possible_years = [
        2029,
        2030,
        2031,
        2032,
        2033,
        2035,
        2040
    ]

    # Deliberately fictional
    predicted_year = random.choice(
        possible_years
    )

    verdict = random.choice(
        VERDICTS
    )

    return score, predicted_year, verdict


# ============================================================
# REVEAL
# ============================================================

def show_reveal():

    clear_screen()

    tk.Label(
        main_frame,
        text="💍",
        font=("Arial", 60),
        bg=BG
    ).pack(
        pady=(30, 5)
    )

    tk.Label(
        main_frame,
        text="ONE IMPORTANT QUESTION...",
        font=("Arial", 16, "bold"),
        bg=BG,
        fg=MUTED
    ).pack(
        pady=5
    )

    tk.Label(
        main_frame,
        text="കല്യാണം എന്നാ?",
        font=("Arial", 44, "bold"),
        bg=BG,
        fg=RED
    ).pack(
        pady=20
    )

    # Dramatic delay
    root.after(
        2200,
        show_result
    )


# ============================================================
# RESULT
# ============================================================

def show_result():

    global scan_complete

    scan_complete = True

    clear_screen()

    score, year, verdict = calculate_result()

    tk.Label(
        main_frame,
        text="💍 KALYANAM ENNA? AI™",
        font=("Arial", 28, "bold"),
        bg=BG,
        fg=WHITE
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        main_frame,
        text="ANALYSIS COMPLETE",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=GREEN
    ).pack(
        pady=5
    )

    result_box = tk.Frame(
        main_frame,
        bg=PANEL,
        highlightbackground=RED_DARK,
        highlightthickness=2,
        padx=35,
        pady=25
    )

    result_box.pack(
        pady=25
    )

    tk.Label(
        result_box,
        text="KALYANAM READINESS",
        font=("Arial", 12, "bold"),
        bg=PANEL,
        fg=MUTED
    ).pack()

    tk.Label(
        result_box,
        text=f"{score}%",
        font=("Arial", 55, "bold"),
        bg=PANEL,
        fg=GOLD
    ).pack(
        pady=5
    )

    tk.Label(
        result_box,
        text="FICTIONAL PREDICTION",
        font=("Arial", 10, "bold"),
        bg=PANEL,
        fg=MUTED
    ).pack(
        pady=(15, 0)
    )

    tk.Label(
        result_box,
        text=str(year),
        font=("Arial", 38, "bold"),
        bg=PANEL,
        fg=RED
    ).pack(
        pady=5
    )

    tk.Label(
        result_box,
        text=verdict,
        font=("Arial", 17, "bold"),
        bg=PANEL,
        fg=WHITE,
        wraplength=650,
        justify="center"
    ).pack(
        pady=(15, 5)
    )

    tk.Label(
        main_frame,
        text="AI CONFIDENCE: 12% 😂",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=CYAN
    ).pack(
        pady=5
    )

    button_frame = tk.Frame(
        main_frame,
        bg=BG
    )

    button_frame.pack(
        pady=20
    )

    tk.Button(
        button_frame,
        text="🔄 ANALYSE ANOTHER HUMAN",
        font=("Arial", 13, "bold"),
        bg=RED_DARK,
        fg=WHITE,
        activebackground=RED,
        activeforeground=WHITE,
        relief="flat",
        padx=20,
        pady=12,
        cursor="hand2",
        command=start_test
    ).pack(
        side="left",
        padx=8
    )

    tk.Button(
        button_frame,
        text="👩 AMMA MODE",
        font=("Arial", 13, "bold"),
        bg=PANEL2,
        fg=GOLD,
        activebackground="#222b38",
        activeforeground=GOLD,
        relief="flat",
        padx=20,
        pady=12,
        cursor="hand2",
        command=amma_mode
    ).pack(
        side="left",
        padx=8
    )

    tk.Button(
        button_frame,
        text="👨 AMMAVAN MODE",
        font=("Arial", 13, "bold"),
        bg=PANEL2,
        fg=CYAN,
        activebackground="#222b38",
        activeforeground=CYAN,
        relief="flat",
        padx=20,
        pady=12,
        cursor="hand2",
        command=ammavan_mode
    ).pack(
        side="left",
        padx=8
    )


# ============================================================
# AMMA MODE
# ============================================================

def amma_mode():

    line = random.choice(
        AMMA_LINES
    )

    show_dialog(
        "👩 AMMA MODE",
        line
    )

    speak_async(
        line
    )


# ============================================================
# AMMAVAN MODE
# ============================================================

def ammavan_mode():

    line = random.choice(
        AMMAVAN_LINES
    )

    show_dialog(
        "👨 AMMAVAN MODE",
        line
    )

    speak_async(
        line
    )


# ============================================================
# CUSTOM DIALOG
# ============================================================

def show_dialog(title, message):

    dialog = tk.Toplevel(root)

    dialog.title(title)

    dialog.geometry(
        "600x320"
    )

    dialog.configure(
        bg=BG
    )

    dialog.transient(
        root
    )

    dialog.grab_set()

    tk.Label(
        dialog,
        text=title,
        font=("Arial", 24, "bold"),
        bg=BG,
        fg=GOLD
    ).pack(
        pady=(35, 15)
    )

    tk.Label(
        dialog,
        text=message,
        font=("Arial", 18, "bold"),
        bg=BG,
        fg=WHITE,
        wraplength=500,
        justify="center"
    ).pack(
        pady=20
    )

    tk.Button(
        dialog,
        text="ശരി 😭",
        font=("Arial", 13, "bold"),
        bg=RED_DARK,
        fg=WHITE,
        relief="flat",
        padx=30,
        pady=10,
        command=dialog.destroy
    ).pack(
        pady=20
    )


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

def keyboard(event):

    key = event.keysym.lower()

    if key == "escape":
        root.destroy()

    elif key == "r" and scan_complete:
        start_test()

    elif key == "a" and scan_complete:
        amma_mode()

    elif key == "m" and scan_complete:
        ammavan_mode()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "KALYANAM ENNA? AI™"
)

root.geometry(
    "1200x800"
)

root.minsize(
    900,
    650
)

root.configure(
    bg=BG
)

root.bind(
    "<Key>",
    keyboard
)


# ============================================================
# LOAD FACE DETECTOR
# ============================================================

cascade_path = cv2.data.haarcascades + \
    "haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier(
    cascade_path
)


# ============================================================
# TOP BAR
# ============================================================

top_bar = tk.Frame(
    root,
    bg="#080b10",
    height=55
)

top_bar.pack(
    fill="x",
    side="top"
)

tk.Label(
    top_bar,
    text="💍 KALYANAM ENNA? AI™",
    font=("Arial", 15, "bold"),
    bg="#080b10",
    fg=WHITE
).pack(
    side="left",
    padx=20,
    pady=15
)

tk.Label(
    top_bar,
    text="KERALA HUMAN ANALYSIS SYSTEM",
    font=("Arial", 9, "bold"),
    bg="#080b10",
    fg=RED
).pack(
    side="right",
    padx=20
)


# ============================================================
# MAIN FRAME
# ============================================================

main_frame = tk.Frame(
    root,
    bg=BG
)

main_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text=(
        "UNOFFICIAL EXPERIMENT • "
        "FOR ENTERTAINMENT ONLY • "
        "PREDICTIONS ARE FICTIONAL"
    ),
    font=("Arial", 8),
    bg="#080b10",
    fg="#4f5865"
)

footer.pack(
    fill="x",
    side="bottom",
    pady=7
)


# ============================================================
# START
# ============================================================

show_home()


# ============================================================
# CLOSE CLEANLY
# ============================================================

def on_close():

    stop_camera()

    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)


# ============================================================
# RUN
# ============================================================

root.mainloop()