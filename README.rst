b2tob3
======

.. image:: https://badge.fury.io/py/b2tob3.png
        :target: http://badge.fury.io/py/b2tob3
.. image:: https://travis-ci.org/metrey/b2tob3.png?branch=master
        :target: https://travis-ci.org/metrey/b2tob3

Easier migration from Boostrap 2 to Boostrap 3 / FontAwesome v3 to v4
---------------------------------------------------------------------
::
     Use at your own risk, I modify it for my need only
      
     ~ metrey

b2tob3 is a command line tool to help migrate Web projects from bootstrap 2
to bootstrap 3 by performing a set of replacements that reflect bootstrap 3
class name changes.

b2tob3 searches all files ending in .html, .htm, .css or .js in the current
directory and its subdirectories. You can specify the working directory with
the ``d`` option like ``b2tob3 -d /path/to/dir``.

b2tob3 does not fully automate migration, but it takes away some of the tedious
work. Still, you'll most likely need to perform manual fixes too.

Including as well the FontAwesome Migration from v3 to v4
  https://github.com/FortAwesome/Font-Awesome/wiki/Upgrading-from-3.2.1-to-4

Installation
------------

::

    pip install b2tob3

::
   
    pip uninstall b2tob3
    python setup.py install
    pip install b2tob3
    pip install b2tob3 --upgrade   
	
Usage
-----

::

    cd /project/html/
    b2tob3

Extension Supports
-------------------

* Style: '.css', '.haml', '.less'	
* HTML: '.html', '.htm', '.js'
* Script files: '.jsp', '.jspf'
* Language: '.java', '.php' (Use it carefully)
	
Follow these steps to avoid frustration:
----------------------------------------

* Put your HTML/template files under version control, if they aren't yet.
* Change to the directory with the files containing Boostrap 2 specific markup.
* Run the b2tob3 script once and only once.
* Review the changes with a diff tool suitable for the version control system you use.
* Perform the rest of the necessary changes manually.

Contributing
------------

* Let me know about bugs by posting `an issue <https://github.com/yaph/b2tob3/issues>`_.
* Help reduce the manual work by improving `the code <https://github.com/yaph/b2tob3>`_.
* Write tests.

Contributors
------------

Thanks to `@demiurg <https://github.com/demiurg>`_ for adding more robust
replacements and command line options.