"""
  cf-submissions (-u | --user <user>) [-v | --verdicts <verdict>...] [-l | --languages <language>...]
  cf-submissions -h | --help

options:
  -v, --verdicts <verdict>...   List of submission's verdicts to be extracted   [default=ac]
  -l, --languages <language>... List of submission's languages to be extracted  [default=all]

arguments:
  verdict: 
	all 			- All Verdicts
	ac 			- Ok
	rejected 		- Rejected
	wa 			- Wrong Answer
	rte 			- Runtime Error
	tle 			- Time Limit Exceeded
	mle 			- Memory Limit Exceeded
	ce 			- Compilation Error
	hacked 			- Challenged
	failed 			- Failed
	partial 		- Partial
	pe 			- Presentation Error
	ile 			- Idleness Limit Exceeded
	sv 			- Security Violated
	crashed 		- Crashed
	ipf 			- Input Preparation Failed
	skipped 		- Skipped
	running 		- Running
	pending 		- Submitted
  language:
	all 			- All Languages
	c 			- GNU C
	c11 			- GNU C11
	cpp.clang++-diagnose 	- Clang++17 Diagnostics
	cpp 			- GNU C++
	c++0x 			- GNU C++0x
	cpp11 			- GNU C++11
	cpp14 			- GNU C++14
	cpp17 			- GNU C++17
	cpp.g++17-drmemory 	- GNU C++17 Diagnostics
	cpp.ms 			- MS C++
	csharp.mono 		- Mono C#
	csharp.ms 		- MS C#
	d 			- D
	go 			- Go
	haskell 		- Haskell
	java6 			- Java6
	java7 			- Java7
	java8 			- Java8
	kotlin 			- Kotlin
	ocaml 			- Ocaml
	pas.dpr 		- Delphi
	pas.fpc 		- FPC
	pas.pascalabc 		- PascalABC.NET
	perl 			- Perl
	php 			- PHP
	py2 			- Python 2
	py3 			- Python 3
	pypy2 			- PyPy 2
	pypy3 			- PyPy 3
	ruby 			- Ruby
	rust 			- Rust
	scala 			- Scala
	js 			- JavaScript
	nodejs 			- Node.js
	cobol 			- Cobol
	mysterious 		- Mysterious Language
	secret171 		- secret_171
	ada 			- Ada
	qsharp 			- Q#
	tcl 			- Tcl
	false 			- False
	io 			- Io
	pike 			- Pike
"""

import argparse
import json
import os
import requests
import sys
import time

from bs4 import BeautifulSoup
from slugify import slugify


class UserAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(UserAction, self).__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        user_status_url = 'https://codeforces.com/api/user.status?handle={}&from=1&count=1'.format(
            values)
        try:
            user_status_request = requests.get(
                user_status_url, headers={'Connection': 'close'})
            user_status_body = user_status_request.json()
            if user_status_body['status'] == 'OK':
                setattr(namespace, self.dest, values)
            else:
                raise argparse.ArgumentTypeError(
                    'Error - ({}) is not a valid Codeforces handle'.format(
                        values))
        except requests.exceptions.RequestException as exception:
            print_error(exception, True)
        except argparse.ArgumentTypeError as exception:
            print_error(exception, True)


def parse_languages_config(languages_json):
    languages = ['all']
    language_code = {}
    language_extension = {}
    for language_json in languages_json:
        name = list(language_json.keys())[0]
        code = list(language_json.values())[0]['name']
        extension = list(language_json.values())[0]['extension']
        language_code[name] = code
        language_extension[name] = extension
        languages.append(code)

    return languages, language_code, language_extension


def parse_verdicts_config(verdicts_json):
    verdicts = ['all']
    verdict_code = {}
    verdict_name = {}
    for verdict_json in verdicts_json:
        name = list(verdict_json.items())[0][0]
        code = list(verdict_json.items())[0][1]
        verdict_code[name] = code
        verdict_name[code] = name
        verdicts.append(code)

    return verdicts, verdict_code, verdict_name


