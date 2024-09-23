import shutil
import os
import time
import meets

def process_meets():
    meets_list = ""
    meets_dir = 'client_data_files/meets'
    if os.path.exists("meets_pages/"):
       shutil.rmtree("meets_pages/")
    os.makedirs("meets_pages/", exist_ok = True)
    counter = 0
    for filename in os.listdir(meets_dir):
        if filename.endswith('.csv'):
            csv_path = os.path.join(meets_dir, filename)
            print(f"Processing {csv_path}...")
            meet_path = "meets_pages/" + os.path.splitext(filename)[0] + ".html"
            meets_list += f'''
            <td><a href="{meet_path}">{os.path.splitext(filename)[0]}</a></td>
            </tr> '''
            meets.process_csv(csv_path, meet_path)
        counter += 1
        if counter >= 5: break
    
    html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- link rel="stylesheet" href="css/reset.css" -->
        <!-- link rel="stylesheet" href="style.css" -->
        <title>Cross Country Meet Tracker</title>
        </head>
        <body>
        <!-- Section for list of teams -->
        <section id="cross-country-meets">
            <h1>Latest Cross Country Meets</h1>
            <table id="meets-list">
                <thead>
                    <tr>
                        <th>Meet Name</th>
                    </tr>
                </thead>
                <tbody> {meets_list}
                </tbody>
            </table>
        </section>
        </body>
        </html>
    '''

    with open("index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
        print(f"HTML file 'index.html' has been generated successfully.")

if __name__=="__main__":
    process_meets()