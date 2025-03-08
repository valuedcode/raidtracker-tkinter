import tkinter as tk
import sqlite3
# This GUI is dogshit, but easy to learn. Very simple styling properties. I hate it but weirdly love it at the same time. ValTracker v2 initiatied. o7
# If I use this project for anything serious, I'd need to clean up this code. Current problem (3/8/25): For collab purposes; structure is not great. Functions aren't sorted by any means. I should restructure to put them in order by function purpose.
# IE: Database functions > Analysis functions > UI

# I also use SQL queries in long form all throughout the code which could be cleaned up I'm sure, still new to python so I'm being super literal with all the code so I understand it properly.
# Code is not python-esque (Pythonic? lol); functions are long and need cleaning up.

# V3 integrations to-do: Clean up functions, organize functions by type/purpose, use execute_query() to reduce amt of redundant SQLite code.

# Create the main application window
root = tk.Tk()
root.title("Tarkov Raid Tracker")
root.geometry("600x400")

container = tk.Frame(root)
container.pack(fill="both", expand=True)

def show_frame(frame):
    frame.tkraise()

home_frame = tk.Frame(container)
raid_entry_frame = tk.Frame(container)
raid_history_frame = tk.Frame(container)

for frame in (home_frame, raid_entry_frame, raid_history_frame):
    frame.grid(row=0, column=0, sticky="nsew")

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

