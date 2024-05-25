# Parar e remover contêineres em execução
docker-compose down

# Remover todos os contêineres parados
docker container prune -f

# Remover todas as imagens não utilizadas
docker image prune -a -f

# Remover todos os volumes não utilizados
docker volume prune -f

# Remover todas as redes não utilizadas
docker network prune -f

# Remover todos os objetos não utilizados
docker system prune -a -f --volumes

# Reconstruir e iniciar os serviços Docker
docker-compose up --build
