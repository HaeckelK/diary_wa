from diary.memories import bp

@bp.route('/memories')
def index():
    return "Memories"