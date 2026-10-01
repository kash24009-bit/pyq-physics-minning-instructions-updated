#!/usr/bin/env python3
"""phy_code_env.py - session setup for the Claude Code (cloud) route of PYQ Pattern Mining - Physics (042).

Run it once at the start of every Claude Code session, before anything else (Bash timeout 600000 ms):
    python3 "$(find / -name phy_code_env.py -not -path '/proc/*' 2>/dev/null | head -1)"
Run it again only if the cloud machine was replaced (the files you made this session are gone).

It never edits, moves or deletes a file inside any repository. It:
  1. finds the cloned repositories by their content, never by their names:
       instructions = the one holding PHY-02-PROTOCOL.md          (read only)
       project      = the one holding PHY-VAULT*.json             (the only one Claude Code commits to)
       papers       = the one(s) holding the question-paper ZIPs  (read only)
  2. installs what the kit needs (poppler-utils if possible; pillow, openpyxl, pypdfium2, pypdf, reportlab);
  3. rebuilds the claude.ai folder layout with links, so pyqkit and the protocol files work exactly as written:
       /mnt/project/            every file of the instructions repo + the project repo (outputs/ excluded)
       /mnt/user-data/uploads/  every file of the papers repo(s)
       /mnt/user-data/outputs   -> <project>/outputs   (what the kit writes there gets committed)
       /home/claude/            working area: vault, renders, the kit copy, a link to phy_gate.py
  4. collects every vault file from the working trees AND from every branch of every repository, restores the
     newest verified one with pyqkit, and uses the newest kit edition (a tie goes to the vault's own copy);
  5. decides this session's batch number, runs validate and status, writes /home/claude/phy_env.json.

Exit codes: 0 ready | 4 no vault anywhere (never start a new one) | 5 no instructions repo | 6 no project repo.
Optional environment variables:
  PHY_BATCH=<n>       use this batch number (after the machine was replaced inside the same conversation)
  PHY_REPOS=a:b:c     use exactly these repository folders instead of searching
  PHY_ROOT=<dir>      build the layout under <dir> instead of /            (testing only)
  PHY_SKIP_INSTALL=1  skip package installation                          (testing only)
"""
import datetime
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.environ.get("PHY_ROOT", "/")


def P(path):
    return os.path.join(ROOT, path.lstrip("/"))


HOME = P("/home/claude")
MNT_PROJECT = P("/mnt/project")
UPLOADS = P("/mnt/user-data/uploads")
OUTPUTS_LINK = P("/mnt/user-data/outputs")
VAULT = os.path.join(HOME, "vault")
KIT = os.path.join(HOME, "pyqkit.py")
GATE_LINK = os.path.join(HOME, "phy_gate.py")
CANDS = os.path.join(HOME, "vault_candidates")
KITS = os.path.join(HOME, "kit_candidates")
ENV_JSON = os.path.join(HOME, "phy_env.json")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".cache", ".venv", ".claude"}
VAULT_RE = re.compile(r"^PHY-VAULT.*\.json$", re.I)
KIT_RE = re.compile(r"^pyqkit.*\.(py|txt)$", re.I)
WARN = []


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd, timeout=900, binary=False, env=None):
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout, env=env)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 99, (b"" if binary else ""), str(e)
    out = r.stdout if binary else r.stdout.decode("utf-8", "replace")
    return r.returncode, out, r.stderr.decode("utf-8", "replace")


def files_of(repo, skip_outputs=False):
    top = os.path.abspath(repo)
    for dp, dns, fns in os.walk(repo):
        at_top = os.path.abspath(dp) == top
        dns[:] = sorted(d for d in dns if d not in SKIP_DIRS and not (skip_outputs and at_top and d == "outputs"))
        for f in sorted(fns):
            yield os.path.join(dp, f)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------ repositories
