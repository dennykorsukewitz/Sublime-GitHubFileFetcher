# [1.1.0] - 2026-10-06

## Fixed

- Percent-encode repository search queries and contents API paths so spaces and special characters no longer raise `InvalidURL`. Thanks to @dpc00 ([#1](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/issues/1)).
- Reset repository search results between queries (`found_repositories`, `new_repo_found`). Thanks to @dpc00 ([#2](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/issues/2)).
- On failed GitHub API calls (404, 403 rate limit, connection errors), show an error dialog with HTTP status where available and stop search, branch, file list, and file fetch instead of `AttributeError` or follow-up crashes. Thanks to @dpc00 ([#3](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/issues/3)).
- Show an error when no workspace folder is open instead of `IndexError` on `folders[0]`. Thanks to @dpc00 ([#4](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/issues/4)).
- Decode fetched file content as UTF-8 with `errors="replace"` so binary files no longer crash with `UnicodeDecodeError`. Thanks to @dpc00 ([#5](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/issues/5)).
- Thanks to @Jah-yee ([#10](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/pull/10)) for contributing these fixes.
