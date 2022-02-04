
gnome-terminal --geometry=80x18+2040+580 -- bash -c "cd backend; sudo docker-compose up -d; sudo docker-compose exec db /bin/sh; bash"

gnome-terminal --geometry=80x18+2040+1070 -- bash -c "cd frontend; sudo docker-compose up -d; sudo docker-compose exec demo-app-front /bin/sh;"

gnome-terminal --geometry=80x18+2040+1560

cd /home/ymtlab/Documents/suzuki/github/fast-api-lms/backend
sudo docker-compose up
