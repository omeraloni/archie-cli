from archie import Archie
import os


def main():

    # Try to get configuration from environment variables
    host = os.getenv('ARCHIE_HOST', default='192.168.0.1')
    username = os.getenv('ARCHIE_USERNAME', default='admin')
    password = os.getenv('ARCHIE_PASSWORD', default='admin')

    try:
        archie = Archie(host, username, password, test_mode=True)
        archie.login()
        #archie.reboot()
    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()