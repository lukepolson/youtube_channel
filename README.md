# Youtube Channel Repository

Contained here is all the code contained in my videos on youtube. I have a docker image that will make things simple (no need to worry about dependencies when running my code)!

https://hub.docker.com/r/lukepolson/psolver_base

To run this Docker image using Docker Desktop (I'm assuming the linux users are already proficient/can follow this and use terminal commands)

1. Pull the repository using `docker pull lukepolson/psolver_base`. You will need to use windows powershell or a MAC terminal
2. Open Docker Desktop, go to images, and click run:


3. Configure with the following settings:
4. Go to windows powershell, use the command `docker ps -a` to see all running containers and look at the ID. Then use `docker logs <ID>` to get the logs for that container. Copy the token for the jupyter login.
5. Open up google chrome, type in the search bar `localhost:8888/lab` and you will be in the correct environment!
