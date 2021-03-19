# MSRTool
## Introduction
MSRTool is a mutant set reduction tool for Java program using genetic algorithm. You can upload a Java program and set the reduction ratio,then we show you a mutant subset. The tool is packaged and deployed through docker containers, saving you the time to install dependencies. So if you want use the tool,you should install docker and docker-compose in your computer.

## How to use

Step 1: Clone the MSRTool repository.

`git clone https://github.com/Provence613/MSRTool.git`

`cd MSRTool`

Step 2: Enter the directory of backend and execute the following command to start MSR Service.

`cd backapp`

`docker-compose up -d`

Step 3: Enter the directory of frontend and execute the following command to start MSRTool.

`cd frontapp`

`docker-compose up -d`

Step 4: Enter the URL http://localhost:8080/ in the browser to enter the login page.