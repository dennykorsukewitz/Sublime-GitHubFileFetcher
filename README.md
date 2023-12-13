<img align="right" width="150" height="150" src="doc/images/icon.png">

# GitHubFileFetcher

**GitHubFileFetcher** is a Sublime Text package that searches and fetches files from GitHub.

| Repository | GitHub | Sublime Text |
| ------ | ------ | ------ |
| ![GitHub release (latest by date)](https://img.shields.io/github/v/release/dennykorsukewitz/Sublime-GitHubFileFetcher) | ![GitHub open issues](https://img.shields.io/github/issues/dennykorsukewitz/Sublime-GitHubFileFetcher) ![GitHub closed issues](https://img.shields.io/github/issues-closed/dennykorsukewitz/Sublime-GitHubFileFetcher?color=#44CC44) | ![Package Control Total](https://img.shields.io/packagecontrol/dt/GitHub%20File%20Fetcher) |
| ![GitHub license](https://img.shields.io/github/license/dennykorsukewitz/Sublime-GitHubFileFetcher) | ![GitHub pull requests](https://img.shields.io/github/issues-pr/dennykorsukewitz/Sublime-GitHubFileFetcher?label=PR) ![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/dennykorsukewitz/Sublime-GitHubFileFetcher?color=g&label=PR) | ![Package Control Month](https://img.shields.io/packagecontrol/dm/GitHub%20File%20Fetcher) |
| ![GitHub language count](https://img.shields.io/github/languages/count/dennykorsukewitz/Sublime-GitHubFileFetcher?style=flat&label=language)  | ![GitHub contributors](https://img.shields.io/github/contributors/dennykorsukewitz/Sublime-GitHubFileFetcher) | ![Package Control Week](https://img.shields.io/packagecontrol/dw/GitHub%20File%20Fetcher) |
| ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/dennykorsukewitz/Sublime-GitHubFileFetcher)  | ![GitHub downloads](https://img.shields.io/github/downloads/dennykorsukewitz/Sublime-GitHubFileFetcher/total?style=flat) | ![Package Control Day](https://img.shields.io/packagecontrol/dd/GitHub%20File%20Fetcher) |

| Status |
| ------ |
| [![GitHub commits since tagged version](https://img.shields.io/github/commits-since/dennykorsukewitz/Sublime-GitHubFileFetcher/1.0.0/dev)](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/compare/1.0.0...dev) ![GitHub Workflow Lint](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/actions/workflows/lint.yml/badge.svg?branch=dev&style=flat&label=Lint) ![GitHub Workflow Pages](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/actions/workflows/pages.yml/badge.svg?branch=dev&style=flat&label=GitHub%20Pages) |

## Feature

The following steps are performed one after the other.

**1. GitHubFileFetcher (1/6):** Fetching GitHub repositories.

    This function allows you to search for GitHub owners or GitHub repositories.
    The search results (owner/repository) are then displayed.

**2. GitHubFileFetcher (2/6):** Fetching branches.

    After selecting the repository, all possible branches are displayed.

**3. GitHubFileFetcher (3/6):** Fetching files.

    After that, select the desired file.

**4. GitHubFileFetcher (4/6):** Fetching destination folder.

    Finally, the destination folder must be selected.

**5. GitHubFileFetcher (5/6):** Enter or change destination file path...

    Enter or change destination file path.

**6. GitHubFileFetcher (6/6):** Added file.

    `Hocus Pocus` - The file was created at the desired location.

**GitHubFileFetcher:** Should I save the new repository in the settings?

    So that you don't have to search for the repositories again and again,
    you can save the currently used one in the settings.

**Command:**  ```GitHubFileFetcher: Searches and fetches files from GitHub.```

![GitHubFileFetcher](doc/images/githubfilefetcher.gif)

### Settings

`Preferences -> Settings -> Extensions -> GitHubFileFetcher`

| Name | Description | Default Value |
| - | - | - |
| information_messages | Information messages will be displayed. | true |
| github_username | GitHub username | dennykorsukewitz |
| github_token | GitHub token | 123xxx789 |
| repositories | List of possible GitHub repositories. GitHub {owner}/{repo}. | dennykorsukewitz/Sublime-GitHubFileFetcher |

The GitHub API is limited to 60 requests per hour for non authorized requests. You can provide your GitHub username and an access token to push this limit to 5000 requests per hour. Please see the [official GitHub doc](https://docs.github.com/en/free-pro-team@latest/rest/rate-limit/rate-limit?apiVersion=2022-11-28) for further information.
You can generate the access token in your [GitHub settings](https://github.com/settings/tokens).

---

## Installation

To install this package, you have **three** options:

### 1. Search Package via `Package Control`

Search and install online package via [Sublime Package Control](http://wbond.net/sublime_packages/package_control).

`Tools` -> `Command Palette` -> `Package Control: Install Package` -> simply search for `GitHubFileFetcher` to install.

### 2. Install via sublime-package file

Download latest [sublime-package file](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/releases) and move the package `GitHubFileFetcher.sublime-package` to `Installed Packages` folder.

#### OSX

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Installed Packages/
    - or ST 3 -
    cd ~/Library/Application\ Support/Sublime\ Text\ 3/Installed Packages/

#### Linux

    cd ~/.config/sublime-text-2/Installed Packages
    - or ST 3 -
    cd ~/.config/sublime-text-3/Installed Packages

#### Windows

    cd "%APPDATA%\Sublime Text 2\Installed Packages"
    - or ST 3 -
    cd "%APPDATA%\Sublime Text 3\Installed Packages"

### 3. Source code

Clone the latest [dev branch](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher) and unpack it to Sublime Package folder `Packages`.

#### OSX

    cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    - or ST 3 -
    cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
    git clone git@github.com:dennykorsukewitz/Sublime-GitHubFileFetcher.git GitHubFileFetcher

#### Linux

    cd ~/.config/sublime-text-2/Packages
    - or ST 3 -
    cd ~/.config/sublime-text-3/Packages
    git clone git@github.com:dennykorsukewitz/Sublime-GitHubFileFetcher.git GitHubFileFetcher

#### Windows

    cd "%APPDATA%\Sublime Text 2\Packages"
    - or ST 3 -
    cd "%APPDATA%\Sublime Text 3\Packages"
    git clone git@github.com:dennykorsukewitz/Sublime-GitHubFileFetcher.git GitHubFileFetcher

---

## Download

For download see [Sublime-GitHubFileFetcher](https://github.com/dennykorsukewitz/Sublime-GitHubFileFetcher/releases)

---

Enjoy!

Your [Denny Korsukéwitz](https://github.com/dennykorsukewitz) 🚀
