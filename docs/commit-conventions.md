# Commit Conventions
This repository uses the following syntax for commits:

    <type>(<scope>): <message>
    <description>

## Example
```
$ git commit -m "docs(readme): update project documention" -m "description"
```


## Definitions
- **&lt;type&gt;:** refers to the type or category of the commit. It indicates the purpose or  
nature of the changes made in the commit.

- **&lt;(scope)&gt;:** represents the scope of the changes made in the commit.It provides  
additional context to the commit by indicating the module, component, or area of  
the project that is affected by the changes (This repo uses component for scope).

- **&lt;message&gt;:** is a short and concise description of the changes introduced by the  
commit. It serves as a brief summary of what the commit is accomplishing.

- **&lt;description&gt;:** Provides additional details & context for changes made in commit.

## Types
- **init** Initialize new part, component or important package.
- **feat:** New feature, indicating a significant addition or enhancement.
- **style:** Code style changes, that do not affect the code's functionality.
- **refactor:** Refactored code that neither fixes a bug nor adds a feature.
- **chore:** Routine tasks, changes that are not related to project functionality.
- **perf:** Indicates that the commit is focused on performance improvements.
- **fix:** Bug fix or resolution of an issue.
- **delete**: Remove a part or feature that is not needed.
- **test:** including new or correcting previous tests.
- **docs:** Adding or changes related to documentation.

## More Examples
```
git commit -m "init(app): create app user in django project"
git commit -m "feat(user): add registration form"
git commit -m "style(css): adjust spacing in stylesheets"
git commit -m "refactor(api): improve error handling"
git commit -m "chore(build): update dependencies for configs"
git commit -m "perf(api): optimize database queries, faster response"
git commit -m "fix(posts): resolve issue with comments"
git commit -m "delete(api): remove test api database"
git commit -m "test(user): add unit tests for login functionality"
git commit -m "docs(readme): update installation instructions"
```
