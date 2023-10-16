sudo docker build -t home-automation/user-service:0.0.1 .
sudo docker run --name user-service -p 5000:5000 home-automation/user-service:0.0.1