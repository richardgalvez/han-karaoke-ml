## HearAndNow Recommendation Machine Learning Python Application - WGU C964 Computer Science Capstone

### Task Requirements

Design and develop your fully functional data product that addresses your identified business problem or organizational need from part A. Include each of the following attributes, as they are the minimum required elements for the product:

•   one descriptive method and one nondescriptive (predictive or prescriptive) method

•   collected or available datasets

•   decision support functionality

•   ability to support featurizing, parsing, cleaning, and wrangling datasets

•   methods and algorithms supporting data exploration and preparation

•   data visualization functionalities for data exploration and inspection

•   implementation of interactive queries

•   implementation of machine-learning methods and algorithms

•   functionalities to evaluate the accuracy of the data product

•   industry-appropriate security features

•   tools to monitor and maintain the product

•   a user-friendly, functional dashboard that includes three visualization types

### Deploy Application with Docker (Local)
1. Download project files and unzip (or clone repository).
2. Go to root directory of folder.
3. Run in terminal/command window

   (Windows/Mac):
          docker compose up --build -d


    (Amazon Linux):

    docker-compose up --build -d 

Done! Next:

(Local):

Access Full Jupyter Notebook Interface/Home at: http://localhost:8888

Access Flask Web App UI at: http://localhost:8080


(Cloud Server/Web - HTTP, not HTTPS):

Access Full Jupyter Notebook Interface/Home at: http://{server-dns-name}:8888

Access Flask Web App UI at: http://{server-dns-name}:8080


To stop container (Windows/Mac):

docker compose down

(Amazon Linux):

docker-compose down


To remove container (All platforms):
docker rmi han-karaoke-ml-c964
