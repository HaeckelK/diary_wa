from dataclasses import dataclass
import json

from flask import render_template, request, flash, redirect, current_app
import requests
from requests.exceptions import ConnectionError

from diary.memories import bp

@dataclass
class Memory:
    text: str


@bp.route('/memories', methods=["GET", "POST"])
def index():
    api_url = current_app.config["MEMORIES_API_URL"]

    # TODO pass some limit to this request
    try:
        response = requests.get(api_url + "/memories")
    except ConnectionError:
        raw_recent_memories = []
        flash("No connection to memories API.")
    else:
        raw_recent_memories = json.loads(response.content).values()

    recent_memories = []
    for memory in raw_recent_memories:
        recent_memories.append(Memory(text=memory["content"]))

    if request.method == "POST":
        content = request.form["content"]
        try:
            post_response = requests.post(api_url + "/memories",
                                          data={"content": content})
        except ConnectionError:
            flash("Memory not added")
        else:
            flash("Memory added")
        return redirect("/memories")


    return render_template("memories/index.html", recent_memories=recent_memories)
