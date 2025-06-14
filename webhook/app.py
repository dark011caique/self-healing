from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/self-healing', methods=['POST'])
def self_healing():
    try:
        # Executa o playbook com inventário
        result = subprocess.run(
            ['ansible-playbook', '/home/caique/self-healing/ansible/restart_nginx.yml', '-i', '../ansible/hosts.ini'],
            capture_output=True,
            text=True
        )

        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)

        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': 'Playbook executado com sucesso!'}), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Falha ao executar o playbook.',
                'log': result.stderr
            }), 500

    except Exception as e:
        return jsonify({'status': 'exception', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

