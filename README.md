🛠 WIT - Python Version Control System
WIT היא מערכת לניהול גרסאות (VCS) קלת משקל שנכתבה בפייתון. הפרויקט מדמה את פעולות הליבה של Git, ומאפשר למשתמשים לנהל מעקב אחר שינויים בקבצים בצורה פשוטה ויעילה דרך שורת הפקודה.

🏗 ארכיטקטורת המערכת
הפרויקט נבנה תוך הקפדה על הפרדת רשויות (Separation of Concerns):

wit.py (The Interface): אחראי על ממשק המשתמש (CLI) באמצעות ספריית click. הוא משמש כ"שלד" הפקודות ומנתב את המשתמש לביצוע הלוגיקה.

logic.py (The Engine): מכיל את כל המימוש הטכני - ניהול קבצים, העתקות רקרסיביות, יצירת קומיטים ייחודיים ושחזור גרסאות.

📋 פקודות זמינות
לצורך אתחול הפרויקט והפעלות כתבו בשורת הפקודה:
pip install -r requirements.txt
1. אתחול המערכת (init)
יוצר את התשתית הנדרשת לפעילות המערכת: תיקיית .wit הכוללת את אזור ה-Staging ותיקיית הקומיטים.

Bash
python wit.py init
2. הוספת קבצים (add)
מעתיק קבצים או תיקיות שלמות לתוך אזור ה-Staging.

המערכת תומכת בהוספה רקרסיבית.

המערכת מתעלמת מקבצים המוגדרים ב-.witignore או מקבצי מערכת (כמו venv).

Bash
python wit.py add <path_to_file_or_folder>
# או להוספת כל התיקייה הנוכחית:
python wit.py add .
3. יצירת גרסה (commit)
שומר את המצב הנוכחי של ה-Staging כגרסה קבועה.

ייחודיות: כל קומיט מקבל מזהה ייחודי (ID) קצר שנוצר באמצעות UUID.

ניקוי אוטומטי: לאחר הקומיט, אזור ה-Staging מתנקה כדי למנוע כפילויות.

אופציונלי: ניתן להוסיף הודעה המתארת את השינוי.

Bash
python wit.py commit -m "Your descriptive message"
# או ללא הודעה (ישתמש בברירת מחדל):
python wit.py commit
4. בדיקת סטטוס (status)
מציג אילו קבצים ממתינים כרגע ב-Staging וטרם נשמרו בקומיט.

Bash
python wit.py status
5. שחזור גרסה (checkout)
מאפשר "לחזור בזמן". הפקודה מוחקת את קבצי העבודה הנוכחיים ומשחזרת אותם בדיוק כפי שהיו בקומיט הספציפי שנבחר.

Bash
python wit.py checkout <commit_id>
🛠 דרישות והתקנה
וודאו שמותקן אצלכן פייתון (גרסה 3.7 ומעלה).

התקינו את התלות היחידה של הפרויקט:

Bash
pip install click
וודאו שהקבצים wit.py ו-logic.py נמצאים תמיד באותה התיקייה.

⚙️ הגדרות התעלמות (.witignore)
ניתן ליצור קובץ בשם .witignore בתיקייה הראשית. כל שם של קובץ או תיקייה שייכתב בו (שורה אחת לכל שם) לא ייכנס למערכת בקרת הגרסאות בעת ביצוע פקודת add.

🔍 Example Scenarios
Step 1: Initialize the repository
Bash
python wit.py init
# Output: Initialized empty WIT repository in .wit/
Step 2: Add files to staging
Bash
# Create a file
echo "Hello World" > hello.txt
# Add it
python wit.py add hello.txt
# Output: Added hello.txt to staging area.
Step 3: Check status
Bash
python wit.py status
# Output: 
# --- Status ---
# Files staged for commit:
#   (staged): hello.txt
# Untracked files:
#   (none)
Step 4: Create a commit
Bash
python wit.py commit -m "Initial commit"
# Output: Created commit a1b2c3d4: Initial commit
# Staging area cleared.
Step 5: Checkout (Going back in time)
Bash
python wit.py checkout a1b2c3d4
# Output: Switched to commit a1b2c3d4.

מפותח על ידי סטודנטיות למדעי המחשב (תמר רותן, שירה שמש,אילה סמסון)- שנה ב'😀.
