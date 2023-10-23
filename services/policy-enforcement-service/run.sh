sudo docker build -t home-automation/policy-enforcement-service:0.0.1 .
sudo docker run --name policy-enforcement -p 5001:5000 home-automation/policy-enforcement-service:0.0.1 .