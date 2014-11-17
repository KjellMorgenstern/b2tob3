#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Perform text replacements in all files in the current directory and sub
# directories to help migrate from bootstrap 2 to bootstrap 3.
#
# This script should be executed in a directory with HTML files or templates.
# Use at your on risk, try it on a copy first!
import os
import re
from optparse import OptionParser

# List of regular expression replacements tuples to be executed in order.
# Does not include all changes from:
# http://getbootstrap.com/migration

# HTML class="btn" class='btn' class='something btn somethingelse'
# CSS .btn .btn.something
affix = r'(["\'\s\.\{]|\Z)'

# omitted classs: .checkbox.inline .radio.inline

all_regexes = {
    'general': [
        (re.compile(affix + r'span(\d+)' + affix), '\\1col-md-\\2\\3'),
        (re.compile(affix + r'offset(\d+)' + affix), '\\1col-md-offset-\\2\\3'),
        (re.compile(affix + r'hero-unit' + affix), '\\1jumbotron\\2'),

        (re.compile(affix + r'(container|row)-fluid' + affix), '\\1\\2\\3'),
        (re.compile(affix + r'nav-(collapse|toggle)' + affix), '\\1navbar-\\2\\3'),

        (re.compile(affix + r'(input|btn)-small' + affix), '\\1\\2-sm\\3'),
        (re.compile(affix + r'(input|btn)-large' + affix), '\\1\\2-lg\\3'),

        (re.compile(affix + r'btn-navbar' + affix), '\\1navbar-btn\\2'),
        (re.compile(affix + r'btn-mini' + affix), '\\1btn-xs\\2'),
        (re.compile(affix + r'unstyled' + affix), '\\1list-unstyled\\2'),

        (re.compile(affix + r'(visible|hidden)-phone' + affix), '\\1\\2-xs\\3'),
        (re.compile(affix + r'(visible|hidden)-tablet' + affix), '\\1\\2-sm\\3'),
        (re.compile(affix + r'(visible|hidden)-desktop' + affix), '\\1\\2-lg\\3'),

        (re.compile(affix + r'input-(prepend|append)' + affix), '\\1input-group\\3'),

        # Should these regexes be more restriced because class names are more
        # likely to occurr in other places?
        (re.compile(affix + r'inline' + affix), '\\1list-inline\\2'),
        (re.compile(affix + r'add-on' + affix), '\\1input-group-addon\\2'),
        (re.compile(affix + r'thumbnail' + affix), '\\1img-thumbnail\\2'),
    ],
    # still missing:
    #  .navbar .nav -> .navbar-nav
    #  .btn -> .btn .btn-default
    #  .control-group.(warning|error|success) -> .form-group.has-*
    #  .(checkbox|radio).inline -> .*-inline
    #  .img-polaroid -> .img-thumbnail
    #  ul.unstyled -> .list-unstyled
    #  ul.inline -> .list-inline
    #  .label -> .label .label-default
    #  .table .error -> .table .danger
    #  .accordion-group -> .panel .panel-default    
    'more': [
        (re.compile(affix + r'brand' + affix), '\\1navbar-brand\\2'),
        (re.compile(affix + r'(alert|text)-error' + affix), '\\1\\2-danger\\3'),
        (re.compile(affix + r'input-block-level' + affix), '\\1form-control\\2'),
        (re.compile(affix + r'control-group' + affix), '\\1form-group\\2'),
        (re.compile(affix + r'muted' + affix), '\\1text-muted\\2'),
        (re.compile(affix + r'label-important' + affix), '\\1label-danger\\2'),
        (re.compile(affix + r'bar(-\w+)?' + affix), '\\1progress-bar\\2\\3'),
        (re.compile(affix + r'accordion' + affix), '\\1panel-group\\2'),
        (re.compile(affix + r'accordion-heading' + affix), '\\1panel-heading\\2'),
        (re.compile(affix + r'accordion-body' + affix), '\\1panel-collapse\\2'),
        (re.compile(affix + r'accordion-inner' + affix), '\\1panel-body\\2'),
    ],
    # Font Awesome: https://github.com/FortAwesome/Font-Awesome/wiki/Upgrading-from-3.2.1-to-4	
    'html': [
        (re.compile(affix + r'icon-rotate-(\w+)' + affix), '\\1fa fa-rotate-\\2\\3'),
        (re.compile(affix + r'icon-spin-(\w+)' + affix), '\\1fa fa-spin-\\2\\3'),
        (re.compile(affix + r'icon-li-(\w+)' + affix), '\\1fa fa-li-\\2\\3'),
        (re.compile(affix + r'icons-ul-(\w+)' + affix), '\\1fa fa-ul-\\2\\3'),
        (re.compile(affix + r'icon-large-(\w+)' + affix), '\\1fa fa-lg-\\2\\3'),
        (re.compile(affix + r'icon-fixed-width-(\w+)' + affix), '\\1fa fa-fw-\\2\\3'),
        (re.compile(affix + r'icon-(\w+)' + affix), '\\1fa fa-\\2\\3'),
    ],
    'css': [
        (re.compile(affix + r'icon-rotate-(\w+)' + affix), '\\1fa fa-rotate-\\2\\3'),
        (re.compile(affix + r'icon-spin-(\w+)' + affix), '\\1fa fa-spin-\\2\\3'),		
        (re.compile(affix + r'icon-li-(\w+)' + affix), '\\1fa fa-li-\\2\\3'),		
        (re.compile(affix + r'icon-ul-(\w+)' + affix), '\\1fa fa-ul-\\2\\3'),		
        (re.compile(affix + r'icon-large-(\w+)' + affix), '\\1fa fa-lg-\\2\\3'),		
        (re.compile(affix + r'icon-fixed-width-(\w+)' + affix), '\\1fa fa-fw-\\2\\3'),		
        (re.compile(affix + r'icon-(\w+)' + affix), '\\1fa fa-\\2\\3'),
    ],
}

