Sublime Lint
=========

A framework for error highlighting in the [Sublime Text](http://sublimetext.com "Sublime Text") editor.

It's easy to add language support. Take a look at the [linter repository](http://github.com/lunixbochs/linters "Linter Repository") for examples.

Linters in your Sublime Text `User/linters` folder will be automatically used. Changes to linters in this folder will be overwritten on automatic update. If you want to change a builtin linter, disable it in the Sublime Lint preferences and copy the source to a new file/class name.

You can also import `Linter` and subclass it inside `plugin_loaded()` from any other Sublime plugin.

Installation
-----

You can install in ST3 by adding this repository to [Package Control](http://wbond.net/sublime_packages/package_control "Package Control"), which does automatic updates.

Alternatively, you can clone `sublimelint` into your Packages folder and switch to the `st3` branch manually, but you will need to update manually.

Usage
-----

Make sure you have the necessary command installed to lint your language - there's a list in the [linter repository](http://github.com/lunixbochs/linters "Linter Repository") README.

It will lint as you edit any file in a supported language. Check the status bar for messages, and take a look at the SublimeLint commands in the Command Palette.

There's a current bug that makes it sometimes take a few seconds to start linting upon an editor restart. Be patient.

Command Palette
-----

Press `cmd+shift+p` on OS X, `ctrl+shift+p` for everyone else. Type `sublimelint` to see the available commands:

* *Next Error* - Jump to the next highlighed error or warning in your code.
* *Previous Error* - Jump to the previous error.
* *Show All Errors* - Open a command panel listing all errors in the current file.
* *Report (Open Files)* - Lint all open files and show a report in a new view.
* *Preferences: SublimeLint Settings - User* - Change global and linter settings.

Settings
-----

You can change a few useful per-language settings by opening "SublimeLint Settings - User" via the Command Palette. Some languages (like C and C++) have additional linter-specific settings.

Example language settings:

    "Ruby": {
        // This command is run against your code.
        // Some linters use a temporary file, while others pipe code to stdin.
        "cmd": ["ruby", "-wc"],
        // Disable the linter.
        "disable": false,
        // Exclude file patterns from being linted.
        "excludes": ["Rakefile", "*.blah"]
    }