def find_repos():
    if os.environ.get("PHY_REPOS"):
        out = []
        for p in os.environ["PHY_REPOS"].split(os.pathsep):
            if p and os.path.exists(os.path.join(p, ".git")) and os.path.realpath(p) not in out:
                out.append(os.path.realpath(p))
        return out
    excluded = [os.path.realpath(x) for x in (HOME, P("/mnt"), "/proc", "/sys", "/dev")]

    def scan(start, depth=3):
        found = []
        base = os.path.realpath(start).rstrip("/").count("/")
        for dp, dns, fns in os.walk(start):
            real = os.path.realpath(dp)
            if any(real == e or real.startswith(e.rstrip("/") + "/") for e in excluded):
                dns[:] = []
                continue
            if ".git" in dns or ".git" in fns:
                if real not in found:
                    found.append(real)
                dns[:] = []
                continue
            if real.rstrip("/").count("/") - base >= depth:
                dns[:] = []
                continue
            dns[:] = sorted(d for d in dns if d not in SKIP_DIRS and not d.startswith("."))
        return found

    # The session's own folder first: in a cloud session with several repositories it sits just above the clones.
    cwd = os.getcwd()
    found = scan(cwd)
    if found:
        if os.path.exists(os.path.join(cwd, ".git")):      # started inside one clone: the others sit beside it
            for r in scan(os.path.dirname(cwd), depth=2):
                if r not in found:
                    found.append(r)
        return found
    for s in (os.path.dirname(cwd), os.path.expanduser("~"), "/workspace", "/workspaces", "/home", "/root", "/code",
              "/repos", "/src", "/srv", "/opt/repos", "/tmp"):
        if s and os.path.isdir(s):
            for r in scan(s):
                if r not in found:
                    found.append(r)
        if found:
            return found
    return found


def roles(repos):
    info = {}
    for r in repos:
        d = {"protocol": False, "vaults": [], "zips": [], "kits": [], "claude_md": [], "gate": [], "pdfs": 0}
        for f in files_of(r):
            b = os.path.basename(f)
            if b.upper() == "PHY-02-PROTOCOL.MD":
                d["protocol"] = True
            if VAULT_RE.match(b):
                d["vaults"].append(f)
            if b.lower().endswith(".zip"):
                d["zips"].append(f)
            if KIT_RE.match(b):
                d["kits"].append(f)
            if b == "CLAUDE.md":
                d["claude_md"].append(f)
            if b == "phy_gate.py":
                d["gate"].append(f)
            if b.lower().endswith(".pdf"):
                d["pdfs"] += 1
        info[r] = d
    instr = next((r for r in repos if info[r]["protocol"]), None)
    others = [r for r in repos if r != instr]
    project = next((r for r in others if info[r]["vaults"]), None)
    if project is None and instr and info[instr]["vaults"]:
        project = instr
    if project is None:
        rest = [r for r in others if not info[r]["zips"]]
        project = rest[0] if len(rest) == 1 else None
    several = [r for r in others if info[r]["vaults"]]
    if len(several) > 1:
        WARN.append("several repositories hold vault files; commits go to " + str(project))
    papers = [r for r in repos if info[r]["zips"] and r not in (instr, project)] or [r for r in repos if info[r]["zips"]]
    return info, instr, project, papers


def git_head(repo):
    b = run(["git", "-C", repo, "rev-parse", "--abbrev-ref", "HEAD"])[1].strip() or "?"
    c = run(["git", "-C", repo, "rev-parse", "--short", "HEAD"])[1].strip() or "?"
    return b, c


