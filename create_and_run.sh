docker build -t samqlite ./
docker run -dit --name samqlite samqlite
docker exec -it samqlite bash
# docker kill samqlite
# docker rmi samqlite