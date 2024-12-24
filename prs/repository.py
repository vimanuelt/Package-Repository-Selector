# prs/repository.py

import os

class RepositoryManager:
    def __init__(self):
        self.repo_dir = "/usr/local/etc/pkg/repos/"
        self.repos = self.load_repositories()

    def load_repositories(self):
        repos = []
        country_mappings = {
            "ca": "Canada",
            "fr": "France",
            "no": "Norway",
            "za": "South Africa"
        }
        for item in os.listdir(self.repo_dir):
            if item.startswith("GhostBSD.conf.") and os.path.isfile(os.path.join(self.repo_dir, item)):
                repo_name = item.replace("GhostBSD.conf.", "").capitalize()
                if repo_name.lower() in country_mappings:
                    repos.append(country_mappings[repo_name.lower()])
                else:
                    repos.append(repo_name.replace("_", " "))
        repos.sort()
        return repos

    def get_repo_path(self, repo_name):
        """Return the full path for the given repo_name."""
        country_mappings = {
            "Canada": "ca",
            "France": "fr",
            "Norway": "no",
            "South Africa": "za"
        }
        if repo_name in country_mappings:
            file_name = "GhostBSD.conf." + country_mappings[repo_name]
        else:
            file_name = "GhostBSD.conf." + repo_name.lower().replace(" ", "_")
        return os.path.join(self.repo_dir, file_name)

