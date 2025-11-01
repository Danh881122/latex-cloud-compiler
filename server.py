from flask import Flask, request, send_file, jsonify
import subprocess, tempfile, os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"ok": True, "message": "LaTeX Cloud Compiler on Fly.io is running"})

@app.route("/compile", methods=["POST"])
def compile_tex():
    data = request.get_json(silent=True) or {}
    tex = data.get("tex", "")
    if not isinstance(tex, str) or not tex.strip():
        return jsonify({"error": "Empty LaTeX content"}), 400

    tmp = tempfile.mkdtemp()
    tex_path = os.path.join(tmp, "main.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)

    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            cwd=tmp,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout (file quá lớn hoặc lỗi TeX)"}), 408

    pdf_path = os.path.join(tmp, "main.pdf")
    if not os.path.exists(pdf_path):
        return jsonify({"error": "Compile failed"}), 500

    return send_file(pdf_path, mimetype="application/pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Fly dùng 8080
    app.run(host="0.0.0.0", port=port)
