
Contributing to QBoson's Kaiwu Software Projects   
==========   

Objective
----------
This document aims to foster a unified understanding among software contributors to QBoson's Kaiwu software projects by adhering to the code conventions and best practices established at QBoson.
This document is designed to evolve over time and is not exhaustive. Your feedback is invaluable and encouraged.

Testing
=======
Completion Criteria:
- A feature or bugfix is deemed complete when it is accompanied by comprehensive unit tests.
- Integral to the pull-request process is the testing of your branch against the `master`. The more extensive your tests, the smoother the pull-request process will be.

Submitting Changes
==================

 Contribution Process:
- To contribute to a QBoson project, begin by forking the repository using the `Github fork <https://guides.github.com/activities/forking/>`_ button and developing in a feature branch within your own repository.
- Commit and push your changes frequently, and utilize local rebasing to maintain a clean and readable commit history.
- Initiate a pull request early to facilitate discussions and save time. Early engagement can significantly streamline the merging process.
- When your feature is ready for integration, notify the repository owner to initiate the merge.

Commit Guidelines:
- Adhere to the commit message conventions outlined in the following resources:
  * https://chris.beams.io/posts/git-commit/
  * https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
  
Commit Message Essentials:
- Separate the subject from the body with a blank line.
- Limit the subject line to 50 characters.
- Capitalize the subject line.
- Avoid ending the subject line with a period.
- Use the imperative mood in the subject line.
- Wrap the body at 72 characters.
- Use the body to explain the 'what' and 'why', not the 'how'.

Branch Management:
- For long-lived branches, periodically rebase off of `master`.
- If you're familiar with Git but find rebasing daunting, consult the `think like a Git guide <http://think-like-a-git.net/>`_.
Repository Structure:
- The `master` branch in a `qbosonsystems` repository represents the latest developments. Older significant versions are maintained in version branches, such as `2.x` and `3.x`, while `master` tracks the `4.x` version.
- We strive to minimize the number of active version branches.

Release Management:
- Stable releases are tracked using tags. These tagged snapshots are deployed to PyPI following successful passage of continuous integration tests.

Coding Conventions
==================
Code Standards:
- Variable names should conform to well-recognized language conventions, avoiding cryptic or overly concise naming.
- Code should be written with readability in mind, as it is read more often than written.
- Functions should have a single responsibility.
- Emphasize early pull requests and code reviews.
- Engage in early architecting and design, with code reviews potentially preceding the writing of code.
- Maintain a consistent character limit of 100.
- Use 4 spaces for indentation, not tabs.
- Ensure all files end with a newline.

Documentation and Comments
--------------------------
Commenting Best Practices:
- Provide thorough and meaningful comments. Refer to this `Coding Horror article <https://blog.codinghorror.com/code-tells-you-how-comments-tell-you-why/>`_ for guidance.
- Comments should complement the code, not duplicate it. Avoid restating what the code does in English or pseudo-code; instead, explain the purpose of the code block.
- Make side effects clear, either in the code or through comments.
- Remember, **the best documentation is clean, simple code with well-chosen variable names**. When clarity in code alone is not possible, use comments to explain the functionality.

Python
------
Python Version Compatibility

- Code must be compatible with all `supported versions <https://devguide.python.org/versions/>`_ of Python, specifically those with "bugfix" or "security" status.

pep8 Style Guide

- As a baseline, follow the `pep8 <https://www.python.org/dev/peps/pep-0008/>`_ style guide for Python.
- In Kaiwu, we enforce a maximum line length of 120 characters. While lines of code up to 100 characters are preferred, lines up to 120 characters are permitted. Docstrings and comments should ideally not exceed 72 characters.

Documentation Standards

- Use Google docstrings convention (`definition <https://google.github.io/styleguide/pyguide.html>`_, `example <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_) for all public-facing functions, with the following exceptions:
  * For QBoson extensions of third-party projects, match the existing convention  project follows `NumPy <https://scipy.org>`_ conventions).
  * Argument defaults should be written as "default=x" rather than "default x".
- Private functions should include some form of docstring.
- Modules with more than one public unit should have a module docstring with a table of contents.
- The docstring for the `__init__` method should be placed on the class.
- All docstrings must be parsable by the `Sphinx <https://www.sphinx-doc.org/>`_ documentation generation tool (i.e., reStructuredText). The sphinx theme should be `readthedocs <https://docs.readthedocs.io/en/latest/>`_.
