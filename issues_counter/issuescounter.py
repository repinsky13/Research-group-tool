from github import Github
from datetime import datetime, timedelta
import config

def read_hashes():
    hashes = []
    with open('hashes.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            current_hash = line[:-1]
            # add item to the list
            hashes.append(current_hash)
    return hashes

def write_to_file(file, hash, date, issues_c):
    file.write("commit hash: " + hash + "\n")
    file.write("commit date: " + date.strftime("%a, %d %b %Y %H:%M:%S") + "\n")
    file.write("open issues: " + str(issues_c) + "\n")
    file.write("\n")

def issues_count(hashes):
    g = Github(config.TOKEN) 
    repo = g.get_repo(config.repo_name)
    f = open("log.txt", "w")
    for hash in hashes:
        print("Analyzing commit #" + hash + "\n")
        commit = repo.get_commit(hash)
        commit_date = commit.commit.committer.date
        print("Commit date: " + commit_date.strftime("%a, %d %b %Y %H:%M:%S") + "\n")
        issue_count = 0
        issues = repo.get_issues(state = "open")
        for issue in issues:
            if (issue.created_at < commit_date):
                if (config.current_debt_label in issue.labels or "debt" in issue.body):
                    issue_count += 1    
        print("Open issues: " + str(issue_count))
        write_to_file(f, hash, commit_date, issue_count)
    f.close()


def main():
    hashes = read_hashes()
    print(hashes)
    issues_count(hashes)


if __name__ == '__main__':
    main()