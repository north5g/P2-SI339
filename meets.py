import csv
import os

def process_csv(csv_file, output_file):
    # Read the data from the CSV file
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Extract meet details
    meet_name = data[0][0]          # Column A - h1 (Meet Name)
    meet_date = data[1][0]          # Column B - h2 (Meet Date)
    team_results_link = data[2][0]  # Column C - hyperlink for the team-results section

    # Extract team results (assuming 2 teams starting from row 8, index 7)
    team_results = []
    i = 0
    while data[i+7] != []:
        row_index = i + 7 # all results start at 7
        if row_index < len(data):
            place = data[row_index][0]
            team_name = data[row_index][1]
            team_score = data[row_index][2]
            team_results.append((place, team_name, team_score))
        i += 1

    # Extract athletes (starting from row 28, index 27)
    athletes = data[i+7+2:]

    # Generate HTML table rows for team results
    team_table_rows = ""
    for place, team_name, team_score in team_results:
        team_table_rows += f'''<tr>
            <td>{place}</td>
            <td>{team_name}</td>
            <td>{team_score}</td>
        </tr> '''

    # Generate HTML table rows for athletes
    athlete_table_rows = ""
    image_folder = "../client_data_files/images/AthleteImages/"
    racer_not_found = "../client_data_files/public_domain_question_mark.jpg"
    for athlete in athletes:
        if len(athlete) < 8:
            # Skip incomplete rows
            continue
        athlete_place = athlete[0][:-1]      # Column A - athlete place
        athlete_grade = athlete[1]      # Column B - athlete grade
        athlete_name = athlete[2]       # Column C - athlete name
        athlete_link = athlete[3]       # Column D - athlete profile link
        athlete_time = athlete[4]       # Column E - athlete time
        athlete_team = athlete[5]       # Column F - athlete team
        team_link = athlete[6]          # Column G - team link
        athlete_image = athlete[7]      # Column H - athlete profile pic (image filename)

        athlete_image_path = os.path.join(image_folder, athlete_image)
        if os.path.exists(athlete_image_path):
            athlete_table_rows += f'''<tr>
                <td>{athlete_place}</td>
                <td>{athlete_grade}</td>
                <td><a href="{athlete_link}">{athlete_name}</a></td>
                <td><a href="{team_link}">{athlete_team}</a></td>
                <td>{athlete_time}</td>
                <td><img src="{athlete_image_path}" alt="{athlete_name}" width="50"></td>
            </tr> '''
        else:
            athlete_table_rows += f'''<tr>
                <td>{athlete_place}</td>
                <td>{athlete_grade}</td>
                <td><a href="{athlete_link}">{athlete_name}</a></td>
                <td><a href="{team_link}">{athlete_team}</a></td>
                <td>{athlete_time}</td>
                <td><img src="{racer_not_found}" alt="No picture of {athlete_name} available" width="50"></td>
            </tr> '''

    # Construct the complete HTML content
    html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- link rel="stylesheet" href="css/reset.css" -->
        <!-- link rel="stylesheet" href="style.css" -->
        <title>{meet_name} Country Meet</title>
        </head>
        <body>
        <header>
            <h3><a href="../index.html">Return to other matches here.</a></h3>
            <h1>{meet_name}</h1>
            <h2>{meet_date}</h2>
        </header>
        <!-- Section for overall team results -->
        <section id="team-results">
            <h3>Overall Team Results</h3>
            <p><a href="{team_results_link}">Team results are available here.</a></p>
            <table id="team-table">
                <thead>
                    <tr>
                        <th>Place</th>
                        <th>Team</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {team_table_rows}
                </tbody>
            </table>
        </section>
        <!-- Section for athlete table -->
        <section id="athlete-results">
            <h3>Athlete Results</h3>
            <table id="athlete-table">
                <thead>
                    <tr>
                        <th>Place</th>
                        <th>Grade</th>
                        <th>Name</th>
                        <th>Team</th>
                        <th>Time</th>
                        <th>Image</th>
                    </tr>
                </thead>
                <tbody>
                    {athlete_table_rows}
                </tbody>
            </table>
        </section>
        <footer></footer>
        </body>
        </html>
    '''

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML file '{output_file}' has been generated successfully.")
