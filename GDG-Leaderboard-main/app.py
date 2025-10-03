from flask import Flask, render_template
import csv

app = Flask(__name__)


def read_csv():
    participants = []
    with open('participants.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            participants.append({
                'name': row['User Name'],
                'email': row['User Email'],
                'profile_url': row['Google Cloud Skills Boost Profile URL'],
                'profile_status': row['Profile URL Status'],
                'redemption_status': row['Access Code Redemption Status'],
                'skill_badges_completed': row['All Skill Badges & Games Completed'],
                'num_skill_badges': row['# of Skill Badges Completed'],
                'completion': row['All Skill Badges & Games Completed'],
                'num_arcade_games': row['# of Arcade Games Completed'],
            })
    return participants

def ranking_key(participant):
    num_skill_badges = int(participant['num_skill_badges']) if participant['num_skill_badges'].isdigit() else 0
    num_arcade_games = int(participant['num_arcade_games']) if participant['num_arcade_games'].isdigit() else 0
    
    if num_skill_badges>0 and num_arcade_games >=1:
        return (0, -num_skill_badges)
    elif num_skill_badges<=15 and num_arcade_games>0:
        return (1, -num_skill_badges)
    elif num_skill_badges<=15 and num_arcade_games == 0:
        return (2, -num_skill_badges)
    return (3, -num_skill_badges)
    
@app.route('/')
def index():
    total_count = 0
    participants = read_csv()
    for participant in participants:
        num_skill_badges = int(participant['num_skill_badges']) if participant['num_skill_badges'].isdigit() else 0
        num_arcade_games = int(participant['num_arcade_games']) if participant['num_arcade_games'].isdigit() else 0

        if num_skill_badges == 15 and num_arcade_games >=1:
            participant['completion']='Yes'
        else:
            participant['completion']='No'
    total_count += 1
        
    participants.sort(key=ranking_key)
            
    return render_template('index.html', participants=participants)



if __name__ == '__main__':
    app.run(debug=True)
