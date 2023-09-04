



# from flask import Flask, request, jsonify
# import paramiko
# from edurange_refactored.extensions import db, csrf_protect, socketio


# # app = Flask(__name__)


# @socketio.on('edu3_command')
# def handle_ssh_command(data):
#     command = data['edu3_command']
#     print('received command', command)
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh_client.connect(hostname='10.0.0.55', port=32799, username='ttttuser1', password='54eqrwQ2PgHXk80L')

#     stdin, stdout, stderr = ssh_client.exec_command(command)
#     result = stdout.read().decode('utf-8')

#     ssh_client.close()

#     # Emit the command result back to the client
#     socketio.emit('edu3_response', {'result': result})

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