# ------------------------------------------------------------------------------------------------ packages
def install():
    if os.environ.get("PHY_SKIP_INSTALL"):
        return "skipped (PHY_SKIP_INSTALL)"
    if not shutil.which("pdftoppm") and shutil.which("apt-get"):
        pre = [] if os.geteuid() == 0 else (["sudo", "-n"] if shutil.which("sudo") else None)
        if pre is not None:
            env = dict(os.environ, DEBIAN_FRONTEND="noninteractive")
            rc = run(pre + ["apt-get", "install", "-y", "-q", "poppler-utils"], timeout=420, env=env)[0]
            if rc != 0:
                run(pre + ["apt-get", "update", "-q"], timeout=420, env=env)
                run(pre + ["apt-get", "install", "-y", "-q", "poppler-utils"], timeout=420, env=env)
    notes = ["poppler " + ("yes" if shutil.which("pdftoppm") else "no (the kit falls back to pypdfium2)")]
    mods = {"pillow": "PIL", "openpyxl": "openpyxl", "pypdfium2": "pypdfium2", "pypdf": "pypdf", "reportlab": "reportlab"}
    missing = [p for p, m in mods.items() if importlib.util.find_spec(m) is None]
    if missing:
        rc, o, e = run([sys.executable, "-m", "pip", "install", "-q"] + missing, timeout=600)
        if rc != 0:
            run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages"] + missing, timeout=600)
        importlib.invalidate_caches()
    still = [p for p, m in mods.items() if importlib.util.find_spec(m) is None]
    notes.append("python packages " + ("all present" if not still else "MISSING " + ", ".join(still)))
    if "pillow" in still or ("pypdfium2" in still and not shutil.which("pdftoppm")):
        WARN.append("the kit cannot render pages until these install: " + ", ".join(still))
    return " | ".join(notes)


# ------------------------------------------------------------------------------------------------ layout
def link_into(src, dst_dir, clashes):
    dst = os.path.join(dst_dir, os.path.basename(src))
    if os.path.islink(dst):
        tgt = os.path.realpath(dst)
        if tgt == os.path.realpath(src):
            return
        if os.path.exists(tgt) and sha(tgt) == sha(src):
            return
        clashes.append(f"{os.path.basename(src)}: kept {tgt}, did not link {src}")
        return
    if os.path.exists(dst):
        clashes.append(f"{dst} exists as a real file; left alone")
        return
    os.symlink(src, dst)


def build_layout(instr, project, papers, gate_src):
    clashes = []
    for d in (MNT_PROJECT, UPLOADS, HOME, os.path.dirname(OUTPUTS_LINK)):
        os.makedirs(d, exist_ok=True)
    for f in files_of(instr):
        link_into(f, MNT_PROJECT, clashes)
    if project and project != instr:
        for f in files_of(project, skip_outputs=True):
            link_into(f, MNT_PROJECT, clashes)
    for r in papers:
        for f in files_of(r):
            link_into(f, UPLOADS, clashes)
    out = os.path.join(project, "outputs")
    for sub in ("vault", "logs", "reports"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    if os.path.islink(OUTPUTS_LINK):
        if os.path.realpath(OUTPUTS_LINK) != os.path.realpath(out):
            os.remove(OUTPUTS_LINK)
            os.symlink(out, OUTPUTS_LINK)
    elif os.path.isdir(OUTPUTS_LINK):
        if not os.listdir(OUTPUTS_LINK):
            os.rmdir(OUTPUTS_LINK)
            os.symlink(out, OUTPUTS_LINK)
        else:
            WARN.append(f"{OUTPUTS_LINK} is a real, non-empty folder: always pass --out {out}")
    else:
        os.symlink(out, OUTPUTS_LINK)
    if gate_src:
        if os.path.islink(GATE_LINK) or os.path.exists(GATE_LINK):
            os.remove(GATE_LINK)
        os.symlink(gate_src, GATE_LINK)
    for c in clashes:
        WARN.append("name clash: " + c)
    return len(os.listdir(MNT_PROJECT)), len(os.listdir(UPLOADS)), out


# ------------------------------------------------------------------------------------------------ vault + kit
def gather_vaults(repos):
    shutil.rmtree(CANDS, ignore_errors=True)
    os.makedirs(CANDS)
    seen, count, branches = set(), {"tree": 0, "branch": 0}, set()

    def put(data, label, name):
        h = hashlib.sha256(data).hexdigest()
        if h in seen:
            return False
        seen.add(h)
        d = os.path.join(CANDS, re.sub(r"[^\w.-]+", "_", label))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, name), "wb") as f:
            f.write(data)
        return True

    for r in repos:
        rname = os.path.basename(r)
        for f in files_of(r):
            if VAULT_RE.match(os.path.basename(f)):
                with open(f, "rb") as fh:
                    if put(fh.read(), "tree-" + rname, os.path.basename(f)):
                        count["tree"] += 1
        rc, o, e = run(["git", "-C", r, "fetch", "--quiet", "--prune", "origin", "+refs/heads/*:refs/remotes/origin/*"], timeout=300)
        if rc != 0:
            WARN.append(f"git fetch failed in {r}: {e.strip()[:160]}")
        rc, o, e = run(["git", "-C", r, "for-each-ref", "--format=%(refname)", "refs/remotes/origin", "refs/heads"])
        for ref in [x.strip() for x in o.splitlines() if x.strip() and not x.strip().endswith("/HEAD")]:
            listing = run(["git", "-C", r, "ls-tree", "-r", "--name-only", ref])[1]
            for path in listing.splitlines():
                if VAULT_RE.match(os.path.basename(path)):
                    rc3, blob, e3 = run(["git", "-C", r, "show", f"{ref}:{path}"], binary=True)
                    if rc3 == 0 and put(blob, f"{rname}-{ref}", os.path.basename(path)):
                        count["branch"] += 1
                        branches.add(ref.replace("refs/remotes/", "").replace("refs/heads/", ""))
    return count, sorted(branches)


