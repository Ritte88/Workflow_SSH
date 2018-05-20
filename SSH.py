import paramiko
import sys
import webbrowser
import keychain
import json
import clipboard

wfdict = json.loads(sys.argv[1])

# If you don't use a passphrase for your private key, comment out the line below
password = keychain.get_password(wfdict['kc_service'], wfdict['kc_account'])


k = paramiko.RSAKey.from_private_key_file(wfdict['privatekey'], password = password) # Comment out if you don't have a passphrase
#k = paramiko.RSAKey.from_private_key_file(wfdict['privatekey']) # Uncomment of you don't have a passphrase 

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
host = wfdict['host']
port = int(wfdict['port'])
user = wfdict['user']

ssh.connect(host, port = port, username=user, pkey = k)

cmd = wfdict['cmd']
stdin, stdout, stderr = ssh.exec_command(cmd)
clipboard.set(stdout.read().decode('ascii'))
ssh.close()
webbrowser.open('workflow://')
