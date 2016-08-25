import re
import sys
import argparse
from datetime import datetime
from subprocess import Popen, PIPE


# fields to fetch from commit log
# For format parameters refer: https://git-scm.com/docs/pretty-formats
GIT_FIELDS = {
    'id': '%H',
    'author_name': '%an',
    'author_email': '%ae',
    'date': '%ad',
    'subject': '%s',
    'body': '%b'
}

def parse_logs(logs, fields):
    logs = logs.strip('\n\x1e').split("\x1e")
    logs = [row.strip().split("\x1f") for row in logs]
    logs = [dict(zip(fields.keys(), row)) for row in logs]
    return logs


def get_print_lines(new_version, logs, issue_id_pattern, issue_url_prefix):
    '''
    Return a list of lines to print based on the `logs`
    '''
    lines = []
    unassigned_issue_ids = []
    date_today = datetime.now().strftime('%d %b %Y')
    
    version_title = '{0} ({1})'.format(new_version, date_today)
    lines.append(version_title)
    lines.append('-'*len(version_title))

    for item in logs:
        title = item['subject']
        if issue_id_pattern:
            issues = re.findall(issue_id_pattern, title + item['body'], re.IGNORECASE)

            if issues:
                for issue in issues:
                    if 'Merge pull' in title:
                        issues = re.findall(issue_id_pattern, title, 
                                            re.IGNORECASE)
                        unassigned_issue_ids.extend(issues)
                        continue
                    elif 'Merge branch' in title:
                        issues = re.findall(issue_id_pattern, title, 
                                            re.IGNORECASE)
                        unassigned_issue_ids.extend(issues)
                        continue

                    if issue_url_prefix:
                        line = '- {0} ([{1}]({2}{1}))'.format(title, issue, 
                                                              issue_url_prefix)
                        lines.append(line)
                    else:
                        lines.append('- {0} ({1})'.format(title, issue))
        else:
            if ('Merge branch' in title) or ('Merge pull' in title):
                continue

        if item['body']:
            lines.append('- {0}\n{1}'.format(title, item['body'].strip()))
        else:
            lines.append('- {0}'.format(title))

    if unassigned_issue_ids:
        unassigned_issue_ids = list(set(unassigned_issue_ids))
        lines.append('\nUnassigned Issue IDs')
        for issue in unassigned_issue_ids:
            lines.append('- {0}'.format(issue))
    return lines

def git_log(from_, to_):
    '''
    Run git log command and return the logs separated by special characters
    '''
    format_str = '%x1f'.join(GIT_FIELDS.values()) + '%x1e'
    command = 'git log {0}...{1} --format="{2}"'.format(from_, to_, format_str)
    process = Popen(command, shell=True, stdout=PIPE)
    (logs, _) = process.communicate()
    return logs

def init_argparser():
    parser = argparse.ArgumentParser(
        description='Publish suggested CHANGELOG from git commits'
    )
    parser.add_argument(
        '-s', '--start',
        type=str, required=True,
        help='Enter commit/tag/branch you want CHANGELOG from'
    )
    parser.add_argument(
        '-e', '--end',
        type=str,
        help=('Enter commit/tag/branch you want CHANGELOG to. '
              'Default value is set to `master` branch')
    )
    parser.add_argument(
        '-v', '--version',
        type=str, required=True,
        help='Enter new version number for the CHANGELOG'
    )
    parser.add_argument(
        '-i', '--issue',
        type=str,
        help='Enter issue ID pattern. Should be a regex pattern to look for'
    )
    parser.add_argument(
        '-u', '--issue-url-prefix',
        type=str,
        help=('Enter issue URL prefix. If your issues are on github then it could be '
              'https://github.com/<username>/<repository-name>/issues/<issue-number>')
    )
    return parser.parse_args()


def print_lines(lines):
    print '\n'.join(lines)


def main():
    parsed = init_argparser()
    from_ = parsed.start
    to_ = parsed.end
    new_version = parsed.version
    issue_id_pattern = parsed.issue
    issue_url_prefix = parsed.issue_url_prefix

    # set defaults
    if not to_:
        to_ = 'master'

    logs = git_log(from_, to_)
    parsed_logs = parse_logs(logs, GIT_FIELDS)
    lines = get_print_lines(new_version, parsed_logs, issue_id_pattern, issue_url_prefix)
    print_lines(lines)

if __name__ == '__main__':
    sys.exit(main())
