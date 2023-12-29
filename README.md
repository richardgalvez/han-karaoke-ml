# HearAndNow Karaoke Song Recommendation System - Machine Learning Python Application

## Task Requirements

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

## Deploy Application with Docker Compose

1.	Install Docker for your platform: https://www.docker.com/products/docker-desktop/.

2.	Ensure Docker Compose is installed your on platform: https://docs.docker.com/compose/install/.

3. Download project files and unzip (or clone repository).

4. Open a Command Line (Windows) or Terminal (Mac/Linux) window and change into the directory of the project root folder.

5. Create the Docker image and deploy the container with commands:

        (Windows/Mac): 
        docker compose up --build -d
        
        
        (Amazon Linux): 
        docker-compose up --build -d 

Done!

### (Local Deployment)

Access Full Jupyter Notebook Interface/Home at: http://localhost:8888.

Access Flask Web App UI at: http://localhost:8080.


### (Cloud Server/Web - HTTP, not HTTPS): 
Must have ports 8888 and 8080 open inbound.

Access Flask Web App UI at: http://{server-dns-name OR ip address}:8080.

Access Full Jupyter Notebook Interface/Home at: http://{server-dns-name OR ip address}:8888.

#### Removal and Clean-up

To stop and remove the running container:

    (Windows/Mac): 
    docker compose down


    (Amazon Linux): 
    docker-compose down


To remove the container image (All platforms): 

        docker rmi han-karaoke-ml-c964