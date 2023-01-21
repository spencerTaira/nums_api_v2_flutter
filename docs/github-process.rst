GitHub Process
==============

Storypointing
-------------

At the start of each sprint, we'll storypoint a set of issues as a team. These
will be the issues that are open to work on in that sprint.

For project team leads:

- This means the stories should be moved to a sprint-specific
  milestone, like `rXX-sprint-1`.

- After storypointing is complete, please edit the description of the issue
  to add a line like "Storypoints: 4"

- When a sprint ends, if there are issues that should move to the next sprint,
  please change their milestone to the next sprint. If there are issues that
  wouldn't make sense for the next sprint, leave them in this milestone, even
  as incomplete.

Working on an issue
-------------------

When assigned an issue, you should do the following:

1. Select you (& your pair, if applicable) as "assignees" on it.

2. If you got clarification on an issue, please add comments to the issue with
   those; this will be important for future people to understand the issue
   and the code that satisfied it.

When you begin working on it:

1. Add the label of `-wip` to it.

2. Create a branch for it; this should be named like `265-ninja-api` (this
   contains the issue number, and a short, lower-cased, dashed-name describing
   the issue in only a few words).

3. Work on the issue in that branch. We expect testing for new code and
   professional documentation & code quality, so make sure you're doing those
   things.

4. When you would like a code review, make a pull request for the issue.

   Make the title of your PR the same as your branch name.

   The description for the PR doesn't need to contain a description of what
   you did (that's what the Git commit messages are for!). Instead, it should
   be "things I'd like reviewers to understand when looking at this work".
   This can include things like: "Not sure if doing ____ is the best way; we'd
   like feedback", "Can't figure out how to test ___, so the coverage has
   gone down", "We're waiting on ______ other issue to be completed, so pausing
   on this", etc.

   Add the team leads as reviewers.

   If you want a review but do not believe you have completed the task, please
   add the label `-wip` to the PR.

   Please add the text `Resolves #265` (substitute the issue number) there.
   Even if this is a WIP, add that --- when this PR is merged & closed, this
   will mark the issue as done. (It will also link the two in general, so you
   can navigate to the issue easily under the heading "linked issues")

The reviewers will receive an automated email requesting their review. (You're
welcome to also ping them on Slack as a heads-up, since not all of us check our
email as often).

After the reviewer(s) are done, they'll either accept & close it, add comments,
or request changes. If changes are requested, complete them, commit & push your
work. The reviewers will receive an automated email---but, again, you can ping
them on Slack to give them a heads-up.

When the issue is marked as `-wip`, reviewers will not resolve the issue. So if
you originally had that label, make sure to remove it when requesting a review
where you believe the work is complete.

Reviewing an issues
-------------------

Team lead reviewers will check for:

- correctness, obviously

- reasonable performance

- make sure there are no print statements causing any unexpected output when
  tests are run

- excellent and comprehensive tests

- good docstrings and, where needed, other helpful comments

- conformance to our code style guide

Once satisfied with the work, reviewers will approve it and merge it in using
"Squash and merge". This will squash all of the commits into one commit; they
will also tidy the commit message to reduce it to just the things needed
(not descriptions of now-unimportant-middle-work). Then they'll delete the
branch associated with it.
