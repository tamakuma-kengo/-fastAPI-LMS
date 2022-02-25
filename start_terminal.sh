
gnome-terminal --geometry=80x18+2040+580 -- bash -c "sudo docker-compose up -d; sudo docker-compose exec db /bin/sh; bash"

gnome-terminal --geometry=80x18+2040+1070 -- bash -c "sudo docker-compose up -d; sudo docker-compose exec frontend /bin/sh;"

gnome-terminal --geometry=80x18+2040+1560

cd /home/ymtlab/Documents/suzuki/github/fast-api-lms/
sudo docker-compose up


