from flask import Flask, request, send_file, jsonify
import subprocess, tempfile, os, shutil

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'Missing data'}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, 'dashboard.pdf')

        env = os.environ.copy()
        env['PDF_OUTPUT'] = output_path
        env['WEEK'] = str(data.get('week', ''))
        env['NAME_SEARCHES'] = str(data.get('name_searches', ''))
        env['SESSIONS'] = str(data.get('sessions', ''))
        env['OPEN_RATE'] = str(data.get('open_rate', ''))
        env['SOLV'] = str(data.get('solv', ''))
        env['SIGNAL_NAME'] = str(data.get('signal_name', ''))
        env['SIGNAL_OPENS'] = str(data.get('signal_opens', ''))
        env['SIGNAL_GBP'] = str(data.get('signal_gbp', ''))
        env['SIGNAL_TRAFFIC'] = str(data.get('signal_traffic', ''))

        try:
            result = subprocess.run(
                ['python3', '/opt/render/project/src/generate_pdf.py'],
                capture_output=True, text=True,
                timeout=60, env=env
            )
        except subprocess.TimeoutExpired:
            return jsonify({'error': 'Timed out'}), 504

        if result.returncode != 0:
            return jsonify({'error': result.stderr[-2000:]}), 400

        if not os.path.exists(output_path):
            return jsonify({'error': 'No PDF produced'}), 400

        return send_file(output_path, mimetype='application/pdf',
                        as_attachment=True, download_name='dashboard.pdf')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
