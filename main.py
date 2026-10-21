import os

from flask import render_template, Flask, abort 
from pathlib import Path
import markdown

from enum import Enum

app = Flask(__name__)

ENTRIES_DIR = Path(app.root_path) / "static" / "entries"

class EntryCategory(Enum):
    blog = "Blog"
    coding = "Coding"
    music = "Music"
    photos = "Photos"
    art = "Art"

def get_entries_from_category(category: EntryCategory):
    entries = []

    for category_dir in ENTRIES_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        if category_dir.name != category.value:
            continue

        for file in category_dir.glob("*.md"):
            if len(file.stem) < 12:
                continue

            date = file.stem[:10]
            slug = file.stem[11:]

            entries.append({
                "title": slug.replace("-", " ").title(),
                "date": date,
                "category": category_dir.name,
                "slug": slug,
                "url": f"{category_dir.name}/{slug}",
            })

    entries.sort(key=lambda entry: entry["date"], reverse=True)
    return entries

def get_entries():
    entries = []

    for category_dir in ENTRIES_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        for file in category_dir.glob("*.md"):
            if len(file.stem) < 12:
                continue

            date = file.stem[:10]
            slug = file.stem[11:]

            entries.append({
                "title": slug.replace("-", " ").title(),
                "date": date,
                "category": category_dir.name,
                "slug": slug,
                "url": f"{category_dir.name}/{slug}",
            })

    entries.sort(key=lambda entry: entry["date"], reverse=True)

    return entries

@app.route("/<category>/<slug>")
def view_entry(category, slug):
    category_dir = ENTRIES_DIR / category

    if not category_dir.is_dir():
        abort(404)

    matches = [
        file for file in category_dir.glob("*.md")
        if len(file.stem) >= 12
        and file.stem[10] == "-"
        and file.stem[11:] == slug
    ]

    if not matches:
        abort(404)

    file = matches[0]

    content = markdown.markdown(
        file.read_text(encoding="utf-8")
    )

    return render_template(
        "entry.html",
        title=slug.replace("-", " ").title(),
        date=file.stem[:10],
        content=content,
    )

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def home():

    entries = get_entries()
    return render_template('home.html', latest_entries=entries[:5], has_sidebar=True)

@app.route("/Blog")
def blog():
    entries = get_entries_from_category(EntryCategory.blog)
    return render_template('Blog.html', latest_blogs=entries, has_sidebar=True)

@app.route("/Music")
def music():
    return render_template('music.html')

@app.route("/Coding")
def coding():
    return render_template('coding.html') 

@app.route("/BidoofTV")
def bidoofTV():
    return render_template('bidooftv.html')

@app.route("/MinecraftServer")
def minecraftserver():
    return render_template('minecraftserver.html')

@app.route("/Photos")
def photos():
    return render_template('photos.html') 

@app.route("/Art")
def art():
    art_dir = Path(app.root_path) / "static" / "images" / "art"

    image_names = [
        filename
        for filename in os.listdir(art_dir)
        if (art_dir / filename).is_file()
        and filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"))
    ]

    image_names.sort()

    return render_template('art.html', image_names=image_names) 

@app.after_request
def remove_sensitive_headers(response):
    # Strip the Server and X-Powered-By headers if they exist
    response.headers.pop('Server', None)
    response.headers.pop('X-Powered-By', None)
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)