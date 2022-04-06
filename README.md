# Some notes
## About directories
Both the client and server should be run on your server. The client is actually a JavaScript frontend server (using Vue), that is, the actual access is as follows:

Your PC (the real client) -(via HTTP)-> JS/Vue frontend --> Python Flask server. 

And, the JS frontend accesses the Flask server via internal links on the server.

## About some codes and known bugs:
The exceed_user_quota() function in settings.py may better be put in the pool.py to keep the code clean.

The update_left_time() function has bugs due to the concurrent accesses, putting that function in a seperate file and running it independently can fix this bug.

# client
npm run serve

# server
python3 app.py
> I recommend that you execute `su` command to switch to the root account to start the python server, as some operations in util.py will use `lxc` command which requires root previledge.

# dependencies

## 后端
1. MongoDB
2. pymongo

后端app.py最后有after_request的同域名规则，如果你不想加详细的规则，可以把这个去掉，不然会报错。

## 前端
1. 安装 nodejs 14.x
2. 安装依赖: 进入client目录, yarn & yarn install

settings.js里把localhost换成服务器ip

## Ref Manual，一些LXD的tips

### inst内的torch无法访问cuda

```bash
#原因不明，第一次恢复是
sudo lxc profile edit default
#在config下面加入这一行  
nvidia.driver.capabilities: all
# 然后重启inst
```

第二次恢复则是把这一行删掉，重启inst。推测是修改profile之后，会重新读取，自然而然就能恢复访问cuda。和怎么改关系不大。

不过还有可能实例重启一段时间之后才能正常访问cuda。

### 网站崩溃

```bash
# 是否是mongodb崩溃

sudo systemctl status mongod

# 如果没在运行，尝试

sudo systemctl start mongod

# 如果启动失败，尝试，一般可能在机房断电重启之后发生

sudo chown mongodb:mongodb /tmp/mongodb-27017.sock

sudo chown -R mongodb:mongodb /var/lib/mongodb
```

### 容器很卡的时候

#### 考虑是否是空间不足

每一个容器的配置文件都是用的default profile

查看/修改default（不建议）

```bash
sudo lxc profile show/edit default # 默认64G一个instance
```

另外，也能看到所有inst的配置文件里都包含了名为root的device，该device就是root file system，所有inst都是从名为zfs-pool的池子中分配的。

在某容器中执行

```bash
df -lh
```

也能看到该容器对zfs-pool的使用情况

#### 暂时添加空间

```bash
lxc stop cbuild service 

sudo truncate -s +10G /var/snap/lxd/common/lxd/disks/lxd.img # 加10G到存储池

sudo zpool set autoexpand=on zfs-pool

sudo zpool online -e zfs-pool /var/snap/lxd/common/lxd/disks/lxd.img

sudo zpool set autoexpand=off zfs-pool 

sudo snap start lxd
```

#### 一劳永逸的扩容

```bash
sudo lxc storage info zfs-pool # 查看zfs-pool的使用情况，目前的分区是zfs-pool占用了/dev/sda下的1号分区;
lsblk # 查看所有分区
```

基本的做法就是扩大/dev/sda分区，使用工具cfdisk

```bash
sudo cfdisk /dev/sda # 在里面选择new size，之后write(保存)，quit即可
```

设置zfs-pool 自动扩张充满sda1

```bash
sudo zpool set autoexpand=on zfs-pool
sudo zpool online -e zfs-pool /dev/sda1
```

那整个sda都用光了怎么办？(几乎不可能发生)。添加硬盘，参考这里

https://www.theshell.guru/how-to-increase-the-size-of-a-zfs-pool-add-drive-to-zfs-pool/

### network not available

#### 非DNS问题

1. 可以ping host server，比如ping 210.28.135.11
2. dns works，ping baidu.com，会显示ping 百度的ip

可能是防火墙问题：

`sudo iptables -P FORWARD ACCEPT`

#### DNS问题

问题比较复杂，参考。

https://discuss.linuxcontainers.org/t/failed-to-run-dnsmasq-address-already-in-use/1132/2

check 端口53

```bash
sudo netstat -lnp | grep ":53 "
```

我当时应该停掉了dnsmasq，安装了systemd-resolved。具体细节记不清了，systemd-resolved可能依赖dnsmasq-base。

目前我的

`systemctl status dnsmasq`

会显示dnsmasq inactive。

但是

`sudo netstat -lnp | grep ":53 "`

会显示存在一个dnsmasq监听了10.176.xxx.xxx。这个IP是lxd instance的虚拟IP段，可以通过lxd list确认。

我猜测是lxd里包含了一个dnsmasq服务用于转发lxd instances的dns请求，之后这个请求被转发到宿主systemd-resolved服务那里。因为systemd-resolved监听了127.0.0.1:53地址。