extensions = {
    'html': ('.html', '.htm', '.js'),
    'css': ('.css', '.haml', '.less'),
    'language': ('.java', '.php'),
    'jsp': ('.jsp', '.jspf'),
}

def make_replacements(content, file_type):
    """Perform replacements in file content. Return changed content and the
    number of replacements made."""

    regexes = all_regexes['general'] + all_regexes[file_type]

    count_rep = 0
    for regex in regexes:
        (content, count) = re.subn(regex[0], regex[1], content)
        count_rep += count
    return (content, count_rep)


def main():
    parser = OptionParser()

    parser.add_option(
        "-d", "--directory", dest="pwd",
        help="Directory to search", metavar="DIR", default=os.curdir
    )

    parser.add_option(
        '-v', '--verbose', action='store_true', dest='verbose',
        help='Be verbose and print names of changed files.'
    )

    (options, args) = parser.parse_args()

    pwd = os.path.abspath(options.pwd)

    count_subs = 0
    count_files = 0
    count_files_changed = 0

    for root, dirs, files in os.walk(pwd):
        for f in files:
            if not f.endswith(extensions['html'] + extensions['css'] + extensions['language'] + extensions['jsp']):
                continue
            file_type = 'html'
            if f.endswith(extensions['css']):
                file_type = 'css'
				
            count_files += 1
            count_file_subs = 0

            fname = os.path.join(root, f)
            with open(fname, 'r') as curr_file:
                content = curr_file.read()

            (content, count_file_subs) = make_replacements(content, file_type)
            if count_file_subs == 0:
                continue

            with open(fname, 'w') as curr_file:
                curr_file.write(content)
            if options.verbose:
                print(('File changed: %s' % fname))

            count_subs += count_file_subs
            count_files_changed += 1

    tpl = 'Replacements:    %d\nFiles changed:   %d\nFiles processed: %d\n'
    print((tpl % (count_subs, count_files_changed, count_files)))

if __name__ == '__main__':
    main()
