from flask import Flask, request, send_file, jsonify
import subprocess, tempfile, os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"ok": True, "message": "LaTeX Cloud Compiler is running"})

@app.route("/compile", methods=["POST"])
def compile_tex():
    data = request.get_json()
    tex = data.get("tex", "")
    if not tex.strip():
        return jsonify({"error": "Empty LaTeX content"}), 400

    tmp = tempfile.mkdtemp()
    tex_path = os.path.join(tmp, "main.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)

    # chạy pdflatex thật
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            cwd=tmp,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=25
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout (file quá lớn hoặc lỗi TeX)"}), 408

    pdf_path = os.path.join(tmp, "main.pdf")
    if not os.path.exists(pdf_path):
        return jsonify({"error": "Compile failed"}), 500

    return send_file(pdf_path, mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