def parse_args(argv, verdicts, languages):
    # Building the command-line arguments parser
    argparser = argparse.ArgumentParser(
        prog='cf-submissions',
        description='Extract submissions of a Codeforces user',
        usage=__doc__,
        add_help=False)
    argparser.add_argument(
        '-u', '--user', action=UserAction, dest='user_handle')
    argparser.add_argument(
        '-v',
        '--verdict',
        nargs='*',
        default=['ac'],
        choices=verdicts,
        dest='user_verdicts')
    argparser.add_argument(
        '-l',
        '--language',
        nargs='*',
        default=['all'],
        choices=languages,
        dest='user_languages')
    argparser.add_argument('-h', '--help', action='store_true')

    # Parsing user's arguments
    args = argparser.parse_args(argv)
    if args.help:
        print(__doc__)
        sys.exit(0)
    elif args.user_handle is None:
        print(__doc__)
        print_error(
            'cf-submissions: error: the following arguments are required: -u/--user',
            True)

    return args


def create_output_directory(user_handle):
    index = 1
    output_directory = user_handle
    while os.path.isdir(output_directory):
        output_directory = '{}-{}'.format(user_handle, index)
        index += 1

    try:
        os.makedirs(output_directory)
    except OSError as exception:
        print_error(exception, False)
        print_error(
            'Error - An error has occurred while creating the output directory',
            True)

    return output_directory


def create_verdicts_subdirectory(output_directory, user_verdicts, verdict_name):
    for verdict in user_verdicts:
        try:
            os.makedirs(output_directory + os.path.sep + verdict_name[verdict])
        except OSError as exception:
            print_error(exception, False)
            print_error(
                'Error - An error has occurred while creating the output directory',
                True)


def get_submissions_list(user_handle, index, count):
    url_template = 'http://codeforces.com/api/user.status?handle={}&from={}&count={}'
    submissions_list_url = url_template.format(user_handle, index, count)
    request_errors = 0
    while True:
        try:
            submissions_list_request = requests.get(
                submissions_list_url, headers={'Connection': 'close'})
            break
        except requests.exceptions.RequestException as exception:
            if request_errors == 3:
                print_error(exception, False)
                print_error(
                    'Error - An error has occurred while fetching submissions of user ({})'
                    .format(user_handle), True)
            request_errors += 1
            continue

    submissions_list_body = submissions_list_request.json()
    return submissions_list_body['result']


def get_submissions_count(user_handle):
    index = 1
    count = 1000
    submissions_count = 0
    while True:
        submissions_list = get_submissions_list(user_handle, index, count)
        if not submissions_list:
            break
        submissions_count += len(submissions_list)
        index += count
    return submissions_count


def get_submission_page(contest, submission_id, user_handle):
    # Requesting submission page
    url_template = 'http://codeforces.com/contest/{}/submission/{}'
    submission_page_url = url_template.format(contest, submission_id)
    request_errors = 0
    while True:
        try:
            submission_page_request = requests.get(
                submission_page_url, headers={'Connection': 'close'})
            break
        except requests.exceptions.RequestException as exception:
            if request_errors == 3:
                print_error(exception, False)
                print_error(
                    'Error - An error has occurred while fetching submissions of user ({})'
                    .format(user_handle), True)
            request_errors += 1

    return submission_page_request.text


def get_submission_output_file(problem_name, submission_id, extension, verdict,
                               output_directory):
    file_name = '{}-{}.{}'.format(problem_name, submission_id, extension)
    return output_directory + os.path.sep + verdict + os.path.sep + file_name


def update_progress_bar(ext_submissions_count, all_submissions_count):
    current_progress = (ext_submissions_count / all_submissions_count) * 100
    sys.stdout.write('\r')
    progress_bar = '[{: <20}] {:.2f}%'.format('=' * int(current_progress / 5),
                                              current_progress)
    sys.stdout.write(progress_bar)


def print_error(exception, exit_code):
    print('', file=sys.stderr)
    print(exception, file=sys.stderr)
    if exit_code:
        sys.exit(1)


