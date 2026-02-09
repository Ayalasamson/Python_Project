import os
import shutil
import uuid
from datetime import datetime
import click

# הגדרת נתיבים קבועים כדי שיהיה קל להשתמש בהם
WIT_DIR = ".wit"
STAGING_DIR = os.path.join(WIT_DIR, "staging")
COMMITS_DIR = os.path.join(WIT_DIR, "commits")


def get_ignore_list():
    """רשימת קבצים ותיקיות שהמערכת לעולם לא תיגע בהם"""
    # כאן אנחנו מוסיפים את כל התיקיות שגורמות לבעיות
    ignore = {
        WIT_DIR,  # התיקייה של המערכת עצמה
        ".witignore",  # קובץ ההתעלמות
        ".venv",  # תיקיית הפייתון (הכי חשוב!)
        ".idea",  # הגדרות של PyCharm
        "__pycache__",  # קבצים זמניים של פייתון
        "wit.py"  # הקוד שלך (כדי שלא ימחק את עצמו בטעות)
    }

    if os.path.exists(".witignore"):
        with open(".witignore", "r") as f:
            for line in f:
                if line.strip():
                    ignore.add(line.strip())
    return ignore



@click.group()
def cli():
    """מערכת WIT - בקרת גרסאות בסיסית"""
    pass


@cli.command()
def init():
    """יוצר את תיקיית .wit ומבנה התיקיות הפנימי"""
    if not os.path.exists(WIT_DIR):
        os.makedirs(STAGING_DIR)  # יוצר גם את .wit וגם את staging
        os.makedirs(COMMITS_DIR)
        click.echo("Initialized empty WIT repository in .wit/")
    else:
        click.echo("WIT repository already exists.")


@cli.command()
@click.argument('path')
def add(path):
    """מוסיף קובץ או תיקייה לאזור ה-staging"""
    if not os.path.exists(WIT_DIR):
        click.echo("Error: Not a WIT repository. Run 'init' first.")
        return

    ignore_list = get_ignore_list()

    # פונקציה פנימית להעתקת קבצים תוך התעלמות ממה שצריך
    def add_to_staging(src):
        if os.path.basename(src) in ignore_list:
            return

        target = os.path.join(STAGING_DIR, src)
        if os.path.isdir(src):
            if not os.path.exists(target):
                os.makedirs(target)
            for item in os.listdir(src):
                add_to_staging(os.path.join(src, item))
        else:
            # יוצר תיקיות בדרך אם הן לא קיימות בתוך staging
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(src, target)

    if path == ".":
        # מוסיף את כל הקבצים בתיקייה הנוכחית
        for item in os.listdir():
            add_to_staging(item)
    else:
        add_to_staging(path)

    click.echo(f"Added {path} to staging area.")


@cli.command()
@click.option('-m', '--message', required=True, help='Commit message')
def commit(message):
    """יוצר תמונת מצב (Snapshot) מה-staging"""
    # יצירת מזהה ייחודי קצר
    commit_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    commit_path = os.path.join(COMMITS_DIR, commit_id)

    # העתקת כל תוכן ה-staging לתיקיית הקומיט החדשה
    shutil.copytree(STAGING_DIR, commit_path)

    # שמירת מטא-דאטה (הודעה וזמן) בקובץ טקסט בתוך הקומיט
    with open(os.path.join(commit_path, ".metadata"), "w") as f:
        f.write(f"Message: {message}\n")
        f.write(f"Timestamp: {timestamp}\n")

    click.echo(f"Created commit {commit_id}: {message}")


@cli.command()
def status():
    """מציג את מצב הקבצים"""
    if not os.path.exists(WIT_DIR):
        click.echo("Not a WIT repository.")
        return

    # בלוגיקה הזו אנחנו בודקים מה ב-staging
    staged_files = []
    for root, dirs, files in os.walk(STAGING_DIR):
        for file in files:
            # מחשב את הנתיב היחסי (בלי הקידומת של staging)
            rel_path = os.path.relpath(os.path.join(root, file), STAGING_DIR)
            staged_files.append(rel_path)

    click.echo("--- Status ---")
    click.echo("Files in staging:")
    for f in staged_files:
        click.echo(f"  (staged): {f}")


@cli.command()
@click.argument('commit_id')
def checkout(commit_id):
    """משחזר את הפרויקט לגרסה קודמת"""
    source_commit = os.path.join(COMMITS_DIR, commit_id)

    if not os.path.exists(source_commit):
        click.echo(f"Error: Commit {commit_id} not found.")
        return

    # מוחק את הקבצים הנוכחיים בתיקיית העבודה (זהירות!)
    ignore_list = get_ignore_list()
    for item in os.listdir():
        if item not in ignore_list:
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)

    # מעתיק את הקבצים מהקומיט חזרה לתיקייה הראשית
    for item in os.listdir(source_commit):
        if item == ".metadata": continue
        src_item = os.path.join(source_commit, item)
        if os.path.isdir(src_item):
            shutil.copytree(src_item, item)
        else:
            shutil.copy2(src_item, item)

    click.echo(f"Switched to commit {commit_id}.")


if __name__ == "__main__":
    cli()