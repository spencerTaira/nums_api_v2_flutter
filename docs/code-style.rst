Numbers API Code Style
======================

- Keep line lengths to 80

- Use ``# TODO: description`` for things that would be nice to fix, but do not
  represent bugs or problems in the system. Use ``# FIXME: description` for
  things which need to urgently be fixed, typically before a branch is merged
  or the site is deployed.

- When pattern matching existing tests, don't include lines you don't
  understand until you've proven they're required

- Write good docstrings::

    def my_method(x, y):
        """Short description of purpose that is one line long.

        More information here, particularly explaining what `x` and `y` are.
        """

- If you see things without good docstrings [or any at all!], please fix them
  or add a TODO to help encourage others to do so
