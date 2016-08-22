from unittest import TestCase
from mock import patch, Mock
from subprocess import PIPE
from changelog.command_line import (init_argparser, git_log, GIT_FIELDS, 
                                    parse_logs, print_logs)

class TestCmdLine(TestCase):

    def test_parse_args(self):
        '''
        Monkey patching `sys.argv` to pass variables to test `argparse`
        '''
        import sys
        store_sys_argv = sys.argv
        
        start = 'HEAD'
        end = 'master'
        version = 'v1.0.0'
        issue = 'CHANGELOG-/d'
        url_prefix = 'https://github.com/kirankoduru/changelog/issues/#'
        
        arguments = [
            ['python'],
            ['--start', start],
            ['--end', end],
            ['--version', version],
            ['--issue', issue],
            ['--issue-url-prefix', url_prefix]
        ]


        sys.argv = ['='.join(arg) for arg in arguments]
        parser = init_argparser()
        self.assertEquals(start, parser.start)
        self.assertEquals(end, parser.end)
        self.assertEquals(version, parser.version)
        self.assertEquals(issue, parser.issue)
        self.assertEquals(url_prefix, parser.issue_url_prefix)

        # remove monkey patch
        sys.argv = store_sys_argv

    def test_git_fields(self):
        expected = {
            'id': '%H',
            'author_name': '%an',
            'author_email': '%ae',
            'date': '%ad',
            'subject': '%s',
            'body': '%b'
        }
        self.assertEquals(expected, GIT_FIELDS)

    def test_git_log(self):
        with patch('changelog.command_line.Popen') as m_popen:
            instance = m_popen.return_value
            instance.communicate.return_value = ('git log', 'mocked')
            result = git_log('from', 'to')
            self.assertEquals('git log', result)

            expected_cmd = 'git log from...to --format="%b%x1f%ae%x1f%an%x1f%ad%x1f%H%x1f%s%x1e"'
            m_popen.assert_called_with(expected_cmd, shell=True, stdout=PIPE)

    def test_parse_logs(self):
        logs = (
            'emailAuthorMon Jul 25 23:30:30 2016 -0400c659536Log 5\n'
            'emailAuthorFri Jul 15 14:27:35 2016 -040075863b5Log 4\n'
            'emailAuthorFri Jul 15 14:20:52 2016 -04005054232Log 3\n'
            'emailAuthorMon May 23 23:59:43 2016 -04000b94b81Log 2\n'
            'Log 2 body\n'
            'emailAuthorMon May 23 02:19:27 2016 -04005a03e2dLog 1\n'
        )
        expected = [
            {
                'body': '',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Mon Jul 25 23:30:30 2016 -0400',
                'id': 'c659536',
                'subject': 'Log 5'
            },
            {
                'body': '',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Fri Jul 15 14:27:35 2016 -0400',
                'id': '75863b5',
                'subject': 'Log 4'
            },
            {
                'body': '',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Fri Jul 15 14:20:52 2016 -0400',
                'id': '5054232',
                'subject': 'Log 3'
            },
            {
                'body': '',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Mon May 23 23:59:43 2016 -0400',
                'id': '0b94b81',
                'subject': 'Log 2'
            },
            {
                'body': 'Log 2 body\n',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Mon May 23 02:19:27 2016 -0400',
                'id': '5a03e2d',
                'subject': 'Log 1'
            }
        ]
        parsed_logs = parse_logs(logs, GIT_FIELDS)
        self.assertEquals(parsed_logs, expected)

    def test_print_logs(self):
        logs = [
            {
                'body': '',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Mon Jul 25 23:30:30 2016 -0400',
                'id': 'c659536',
                'subject': 'Log 5'
            },
            {
                'body': '',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Fri Jul 15 14:27:35 2016 -0400',
                'id': '75863b5',
                'subject': 'Log 4'
            },
            {
                'body': '',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Fri Jul 15 14:20:52 2016 -0400',
                'id': '5054232',
                'subject': 'Log 3'
            },
            {
                'body': '',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Mon May 23 23:59:43 2016 -0400',
                'id': '0b94b81',
                'subject': 'Log 2'
            },
            {
                'body': 'Log 2 body\n',
                'author_email': 'email',
                'author_name': 'Author',
                'date': 'Mon May 23 02:19:27 2016 -0400',
                'id': '5a03e2d',
                'subject': 'Log 1'
            }
        ]
        print_logs('v1.0.0', logs, 'CLOG-/d+', 'http://changelog/#')
