import back_end
import getpass


def run_server():
    '''Aquires login information and launch the server
    '''
    username = raw_input("Bamboo username: ")
    password = getpass.getpass("Bamboo password: ")
    back_end.server_run(username, password)

if __name__ == '__main__':
    run_server()
