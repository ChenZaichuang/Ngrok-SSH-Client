import json
from ssh.connect import connect_ssh

if __name__ == '__main__':
    with open('config.json') as f:
        config = json.loads(f.read())
    connect_ssh(config['host'], config['port'], config['username'], config['password'])