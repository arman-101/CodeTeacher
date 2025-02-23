import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from questions import questions_data

class ProgrammingTriviaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Programming Trivia Challenge")
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
        
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", 
                           font=("Helvetica", 12, "bold"),
                           padding=5,
                           background="#34495e",
                           foreground="#ffffff",
                           borderwidth=0)
        self.style.map("Custom.TButton",
                      background=[("active", "#2c3e50")],
                      foreground=[("active", "#ffffff")])
        
        self.show_name_entry()

    def show_name_entry(self):
        self.content_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(self.content_frame, text="Enter your name:", 
                font=("Helvetica", 14), bg="#f0f2f5", fg="#333333").pack(pady=20)
        
        self.name_entry = ttk.Entry(self.content_frame, width=30)
        self.name_entry.pack(pady=10)
        
        ttk.Button(self.content_frame, text="Start", command=self.validate_name,
                  style="Custom.TButton").pack(pady=5)

    def validate_name(self):
        name = self.name_entry.get().strip()
        profanity = ["damn", "fuck", "shit", "ass", "bitch"]
        
        if len(name) < 5:
            messagebox.showwarning("Invalid Name", "Name must be at least 5 characters!")
        elif len(name) > 15:
            messagebox.showwarning("Invalid Name", "Name must be 15 characters or less!")
        elif any(word in name.lower() for word in profanity):
            messagebox.showwarning("Invalid Name", "Invalid name!")
        else:
            # Capitalize first letter of each word
            self.current_user = " ".join(word.capitalize() for word in name.split())
            if self.current_user.lower() not in self.user_data:
                self.user_data[self.current_user.lower()] = {topic: 0 for topic in questions_data.keys()}
            self.save_user_data()
            self.content_frame.destroy()
            self.create_ui()
            self.show_home()

    def create_ui(self):
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="Programming Trivia Challenge", 
                font=("Helvetica", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=15)
        
        self.content_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.content_frame.pack(fill="both", expand=True)
        
        self.score_label = tk.Label(self.content_frame, text=f"Score: {self.score}", 
                                  font=("Helvetica", 12, "bold"), bg="#f0f2f5", fg="#333333")
        self.score_label.pack(pady=5)
        
        self.question_frame = tk.Frame(self.content_frame, bg="#f0f2f5")
        self.question_frame.pack(pady=5)
        
        self.question_label = tk.Label(self.question_frame, text="", 
                                     font=("Helvetica", 14), bg="#f0f2f5", fg="#333333", wraplength=600)
        self.question_label.pack(side="left", padx=(0, 10))
        
        self.difficulty_label = tk.Label(self.question_frame, text="", 
                                       font=("Helvetica", 12, "bold"), width=10, height=2,
                                       relief="solid", borderwidth=1)
        self.difficulty_label.pack(side="left")
        self.difficulty_label.pack_forget()
        
        self.options_frame = tk.Frame(self.content_frame, bg="#f0f2f5")
        self.options_frame.pack()
        
        self.feedback_label = tk.Label(self.content_frame, text="", 
                                     font=("Helvetica", 11), bg="#f0f2f5", fg="#333333")
        self.feedback_label.pack(pady=5)
        
        self.button_frame = tk.Frame(self.content_frame, bg="#f0f2f5")
        self.button_frame.pack()
        
        ttk.Button(self.button_frame, text="View Leaderboard", command=self.show_high_scores,
                  style="Custom.TButton").pack(side="left", padx=2)
        self.home_button = ttk.Button(self.button_frame, text="Home", command=self.return_home,
                                    style="Custom.TButton")
        self.home_button.pack(side="left", padx=2)
        self.home_button.pack_forget()

    def show_home(self):
        self.current_topic = None
        self.in_high_scores = False
        self.score = 0
        self.current_question = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.question_label.config(text=f"Welcome, {self.current_user}!\nChoose a topic:")
        self.difficulty_label.pack_forget()
        self.clear_options()
        self.feedback_label.config(text="")
        self.home_button.pack_forget()
        
        topics = list(questions_data.keys())
        for topic in topics:
            completed = self.user_data[self.current_user.lower()][topic]
            text = f"{topic.capitalize()} ({completed}/10)"
            if completed == 10:
                text += " - Completed!"
            btn = ttk.Button(self.options_frame, text=text,
                           command=lambda t=topic: self.start_topic(t),
                           style="Custom.TButton")
            btn.pack(pady=2)

    def start_topic(self, topic):
        completed = self.user_data[self.current_user.lower()][topic]
        if completed == 10:
            if messagebox.askyesno("Reset?", f"You've completed {topic}! Want to try again?"):
                self.user_data[self.current_user.lower()][topic] = 0
                self.save_user_data()
        
        self.current_topic = topic
        self.current_question = 0
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.home_button.pack(side="left", padx=2)
        self.display_question()

    def return_home(self):
        if not self.in_high_scores and self.current_topic:
            if messagebox.askyesno("Confirm", "Are you sure? This will reset your progress in this topic."):
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
            btn.pack(pady=2)
        self.enable_buttons()

    def update_difficulty(self, difficulty):
        if difficulty <= 3:
            color = "#2ecc71"
            text = "Easy"
        elif difficulty <= 7:
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
            points = (question["difficulty"] + 1) * 10
            self.score += points
            self.score_label.config(text=f"Score: {self.score}")
            self.feedback_label.config(text="Correct!", fg="green")
            messagebox.showinfo("Congratulations!", f"Correct answer!\nYou gained {points} points\nTotal Score: {self.score}")
            self.user_data[self.current_user.lower()][self.current_topic] = max(
                self.user_data[self.current_user.lower()][self.current_topic], self.current_question + 1)
            self.save_user_data()
            self.current_question += 1
            self.root.after(100, self.display_question)
        else:
            self.feedback_label.config(text=f"Wrong! Correct answer was: {correct}", fg="red")
            self.current_question += 1

    def end_game(self):
        self.question_label.config(text=f"Topic Complete! Final Score: {self.score}")
        self.difficulty_label.pack_forget()
        self.clear_options()
        self.feedback_label.config(text="Enter your name to save your score:")
        
        name_entry = ttk.Entry(self.options_frame)
        name_entry.pack(pady=5)
        
        ttk.Button(self.options_frame, text="Save Score",
                  command=lambda: self.save_score(name_entry.get()),
                  style="Custom.TButton").pack(pady=2)

    def load_high_scores(self):
        if os.path.exists("high_scores.json"):
            with open("high_scores.json", "r") as f:
                return json.load(f)
        return []

    def load_user_data(self):
        if os.path.exists("user_data.json"):
            with open("user_data.json", "r") as f:
                return json.load(f)
        return {}

    def save_user_data(self):
        with open("user_data.json", "w") as f:
            json.dump(self.user_data, f)

    def save_score(self, name):
        if name:
            self.high_scores.append({"name": name, "score": self.score, "topic": self.current_topic})
            self.high_scores.sort(key=lambda x: x["score"], reverse=True)
            self.high_scores = self.high_scores[:5]
            
            with open("high_scores.json", "w") as f:
                json.dump(self.high_scores, f)
            
            self.show_high_scores()
        else:
            messagebox.showwarning("Warning", "Please enter a name!")

    def show_high_scores(self):
        self.in_high_scores = True
        self.clear_options()
        self.question_label.config(text="Leaderboard")
        self.difficulty_label.pack_forget()
        self.home_button.pack(side="left", padx=2)
        
        self.feedback_label.config(text="")
        
        # Create table-like structure
        tk.Label(self.options_frame, text="Name", font=("Helvetica", 12, "bold"), 
                bg="#f0f2f5", fg="#333333", width=20, anchor="w").grid(row=0, column=0, pady=2)
        tk.Label(self.options_frame, text="Solved /30", font=("Helvetica", 12, "bold"), 
                bg="#f0f2f5", fg="#333333", width=10).grid(row=0, column=1, pady=2)
        
        # Calculate total solved for each user
        leaderboard = {}
        for user in self.user_data:
            total_solved = sum(self.user_data[user][topic] for topic in questions_data.keys())
            leaderboard[user] = total_solved
        
        # Sort by solved questions, then alphabetically
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: (-x[1], x[0]))
        
        for i, (user, solved) in enumerate(sorted_leaderboard[:10], 1):  # Top 10
            tk.Label(self.options_frame, text=user.title(), font=("Helvetica", 12), 
                    bg="#f0f2f5", fg="#333333", width=20, anchor="w").grid(row=i, column=0, pady=2)
            tk.Label(self.options_frame, text=f"{solved}/30", font=("Helvetica", 12), 
                    bg="#f0f2f5", fg="#333333", width=10).grid(row=i, column=1, pady=2)
        
        ttk.Button(self.options_frame, text="Play Again",
                  command=self.show_home,
                  style="Custom.TButton").grid(row=11, column=0, columnspan=2, pady=2)

def main():
    root = tk.Tk()
    app = ProgrammingTriviaGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()