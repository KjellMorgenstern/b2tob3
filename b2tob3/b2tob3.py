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

        #(re.compile(affix + r'(container|row)-fluid' + affix), '\\1\\2\\3'),
        (re.compile(affix + r'row-fluid' + affix), '\\1row\\2'),
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
        (re.compile(affix + r'btn' + affix), '\\1btn btn-default\\2'),
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
        (re.compile(affix + r'btn' + affix), '\\1btn btn-default\\2'),
        (re.compile(affix + r'well-large' + affix), '\\1well-lg\\2'),
        (re.compile(affix + r'well-small' + affix), '\\1well-sm\\2'),
        (re.compile(affix + r'(alert|text)-error' + affix), '\\1\\2-danger\\3'),
        (re.compile(affix + r'input-block-level' + affix), '\\1form-control\\2'),
        (re.compile(affix + r'control-group' + affix), '\\1form-group\\2'),
        (re.compile(affix + r'label-important' + affix), '\\1label-danger\\2'),        
        (re.compile(affix + r'accordion-heading' + affix), '\\1panel-heading\\2'),
        (re.compile(affix + r'accordion-body' + affix), '\\1panel-collapse\\2'),
        (re.compile(affix + r'accordion-inner' + affix), '\\1panel-body\\2'),
        (re.compile(affix + r'accordion' + affix), '\\1panel-group\\2'),
        (re.compile(affix + r'icon-rotate-(\w+)' + affix), '\\1fa fa-rotate-\\2\\3'), # icons
        (re.compile(affix + r'icon-spin-(\w+)' + affix), '\\1fa fa-spin-\\2\\3'),
        (re.compile(affix + r'icon-li-(\w+)' + affix), '\\1fa fa-li-\\2\\3'),
        (re.compile(affix + r'icons-ul-(\w+)' + affix), '\\1fa fa-ul-\\2\\3'),
        (re.compile(affix + r'icon-large-(\w+)' + affix), '\\1fa fa-lg-\\2\\3'),
        (re.compile(affix + r'icon-hand-(\w+)' + affix), '\\1fa fa-hand-o-\\2\\3'),
        (re.compile(affix + r'icon-fixed-width-(\w+)' + affix), '\\1fa fa-fw-\\2\\3'),
        (re.compile(affix + r'icon-chevron-sign-(\w+)' + affix), '\\1fa fa-chevron-circle-\\2\\3'),
        (re.compile(affix + r'icon-chevron-(\w+)' + affix), '\\1fa fa-chevron-\\2\\3'),
        (re.compile(affix + r'icon-arrow-(\w+)' + affix), '\\1fa fa-arrow-\\2\\3'),        
        (re.compile(affix + r'icon-circle-arrow-(\w+)' + affix), '\\1fa fa-arrow-circle-\\2\\3'),
        (re.compile(affix + r'icon-double-angle-(\w+)' + affix), '\\1fa fa-angle-double-\\2\\3'),
        (re.compile(affix + r'icon-fixed-width' + affix), '\\1fa fa-fw\\2'),
        (re.compile(affix + r'icon-large' + affix), '\\1fa-lg\\2'),
        (re.compile(affix + r'icon-ul' + affix), '\\1fa-ul\\2'),
        (re.compile(affix + r'icon-li' + affix), '\\1fa-li\\2'),
        (re.compile(affix + r'icon-spin' + affix), '\\1fa-spin\\2'),
        (re.compile(affix + r'icon-th-list' + affix), '\\1fa fa-th-list\\2'),
        (re.compile(affix + r'icon-user-md' + affix), '\\1fa fa-user-md\\2'),
        (re.compile(affix + r'icon-external-link' + affix), '\\1fa fa-external-link\\2'),
        
        (re.compile(affix + r'icon-ban-circle' + affix), '\\1fa fa-ban\\2'),
        (re.compile(affix + r'icon-bar-chart' + affix), '\\1fa fa-bar-chart-o\\2'),        
        (re.compile(affix + r'icon-beaker' + affix), '\\1fa fa-flask\\2'),
        (re.compile(affix + r'icon-bell' + affix), '\\1fa fa-bell-o\\2'),        
        (re.compile(affix + r'icon-bell-alt' + affix), '\\1fa fa-bell\\2'),
        (re.compile(affix + r'icon-bitbucket-sign' + affix), '\\1fa fa-bitbucket-square\\2'),
        (re.compile(affix + r'icon-bookmark-empty' + affix), '\\1fa fa-bookmark-o\\2'),        
        (re.compile(affix + r'icon-building' + affix), '\\1fa fa-building-o\\2'),
        (re.compile(affix + r'icon-calendar-empty' + affix), '\\1fa fa-calendar-o\\2'),
        (re.compile(affix + r'icon-check-empty' + affix), '\\1fa fa-square-o\\2'),
        (re.compile(affix + r'icon-check-minus' + affix), '\\1fa fa-minus-square-o\\2'),
        (re.compile(affix + r'icon-check-sign' + affix), '\\1fa fa-check-square\\2'),
        (re.compile(affix + r'icon-check' + affix), '\\1fa fa-check-square-o\\2'),
        # replace by regExp
        #(re.compile(affix + r'icon-chevron-sign-down' + affix), '\\1fa-chevron-circle-down\\2'),
        #(re.compile(affix + r'icon-chevron-sign-left' + affix), '\\1fa-chevron-circle-left\\2'),
        #(re.compile(affix + r'icon-chevron-sign-right' + affix), '\\1fa-chevron-circle-right\\2'),
        #(re.compile(affix + r'icon-chevron-sign-up' + affix), '\\1fa-chevron-circle-up\\2'),
        #
        #(re.compile(affix + r'icon-circle-arrow-down' + affix), '\\1fa-arrow-circle-down\\2'),
        #(re.compile(affix + r'icon-circle-arrow-left' + affix), '\\1fa-arrow-circle-left\\2'),
        #(re.compile(affix + r'icon-circle-arrow-right' + affix), '\\1fa-arrow-circle-right\\2'),
        #(re.compile(affix + r'icon-circle-arrow-up' + affix), '\\1fa-arrow-circle-up\\2'),
        
        (re.compile(affix + r'icon-circle-blank' + affix), '\\1fa fa-circle-o\\2'),
        (re.compile(affix + r'icon-cny' + affix), '\\1fa fa-rub\\2'),
        (re.compile(affix + r'icon-collapse-alt' + affix), '\\1fa fa-minus-square-o\\2'),
        (re.compile(affix + r'icon-collapse-top' + affix), '\\1fa fa-caret-square-o-up\\2'),
        (re.compile(affix + r'icon-collapse' + affix), '\\1fa fa-caret-square-o-down\\2'),
        (re.compile(affix + r'icon-comment-alt' + affix), '\\1fa fa-comment-o\\2'),
        (re.compile(affix + r'icon-comments-alt' + affix), '\\1fa fa-comments-o\\2'),        
        (re.compile(affix + r'icon-copy' + affix), '\\1fa fa-files-o\\2'),
        (re.compile(affix + r'icon-cut' + affix), '\\1fa fa-scissors\\2'),
        (re.compile(affix + r'icon-dashboard' + affix), '\\1fa fa-tachometer\\2'),
        
        #(re.compile(affix + r'icon-double-angle-down' + affix), '\\1fa-angle-double-down\\2'),
        #(re.compile(affix + r'icon-double-angle-left' + affix), '\\1fa-angle-double-left\\2'),
        #(re.compile(affix + r'icon-double-angle-right' + affix), '\\1fa-angle-double-right\\2'),
        #(re.compile(affix + r'icon-double-angle-up' + affix), '\\1fa-angle-double-up\\2'),
        
        (re.compile(affix + r'icon-download' + affix), '\\1fa fa-arrow-circle-o-down\\2'),
        (re.compile(affix + r'icon-download-alt' + affix), '\\1fa fa-download\\2'),
        (re.compile(affix + r'icon-edit-sign' + affix), '\\1fa fa-pencil-square\\2'),
        (re.compile(affix + r'icon-edit' + affix), '\\1fa fa-pencil-square-o\\2'),
        (re.compile(affix + r'icon-ellipsis-horizontal' + affix), '\\1fa fa-ellipsis-h\\2'),
        (re.compile(affix + r'icon-ellipsis-vertical' + affix), '\\1fa fa-ellipsis-v\\2'),
        (re.compile(affix + r'icon-envelope-alt' + affix), '\\1fa fa-envelope-o\\2'),
        (re.compile(affix + r'icon-exclamation-sign' + affix), '\\1fa fa-exclamation-circle\\2'),
        (re.compile(affix + r'icon-expand-alt' + affix), '\\1fa fa-expand-o\\2'),
        (re.compile(affix + r'icon-expand' + affix), '\\1fa fa-caret-square-o-right\\2'),
        (re.compile(affix + r'icon-external-link-sign' + affix), '\\1fa fa-external-link-square\\2'),
        (re.compile(affix + r'icon-eye-close' + affix), '\\1fa fa-eye-slash\\2'),
        (re.compile(affix + r'icon-eye-open' + affix), '\\1fa fa-eye\\2'),
        (re.compile(affix + r'icon-facebook-sign' + affix), '\\1fa fa-facebook-square\\2'),
        (re.compile(affix + r'icon-facetime-video' + affix), '\\1fa fa-video-camera\\2'),
        (re.compile(affix + r'icon-file-alt' + affix), '\\1fa fa-file-o\\2'),
        (re.compile(affix + r'icon-file-text-alt' + affix), '\\1fa fa-file-text-o\\2'),
        (re.compile(affix + r'icon-flag-alt' + affix), '\\1fa fa-flag-o\\2'),
        (re.compile(affix + r'icon-folder-close-alt' + affix), '\\1fa fa-folder-o\\2'),
        (re.compile(affix + r'icon-folder-close' + affix), '\\1fa fa-folder\\2'),
        (re.compile(affix + r'icon-folder-open-alt' + affix), '\\1fa fa-folder-open-o\\2'),
        (re.compile(affix + r'icon-food' + affix), '\\1fa fa-cutlery\\2'),
        (re.compile(affix + r'icon-frown' + affix), '\\1fa fa-frown-o\\2'),
        (re.compile(affix + r'icon-fullscreen' + affix), '\\1fa fa-arrows-alt\\2'),
        (re.compile(affix + r'icon-github-sign' + affix), '\\1fa fa-github-square\\2'),
        (re.compile(affix + r'icon-google-plus-sign' + affix), '\\1fa fa-google-plus-square\\2'),
        (re.compile(affix + r'icon-group' + affix), '\\1fa fa-users\\2'),
        (re.compile(affix + r'icon-h-sign' + affix), '\\1fa fa-h-square\\2'),
        
        #(re.compile(affix + r'icon-hand-down' + affix), '\\1fa-hand-o-down\\2'),
        #(re.compile(affix + r'icon-hand-left' + affix), '\\1fa-hand-o-left\\2'),
        #(re.compile(affix + r'icon-hand-right' + affix), '\\1fa-hand-o-right\\2'),
        #(re.compile(affix + r'icon-hand-up' + affix), '\\1fa-hand-o-up\\2'),
        
        (re.compile(affix + r'icon-hdd' + affix), '\\1fa fa-hdd-o\\2'),
        (re.compile(affix + r'icon-heart-empty' + affix), '\\1fa fa-heart-o\\2'),
        (re.compile(affix + r'icon-hospital' + affix), '\\1fa fa-hospital-o\\2'),
        (re.compile(affix + r'icon-indent-left' + affix), '\\1fa fa-outdent\\2'),
        (re.compile(affix + r'icon-indent-right' + affix), '\\1fa fa-indent\\2'),
        (re.compile(affix + r'icon-info-sign' + affix), '\\1fa fa-info-circle\\2'),
        (re.compile(affix + r'icon-keyboard' + affix), '\\1fa fa-keyboard-o\\2'),
        (re.compile(affix + r'icon-legal' + affix), '\\1fa fa-gavel\\2'),
        (re.compile(affix + r'icon-lemon' + affix), '\\1fa fa-lemon-o\\2'),
        (re.compile(affix + r'icon-lightbulb' + affix), '\\1fa fa-lightbulb-o\\2'),
        (re.compile(affix + r'icon-linkedin-sign' + affix), '\\1fa fa-linkedin-square\\2'),
        (re.compile(affix + r'icon-meh' + affix), '\\1fa fa-meh-o\\2'),
        (re.compile(affix + r'icon-microphone-off' + affix), '\\1fa fa-microphone-slash\\2'),
        (re.compile(affix + r'icon-minus-sign-alt' + affix), '\\1fa fa-minus-square\\2'),
        (re.compile(affix + r'icon-minus-sign' + affix), '\\1fa fa-minus-circle\\2'),
        (re.compile(affix + r'icon-mobile-phone' + affix), '\\1fa fa-mobile\\2'),
        (re.compile(affix + r'icon-moon' + affix), '\\1fa fa-moon-o\\2'),
        (re.compile(affix + r'icon-move' + affix), '\\1fa fa-arrows\\2'),
        (re.compile(affix + r'icon-off' + affix), '\\1fa fa-power-off\\2'),
        (re.compile(affix + r'icon-ok-circle' + affix), '\\1fa fa-check-circle-o\\2'),
        (re.compile(affix + r'icon-ok-sign' + affix), '\\1fa fa-check-circle\\2'),
        (re.compile(affix + r'icon-ok' + affix), '\\1fa fa-check\\2'),
        (re.compile(affix + r'icon-paper-clip' + affix), '\\1fa fa-paperclip\\2'),
        (re.compile(affix + r'icon-paste' + affix), '\\1fa fa-clipboard\\2'),
        (re.compile(affix + r'icon-phone-sign' + affix), '\\1fa fa-phone-square\\2'),
        (re.compile(affix + r'icon-picture' + affix), '\\1fa fa-picture-o\\2'),
        (re.compile(affix + r'icon-pinterest-sign' + affix), '\\1fa fa-pinterest-square\\2'),
        (re.compile(affix + r'icon-play-circle' + affix), '\\1fa fa-play-circle-o\\2'),
        (re.compile(affix + r'icon-play-sign' + affix), '\\1fa fa-play-circle\\2'),
        (re.compile(affix + r'icon-plus-sign-alt' + affix), '\\1fa fa-plus-square\\2'),
        (re.compile(affix + r'icon-plus-sign' + affix), '\\1fa fa-plus-circle\\2'),
        (re.compile(affix + r'icon-pushpin' + affix), '\\1fa fa-thumb-tack\\2'),
        (re.compile(affix + r'icon-question-sign' + affix), '\\1fa fa-question-circle\\2'),
        (re.compile(affix + r'icon-remove-circle' + affix), '\\1fa fa-times-circle-o\\2'),
        (re.compile(affix + r'icon-remove-sign' + affix), '\\1fa fa-times-circle\\2'),
        (re.compile(affix + r'icon-remove' + affix), '\\1fa fa-times\\2'),
        (re.compile(affix + r'icon-reorder' + affix), '\\1fa fa-bars\\2'),
        (re.compile(affix + r'icon-resize-full' + affix), '\\1fa fa-expand\\2'),
        (re.compile(affix + r'icon-resize-horizontal' + affix), '\\1fa fa-arrows-h\\2'),
        (re.compile(affix + r'icon-resize-small' + affix), '\\1fa fa-compress\\2'),
        (re.compile(affix + r'icon-resize-vertical' + affix), '\\1fa fa-arrows-v\\2'),
        (re.compile(affix + r'icon-rss-sign' + affix), '\\1fa fa-rss-square\\2'),
        (re.compile(affix + r'icon-save' + affix), '\\1fa fa-floppy-o\\2'),
        (re.compile(affix + r'icon-screenshot' + affix), '\\1fa fa-crosshairs\\2'),
        (re.compile(affix + r'icon-share-alt' + affix), '\\1fa fa-share\\2'),
        (re.compile(affix + r'icon-share-sign' + affix), '\\1fa fa-share-square\\2'),
        (re.compile(affix + r'icon-share' + affix), '\\1fa fa-share-square-o\\2'),
        (re.compile(affix + r'icon-sign-blank' + affix), '\\1fa fa-square\\2'),
        (re.compile(affix + r'icon-signin' + affix), '\\1fa fa-sign-in\\2'),
        (re.compile(affix + r'icon-signout' + affix), '\\1fa fa-sign-out\\2'),
        (re.compile(affix + r'icon-smile' + affix), '\\1fa fa-smile-o\\2'),
        (re.compile(affix + r'icon-sort-by-alphabet-alt' + affix), '\\1fa fa-sort-alpha-desc\\2'),
        (re.compile(affix + r'icon-sort-by-alphabet' + affix), '\\1fa fa-sort-alpha-asc\\2'),
        (re.compile(affix + r'icon-sort-by-attributes-alt' + affix), '\\1fa fa-sort-amount-desc\\2'),
        (re.compile(affix + r'icon-sort-by-attributes' + affix), '\\1fa fa-sort-amount-asc\\2'),
        (re.compile(affix + r'icon-sort-by-order-alt' + affix), '\\1fa fa-sort-numeric-desc\\2'),
        (re.compile(affix + r'icon-sort-by-order' + affix), '\\1fa fa-sort-numeric-asc\\2'),
        (re.compile(affix + r'icon-sort-down' + affix), '\\1fa fa-sort-asc\\2'),
        (re.compile(affix + r'icon-sort-up' + affix), '\\1fa fa-sort-desc\\2'),
        (re.compile(affix + r'icon-stackexchange' + affix), '\\1fa fa-stack-overflow\\2'),
        (re.compile(affix + r'icon-star-empty' + affix), '\\1fa fa-star-o\\2'),
        (re.compile(affix + r'icon-star-half-empty' + affix), '\\1fa fa-star-half-o\\2'),
        (re.compile(affix + r'icon-sun' + affix), '\\1fa fa-sun-o\\2'),
        (re.compile(affix + r'icon-thumbs-down-alt' + affix), '\\1fa fa-thumbs-o-down\\2'),
        (re.compile(affix + r'icon-thumbs-up-alt' + affix), '\\1fa fa-thumbs-o-up\\2'),
        (re.compile(affix + r'icon-time' + affix), '\\1fa fa-clock-o\\2'),
        (re.compile(affix + r'icon-trash' + affix), '\\1fa fa-trash-o\\2'),
        (re.compile(affix + r'icon-tumblr-sign' + affix), '\\1fa fa-tumblr-square\\2'),
        (re.compile(affix + r'icon-twitter-sign' + affix), '\\1fa fa-twitter-square\\2'),
        (re.compile(affix + r'icon-unlink' + affix), '\\1fa fa-chain-broken\\2'),
        (re.compile(affix + r'icon-upload' + affix), '\\1fa fa-arrow-circle-o-up\\2'),
        (re.compile(affix + r'icon-upload-alt' + affix), '\\1fa fa-upload\\2'),
        (re.compile(affix + r'icon-warning-sign' + affix), '\\1fa fa-exclamation-triangle\\2'),
        (re.compile(affix + r'icon-xing-sign' + affix), '\\1fa fa-xing-square\\2'),
        (re.compile(affix + r'icon-youtube-sign' + affix), '\\1fa fa-youtube-square\\2'),
        (re.compile(affix + r'icon-zoom-in' + affix), '\\1fa fa-search-plus\\2'),
        (re.compile(affix + r'icon-zoom-out' + affix), '\\1fa fa-search-minus\\2'),
        (re.compile(affix + r'icon-shopping-cart' + affix), '\\1fa fa-shopping-cart\\2'),
        (re.compile(affix + r'icon-2x' + affix), '\\1fa-2x\\2'),
        (re.compile(affix + r'icon-4x' + affix), '\\1fa-4x\\2'),
        (re.compile(affix + r'icon-(\w+)' + affix), '\\1fa fa-\\2\\3'), # end regular expression
    ],
    'css': [
        #(re.compile(affix + r'icon-rotate-(\w+)' + affix), '\\1fa fa-rotate-\\2\\3'),
        #(re.compile(affix + r'icon-spin-(\w+)' + affix), '\\1fa fa-spin-\\2\\3'),		
        #(re.compile(affix + r'icon-li-(\w+)' + affix), '\\1fa fa-li-\\2\\3'),		
        #(re.compile(affix + r'icon-ul-(\w+)' + affix), '\\1fa fa-ul-\\2\\3'),		
        #(re.compile(affix + r'icon-large-(\w+)' + affix), '\\1fa fa-lg-\\2\\3'),		
        #(re.compile(affix + r'icon-fixed-width-(\w+)' + affix), '\\1fa fa-fw-\\2\\3'),		
        #(re.compile(affix + r'icon-(\w+)' + affix), '\\1fa fa-\\2\\3'), #end regular expression
        (re.compile(affix + r'icon-fixed-width' + affix), '\\1fa-fw\\2'),
        (re.compile(affix + r'icon-large' + affix), '\\1fa-lg\\2'),
        (re.compile(affix + r'icon-ul' + affix), '\\1fa-ul\\2'),
        (re.compile(affix + r'icon-li' + affix), '\\1fa-li\\2'),
        (re.compile(affix + r'icon-spin' + affix), '\\1fa-spin\\2'),
        (re.compile(affix + r'icon-ban-circle' + affix), '\\1fa-ban\\2'),
        (re.compile(affix + r'icon-bar-chart' + affix), '\\1fa-bar-chart-o\\2'),
        (re.compile(affix + r'icon-beaker' + affix), '\\1fa-flask\\2'),
        (re.compile(affix + r'icon-bell' + affix), '\\1fa-bell-o\\2'),
        (re.compile(affix + r'icon-bell-alt' + affix), '\\1fa-bell\\2'),
        (re.compile(affix + r'icon-bitbucket-sign' + affix), '\\1fa-bitbucket-square\\2'),
        (re.compile(affix + r'icon-bookmark-empty' + affix), '\\1fa-bookmark-o\\2'),
        (re.compile(affix + r'icon-building' + affix), '\\1fa-building-o\\2'),
        (re.compile(affix + r'icon-calendar-empty' + affix), '\\1fa-calendar-o\\2'),
        (re.compile(affix + r'icon-check-empty' + affix), '\\1fa-square-o\\2'),
        (re.compile(affix + r'icon-check-minus' + affix), '\\1fa-minus-square-o\\2'),
        (re.compile(affix + r'icon-check-sign' + affix), '\\1fa-check-square\\2'),
        (re.compile(affix + r'icon-check' + affix), '\\1fa-check-square-o\\2'),
        (re.compile(affix + r'icon-chevron-sign-down' + affix), '\\1fa-chevron-circle-down\\2'),
        (re.compile(affix + r'icon-chevron-sign-left' + affix), '\\1fa-chevron-circle-left\\2'),
        (re.compile(affix + r'icon-chevron-sign-right' + affix), '\\1fa-chevron-circle-right\\2'),
        (re.compile(affix + r'icon-chevron-sign-up' + affix), '\\1fa-chevron-circle-up\\2'),
        (re.compile(affix + r'icon-circle-arrow-down' + affix), '\\1fa-arrow-circle-down\\2'),
        (re.compile(affix + r'icon-circle-arrow-left' + affix), '\\1fa-arrow-circle-left\\2'),
        (re.compile(affix + r'icon-circle-arrow-right' + affix), '\\1fa-arrow-circle-right\\2'),
        (re.compile(affix + r'icon-circle-arrow-up' + affix), '\\1fa-arrow-circle-up\\2'),
        (re.compile(affix + r'icon-circle-blank' + affix), '\\1fa-circle-o\\2'),
        (re.compile(affix + r'icon-cny' + affix), '\\1fa-rub\\2'),
        (re.compile(affix + r'icon-collapse-alt' + affix), '\\1fa-minus-square-o\\2'),
        (re.compile(affix + r'icon-collapse-top' + affix), '\\1fa-caret-square-o-up\\2'),
        (re.compile(affix + r'icon-collapse' + affix), '\\1fa-caret-square-o-down\\2'),
        (re.compile(affix + r'icon-comment-alt' + affix), '\\1fa-comment-o\\2'),
        (re.compile(affix + r'icon-comments-alt' + affix), '\\1fa-comments-o\\2'),
        (re.compile(affix + r'icon-copy' + affix), '\\1fa-files-o\\2'),
        (re.compile(affix + r'icon-cut' + affix), '\\1fa-scissors\\2'),
        (re.compile(affix + r'icon-dashboard' + affix), '\\1fa-tachometer\\2'),
        (re.compile(affix + r'icon-double-angle-down' + affix), '\\1fa fa-angle-double-down\\2'),
        (re.compile(affix + r'icon-double-angle-left' + affix), '\\1fa fa-angle-double-left\\2'),
        (re.compile(affix + r'icon-double-angle-right' + affix), '\\1fa fa-angle-double-right\\2'),
        (re.compile(affix + r'icon-double-angle-up' + affix), '\\1fa fa-angle-double-up\\2'),
        (re.compile(affix + r'icon-download' + affix), '\\1fa fa-arrow-circle-o-down\\2'),
        (re.compile(affix + r'icon-download-alt' + affix), '\\1fa fa-download\\2'),
        (re.compile(affix + r'icon-edit-sign' + affix), '\\1fa-pencil-square\\2'),
        (re.compile(affix + r'icon-edit' + affix), '\\1fa-pencil-square-o\\2'),
        (re.compile(affix + r'icon-ellipsis-horizontal' + affix), '\\1fa-ellipsis-h\\2'),
        (re.compile(affix + r'icon-ellipsis-vertical' + affix), '\\1fa-ellipsis-v\\2'),
        (re.compile(affix + r'icon-envelope-alt' + affix), '\\1fa-envelope-o\\2'),
        (re.compile(affix + r'icon-exclamation-sign' + affix), '\\1fa-exclamation-circle\\2'),
        (re.compile(affix + r'icon-expand-alt' + affix), '\\1fa-expand-o\\2'),
        (re.compile(affix + r'icon-expand' + affix), '\\1fa-caret-square-o-right\\2'),
        (re.compile(affix + r'icon-external-link-sign' + affix), '\\1fa-external-link-square\\2'),
        (re.compile(affix + r'icon-eye-close' + affix), '\\1fa-eye-slash\\2'),
        (re.compile(affix + r'icon-eye-open' + affix), '\\1fa-eye\\2'),
        (re.compile(affix + r'icon-facebook-sign' + affix), '\\1fa-facebook-square\\2'),
        (re.compile(affix + r'icon-facetime-video' + affix), '\\1fa-video-camera\\2'),
        (re.compile(affix + r'icon-file-alt' + affix), '\\1fa-file-o\\2'),
        (re.compile(affix + r'icon-file-text-alt' + affix), '\\1fa-file-text-o\\2'),
        (re.compile(affix + r'icon-flag-alt' + affix), '\\1fa-flag-o\\2'),
        (re.compile(affix + r'icon-folder-close-alt' + affix), '\\1fa-folder-o\\2'),
        (re.compile(affix + r'icon-folder-close' + affix), '\\1fa-folder\\2'),
        (re.compile(affix + r'icon-folder-open-alt' + affix), '\\1fa-folder-open-o\\2'),
        (re.compile(affix + r'icon-folder-open' + affix), '\\1fa fa-folder-open\\2'),
        (re.compile(affix + r'icon-food' + affix), '\\1fa-cutlery\\2'),
        (re.compile(affix + r'icon-frown' + affix), '\\1fa-frown-o\\2'),
        (re.compile(affix + r'icon-fullscreen' + affix), '\\1fa-arrows-alt\\2'),
        (re.compile(affix + r'icon-github-sign' + affix), '\\1fa-github-square\\2'),
        (re.compile(affix + r'icon-google-plus-sign' + affix), '\\1fa-google-plus-square\\2'),
        (re.compile(affix + r'icon-group' + affix), '\\1fa-users\\2'),
        (re.compile(affix + r'icon-h-sign' + affix), '\\1fa-h-square\\2'),
        (re.compile(affix + r'icon-hand-down' + affix), '\\1fa-hand-o-down\\2'),
        (re.compile(affix + r'icon-hand-left' + affix), '\\1fa-hand-o-left\\2'),
        (re.compile(affix + r'icon-hand-right' + affix), '\\1fa-hand-o-right\\2'),
        (re.compile(affix + r'icon-hand-up' + affix), '\\1fa-hand-o-up\\2'),
        (re.compile(affix + r'icon-hdd' + affix), '\\1fa-hdd-o\\2'),
        (re.compile(affix + r'icon-heart-empty' + affix), '\\1fa-heart-o\\2'),
        (re.compile(affix + r'icon-hospital' + affix), '\\1fa-hospital-o\\2'),
        (re.compile(affix + r'icon-indent-left' + affix), '\\1fa-outdent\\2'),
        (re.compile(affix + r'icon-indent-right' + affix), '\\1fa-indent\\2'),
        (re.compile(affix + r'icon-info-sign' + affix), '\\1fa-info-circle\\2'),
        (re.compile(affix + r'icon-keyboard' + affix), '\\1fa-keyboard-o\\2'),
        (re.compile(affix + r'icon-legal' + affix), '\\1fa-gavel\\2'),
        (re.compile(affix + r'icon-lemon' + affix), '\\1fa-lemon-o\\2'),
        (re.compile(affix + r'icon-lightbulb' + affix), '\\1fa-lightbulb-o\\2'),
        (re.compile(affix + r'icon-linkedin-sign' + affix), '\\1fa-linkedin-square\\2'),
        (re.compile(affix + r'icon-meh' + affix), '\\1fa-meh-o\\2'),
        (re.compile(affix + r'icon-microphone-off' + affix), '\\1fa-microphone-slash\\2'),
        (re.compile(affix + r'icon-minus-sign-alt' + affix), '\\1fa-minus-square\\2'),
        (re.compile(affix + r'icon-minus-sign' + affix), '\\1fa-minus-circle\\2'),
        (re.compile(affix + r'icon-mobile-phone' + affix), '\\1fa-mobile\\2'),
        (re.compile(affix + r'icon-moon' + affix), '\\1fa-moon-o\\2'),
        (re.compile(affix + r'icon-move' + affix), '\\1fa-arrows\\2'),
        (re.compile(affix + r'icon-off' + affix), '\\1fa-power-off\\2'),
        (re.compile(affix + r'icon-ok-circle' + affix), '\\1fa-check-circle-o\\2'),
        (re.compile(affix + r'icon-ok-sign' + affix), '\\1fa-check-circle\\2'),
        (re.compile(affix + r'icon-ok' + affix), '\\1fa-check\\2'),
        (re.compile(affix + r'icon-paper-clip' + affix), '\\1fa-paperclip\\2'),
        (re.compile(affix + r'icon-paste' + affix), '\\1fa-clipboard\\2'),
        (re.compile(affix + r'icon-phone-sign' + affix), '\\1fa-phone-square\\2'),
        (re.compile(affix + r'icon-picture' + affix), '\\1fa-picture-o\\2'),
        (re.compile(affix + r'icon-pinterest-sign' + affix), '\\1fa-pinterest-square\\2'),
        (re.compile(affix + r'icon-play-circle' + affix), '\\1fa-play-circle-o\\2'),
        (re.compile(affix + r'icon-play-sign' + affix), '\\1fa-play-circle\\2'),
        (re.compile(affix + r'icon-plus-sign-alt' + affix), '\\1fa-plus-square\\2'),
        (re.compile(affix + r'icon-plus-sign' + affix), '\\1fa-plus-circle\\2'),
        (re.compile(affix + r'icon-pushpin' + affix), '\\1fa-thumb-tack\\2'),
        (re.compile(affix + r'icon-question-sign' + affix), '\\1fa-question-circle\\2'),
        (re.compile(affix + r'icon-remove-circle' + affix), '\\1fa-times-circle-o\\2'),
        (re.compile(affix + r'icon-remove-sign' + affix), '\\1fa-times-circle\\2'),
        (re.compile(affix + r'icon-remove' + affix), '\\1fa-times\\2'),
        (re.compile(affix + r'icon-reorder' + affix), '\\1fa-bars\\2'),
        (re.compile(affix + r'icon-resize-full' + affix), '\\1fa-expand\\2'),
        (re.compile(affix + r'icon-resize-horizontal' + affix), '\\1fa-arrows-h\\2'),
        (re.compile(affix + r'icon-resize-small' + affix), '\\1fa-compress\\2'),
        (re.compile(affix + r'icon-resize-vertical' + affix), '\\1fa-arrows-v\\2'),
        (re.compile(affix + r'icon-rss-sign' + affix), '\\1fa-rss-square\\2'),
        (re.compile(affix + r'icon-save' + affix), '\\1fa-floppy-o\\2'),
        (re.compile(affix + r'icon-screenshot' + affix), '\\1fa-crosshairs\\2'),
        (re.compile(affix + r'icon-share-alt' + affix), '\\1fa-share\\2'),
        (re.compile(affix + r'icon-share-sign' + affix), '\\1fa-share-square\\2'),
        (re.compile(affix + r'icon-share' + affix), '\\1fa-share-square-o\\2'),
        (re.compile(affix + r'icon-sign-blank' + affix), '\\1fa-square\\2'),
        (re.compile(affix + r'icon-signin' + affix), '\\1fa-sign-in\\2'),
        (re.compile(affix + r'icon-signout' + affix), '\\1fa-sign-out\\2'),
        (re.compile(affix + r'icon-smile' + affix), '\\1fa-smile-o\\2'),
        (re.compile(affix + r'icon-sort-by-alphabet-alt' + affix), '\\1fa-sort-alpha-desc\\2'),
        (re.compile(affix + r'icon-sort-by-alphabet' + affix), '\\1fa-sort-alpha-asc\\2'),
        (re.compile(affix + r'icon-sort-by-attributes-alt' + affix), '\\1fa-sort-amount-desc\\2'),
        (re.compile(affix + r'icon-sort-by-attributes' + affix), '\\1fa-sort-amount-asc\\2'),
        (re.compile(affix + r'icon-sort-by-order-alt' + affix), '\\1fa-sort-numeric-desc\\2'),
        (re.compile(affix + r'icon-sort-by-order' + affix), '\\1fa-sort-numeric-asc\\2'),
        (re.compile(affix + r'icon-sort-down' + affix), '\\1fa-sort-asc\\2'),
        (re.compile(affix + r'icon-sort-up' + affix), '\\1fa-sort-desc\\2'),
        (re.compile(affix + r'icon-stackexchange' + affix), '\\1fa-stack-overflow\\2'),
        (re.compile(affix + r'icon-star-empty' + affix), '\\1fa-star-o\\2'),
        (re.compile(affix + r'icon-star-half-empty' + affix), '\\1fa-star-half-o\\2'),
        (re.compile(affix + r'icon-sun' + affix), '\\1fa-sun-o\\2'),
        (re.compile(affix + r'icon-thumbs-down-alt' + affix), '\\1fa-thumbs-o-down\\2'),
        (re.compile(affix + r'icon-thumbs-up-alt' + affix), '\\1fa-thumbs-o-up\\2'),
        (re.compile(affix + r'icon-time' + affix), '\\1fa-clock-o\\2'),
        (re.compile(affix + r'icon-trash' + affix), '\\1fa-trash-o\\2'),
        (re.compile(affix + r'icon-tumblr-sign' + affix), '\\1fa-tumblr-square\\2'),
        (re.compile(affix + r'icon-twitter-sign' + affix), '\\1fa-twitter-square\\2'),
        (re.compile(affix + r'icon-unlink' + affix), '\\1fa-chain-broken\\2'),
        (re.compile(affix + r'icon-upload' + affix), '\\1fa-arrow-circle-o-up\\2'),
        (re.compile(affix + r'icon-upload-alt' + affix), '\\1fa-upload\\2'),
        (re.compile(affix + r'icon-warning-sign' + affix), '\\1fa-exclamation-triangle\\2'),
        (re.compile(affix + r'icon-xing-sign' + affix), '\\1fa-xing-square\\2'),
        (re.compile(affix + r'icon-youtube-sign' + affix), '\\1fa-youtube-square\\2'),
        (re.compile(affix + r'icon-zoom-in' + affix), '\\1fa-search-plus\\2'),
        (re.compile(affix + r'icon-zoom-out' + affix), '\\1fa-search-minus\\2'),
        (re.compile(affix + r'icon-shopping-cart' + affix), '\\1fa-shopping-cart\\2'),
        (re.compile(affix + r'icon-2x' + affix), '\\1fa-2x\\2'),
        (re.compile(affix + r'icon-4x' + affix), '\\1fa-4x\\2'),
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
