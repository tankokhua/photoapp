o. Start 'Powershell' in Admin mode
o. How to deploy using 'gcloud'
   %> gcloud app deploy --project photoapp-334704


Notes:
1. In 'app.yaml', remove 'application' and 'version' keywords.
2. Enable Cloud Build api
   https://console.developers.google.com/apis/api/cloudbuild.googleapis.com/overview?project=pyschools-3


o. Powershell (run as adminstrator)
   o. Outside the project directory:
      % > python -m venv env
      % > env/Scipts/activate
   o. Inside project Directory
      - Deploy to server
        %> gcloud app deploy

      - Run locally
        %> pip install -r requirements.txt
        %> python .\main.py


o. Run in runtime: python27
   - In PowerShell (Admin mode)
   - PS> c:\python27\python.exe 'C:\Users\KokHua\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\dev_appserver.py' app.yaml
   - Click on 'default' Link in localhost:8000/instances
   - Will be directed to localhost:8080