def main():
    # Initializing start time counter
    start_time = time.time()

    # Parsing configuration file
    try:
        with open('config.json') as config_json_file:
            try:
                config_json = json.load(config_json_file)
            except ValueError as exception:
                print_error(exception, False)
                print_error(
                    'Error - An error has occurred while parsing the configuration file',
                    True)
    except FileNotFoundError as exception:
        print_error(exception, False)
        print_error('Error - Configuration file is missing', True)

    # Extracting programming languages configuration
    try:
        languages, language_code, language_extension = parse_languages_config(
            config_json['languages'])
    except KeyError as exception:
        print_error('Error - Configuration of Programming Languages is missing',
                    True)

    # Extracting verdicts configuration
    try:
        verdicts, verdict_code, verdict_name = parse_verdicts_config(
            config_json['verdicts'])
    except KeyError as exception:
        print_error('Error - Configuration of Verdicts is missing', True)

    # Parsing user's arguments
    args = parse_args(sys.argv[1:], verdicts, languages)
    user_handle = args.user_handle
    user_verdicts = sorted(set(args.user_verdicts))
    user_languages = sorted(set(args.user_languages))
    all_verdicts = 'all' in user_verdicts
    all_languages = 'all' in user_languages

    # Creating output directory
    output_directory = create_output_directory(user_handle)

    # Creating subdirectory for each verdict
    if all_verdicts:
        create_verdicts_subdirectory(output_directory, verdict_name,
                                     verdict_name)
    else:
        create_verdicts_subdirectory(output_directory, user_verdicts,
                                     verdict_name)

    # Defining variables to build progress bar
    ext_submissions_count = 0
    all_submissions_count = get_submissions_count(user_handle)

    # Getting the user's submissions
    submission_from = 1
    submission_count = 1000
    while True:
        # Getting a new submissions list
        submissions_list = get_submissions_list(user_handle, submission_from,
                                                submission_count)
        if not submissions_list:
            break

        # Iterating over each submission
        for submission in submissions_list:
            # Updating the number of extracted submissions and the progress bar
            ext_submissions_count += 1
            update_progress_bar(ext_submissions_count, all_submissions_count)

            # Checking if the submission was mad on a ACMSGURU problem
            if 'problemsetName' in submission['problem'] and submission[
                    'problem']['problemsetName'] == 'acmsguru':
                continue

            # Extracting submission's information
            submission_id = submission['id']
            contest = submission['contestId']
            verdict = submission['verdict'].lower()
            language = submission['programmingLanguage'].lower()
            problem_info = submission['problem']
            problem_name = '{}{}_-_{}'.format(contest, problem_info['index'],
                                              problem_info['name'])

            # Checking if the submission was on a Codeforces Gym contest
            if contest >= 100001:
                continue

            # Checking if the submission matches the user's conditions
            if not all_verdicts:
                if verdict_code[verdict] not in user_verdicts:
                    continue
            if not all_languages:
                if language_code[language] not in user_languages:
                    continue

            # Getting submission page
            submission_page_body = get_submission_page(contest, submission_id,
                                                       user_handle)

            # Parsing HTML page and extracting the code
            submission_soup = BeautifulSoup(submission_page_body, 'html.parser')
            try:
                submission_code = submission_soup.find_all(
                    'pre', {'id': 'program-source-text'})[0].text
            except IndexError as exception:
                continue

            # Finding the extension of the source code
            try:
                extension = language_extension[language]
            except KeyError as exception:
                extension = 'txt'

            # Slugify the problem name
            problem_name = slugify(problem_name)

            # Saving the code to the output file
            submission_output_file = get_submission_output_file(
                problem_name, submission_id, extension, verdict,
                output_directory)
            try:
                with open(
                        submission_output_file, 'w',
                        encoding='utf-8') as output_file:
                    output_file.write(submission_code)
            except EnvironmentError as exception:
                print_error(exception, False)
                print_error(
                    'Error - An error has occurred while writing the soure code to the file',
                    True)

        # Updating the starting position of the next iteration
        submission_from += submission_count

    # Finishing the progress bar
    sys.stdout.write('\n')

    # Initializing finish time counter
    finish_time = time.time()

    print('Extracting ({}) submissions has been completed successfully'.format(
        user_handle))
    print('Submissions can be found on {}{}{}'.format(os.getcwd(), os.path.sep,
                                                      output_directory))
    print('Elapsed time: {:.2f} seconds'.format(finish_time - start_time))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as exception:
        sys.stdout.flush()
        sys.stdout.write('\n')
        print_error('Error - Execution has been terminated', True)
