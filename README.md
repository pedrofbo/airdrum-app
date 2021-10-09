# airdrum-app
Aplicação de airdrum, com o uso do OpenCV

Módulo Detecção das baquetas

## Instalação
### Docker
```bash
docker build -t airdrum .
```

### Manual
(Requer pip >= 20)

```bash
sudo apt-get install libcblas-dev 
sudo apt-get install libhdf5-dev 
sudo apt-get install libhdf5-serial-dev 
sudo apt-get install libatlas-base-dev 
sudo apt-get install libjasper-dev 
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test
pip install .
```

## Como usar o projeto
### Docker
```bash
make docker-start
```
### Manual
```bash
make-start
```
