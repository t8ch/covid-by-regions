# covid-by-regions
Show COVID numbers for specific regions/countries only (as of now, there is Madeira).  
Streamlit and plotly are used for the app. 

# steps for deployment
1. set-up new project in GCP console
2. set role for user (App engine deployer, admin)
3. using the CLI: login, set current project, deploy:
```shell
gcloud auth login

gcloud config set project <project-name>

gcloud app deploy
```

# files
## Dockerfile
https://docs.docker.com/get-started/part2/#build-and-test-your-image

## `requirements.txt`
Used to define python environment. Lists all packages to be installed in docker container via pip.  
`pip freeze > requirements.txt`

## `app.yaml`
Configuration for deployment used by GCP. Here, very minimalistic.

# notes
## resources used
https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app
https://scotch.io/tutorials/google-cloud-platform-i-deploy-a-docker-app-to-google-container-engine-with-kubernetes
https://blog.jcharistech.com/2020/01/14/how-to-deploy-streamlit-apps-to-google-cloud-platformgcp-app-engine/