# 实验二模型约定

## 接口与方向
Endpoint(link_id,timeslot)表示一个用户的输入/输出位置。Tables包含两条输入链路的t_maps、一个s_map和pairs。
对方向src→dst，T[src.link_id][dst.timeslot]=src.timeslot；S[(dst.link_id,dst.timeslot)]=src.link_id。输入帧k完成T和S后，结果在输出帧k+1可用。

## 资源与阻塞
每个端点独占；一对端点占用两端，不能再用于其他连接。connection_id也必须唯一。
每个方向占用一个内部T输出(src.link_id,dst.timeslot)和一个S输出(dst.link_id,dst.timeslot)。这些表项不能被另一连接覆盖，即使映射值相同也不共享。
例如C1连接(0,1)与(1,5)，再请求(0,2)与(0,5)，端点不同但都需要T0的输出TS5，后者返回False。该结果是固定T→S路径的内部阻塞，不是用户忙。
所有检查成功后同时写入两个方向；拒绝时不改动任意表项。非法端口或两端相同抛ValueError；重复ID、占用端点或内部资源冲突返回False。

## 释放
按pairs找到两端，删除其两组T/S表项和连接记录。不存在ID返回False；其他连接保持不变。之后这些资源可被新连接使用。

## 帧与缓存
输入输出必须为uint8数组。T输入[32]、输出[32]；S输入[2,32]、输出[2,32]；不得原地改输入。
未连接业务位置填0xD5。TS0与TS16在各单元按本链路相同时隙透传。保留时隙不可出现在控制映射中。
run_frames为输入帧编号k生成available_frame_id=k+1。这里是离线仿真，无需Python每125微秒唤醒。控制表变更发生在两次exchange_frame调用之间；函数处理期间不并发改表。

## 时分传输与实验一的区别
每链路32×8×8000=2.048 Mbit/s；一个时隙通道64 kbit/s。TS16保留是本课配置，不代表所有E1配置。实验一的128 bit/tick服务模型不能直接当作这条PCM链路的物理速率。
