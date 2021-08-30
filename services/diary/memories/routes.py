from dataclasses import dataclass

from flask import render_template, request, flash, redirect

from diary.memories import bp

@dataclass
class Memory:
    text: str


DATA = [Memory("item1"), Memory("item2")]


@bp.route('/memories', methods=["GET", "POST"])
def index():
    recent_memories = DATA

    if request.method == "POST":
        DATA.append(Memory(request.form["content"]))
        flash("Memory Added")
        return redirect("/memories")


    return render_template("memories/index.html", recent_memories=recent_memories)
