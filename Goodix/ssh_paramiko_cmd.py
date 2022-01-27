import paramiko
import argparse

CMD_LIST = ['lsb_release -a', 'lsusb', 'mount']


def execute_remote_cmd(host, username, password):
    port = 22
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        print("Connection Successful.")
    except paramiko.ssh_exception.AuthenticationException as ex:
        print(ex)
        return None
    try:
        for command in CMD_LIST:
            print("Running command: {}".format(command))
            stdin, stdout, stderr = ssh.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            outlines = stdout.readlines()
            resp = ''.join(outlines)
            print("Command output:")
            print(resp)
            print("Exit code:")
            print(exit_code)
            if exit_code:
                print("Command error:")
                errlines = stderr.readlines()
                resp = ''.join(outlines)
                print(resp)
    except Exception as ex:
        print(ex)
        return None
    finally:
        ssh.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run commands on remote machines.')
    parser.add_argument('-H', '--host', help='Hostname or IP', required=True)
    parser.add_argument('-u', '--username', help='Username of remote machine', required=True)
    parser.add_argument('-p', '--password', help='Password of remote machine', required=True)
    args = vars(parser.parse_args())
    execute_remote_cmd(args['host'], args['username'], args['password'])
