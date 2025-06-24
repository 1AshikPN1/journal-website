from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("main_page.html")

@app.route("/add", methods=['GET', 'POST'])
def add_entry():
    if request.method == "POST":
        date = request.form['date']
        mood = request.form['mood']
        content = request.form['content']

        with open("entries.txt", 'a') as file:
            file.write(f"{date}|{mood}|{content}\n")
        return redirect("/view")
    return render_template('add_entry.html')

@app.route("/view")
def view_entries():
    entries = []
    try:
        with open("entries.txt", "r") as file:
            for line in file:
                block = line.strip().split('|')
                if len(block) == 3:
                    entries.append({
                        'date': block[0],
                        'mood': block[1],
                        'content': block[2]
                    })
    except FileNotFoundError:
        pass
    entries = list(entries)
    total = len(entries)
    return render_template('view_entries.html', entries=reversed(entries), total_entries=total)

@app.route("/delete/<int:entry_id>")
def delete_entry(entry_id):
    try:
        with open("entries.txt", "r") as file:
            lines = file.readlines()

        if 0 <= entry_id < len(lines):
            del lines[entry_id]

        with open("entries.txt", "w") as file:
            file.writelines(lines)
    except FileNotFoundError:
        pass

    return redirect("/view")

if __name__ == '__main__':
    app.run(debug=True)
