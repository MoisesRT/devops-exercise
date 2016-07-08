#! /usr/bin/python2.7

def main():
    import argparse
    import os

    APPS = ['big-panda', 'panda-service']
    # Initialize the argparser
    def create_parser():
        parser = argparse.ArgumentParser(
            description='The script that you should use in order to deploy panda-service or big-panda')
        parser.add_argument('-app', nargs='+', choices=APPS, required=True, help='Which service will be deployed'
                                                                                 '(multiple choice is available by spacing)')
        parser.add_argument('-inventory', required=True, help='The path of the Ansible Inventory will be used')
        parser.add_argument('-key', required=False, help="<OPTIONAL> Which key will be used in order to SSH")
        parser.add_argument('-user', required=False, help="<OPTIONAL> Which user will be used in order to SSH")
        return parser

    # Create the ansible command
    def command_build():
        PLAYBOOK_NAME = 'panda.yml'
        cmd = 'ansible-playbook -i %s --tags "%s,common"' % (args.inventory, ','.join(args.app))
        if args.key is not None:
            cmd += ' --private-key=%s' % args.key
        if args.user is not None:
            cmd += ' -u %s' % args.user
        cmd += ' %s' % PLAYBOOK_NAME
        return cmd

    parser = create_parser()
    args = parser.parse_args()

    # Runs the Ansible command in a simple way
    #os.system(command_build())


if __name__ == '__main__':
    main()