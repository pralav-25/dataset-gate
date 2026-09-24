"""Deterministic synthetic records for demonstrations; no real customer data."""

import csv
import io
from datetime import UTC, datetime, timedelta

from dataset_gate.errors import GateError

COLUMNS = [
    "ticket_id",
    "created_at",
    "resolved_at",
    "channel",
    "priority",
    "status",
    "first_response_minutes",
    "handling_minutes",
    "wait_minutes",
    "resolution_minutes",
    "satisfaction",
    "agent_id",
]


def sample_csv(rows=300, *, dirty=False):
    if type(rows) is not int or not 12 <= rows <= 50000:
        raise GateError("demo rows must be 12..50000")
    records = []
    for i in range(rows):
        created = datetime(2026, 9, 1, tzinfo=UTC) + timedelta(minutes=i * 7)
        handling, waiting = 20 + i % 40, 5 + (i * 7) % 40
        closed = i % 5 != 0
        records.append(
            [
                f"T-{i + 1:05d}",
                created.isoformat(),
                (created + timedelta(minutes=handling + waiting)).isoformat() if closed else "",
                ["web", "email", "chat"][i % 3],
                ["low", "medium", "high"][i % 3],
                "closed" if closed else "open",
                str(5 + i % 20),
                str(handling),
                str(waiting),
                str(handling + waiting),
                str(1 + i % 5) if closed else "",
                f"A-{i % 12 + 1:02d}",
            ]
        )
    if dirty:
        records[1][0] = records[0][0]
        records[2][3] = "fax"
        records[3][6] = "-1"
        records[4][9] = "999"
        records[6][2] = ""
        records[7][1] = "yesterday"
        records[8][10] = "9"
        records[9][11] = " A-10 "
        records[11][1] = "2027-01-01T00:00:00+00:00"
        records[10][0] = "BAD-001"
        records[5][4] = ""
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(COLUMNS)
    writer.writerows(records)
    return stream.getvalue()