def get_last_5_raids():
    conn = sqlite3.connect("tarkov_raids.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
    AVG(kills), AVG(xp), SUM(CASE WHEN survived = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
    FROM raids
    ORDER BY date DESC
    LIMIT 5;
    """)

    result = cursor.fetchone()

    conn.close()

    return result

def get_historical_performance():

    conn = sqlite3.connect("tarkov_raids.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
    AVG(kills), AVG(xp), SUM(CASE WHEN survived = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
    FROM raids
    ORDER BY date DESC
    """)

    result = cursor.fetchone()

    conn.close()

    return result

def get_total_raids():
    conn = sqlite3.connect("tarkov_raids.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM raids")
    total = cursor.fetchone()[0]
    
    conn.close()
    
    return total

def performance_flair():
    last_5 = get_last_5_raids()
    historical = get_historical_performance()
    raid_count = get_total_raids()

    if not last_5 or not historical:
        return "We'll show your progress as you play! Track some raids!", "black"
    
    if raid_count < 10:
        return "", "black"
    
    last_kills, last_xp, last_survival = last_5
    hist_kills, hist_xp, hist_survival = historical

    if last_kills > hist_kills and last_xp > hist_xp and last_survival > hist_survival:
        return "You're crushing it! Keep it up! 💪", "green"
    
    elif last_kills < hist_kills and last_xp < hist_xp and last_survival < hist_survival:
        return "You're slipping! Time to slow it down and survive! 😬", "red"
    
    else:
        return "🔥 Keep grinding!", "orange"  # Neutral message

def load_raid_history():
    for widget in raid_history_list.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("tarkov_raids.db")
    cursor = conn.cursor()

    cursor.execute("SELECT map_name, survived, kills, xp, time_spent, date FROM raids ORDER BY date DESC LIMIT 10")
    raids = cursor.fetchall()

    conn.close()

    if not raids:
        tk.Label(raid_history_list, text="Get to it! You don't have any raids yet!", fg="red").pack()
        return
    
    for idx, raid in enumerate(raids, start=1):
        map_name, survived, kills, xp, time_spent, date = raid
        outcome = "Victory" if survived == "Yes" else "Defeat"
        color = "green" if survived == "Yes" else "red"

        flair_text = f"Raid {idx}: Outcome - {outcome} | Map: {map_name}, Kills: {kills}, XP: {xp}, Time: {time_spent} min"

        tk.Label(raid_history_list, text=flair_text, fg=color).pack()

    show_frame(raid_history_frame)

def get_most_recent_raid():
    conn = sqlite3.connect("tarkov_raids.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT map_name, survived, kills, xp, time_spent, date 
        FROM raids 
        ORDER BY date DESC 
        LIMIT 1;
    """)

    recent_raid = cursor.fetchone()
    conn.close()

    return recent_raid

tk.Label(home_frame, text="Welcome to ValTracker", font=("Arial", 16)).pack(pady=20)
# Recent Raid Display
recent_raid_label = tk.Label(home_frame, text="Your most recent raid: No data yet.", font=("Arial", 12))
recent_raid_label.pack(pady=10)

# Performance Flair Display (NEW)
performance_flair_label = tk.Label(home_frame, text="We'll show your progress as you play! Track some raids!", font=("Arial", 10, "italic"))
performance_flair_label.pack(pady=10)

tk.Button(home_frame, text="Log a New Raid", command=lambda: show_frame(raid_entry_frame)).pack(pady=10) # Explaining command=lambda: This is a pseudo function (anonymous) allowing me to run a function upon request. We've defined a function called "show_frame" which allows us. This syntax prevents the function from 
    # being ran automatically when the code is started, but instead only using this function when it's called on by the user action. In this case, upon clicking the button we're creating with Tkinter command tk.Button
tk.Button(home_frame, text="Raid History", command=lambda: load_raid_history()).pack(pady=10)

def update_recent_raid():
    recent_raid = get_most_recent_raid()

    if recent_raid:
        map_name, survived, kills, xp, time_spent, date = recent_raid
        outcome = "Victory" if survived == "Yes" else "Defeat"
        color = "green" if survived == "Yes" else "red"

        flair_text = f"Your most recent raid: {map_name} | {outcome} | Kills: {kills}, XP: {xp}, Time: {time_spent} min"

        recent_raid_label.config(text=flair_text, fg=color) # Dynamic label updating (AI assisted here)

        flair_message, flair_color = performance_flair()

        if flair_message:  
            performance_flair_label.config(text=flair_message, fg=flair_color)
            performance_flair_label.pack(pady=10)
        else:
            performance_flair_label.pack_forget()

    else:
        recent_raid_label.config(text="Your most recent raid: No data yet.", fg="gray")
        performance_flair_label.pack_forget()


update_recent_raid()

tk.Label(raid_history_frame, text="Your Raids", font=("Arial", 16)).pack(pady=10)
tk.Label(raid_history_frame, text="Showing your last 10 raids", font=("Arial", 10, "italic")).pack()

raid_history_list = tk.Frame(raid_history_frame)
raid_history_list.pack(pady=10)

tk.Button(raid_history_frame, text="Back to Home", command=lambda: show_frame(home_frame)).pack(pady=10)

tk.Label(raid_entry_frame, text="Log a New Raid", font=("Arial", 16)).pack(pady=10)

def submit_raid():
    map_name = map_name_var.get()
    survived = survived_var.get()
    kills = kills_entry.get()
    xp = xp_entry.get()
    time_spent = time_entry.get()

    if not kills.isdigit() or not xp.isdigit() or not time_spent.isdigit():
        success_label.config(text="Error: Please enter valid numbers.", fg="red")
        return
    if int(kills) < 0 or int(xp) < 0 or int(time_spent) < 0:
        success_label.config(text="Error: Values cannot be negative numbers.", fg="red")
        return
    
    conn = sqlite3.connect("tarkov_raids.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO raids (map_name, survived, kills, xp, time_spent) 
        VALUES (?, ?, ?, ?, ?)
    """, (map_name_var.get(), survived, int(kills), int(xp), int(time_spent)))

    conn.commit()
    conn.close()

    success_label.config(text="Raid Logged Successfully!", fg="green")
    success_label.after(3000, lambda: success_label.config(text=""))

    map_name_var.set("Customs")
    survived_var.set("Yes")

    kills_entry.delete(0, tk.END)
    xp_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

    update_recent_raid()

input_frame = tk.Frame(raid_entry_frame)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Map:").grid(row=0, column=0)
map_name_var = tk.StringVar(value="Customs")
map_name_dropdown = tk.OptionMenu(input_frame, map_name_var, "Customs", "Woods", "The Lab", "Lighthouse", "Shoreline", "Streets of Tarkov", "Interchange", "Ground Zero", "Reserve", "Factory")
map_name_dropdown.grid(row=0, column=1)

tk.Label(input_frame, text="Survived?").grid(row=1, column=0)
survived_var = tk.StringVar(value="Yes")
survived_dropdown = tk.OptionMenu(input_frame, survived_var, "Yes", "No")
survived_dropdown.grid(row=1, column=1)

tk.Label(input_frame, text="Kills:").grid(row=2, column=0)
kills_entry = tk.Entry(input_frame)
kills_entry.grid(row=2, column=1)

tk.Label(input_frame, text="XP Earned:").grid(row=3, column=0)
xp_entry = tk.Entry(input_frame)
xp_entry.grid(row=3, column=1)

tk.Label(input_frame, text="Time Spent(m):").grid(row=4, column=0)
time_entry = tk.Entry(input_frame)
time_entry.grid(row=4, column=1)

time_entry.bind("<Return>", lambda event: submit_raid()) # Cutesy UX fix to let users press ENTER to submit entries

submit_button = tk.Button(raid_entry_frame, text="Submit Raid", bg="green", fg="white", command=submit_raid) # Change to submit_raid instead of show_success_message because our validation now dictates how the success message is shown.
submit_button.pack(pady=10)

success_label = tk.Label(raid_entry_frame, text="", font=("Arial", 12))
success_label.pack()

tk.Button(raid_entry_frame, text="Back to Home", command=lambda: show_frame(home_frame)).pack(pady=10)

show_frame(home_frame)

root.mainloop()

