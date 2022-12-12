#
from __future__ import annotations
import os, json, random
from datetime import datetime
from string import ascii_letters, digits
random_str_space = ascii_letters + digits

push_string = """**__-----------------------__ {repo} __-----------------------__**
New push from **{user_name}** !
 * branch: ***{branch_name}***
{commit_messages}
 * Time: {time}
 * hashes: `{from_hash}` → `{to_hash}`"""

MAX_MSG_LENGTH = 1500

def format_push_hook(d: dict, config: dict):
    global push_string

    ## discord channel to write to
    repo_full_name = d["repository"]["full_name"]
    for project_name, project in config.items():
        if project_name == "default":
            continue
        if project["name"] == repo_full_name:
            channel_id = project["channel-id"]
            break
    else:
        channel_id = config["default"]["channel-id"]
        print(f"Didn't find project  associated to {repo_full_name}. Writing to default channel.")

    ## repo and branch
    repo = d["repository"]["name"]
    branch = d["ref"].removeprefix("refs/heads/")

    ## commit hashes
    before_ref = d["before"]
    after_ref = d["after"]

    ## pusher
    pusher_name = d["pusher"]["name"]

    ## head commit
    head_commit = d["head_commit"]
    # messages = head_commit["message"]
    time = head_commit["timestamp"]
    time_date, time_clock = time.split("T")
    time_date = time_date.split("-")
    time_clock = time_clock.split(":")
    time_clock[2] = time_clock[2][:2]
    dtime = datetime(
        int(time_date[0]),
        int(time_date[1]),
        int(time_date[2]),
        int(time_clock[0]),
        int(time_clock[1]),
        int(time_clock[2]),
    )
    time_str = dtime.strftime("%d %h %Y - %H:%M:%S")

    # all commits
    all_commits = d["commits"]
    added = list(set([file_ for commit in all_commits for file_ in commit["added"]]))
    removed = list(set([file_ for commit in all_commits for file_ in commit["removed"]]))
    modified = list(set([file_ for commit in all_commits for file_ in commit["modified"]]))
    commit_msg_prefix = " * msg : __"
    commit_msg_suffix = "__"
    url_string = " (<{url}>)"
    messages_str: str = ""
    for commit in all_commits:
        # You have to come up with your own solution, here :-}
        ## Basically creating an short url for the commit site on github
        try:
            # this is not even collision-safe but chances of a collision happening for two urls are
            # around 3.5447041512174644e-11% so I'm not going to worry too much
            # (won't have billions of pushes anyway)
            random_str = "".join(random.choice(random_str_space) for _ in range(8))
            with open(f"/short-urls/{random_str}", "w") as file_:
                file_.write(commit["url"])
            shortened_url = f"https://reyland.dev/s/{random_str}"
        except:
            # Try and come up with your own url shortener !
            shortened_url = commit["url"]
        finally:
            # End of short url generation
            current_commit = commit_msg_prefix + commit["message"] + commit_msg_suffix + url_string.format(url=shortened_url)
            messages_str += "\n" + current_commit
    messages_str = messages_str.removeprefix("\n")

    # create msg str
    main_msg = push_string.format(
        repo=repo,
        user_name=pusher_name,
        from_hash=before_ref,
        to_hash=after_ref,
        branch_name=branch,
        commit_messages=messages_str,
        time=time_str,
    )

    messages: list[str] = [ main_msg ]

    if added:
        messages.extend(split_str_list_content("\nAdded:\n```diff\n", "+ '{}'\n", "```", added))
    if removed:
        messages.extend(split_str_list_content("\nRemoved:\n```diff\n", "- '{}'\n", "```", removed))
    if modified:
        messages.extend(split_str_list_content("\nModified:\n```py\n", "* '{}'\n", "```", modified))

    return messages, channel_id

def split_str_list_content(prefix: str, fstr: str, suffix: str, l: list[str]) -> list[str]:
    """ Splits the list 'l' into messages using the 'prefix', 'fstr' and 'suffix' """

    messages: list [str] = list()
    index: int = 0
    num_elements: int = len(l)
    current_msg: str = ""
    while index < num_elements:
        element = l[index]
        if len(current_msg) < MAX_MSG_LENGTH:
            current_msg += fstr.format(element)
            index += 1
        else:
            msg = prefix + current_msg + suffix
            messages.append(msg)
            current_msg = ""
    if current_msg:
        msg = prefix + current_msg + suffix
        messages.append(msg)
    return messages

