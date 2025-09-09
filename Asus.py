import customtkinter as ctk
import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import os
import datetime
import json
import time
import difflib

def heard_asus(text):
    return difflib.get_close_matches("asus", [text], n=1, cutoff=0.6)




# After catch blocks in listen():
time.sleep(0.5)  # Add slight delay to avoid CPU hogging


# ==== Memory File Setup ====
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {"name": None, "favorite_app": None}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)

memory = load_memory()

# ==== Voice Setup ====
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    response_box.configure(state="normal")
    response_box.insert(tk.END, f"\n🗣️ {text}\n")
    response_box.configure(state="disabled")
    response_box.see(tk.END)
    print("🗣️", text)
    engine.say(text)
    engine.runAndWait()

    

# ==== Command Processor ====
def process_command(command):
    command = command.lower()
    print("✅ You said:", command)

    if "open notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "open chrome" in command:
        speak("Opening Chrome.")
        os.system("start chrome")

    elif "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query}")
        os.system(f"start https://www.google.com/search?q={query}")

    elif "remember my name is" in command:
        name = command.replace("remember my name is", "").strip().capitalize()
        memory["name"] = name
        save_memory(memory)
        speak(f"I will remember your name is {name}.")

    elif "what is my name" in command or "what ise my name" in command:
        if memory["name"]:
            speak(f"Your name is {memory['name']}.")
        else:
            speak("I don't know your name yet.")

    elif "remember my favorite faculty is" in command:
        faculty_name = command.replace("remember my favorite faculty is", "").strip().capitalize()
        memory["favorite_faculty"] = faculty_name
        save_memory(memory)
        speak(f"Got it. Your favorite faculty is {faculty_name}.")

    elif "what is my favorite faculty" in command:
        if memory["favorite_faculty"]:
            speak(f"Your favorite faculty is {memory['favorite_faculty']}.")
        else:
            speak("I don't know your favorite faculty yet.")

    elif "open youtube" in command:
        speak("Opening YouTube.")
        os.system("start https://youtube.com")
        
    elif "system info" in command:
        import platform
        sys_info = platform.uname()
        speak(f"System: {sys_info.system}, Node: {sys_info.node}, Processor: {sys_info.processor}")

    elif "shutdown" in command:
        speak("Shutting down your system.")
        os.system("shutdown /s /t 5")

    elif "play music" in command:
        speak("Playing music.")
        music_path = "C:/Path/To/Your/Music.mp3"
        os.startfile(music_path)

    elif "tell me a joke" in command:
        speak("Why did the developer go broke? Because he used up all his cache!")

   
            
    elif "internet speed" in command:
        import speedtest
        speak("Checking internet speed...")
        st = speedtest.Speedtest()
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        speak(f"Download speed is {download:.2f} megabits per second. Upload speed is {upload:.2f}.")

    elif "open whatsapp" in command:
        speak("Opening WhatsApp.")
        try:
            os.system("start whatsapp")  # Works if WhatsApp Desktop is installed and registered in PATH
        except:
            speak("WhatsApp is not installed or couldn't be found.")

    elif "tell me a joke" in command:
        import pyjokes
        joke = pyjokes.get_joke()
        speak(joke)

    elif "play" in command and "on youtube" in command:
        query = command.replace("play", "").replace("on youtube", "").strip()
        speak(f"Playing {query} ")
        os.system(f"start https://www.youtube.com/results?search_query={query}")


    elif "stop listening" in command:
        speak("stop now.")
        app.quit()

    else:
        speak("Sorry, I didn't understand that.")

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        try:
            status_label.configure(text="🎧 Waiting for wake word 'Asus'...")
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, phrase_time_limit=4)

            wake_up = recognizer.recognize_google(audio).lower()
            print("Wake attempt:", wake_up)

           
            if "asus" in wake_up:
                speak("At your service. What can I do for you Sir?")
                status_label.configure(text="🎤 Listening for command...")

                with mic as source:
                    audio2 = recognizer.listen(source, phrase_time_limit=5)
                command = recognizer.recognize_google(audio2)
                process_command(command)
                status_label.configure(text="Idle. Say 'Asus' to activate.")

        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError:
            speak("Network error.")
        except Exception as e:
            print("Error:", e)

# ==== GUI Setup ====
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x600")
app.title("ASUS - Your AI Assistant")
app.resizable(False, False)

# ==== Top Section ====
title_label = ctk.CTkLabel(app, text="🤖 SURABHBOOK", font=("Arial Black", 32))
title_label.pack(pady=(15, 5))

status_label = ctk.CTkLabel(app, text="Idle. Say 'Asus' to activate.", font=("Arial", 16))

status_label.pack(pady=5)

# ==== Response Display Box ====
response_box = tk.Text(app, height=10, width=70, bg="#1e1e1e", fg="cyan", font=("Consolas", 13), wrap="word")
response_box.pack(pady=10)
response_box.configure(state="disabled")

# ==== Command Buttons (Popular Commands Section) ====
button_frame = ctk.CTkFrame(app, fg_color="#2b2b2b")
button_frame.pack(pady=10)

# List of commands: (Button Label, Action)
suggested_commands = [
    ("Open Notepad", lambda: process_command("open notepad")),
    ("Open Chrome", lambda: process_command("open chrome")),
    ("What is my name", lambda: process_command("what is my name")),
    ("Search Python", lambda: process_command("search python")),

    # 🆕 Added more buttons below
    ("Open YouTube", lambda: process_command("open youtube")),
    ("Shutdown", lambda: process_command("shutdown")),
    ("Play Music", lambda: process_command("play music")),
    ("Tell a Joke", lambda: process_command("tell me a joke"))
  
]

# Organize buttons in rows (3 buttons per row)
for i in range(0, len(suggested_commands), 3):  # 3 buttons per row
    row_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
    row_frame.pack()
    for text, action in suggested_commands[i:i+3]:
        btn = ctk.CTkButton(row_frame, text=text, command=action, width=150)
        btn.pack(side="left", padx=10, pady=10)


# ==== Bottom Controls ====
bottom_frame = ctk.CTkFrame(app, fg_color="transparent")
bottom_frame.pack(side="bottom", pady=10, fill="x")

exit_button = ctk.CTkButton(bottom_frame, text="Exit", command=app.quit, fg_color="red")
exit_button.pack(side="left", padx=20, pady=5)

# ==== Greeting (No Initial Speak) ====
print("ASUS is idle. Waiting for wake word...")

# ==== Start Listening Thread ====
threading.Thread(target=listen, daemon=True).start()

app.mainloop()