def edition(path):
    rc, o, e = run([sys.executable, path, "version"], timeout=120)
    m = re.search(r"kit edition (\S+)", o)
    return m.group(1) if (rc == 0 and m) else None


def repo_kits(repos):
    shutil.rmtree(KITS, ignore_errors=True)
    os.makedirs(KITS)
    found = []
    for r in repos:
        for f in files_of(r, skip_outputs=True):
            if KIT_RE.match(os.path.basename(f)):
                d = os.path.join(KITS, str(len(found) + 1))
                os.makedirs(d, exist_ok=True)
                dst = os.path.join(d, "pyqkit.py")
                shutil.copy2(f, dst)
                ed = edition(dst)
                if ed:
                    found.append((ed, f, dst))
    return found


def kit_from_candidates():
    """No kit file in any repository: take the kit that travels inside the newest candidate vault file."""
    best = None
    for f in sorted(os.path.join(dp, x) for dp, _, fs in os.walk(CANDS) for x in fs):
        try:
            obj = json.load(open(f, encoding="utf-8"))
            st = obj.get("state", {})
            key = (int(st.get("batch", 0) or 0), str(st.get("created_utc", "")))
            text = obj["files"]["tools/pyqkit.py"]["text"]
        except Exception:
            continue
        if best is None or key > best[0]:
            best = (key, text)
    if not best:
        return False
    with open(KIT, "w", encoding="utf-8") as f:
        f.write(best[1])
    return True


