import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import time
from questions import questions_data

class CodeTeacher:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Teacher")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f2f5")
        
        self.score = 0
        self.current_question = 0
        self.high_scores = self.load_high_scores()
        self.user_data = self.load_user_data()
        self.buttons_enabled = True
        self.current_topic = None
        self.in_high_scores = False
        self.current_user = None
        self.start_time = None
        self.topic_complete = False
        
        self.style = ttk.Style()
        # Topic button style
        self.style.configure("Custom.TButton", 
                           font=("Helvetica", 12, "bold"),
                           padding=8,
                           background="#34495e",
                           foreground="#ffffff",
                           borderwidth=0)
        self.style.map("Custom.TButton",
                      background=[("active", "#2c3e50")],
                      foreground=[("active", "#e0e0e0")])
        # Navigation button style (different color)
        self.style.configure("Nav.TButton", 
                           font=("Helvetica", 12, "bold"),
                           padding=8,
                           background="#e67e22",
                           foreground="#ffffff",
                           borderwidth=0)
        self.style.map("Nav.TButton",
                      background=[("active", "#d35400")],
                      foreground=[("active", "#f0f0f0")])
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_name_entry()

    def show_name_entry(self):
        self.content_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(self.content_frame, text="Enter your name:", 
                font=("Helvetica", 16, "bold"), bg="#f0f2f5", fg="#333333").pack(pady=30)
        
        self.name_entry = ttk.Entry(self.content_frame, width=40, font=("Helvetica", 12))
        self.name_entry.pack(pady=15)
        
        ttk.Button(self.content_frame, text="Start", command=self.validate_name,
                  style="Nav.TButton").pack(pady=20)

    def validate_name(self):
        name = self.name_entry.get().strip().lower()
        profanity = ["damn", "fuck", "shit", "ass", "bitch"]
        
        if len(name) < 5:
            messagebox.showwarning("Invalid Name", "Name must be at least 5 characters!")
        elif len(name) > 15:
            messagebox.showwarning("Invalid Name", "Name must be 15 characters or less!")
        elif any(word in name for word in profanity):
            messagebox.showwarning("Invalid Name", "Invalid name!")
        else:
            if name in self.user_data:
                print(f"Existing user found: {name}, loading progress")
                for topic in questions_data.keys():
                    if topic not in self.user_data[name]:
                        self.user_data[name][topic] = {"completed": 0, "time": None, "elapsed": 0}
                    elif isinstance(self.user_data[name][topic], int):
                        self.user_data[name][topic] = {"completed": self.user_data[name][topic], "time": None, "elapsed": 0}
                    elif "elapsed" not in self.user_data[name][topic]:
                        self.user_data[name][topic]["elapsed"] = 0
            else:
                print(f"New user: {name}, initializing progress")
                self.user_data[name] = {topic: {"completed": 0, "time": None, "elapsed": 0} for topic in questions_data.keys()}
            self.current_user = name
            self.save_user_data()
            self.content_frame.destroy()
            self.create_ui()
            self.show_home()

    def create_ui(self):
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="Code Teacher", 
                font=("Helvetica", 18, "bold"), fg="white", bg="#2c3e50").pack(pady=20)
        
        self.content_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.score_label = tk.Label(self.content_frame, text=f"Score: {self.score}", 
                                  font=("Helvetica", 14, "bold"), bg="#f0f2f5", fg="#333333")
        self.score_label.pack(pady=10)
        
        self.timer_label = tk.Label(self.content_frame, text="Time: 00:00", 
                                   font=("Helvetica", 12), bg="#f0f2f5", fg="#555555")
        self.timer_label.pack(pady=5)
        self.timer_label.pack_forget()
        
        self.question_frame = tk.Frame(self.content_frame, bg="#f0f2f5")
        self.question_frame.pack(pady=10)
        
        self.question_label = tk.Label(self.question_frame, text="", 
                                     font=("Helvetica", 16), bg="#f0f2f5", fg="#333333", wraplength=700)
        self.question_label.pack(side="left", padx=(0, 15))
        
        self.difficulty_label = tk.Label(self.question_frame, text="", 
                                       font=("Helvetica", 12, "bold"), width=12, height=2,
                                       relief="solid", borderwidth=1)
        self.difficulty_label.pack(side="left")
        self.difficulty_label.pack_forget()
        
        self.options_frame = tk.Frame(self.content_frame, bg="#f0f2f5")
        self.options_frame.pack(pady=15)
        
        self.feedback_label = tk.Label(self.content_frame, text="", 
                                     font=("Helvetica", 12), bg="#f0f2f5", fg="#333333")
        self.feedback_label.pack(pady=10)
        
        self.button_frame = tk.Frame(self.content_frame, bg="#f0f2f5")
        self.button_frame.pack(pady=15)
        
        ttk.Button(self.button_frame, text="View Leaderboard", command=self.show_high_scores,
                  style="Nav.TButton").pack(side="left", padx=5)
        self.faq_button = ttk.Button(self.button_frame, text="FAQ", command=self.show_faq,
                                    style="Nav.TButton")
        self.faq_button.pack(side="left", padx=5)
        self.faq_button.pack_forget()
        self.reset_button = ttk.Button(self.button_frame, text="Reset Score", command=self.reset_score,
                                      style="Nav.TButton")
        self.reset_button.pack(side="left", padx=5)
        self.reset_button.pack_forget()
        self.home_button = ttk.Button(self.button_frame, text="Home", command=self.return_home,
                                    style="Nav.TButton")
        self.home_button.pack(side="left", padx=5)
        self.home_button.pack_forget()

    def show_home(self):
        self.current_topic = None
        self.in_high_scores = False
        self.score = 0
        self.current_question = 0
        self.topic_complete = False
        total_score = self.calculate_user_score(self.current_user)
        self.score_label.config(text=f"Score: {total_score}")
        self.timer_label.pack_forget()
        self.question_label.config(text=f"Welcome, {self.current_user.capitalize()}!\nChoose a topic:")
        self.difficulty_label.pack_forget()
        self.clear_options()
        self.feedback_label.config(text="")
        self.home_button.pack_forget()
        self.faq_button.pack(side="left", padx=5)
        self.reset_button.pack(side="left", padx=5)
        
        topics = list(questions_data.keys())
        left_column = topics[:3]  # First 3 topics
        right_column = topics[3:]  # Last 3 topics
        
        self.topics_frame = tk.Frame(self.options_frame, bg="#f0f2f5")
        self.topics_frame.pack()
        
        left_frame = tk.Frame(self.topics_frame, bg="#f0f2f5")
        left_frame.pack(side="left", padx=10)
        right_frame = tk.Frame(self.topics_frame, bg="#f0f2f5")
        right_frame.pack(side="left", padx=10)
        
        # Left column
        for topic in left_column:
            completed = self.user_data[self.current_user][topic]["completed"]
            time_taken = self.user_data[self.current_user][topic]["time"]
            topic_score = sum(10 if q["difficulty"] <= 10 else (20 if q["difficulty"] <= 20 else 30)
                             for q in questions_data[topic][:completed])
            max_score = self.calculate_topic_score(topic)
            topic_display = " ".join(word.capitalize() for word in topic.split("_"))
            text = f"{topic_display} ({completed}/30 - {topic_score}/{max_score})"
            if completed == 30 and time_taken:
                text += f" - {time_taken}"
            btn = ttk.Button(left_frame, text=text,
                           command=lambda t=topic: self.start_topic(t),
                           style="Custom.TButton", width=40)
            btn.pack(pady=10)
        
        # Right column
        for topic in right_column:
            completed = self.user_data[self.current_user][topic]["completed"]
            time_taken = self.user_data[self.current_user][topic]["time"]
            topic_score = sum(10 if q["difficulty"] <= 10 else (20 if q["difficulty"] <= 20 else 30)
                             for q in questions_data[topic][:completed])
            max_score = self.calculate_topic_score(topic)
            topic_display = " ".join(word.capitalize() for word in topic.split("_"))
            text = f"{topic_display} ({completed}/30 - {topic_score}/{max_score})"
            if completed == 30 and time_taken:
                text += f" - {time_taken}"
            btn = ttk.Button(right_frame, text=text,
                           command=lambda t=topic: self.start_topic(t),
                           style="Custom.TButton", width=40)
            btn.pack(pady=10)
        
        self.root.update()

    def reset_score(self):
        if messagebox.askyesno("Confirm", "Are you sure you want your score and progress to be wiped out?"):
            self.user_data[self.current_user] = {topic: {"completed": 0, "time": None, "elapsed": 0} for topic in questions_data.keys()}
            self.high_scores = [entry for entry in self.high_scores if entry["name"] != self.current_user]
            self.save_user_data()
            self.save_high_score(0)
            self.show_home()

    def start_topic(self, topic):
        self.current_topic = topic
        completed = self.user_data[self.current_user][topic]["completed"]
        if completed == 30:
            if messagebox.askyesno("Reset?", f"You’ve completed {topic.capitalize()}! Want to try again? This will reset your progress and score."):
                old_score = self.calculate_topic_score(topic)
                for entry in self.high_scores:
                    if entry["name"] == self.current_user and entry["topic"] == topic:
                        entry["score"] = max(0, entry["score"] - old_score)
                        break
                self.user_data[self.current_user][topic] = {"completed": 0, "time": None, "elapsed": 0}
                self.score = 0
                self.current_question = 0
                self.start_time = time.time()
            else:
                return
        else:
            self.current_question = completed
            self.score = 0
            self.start_time = time.time() - self.user_data[self.current_user][topic]["elapsed"]
        
        self.topic_complete = False
        self.score_label.config(text=f"Score: {self.score}")
        self.timer_label.pack()
        self.update_timer()
        self.home_button.pack(side="left", padx=5)
        self.faq_button.pack_forget()
        self.reset_button.pack_forget()
        self.display_question()

    def update_timer(self):
        if self.current_topic and not self.in_high_scores and not self.topic_complete:
            elapsed = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed, 60)
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def return_home(self):
        if not self.in_high_scores and self.current_topic:
            if not self.topic_complete and messagebox.askyesno("Confirm", "Are you sure you want to quit? Your work will be saved if you quit."):
                if self.current_topic:
                    elapsed = int(time.time() - self.start_time)
                    self.user_data[self.current_user][self.current_topic]["elapsed"] = elapsed
                self.save_user_data()
                self.show_home()
            elif self.topic_complete:
                self.show_home()
        else:
            self.show_home()

    def clear_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

    def disable_buttons(self):
        self.buttons_enabled = False
        for widget in self.options_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.config(state="disabled")

    def enable_buttons(self):
        self.buttons_enabled = True
        for widget in self.options_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.config(state="normal")

    def display_question(self):
        if self.current_question >= len(questions_data[self.current_topic]):
            self.end_game()
            return
            
        question = questions_data[self.current_topic][self.current_question]
        self.question_label.config(text=f"Question {self.current_question + 1}: {question['question']}")
        self.difficulty_label.pack()
        self.update_difficulty(question["difficulty"])
        self.feedback_label.config(text="")
        
        self.clear_options()
        for option in question["options"]:
            btn = ttk.Button(self.options_frame, text=option,
                           command=lambda x=option: self.check_answer(x),
                           style="Custom.TButton")
            btn.pack(pady=8, padx=10, fill="x")
        self.enable_buttons()

    def update_difficulty(self, difficulty):
        if difficulty <= 10:
            color = "#2ecc71"
            text = "Easy"
        elif difficulty <= 20:
            color = "#3498db"
            text = "Medium"
        else:
            color = "#e74c3c"
            text = "Hard"
        self.difficulty_label.config(text=text, bg=color, fg="white")

    def check_answer(self, selected):
        if not self.buttons_enabled or not self.current_topic:
            return
            
        self.disable_buttons()
        question = questions_data[self.current_topic][self.current_question]
        correct = question["correct"]
        
        if selected == correct:
            points = 10 if question["difficulty"] <= 10 else (20 if question["difficulty"] <= 20 else 30)
            self.score += points
            self.score_label.config(text=f"Score: {self.score}")
            self.feedback_label.config(text="Correct!", fg="green")
            messagebox.showinfo("Congratulations!", f"Correct answer!\nYou gained {points} points\nTotal Score: {self.score}")
            self.user_data[self.current_user][self.current_topic]["completed"] = max(
                self.user_data[self.current_user][self.current_topic]["completed"], self.current_question + 1)
            self.save_user_data()
            self.current_question += 1
            self.root.after(100, self.display_question)
        else:
            self.feedback_label.config(text=f"Wrong! Correct answer was: {correct}", fg="red")
            messagebox.showinfo("Wrong!", f"Wrong answer!\nCorrect answer was: {correct}")
            self.current_question += 1
            self.root.after(100, self.display_question)

    def calculate_topic_score(self, topic):
        total = 0
        for question in questions_data[topic]:
            points = 10 if question["difficulty"] <= 10 else (20 if question["difficulty"] <= 20 else 30)
            total += points
        return total

    def calculate_user_score(self, user):
        total_score = 0
        for topic in questions_data.keys():
            completed = self.user_data[user][topic]["completed"]
            for i in range(completed):
                question = questions_data[topic][i]
                points = 10 if question["difficulty"] <= 10 else (20 if question["difficulty"] <= 20 else 30)
                total_score += points
        return total_score

    def calculate_max_score(self):
        total = 0
        for topic in questions_data.keys():
            total += self.calculate_topic_score(topic)
        return total

    def end_game(self):
        elapsed = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.user_data[self.current_user][self.current_topic]["time"] = time_str
        self.save_high_score(self.score)
        self.question_label.config(text=f"Topic Complete! Final Score: {self.score} (Time: {time_str})")
        self.timer_label.pack_forget()
        self.difficulty_label.pack_forget()
        self.clear_options()
        self.feedback_label.config(text="Progress saved automatically.")
        self.topic_complete = True

    def load_high_scores(self):
        if os.path.exists("high_scores.json"):
            with open("high_scores.json", "r") as f:
                content = f.read().strip()
                if content:
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        print("Warning: high_scores.json contains invalid JSON, returning empty list")
                        return []
                else:
                    print("Warning: high_scores.json is empty, returning empty list")
                    return []
        return []

    def load_user_data(self):
        if os.path.exists("user_data.json"):
            with open("user_data.json", "r") as f:
                content = f.read().strip()
                if content:
                    try:
                        data = json.loads(content)
                        for user in data:
                            for topic in data[user]:
                                if isinstance(data[user][topic], int):
                                    data[user][topic] = {"completed": data[user][topic], "time": None, "elapsed": 0}
                                elif "elapsed" not in data[user][topic]:
                                    data[user][topic]["elapsed"] = 0
                        return data
                    except json.JSONDecodeError:
                        print("Warning: user_data.json contains invalid JSON, returning empty dict")
                        return {}
                else:
                    print("Warning: user_data.json is empty, returning empty dict")
                    return {}
        return {}

    def save_user_data(self):
        with open("user_data.json", "w") as f:
            json.dump(self.user_data, f)

    def save_high_score(self, score):
        found = False
        for entry in self.high_scores:
            if entry["name"] == self.current_user and entry["topic"] == self.current_topic:
                entry["score"] = max(entry["score"], score)
                found = True
                break
        if not found:
            self.high_scores.append({"name": self.current_user, "score": score, "topic": self.current_topic})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:5]
        with open("high_scores.json", "w") as f:
            json.dump(self.high_scores, f)

    def show_high_scores(self):
        if not self.in_high_scores and self.current_topic and not self.topic_complete:
            if not messagebox.askyesno("Confirm", "Are you sure you want to quit? Your work will be saved if you quit."):
                return
            if self.current_topic:
                elapsed = int(time.time() - self.start_time)
                self.user_data[self.current_user][self.current_topic]["elapsed"] = elapsed
            self.save_user_data()
        
        self.in_high_scores = True
        self.clear_options()
        self.question_label.config(text="Leaderboard")
        self.timer_label.pack_forget()
        self.difficulty_label.pack_forget()
        self.home_button.pack(side="left", padx=5)
        self.faq_button.pack_forget()
        self.feedback_label.config(text="")
        
        tk.Label(self.options_frame, text="Order", font=("Helvetica", 12, "bold"), 
                bg="#f0f2f5", fg="#333333", width=10).grid(row=0, column=0, pady=5)
        tk.Label(self.options_frame, text="Name", font=("Helvetica", 12, "bold"), 
                bg="#f0f2f5", fg="#333333", width=20, anchor="w").grid(row=0, column=1, pady=5)
        tk.Label(self.options_frame, text="Solved", font=("Helvetica", 12, "bold"), 
                bg="#f0f2f5", fg="#333333", width=10).grid(row=0, column=2, pady=5)
        tk.Label(self.options_frame, text="Score", font=("Helvetica", 12, "bold"), 
                bg="#f0f2f5", fg="#333333", width=15).grid(row=0, column=3, pady=5)
        
        leaderboard = {}
        max_score = self.calculate_max_score()
        for user in self.user_data:
            total_solved = sum(self.user_data[user][topic]["completed"] for topic in questions_data.keys())
            total_score = self.calculate_user_score(user)
            leaderboard[user] = (total_solved, total_score)
        
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: (-x[1][1], -x[1][0], x[0]))
        
        for i, (user, (solved, score)) in enumerate(sorted_leaderboard, 1):
            tk.Label(self.options_frame, text=str(i), font=("Helvetica", 12), 
                    bg="#f0f2f5", fg="#333333", width=10).grid(row=i, column=0, pady=5)
            tk.Label(self.options_frame, text=user.title(), font=("Helvetica", 12), 
                    bg="#f0f2f5", fg="#333333", width=20, anchor="w").grid(row=i, column=1, pady=5)
            tk.Label(self.options_frame, text=f"{solved}/180", font=("Helvetica", 12), 
                    bg="#f0f2f5", fg="#333333", width=10).grid(row=i, column=2, pady=5)
            tk.Label(self.options_frame, text=f"{score}/{max_score}", font=("Helvetica", 12), 
                    bg="#f0f2f5", fg="#333333", width=15).grid(row=i, column=3, pady=5)

    def show_faq(self):
        self.clear_options()
        self.question_label.config(text="Frequently Asked Questions")
        self.timer_label.pack_forget()
        self.difficulty_label.pack_forget()
        self.home_button.pack(side="left", padx=5)
        self.faq_button.pack_forget()
        self.feedback_label.config(text="")
        
        tk.Label(self.options_frame, text="How are scores calculated?", 
                font=("Helvetica", 14, "bold"), bg="#f0f2f5", fg="#333333", anchor="w").pack(pady=(10, 5), padx=10, anchor="w")
        tk.Label(self.options_frame, text="Questions 1-10 are Easy (worth 10 points each), Questions 11-20 are Medium (20 points), and Questions 21-30 are Hard (30 points).", 
                font=("Helvetica", 12), bg="#f0f2f5", fg="#333333", wraplength=700, justify="left").pack(pady=5, padx=20, anchor="w")
        
        tk.Label(self.options_frame, text="What happens to my data?", 
                font=("Helvetica", 14, "bold"), bg="#f0f2f5", fg="#333333", anchor="w").pack(pady=(10, 5), padx=10, anchor="w")
        tk.Label(self.options_frame, text="We don’t use your data for any other purposes except showing it on the leaderboard.", 
                font=("Helvetica", 12), bg="#f0f2f5", fg="#333333", wraplength=700, justify="left").pack(pady=5, padx=20, anchor="w")

    def on_closing(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            if self.current_topic and not self.topic_complete:
                elapsed = int(time.time() - self.start_time)
                self.user_data[self.current_user][self.current_topic]["elapsed"] = elapsed
            self.save_user_data()
            self.root.destroy()

def main():
    root = tk.Tk()
    app = CodeTeacher(root)
    root.mainloop()

if __name__ == "__main__":
    main()