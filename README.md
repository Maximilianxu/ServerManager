# client
npm run serve

# server
python3 app.py

# dependencies

## 后端
1. MongoDB
2. pymongo
后端app.py最后有after_request的同域名规则，如果你不想加详细的规则，可以把这个去掉，不然会报错。

## 前端
1. 安装 nodejs 14.x
2. 安装依赖: 进入client目录, yarn & yarn install
settings.js里把localhost换成服务器ip