# ------------------------------------------------------------------------------------------------ main
def main():
    print(f"PHY Claude Code setup | {now()} | layout root {ROOT}")
    repos = find_repos()
    info, instr, project, papers = roles(repos) if repos else ({}, None, None, [])
    print("Repositories found: " + (", ".join(repos) if repos else "none"))
    if not instr:
        print("STOP: no repository holds PHY-02-PROTOCOL.md. Add the instructions repository to this session.")
        sys.exit(5)
    if not project:
        print("STOP: no repository holds a PHY-VAULT file. Add the project repository (with the vault file) to this session.")
        sys.exit(6)
    if not papers:
        WARN.append("no repository holds question-paper ZIPs: paper stages wait; scheme, classification and derive work can go on")
    cmds = [f for r in repos for f in info[r]["claude_md"]]
    if len(cmds) > 1:
        WARN.append("several CLAUDE.md files: " + ", ".join(cmds) + " - only the one in the instructions repository is current; "
                    "ask her to delete the others")
    gate_src = (info[instr]["gate"] or [None])[0]
    if not gate_src:
        WARN.append("phy_gate.py not found in the instructions repository")
    os.makedirs(HOME, exist_ok=True)
    print("Packages: " + install())
    n_proj, n_up, out = build_layout(instr, project, papers, gate_src)

    counts, branches = gather_vaults(repos)
    kits = repo_kits([instr] + ([project] if project != instr else []))
    best = max(kits, key=lambda k: k[0]) if kits else None
    if best:
        shutil.copy2(best[2], KIT)
    elif not kit_from_candidates():
        print("STOP: no kit (pyqkit) in the repositories and no vault file carrying one.")
        sys.exit(4)
    rc, o, e = run([sys.executable, KIT, "restore", VAULT, "--sources", CANDS], timeout=900)
    restore_lines = [ln for ln in o.splitlines() if ln.strip()]
    if rc != 0 or not os.path.exists(os.path.join(VAULT, "STATE.json")):
        print("\n".join(restore_lines) or e.strip())
        print("STOP: no vault file was found in any repository or branch. Never start a new vault: "
              "ask her to upload the newest PHY-VAULT file to the project repository.")
        sys.exit(4)
    vk = os.path.join(VAULT, "tools", "pyqkit.py")
    ved = edition(vk) if os.path.exists(vk) else None
    kit_from = f"{best[0]} from {best[1]}" if best else "from a vault file"
    if ved and (not best or ved >= best[0]):
        shutil.copy2(vk, KIT)
        kit_from = f"{ved} from the vault's tools/pyqkit.py"
    kit_ed = edition(KIT)

    st = json.load(open(os.path.join(VAULT, "STATE.json"), encoding="utf-8"))
    restored_batch = int(st.get("batch", 0) or 0)
    sid = os.environ.get("CLAUDE_CODE_REMOTE_SESSION_ID", "")
    if os.environ.get("PHY_BATCH"):
        session_batch, why = int(os.environ["PHY_BATCH"]), "set by PHY_BATCH"
    elif sid and st.get("cc_session") == sid:
        session_batch, why = restored_batch, "same Claude Code session as the newest vault"
    else:
        session_batch, why = restored_batch + 1, "new session"

    rc, vo, ve = run([sys.executable, KIT, "validate", VAULT], timeout=600)
    vline = next((ln for ln in reversed(vo.splitlines()) if "checks pass" in ln), (vo or ve).strip()[-200:])
    rc, so, se = run([sys.executable, KIT, "status", VAULT], timeout=600)
    pb, pc = git_head(project)

    env = {
        "created_utc": now(), "root": ROOT, "home": HOME, "vault": VAULT, "kit": KIT, "kit_edition": kit_ed,
        "gate": GATE_LINK if gate_src else "",
        "repos": {"instructions": instr, "project": project, "papers": papers},
        "mnt_project": MNT_PROJECT, "uploads": UPLOADS, "outputs": out,
        "packs_dir": os.path.join(out, "vault"), "logs_dir": os.path.join(out, "logs"),
        "reports_dir": os.path.join(out, "reports"),
        "restored": {"batch": restored_batch, "created_utc": st.get("created_utc", ""), "rows": st.get("rows", {}),
                     "cc_session": st.get("cc_session", "")},
        "session_batch": session_batch, "batch_reason": why, "cc_session": sid,
        "project_branch": pb, "project_head": pc, "warnings": WARN,
    }
    with open(ENV_JSON, "w", encoding="utf-8") as f:
        json.dump(env, f, indent=2)

    print("Roles:")
    for label, r in (("instructions", instr), ("project", project)):
        b, c = git_head(r)
        print(f"  {label:12} {r}  (branch {b}, commit {c})")
    for r in papers:
        b, c = git_head(r)
        print(f"  {'papers':12} {r}  (branch {b}, commit {c})")
    print(f"Layout: /mnt/project {n_proj} links | /mnt/user-data/uploads {n_up} links | outputs -> {out}")
    print(f"Vault candidates: {counts['tree']} from working trees, {counts['branch']} more from branches "
          f"{', '.join(branches) if branches else '(none)'}")
    for ln in restore_lines:
        print("  " + ln.strip())
    print(f"Kit: edition {kit_ed} ({kit_from})")
    print(f"Session batch: B{session_batch:02d} ({why}; restored vault is batch {restored_batch})")
    print(f"Validate: {vline.strip()}")
    print("Status:")
    for ln in so.splitlines():
        print("  " + ln)
    print("Warnings: " + ("none" if not WARN else ""))
    for w in WARN:
        print("  - " + w)
    print(f"Wrote {ENV_JSON}. The gate is {GATE_LINK if gate_src else 'MISSING'}.")
    sys.exit(0)


if __name__ == "__main__":
    main()
