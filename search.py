from datetime import datetime


def search_notes(query, username, db):
    cursor = db.cursor()
    pattern = query + "%"
    cursor.execute(
        "SELECT title, content, time, code FROM notes WHERE username = ? AND content LIKE ?",
        (username, pattern),
    )
    fdata = cursor.fetchall()

    return [
        (
            title,
            content,
            datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%b %d, %Y at %I:%M %p"
            ),
            code,
        )
        for title, content, time, code in fdata
    ]
