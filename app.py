from flask import Flask, request, send_file, jsonify
import subprocess, tempfile, os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json(force=True)
    if not data or 'code' not in data:
        return jsonify({'error': 'Missing code field'}), 400

    code = data['code']

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, 'script.py')
        output_path = os.path.join(tmpdir, 'dashboard.pdf')

        with open(script_path, 'w') as f:
            f.write(code)

        env = os.environ.copy()
        env['PDF_OUTPUT'] = output_path

        try:
            result = subprocess.run(
                ['python3', script_path],
                capture_output=True, text=True,
                timeout=90, cwd=tmpdir, env=env
            )
        except subprocess.TimeoutExpired:
            return jsonify({'error': 'Script timed out'}), 504

        if result.returncode != 0:
            return jsonify({'error': result.stderr[-2000:]}), 400

        if not os.path.exists(output_path):
            return jsonify({'error': 'No PDF produced'}), 400

        return send_file(output_path, mimetype='application/pdf',
                        as_attachment=True, download_name='dashboard.pdf')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
