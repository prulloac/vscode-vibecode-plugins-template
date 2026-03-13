# Contributing

Thank you for your interest in contributing!

## Coding Guidelines

<!-- TODO: Add coding guidelines specific to this project. Consider including:
- Language-specific style conventions
- Code formatting standards
- Naming conventions
- Architecture patterns
- File organization
-->

## Testing Guidelines

<!-- TODO: Add testing guidelines specific to this project. Consider including:
- Testing framework used
- How to run tests
- Test file location conventions
- Coverage requirements
- Types of tests (unit, integration, e2e)
-->

## Issue Submission

When reporting a bug, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (OS, versions, etc.)
- Any relevant logs or screenshots

## Feature Requests

For feature requests, please include:

- A clear description of the feature
- Use cases and why this feature would be valuable
- Any ideas for implementation (optional)

## Commit Message Guidelines

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (formatting, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Changes to build process, dependencies, or tooling
- `perf`: A code change that improves performance
- `ci`: Changes to CI configuration

### Rules

- Use lowercase for type and scope
- Keep the subject line under 72 characters
- Use imperative mood ("add" not "added" or "adds")
- Reference issues and pull requests where relevant
- Separate subject from body with a blank line

### Examples

```
feat(auth): add JWT authentication support
```

```
fix(api): resolve null pointer exception in user endpoint

The user endpoint was throwing a null pointer exception when
the user ID was not found in the database.

Fixes #42
```

```
docs(readme): update installation instructions
```

```
refactor(database): extract query builder into separate module

This improves code organization and makes the database layer
more testable.
```

```
test(auth): add unit tests for login functionality
```

```
chore(deps): update lodash to version 4.17.21
```

## Pull Requests

1. Fork the repository and create a branch from `main`
1. Make your changes following the coding guidelines
1. Add or update tests as appropriate
1. Ensure all tests pass
1. Update documentation if needed
1. Keep your commit history clean:
   - The number of commits should not exceed the number of files changed
   - Consider rebasing and squashing commits to consolidate related changes
   - Each commit should represent a meaningful, atomic change
1. Submit a pull request with a clear description of the changes
1. Respond to any feedback or review comments
