import csv
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)

PROGRAM_COMPLETION_BADGES = 10
PARTICIPANTS_CSV = Path(__file__).with_name('participants.csv')


def read_csv():
    participants = []
    required_columns = {
        'User Name',
        'Google Skills Profile URL',
        'Milestone Completed',
        'GEAR Digital Badges',
        'Skill Badges Completed Count',
    }

    with PARTICIPANTS_CSV.open('r', newline='', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        missing_columns = required_columns.difference(csv_reader.fieldnames or [])
        if missing_columns:
            raise ValueError(
                f"participants.csv is missing required columns: {', '.join(sorted(missing_columns))}"
            )

        for line_number, row in enumerate(csv_reader, start=2):
            try:
                num_skill_badges = int(row['Skill Badges Completed Count'].strip())
            except (AttributeError, ValueError) as error:
                raise ValueError(
                    f"Invalid skill badge count on participants.csv line {line_number}"
                ) from error

            participants.append({
                'name': row['User Name'],
                'profile_url': row['Google Skills Profile URL'],
                'milestone': row['Milestone Completed'],
                'gear_badges': row['GEAR Digital Badges'],
                'num_skill_badges': num_skill_badges,
                'completion': num_skill_badges >= PROGRAM_COMPLETION_BADGES,
            })
    return participants


def ranking_key(participant):
    return (-participant['num_skill_badges'], participant['name'].casefold())


@app.route('/')
def index():
    participants = read_csv()
    participants.sort(key=ranking_key)
    for rank, participant in enumerate(participants, start=1):
        participant['rank'] = rank

    return render_template(
        'index.html',
        participants=participants,
        total_count=len(participants),
        completed_count=sum(participant['completion'] for participant in participants),
        completion_badges=PROGRAM_COMPLETION_BADGES,
    )


if __name__ == '__main__':
    app.run(debug=True)
