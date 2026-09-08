import time

from flask import render_template, request

from . import admin_bp
from .helpers import _db


@admin_bp.route("/events")
def events():
    q = (request.args.get("q") or "").strip().lower()
    page = max(1, request.args.get("page", 1, type=int))
    per = 100

    conn = _db()
    try:
        where = ""
        params = []
        if q:
            where = " WHERE event_type LIKE ? OR detail LIKE ?"
            like = f"%{q}%"
            params = [like, like]

        total = conn.execute(
            "SELECT COUNT(*) c FROM admin_events" + where, params
        ).fetchone()["c"]
        total_pages = max(1, (total + per - 1) // per)
        page = min(page, total_pages)

        offset = (page - 1) * per
        rows = conn.execute(
            "SELECT id, ts, event_type, detail, guild_id, user_id "
            "FROM admin_events" + where + " ORDER BY id DESC LIMIT ? OFFSET ?",
            params + [per, offset]
        ).fetchall()

        event_types = [
            dict(r) for r in conn.execute(
                "SELECT event_type, COUNT(*) c FROM admin_events "
                "GROUP BY event_type ORDER BY c DESC"
            ).fetchall()
        ]

        uids = {r["user_id"] for r in rows if r["user_id"]}
        names = {}
        if uids:
            marks = ",".join("?" for _ in uids)
            for r in conn.execute(
                f"SELECT DISTINCT user_id, display_name, username "
                f"FROM users WHERE user_id IN ({marks})",
                tuple(uids)
            ):
                names.setdefault(r["user_id"], r["display_name"] or r["username"] or "")
    finally:
        conn.close()

    entries = []
    for r in rows:
        entries.append({
            "id": r["id"],
            "time": time.strftime("%b %d, %Y %H:%M", time.localtime(r["ts"])),
            "type": r["event_type"],
            "detail": r["detail"] or "",
            "guild_id": r["guild_id"],
            "user_id": r["user_id"],
            "user_name": names.get(r["user_id"], ""),
        })

    return render_template(
        "admin_events.html",
        entries=entries,
        event_types=event_types,
        total=total,
        q=q,
        page=page,
        total_pages=total_pages,
    )