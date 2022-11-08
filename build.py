import requests, zipfile, os

def create_manifest():
    path = 'full'

    files = os.listdir(path)

    for f in files:
        print(f)

OUTPUT_DIR = ''
for d in ['firmware', 'ota', 'full']:
    if not os.path.isdir("{}{}".format(OUTPUT_DIR, d)):
        os.mkdir("{}{}".format(OUTPUT_DIR, d))
        
headers = {'Accept': 'application/json', 'Authorization': "token {}".format(os.environ['GITHUB_TOKEN'])}

owner = 'haswitchplate'
repo = 'openhasp'

runs_url = "https://api.github.com/repos/{}/{}/actions/runs".format(owner, repo)

response = requests.get(runs_url, headers=headers)
json_data = response.json()
run = 0

for run in json_data['workflow_runs']:
    if run['conclusion'] == "success":
        break;

run_id = run['id']
artifacts_url = "https://api.github.com/repos/{}/{}/actions/runs/{}/artifacts".format(owner, repo, run_id)

response = requests.get(artifacts_url, headers=headers)
json_data = response.json()

token = {'Authorization': "token {}".format(os.environ['GITHUB_TOKEN'])}

for artifact in json_data['artifacts']:
    artifact_url = "https://api.github.com/repos/{}/{}/actions/artifacts/{}/zip".format(owner, repo, {artifact['id']})
    response = requests.get(artifacts_url, headers=headers)
    link = response.headers
    print(f"{artifact['name']} {artifact['archive_download_url']} {response}")
    for key, value in link.items():
        print(key, ' : ', value)

    zip_filename = f"firmware{os.path.sep}{artifact['name']}.zip"
    with open(zip_filename, 'wb') as f:
        response = requests.get(artifact['archive_download_url'], headers=token)
        f.write(response.content)
        f.close()
        # try:
        with zipfile.ZipFile(zip_filename) as z:
            for file in z.namelist():
                print(f"{file}")
                if file.find("_ota_") > 0:
                    z.extract(file, path="ota")
                if file.find("_full_") > 0:
                    z.extract(file, path="full")
            print("Extracted all ")
        # except:
        #     print("Invalid file")
        os.remove(zip_filename)
