import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import re
import math

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

previous_result = 0
running = True

# GUI Setup
root = tk.Tk()
root.title("Voice Controlled Calculator")
root.geometry("600x450")
root.config(bg="#1e1e2f")

expression_var = tk.StringVar()
result_var = tk.StringVar()
status_var = tk.StringVar(value="🔒 Awaiting authentication...")

status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 12, "italic"), fg="orange", bg="#1e1e2f")
status_label.pack(pady=5)

expression_label = tk.Label(root, textvariable=expression_var, font=("Consolas", 14), fg="lime", bg="#1e1e2f", wraplength=550, justify="left")
expression_label.pack(pady=20)

result_label = tk.Label(root, textvariable=result_var, font=("Consolas", 24, "bold"), fg="cyan", bg="#1e1e2f")
result_label.pack(pady=10)

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def get_voice_input():
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Didn't catch that.")
        except sr.RequestError:
            print("❌ Speech service error.")
    return None

def words_to_number(text):
    num_words = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
        "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
        "eighteen": "18", "nineteen": "19", "twenty": "20", "thirty": "30",
        "forty": "40", "fifty": "50", "sixty": "60", "seventy": "70",
        "eighty": "80", "ninety": "90"
    }

    for word, digit in num_words.items():
        text = re.sub(rf"\\b{word}\\b", digit, text)

    text = re.sub(r"(\d+)\s+point\s+(\d+)", r"\1.\2", text)
    return text

def parse_input(text, previous_result):
    text = words_to_number(text)

    if "change" in text:
        parts = text.split("change")[-1].strip().split("to")
        if len(parts) == 2:
            return ["__change__", parts[0].strip(), parts[1].strip()]

    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("times", "*")
    text = text.replace("multiplied by", "*")
    text = text.replace("divided by", "/")
    text = text.replace("over", "/")

    if "previous result" in text:
        text = text.replace("previous result", str(previous_result))

    sqrt_matches = re.findall(r"square root(?: of)? (\d*\.?\d+)", text)
    for match in sqrt_matches:
        number = float(match)
        sqrt_val = round(math.sqrt(number), 4)
        text = text.replace(f"square root of {match}", str(sqrt_val))
        text = text.replace(f"square root {match}", str(sqrt_val))

    raw_tokens = re.findall(r"[-+]?\d*\.?\d+|[+\-*/]", text)
    return raw_tokens

def evaluate_expression(tokens):
    expression = " ".join(tokens)
    try:
        result = eval(expression)
        if '/' in expression:
            result = round(result, 2)
        if '+' in expression:
            result = round(result, 2)
        return expression, result
    except Exception as e:
        print(f"❌ Evaluation error: {e}")
        return None, None

def is_valid_math_input(text):
    math_keywords = ["plus", "minus", "times", "divided", "over", "square root", "point", "equals", "equal", "delete", "previous result", "change"]
    if any(word in text for word in math_keywords):
        return True
    if re.search(r"\d", text):
        return True
    return False

def voice_loop():
    global previous_result, running
    expression_tokens = []

    speak("Let me confirm if you are Imtiaz")
    status_var.set("🔐 Confirming identity...")

    while running:
        command = get_voice_input()
        if command and "start buddy" in command:
            speak("Welcome back!")
            status_var.set("✅ Authenticated. Speak your expression.")
            break

    while running:
        user_input = get_voice_input()
        if user_input is None:
            continue

        if "that's it buddy" in user_input or "void" in user_input:
            speak("Goodbye.")
            status_var.set("🔚 Session ended.")
            running = False
            root.after(1000, root.quit)
            break

        if "delete" in user_input:
            if expression_tokens:
                removed = expression_tokens.pop()
                speak(f"Deleted {removed}")
                expression_var.set(" ".join(expression_tokens))
            continue

        if "equals" in user_input or "equal" in user_input:
            expression, result = evaluate_expression(expression_tokens)
            if result is not None:
                expression_var.set(f"Expression: {expression}")
                result_var.set(f"Result: {result}")
                speak(f"The result is {result}")
                previous_result = result
            else:
                speak("Sorry, I couldn't evaluate that.")
            expression_tokens = []
            continue

        if is_valid_math_input(user_input):
            tokens = parse_input(user_input, previous_result)
            if tokens and tokens[0] == "__change__":
                old_val, new_val = tokens[1], tokens[2]
                found = False
                for idx, val in enumerate(expression_tokens):
                    if val == old_val:
                        expression_tokens[idx] = new_val
                        speak(f"Changed {old_val} to {new_val}")
                        found = True
                        break
                if not found:
                    speak(f"Couldn't find {old_val} in expression.")
            else:
                valid_tokens = [t for t in tokens if re.match(r'^[-+]?\d*\.?\d+$|^[+\-*/]$', t)]
                if valid_tokens:
                    expression_tokens.extend(valid_tokens)
            expression_var.set(" ".join(expression_tokens))
        else:
            speak("Ignored non-mathematical input.")

# Run the voice thread
threading.Thread(target=voice_loop, daemon=True).start()

# Start GUI loop
root.mainloop()

