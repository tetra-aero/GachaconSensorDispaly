# 開発メモ（北神）

起動時にやる事（その内スクリプト）

sudo mount -t tmpfs -o size=128m tmpf /mnt/ramdisk
ip link show type can
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
sudo ip link set can1 type can bitrate 1000000
sudo ip link set can1 up


# DroneCAN開発メモ

sudo pip install dronecan  --break-system-packages

https://dronecan.github.io/GUI_Tool/Overview/

 pip install pyuavcan --break-system-packages