import base64
import codecs
import json
import os

import sublime
import sublime_plugin

try:
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen
    from urllib.parse import quote
except ImportError:
    from urllib2 import HTTPError, URLError, urlopen
    from urllib import quote


def plugin_loaded():

    global settings
    settings = sublime.load_settings("GitHubFileFetcher.sublime-settings")


class GitHubFileFetcherCommand(sublime_plugin.WindowCommand):
    search_owner_string = "-- Search Owner --"
    search_repo_string = "-- Search Repository --"

    information_messages = ""
    message = ""
    value = ""

    new_repo_found = 0
    owner_repository = ""
    branch = ""

    def run(self):

        self.found_repositories = []
        self.branches = []
        self.files = []
        self.file = {}
        self.folders = []
        self.new_repo_found = 0
        self.owner_repository = ""
        self.branch = ""
        self.last_request_error = ""

        self.repositories = settings.get("repositories")
        self.information_messages = settings.get("information_messages")

        # Add search_repo_string to possible selection
        if self.search_repo_string not in self.repositories:
            self.repositories.insert(0, self.search_repo_string)

        # Add search_owner_string to possible selection
        if self.search_owner_string not in self.repositories:
            self.repositories.insert(0, self.search_owner_string)

        # Status Message
        if self.information_messages != "false":
            self.message = "GitHubFileFetcher (1/6): Fetching GitHub repositories."
            sublime.status_message(self.message)
            print(self.message)

        # Owner/Repository Selection.
        self.window.show_quick_panel(
            items=self.repositories,
            on_select=self.repository_get,
            flags=32,
            selected_index=-1,
            on_highlight=None,
            placeholder="GitHubFileFetcher (1/6): Search/Select GitHub repositories...",
        )

    def repository_get(self, index):

        if index == -1:
            return

        self.owner_repository = self.repositories[index]

        if len(self.owner_repository) == 0:
            return

        # Search for Owner or Repository
        if (
            self.owner_repository == self.search_owner_string
            or self.owner_repository == self.search_repo_string
        ):
            self.repository_search_input()
        else:
            self.repository_selected(index)

    def repository_search_input(self):

        if self.owner_repository == self.search_owner_string:
            self.value = "Owner"
            self.message = f"Enter GitHub {self.value}. Example: dennykorsukewitz"

        if self.owner_repository == self.search_repo_string:
            self.value = "Repositories"
            self.message = (
                f"Enter GitHub {self.value}. Example: VSCode-GitHubFileFetcher"
            )

        # Create search_string input panel
        self.window.show_input_panel(
            caption=self.message,
            initial_text=self.value,
            on_done=self.repository_search,
            on_change=None,
            on_cancel=None,
        )

    def repository_search(self, search_string):

        self.found_repositories = []
        self.new_repo_found = 0

        if self.owner_repository == self.search_owner_string:
            search_string += "/"

        url = "https://api.github.com/search/repositories?q="
        url += quote(search_string, safe="")

        # Log.
        if self.information_messages == "verbose":
            self.message = (
                f"GitHubFileFetcher: Fetching {self.value} from url: '{url}'."
            )
            print(self.message)

        response = self.url_json(url)

        if response is None:
            self.show_github_request_failure()
            return

        for repository in response["items"]:
            self.found_repositories.append(repository["full_name"])

        if len(self.found_repositories) >= 1:
            self.new_repo_found = 1

            # New Repository selection
            self.window.show_quick_panel(
                items=self.found_repositories,
                on_select=self.repository_selected,
                flags=32,
                selected_index=-1,
                on_highlight=None,
                placeholder="GitHubFileFetcher (1/6): Select GitHub repositories...",
            )

    def repository_selected(self, index):

        if index == -1:
            return

        if self.new_repo_found == 1:
            self.owner_repository = self.found_repositories[index]
        else:
            self.owner_repository = self.repositories[index]

        self.branches_get()

    def branches_get(self):

        url = f"https://api.github.com/repos/{self.owner_repository}/branches"

        # Log
        if self.information_messages != "false":
            self.message = "GitHubFileFetcher (2/6): Fetching branches."
            sublime.status_message(self.message)
            print(self.message)

        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher (2/6): Fetching branches from '{url}'"
            print(self.message)

        branches_json = self.url_json(url)

        if branches_json is None:
            self.show_github_request_failure()
            return

        self.branches = []
        for branch in branches_json:
            self.branches.append(branch["name"])

        # Reverse branches
        self.branches = self.branches[::-1]

        # Status Message
        if self.information_messages == "verbose":
            self.message = "GitHubFileFetcher (2/6): Select branch..."
            print(self.message)

        # Branch selection
        self.window.show_quick_panel(
            items=self.branches,
            on_select=self.branch_selected,
            flags=32,
            selected_index=-1,
            on_highlight=None,
            placeholder="GitHubFileFetcher (2/6): Select branch...",
        )

    def branch_selected(self, index):

        if index == -1:
            return

        self.branch = self.branches[index]

        # Log
        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher (2/6): Branch '{self.branch}' selected."
            print(self.message)

        self.files_get()

    def files_get(self):

        url = f"https://api.github.com/repos/{self.owner_repository}/git/trees/{self.branch}?recursive=1"

        # Log
        if self.information_messages != "false":
            self.message = "GitHubFileFetcher (3/6): Fetching files."
            sublime.status_message(self.message)
            print(self.message)

        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher (3/6): Fetching files for branch '{self.branch}' from '{url}'."
            print(self.message)

        self.files = []

        tree = self.url_json(url)

        if tree is None:
            self.show_github_request_failure()
            return

        for file in tree["tree"]:
            # skip folder names
            if file["type"] == "tree":
                continue

            self.files.append(file["path"])

        # Log
        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher (3/6): Showing file selection for branch '{self.branch}'."
            print(self.message)

        # File Selection
        self.window.show_quick_panel(
            items=self.files,
            on_select=self.file_selected,
            flags=32,
            selected_index=-1,
            on_highlight=None,
            placeholder="GitHubFileFetcher (3/6): Select file...",
        )

    def file_selected(self, index):

        if index == -1:
            return

        file_path = self.files[index]

        # Log
        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher (3/6): Selected file '{file_path}' from branch '{self.branch}'."
            print(self.message)

        url = (
            f"https://api.github.com/repos/{self.owner_repository}/contents/"
            f"{quote(file_path, safe='')}?ref={quote(self.branch, safe='')}"
        )

        # Log
        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher (3/6): Fetching file data for file: '{file_path}' from branch: '{self.branch}' from url: '{url}'."
            print(self.message)

        file_json = self.url_json(url)

        if file_json is None:
            self.show_github_request_failure()
            return

        content = base64.decodebytes(file_json["content"].encode("utf-8")).decode(
            "utf-8", errors="replace"
        )

        # Log
        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher (3/6): Decoded file '{file_path}' from branch '{self.branch}'. Adding custom header."
            print(self.message)

        # Fix windows line endings
        content = content.replace("\r\n", "\n")
        content = content.replace("\r", "\n")

        self.file["path"] = file_path
        self.file["content"] = content

        self.folders_get()

    def folders_get(self):

        # Log
        if self.information_messages != "false":
            self.message = "GitHubFileFetcher (4/6): Fetching destination folder."
            sublime.status_message(self.message)
            print(self.message)

        self.folders = self.window.folders()

        if len(self.folders) > 1:
            # Log
            if self.information_messages == "verbose":
                self.message = "GitHubFileFetcher (4/6): Showing folder selection for file '{}' from branch '{}'.".format(
                    self.file["path"], self.branch
                )
                print(self.message)

            # Folder / Workspace Selection
            self.window.show_quick_panel(
                items=self.folders,
                on_select=self.folder_selected,
                flags=32,
                selected_index=-1,
                on_highlight=None,
                placeholder="GitHubFileFetcher (4/6): Select destination workspace...",
            )

        else:
            if not self.folders:
                sublime.error_message(
                    "GitHubFileFetcher: No folder is open in the workspace. "
                    "Open a folder first, then try again."
                )
                return
            self.file["folder"] = self.folders[0]
            self.file_path_get()

    def folder_selected(self, index):

        if index == -1:
            return

        self.file["folder"] = self.folders[index]

        self.file_path_get()

    def file_path_get(self):

        # Log
        if self.information_messages != "false":
            self.message = (
                "GitHubFileFetcher (5/6): Enter or change destination file path..."
            )
            sublime.status_message(self.message)
            print(self.message)

        if self.information_messages == "verbose":
            self.message = "GitHubFileFetcher (5/6): Enter or change destination file path... '{}".format(
                self.file["path"]
            )
            print(self.message)

        # Create destination file path input panel
        self.window.show_input_panel(
            caption="GitHubFileFetcher (5/6): Enter or change destination file path...",
            initial_text=self.file["path"],
            on_done=self.write_and_open_file,
            on_change=None,
            on_cancel=None,
        )

    def write_and_open_file(self, path):

        self.file["path"] = path

        # Log
        if self.information_messages != "false":
            self.message = "GitHubFileFetcher (6/6): Added file {}".format(
                self.file["path"]
            )
            sublime.status_message(self.message)
            print(self.message)

        self.file["absolut_path"] = "{}/{}".format(
            self.file["folder"], self.file["path"]
        )

        self.write_to_file()

        if self.information_messages == "verbose":
            self.message = (
                "GitHubFileFetcher: Opening file '{}' from branch '{}'.".format(
                    self.file["path"],
                    self.branch,
                )
            )
            print(self.message)

        sublime.active_window().open_file(self.file["absolut_path"])

        self.refresh_folders()

        if self.information_messages == "verbose":
            self.message = "GitHubFileFetcher: Activating view for file '{}' from branch '{}'.".format(
                self.file["path"], self.branch
            )
            print(self.message)

        sublime.active_window().focus_view(sublime.active_window().active_view())

        self.file = {}

        if self.new_repo_found == 1:
            if self.information_messages == "verbose":
                self.message = "GitHubFileFetcher: Should I save the new repository in the settings?"
                print(self.message)

            # Folder / Workspace Selection
            self.window.show_quick_panel(
                items=["yes", "no"],
                on_select=self.store_repository,
                flags=32,
                selected_index=-1,
                on_highlight=None,
                placeholder="GitHubFileFetcher: Should I save the new repository in the settings?",
            )

    def store_repository(self, index):

        if index == -1:
            return

        if index == 1:
            return

        if self.information_messages != "false":
            self.message = "GitHubFileFetcher: Repository has been stored."
            sublime.status_message(self.message)
            print(self.message)

        self.repositories = settings.get("repositories")
        self.repositories.append(self.owner_repository)

        settings.set("repositories", self.repositories)
        sublime.save_settings("GitHubFileFetcher.sublime-settings")

    def refresh_folders(self):

        if self.information_messages == "verbose":
            self.message = "GitHubFileFetcher: Refreshing folders."
            print(self.message)

        data = sublime.active_window().project_data()
        sublime.active_window().set_project_data({})
        sublime.active_window().set_project_data(data)

    def write_to_file(self):

        directory = os.path.dirname(self.file["absolut_path"])
        if not os.path.exists(directory):
            if self.information_messages == "verbose":
                sublime.status_message(
                    "Creating folder structure '{}' for file '{}' from branch '{}'.".format(
                        directory, self.file["path"], self.branch
                    )
                )
            os.makedirs(directory)

        if self.information_messages == "verbose":
            sublime.status_message(
                "Writing content to file '{}' from branch '{}'.".format(
                    self.file["path"], self.branch
                )
            )

        with codecs.open(self.file["absolut_path"], "w", "utf-8") as file_handle:
            file_handle.write(self.file["content"])

    def show_github_request_failure(self):

        message = self.last_request_error or "GitHub request failed."
        if not message.startswith("GitHubFileFetcher:"):
            message = "GitHubFileFetcher: " + message
        sublime.error_message(message)

    def format_http_error(self, err, url):

        if err.code == 403:
            return (
                "GitHub returned 403 (Forbidden). "
                "Rate limit exceeded or access denied — "
                "set github_username and github_token in GitHubFileFetcher settings."
            )

        if err.code == 404:
            return f"GitHub returned 404 (Not Found) for:\n{url}"

        return f"GitHub returned HTTP {err.code} for:\n{url}"

    def url_json(self, url):

        json_result = self.url_content(url)

        if json_result is None:
            return None

        # Log.
        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher: Successfully fetch from '{url}'"
            print(self.message)

        if self.information_messages == "verbose":
            self.message = f"GitHubFileFetcher: JSON Result: '{json_result}'"
            print(self.message)

        return json.loads(json_result)

    def url_content(self, url):

        req = self.url_request(url)

        if req is None:
            return None

        return req.read().decode(req.headers.get_content_charset())

    def url_request(self, url):

        self.last_request_error = ""

        request = Request(url)

        github_username = settings.get("github_username")
        github_token = settings.get("github_token")

        if (
            github_username
            and github_token
            and len(github_username) > 0
            and len(github_token) > 0
        ):
            credentials = f"{github_username}:{github_token}"

            credentials_base64 = base64.b64encode(credentials.encode("utf-8"))

            request.add_header(
                "Authorization", "Basic {}".format(credentials_base64.decode("utf-8"))
            )

        # Attempt to open the url
        try:
            # Make our open request
            req = urlopen(request)

        except TypeError as err:
            self.last_request_error = str(err)
            sublime.status_message(str(err))
            return None

        except HTTPError as err:
            self.last_request_error = self.format_http_error(err, url)
            sublime.status_message(self.last_request_error)
            return None

        except URLError as err:
            reason = getattr(err, "reason", err)
            self.last_request_error = f"Could not connect to GitHub ({reason})."
            sublime.status_message(self.last_request_error)
            return None

        return req