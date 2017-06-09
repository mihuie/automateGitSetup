#! /usr/bin/python3
# githubSetup.py - script creates repo and complete initial commit  
# TODO: validate with token

import requests
import getpass
import json
import os
from githubtoken import githubtoken
import argparse

GITHUBAPI = 'https://api.github.com/'

parser = argparse.ArgumentParser(description="Automate github repository creation and make initial commit")
parser.add_argument("-u", "--username", action="store")
parser.add_argument("-t", "--token", action="store")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("repo", metavar='Repository', help="Name of new repository")
parser.add_argument("desc", metavar='Description', help="Description of repository (must be entered in double or single quotes)")


class StatusException(Exception):
	pass

	
def request_status(code):
	err = "Error: post failed - %s" % code
	if code != 201:
		raise StatusException(err)


def automate(repo, description, verbose, username=None, token=None):
	payload = {"name": repo, "description": description}
	password = ''
	verbose_status = ''

	if not verbose:
		verbose_status = '--quiet'

	if username is None: 
		try:
			username = githubtoken['token'][0]
		except Exception as e:
			print ('\nusername not stored.\nSupply one via command line or update githubtoken.py\n')
			print (parser.print_help())
			exit()

	# if token is None:
		# try:
		# 	token = githubtoken['token'][1]
		# except Exception as e:
		# 	print ('\ntoken not stored.\n')
		# 	password = getpass.getpass(prompt='Password: ')

	password = getpass.getpass(prompt='Password: ')
	try:
		response = requests.post(GITHUBAPI + 'user/repos', auth=(username, password), data=json.dumps(payload))
		request_status(response.status_code)
	# except StatusException as e:
	# 	response = requests.post(GITHUBAPI + 'user/repos', auth=(username, token), data=json.dumps(payload))
	# 	request_status(response.status_code)
	# except Exception as e:
	# 	print (e)
	# else:
		os.system("git config --global credential.helper 'cache --timeout=3600'")
		os.system('git config --global push.default simple')
		if verbose:
			print('\nRepository created successfully!')
			print('Setting up git in %s' % os.getcwd())
			print('Initializing...')
		os.system("git init")
		if verbose: print('adding files...')
		os.system("git add . ")
		if verbose: print('committing...')
		os.system("git commit -m 'Initial commit'")
		repo_url = 'https://github.com/mihuie/%s.git' % repo
		os.system("git remote add origin %s" % repo_url)
		
		try:
			os.system("git push -u origin master %s" % verbose_status)
		except:
			print('push failed')

	except StatusException as e:
		print (e)

def main():
	args = parser.parse_args()
	if args.username != None or args.username != '':
		# if args.token != None:
		# 	automate(repo=args.repo, description=args.desc, username=args.username, token=args.token, verbose=args.verbose)
		# else:
		# 	automate(repo=args.repo, description=args.desc, username=args.username, verbose=args.verbose)
		automate(repo=args.repo, description=args.desc, username=args.username, verbose=args.verbose)
	else:
		automate(repo=args.repo, description=args.desc, verbose=args.verbose)


if __name__ == '__main__':
	main()
