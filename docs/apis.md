# ？？？聊天系统 **`V0.0.1`**

## HTTP接口

- ### 用户
  - **POST** `/chat/create-chat-user/` **创建用户**
    - 请求参数：
      - `user_id` 用户唯一标识符 _字符串_ **非空** **唯一**
      - `name` 姓名 _字符串_ **可选**
      - `nickname` 昵称 _字符串_ **可选**
      - `username` 用户名 _字符串_ **可选**
      - `gender` 性别 _字符串_ **可选**
      - `birthday` 出生日期 _字符串_ **可选** _格式：`YYYY-MM-dd`_
      - `id_card_num` 身份证号 _字符串_ **可选**
      - `phone` 手机号 _字符串_ **可选**
      - `email` 电子邮箱 _字符串_ **可选**
      - `province` 省 _字符串_ **可选**
      - `city` 市 _字符串_ **可选**
      - `avatar` 头像 _字符串_ **可选**
      - `description` 描述 _字符串_ **可选**
    - 响应：
      > 返回创建的用户信息

  - **GET** `/chat/chat-user-info/` **用户信息**
    - 请求参数：
      - `user_id` 用户唯一标识符 *字符串* **非空**
    - 响应：
      - > **成功** 返回相应的用户信息
      - > **失败** 
        - `未找到用户` 返回自定义的404code

  - **POST** `/chat/get-user-sig/` **获取user_sig**
    - 请求参数：
      - `user_id` 用户唯一标识符 *字符串* **非空**
      - `token` 规则密钥 *字符串* **非空**
    - 响应：
      - > **成功** 返回有效期为5mins的user_sig
      - > **失败** 
        - `验证失败` 返回自定义的403code
  
  - **POST** `/chat/change-chat-user-info/` **更改用户信息**
    - 请求参数：
      > 跟创建用户一样，`user_id`不可以更改。按需更改，所有的可用参数都是可选的，只会更改携带的参数信息
    - 响应：
      - > **成功** 返回更改后的该用户信息
      - > **失败**
        - `未找到用户` 返回自定义的404code


- ### 聊天会话
  - **POST** `/chat/create-session/` **创建会话**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `name` 会话名 _字符串_ **非空** **可重复**
      - `type` 会话类型 _字符串/整型_ **非空** _单选：`1`单聊、`2`群聊_
      - `chat_user_id_list` 会话参与者的`user_id`列表 _列表_ **非空** _包含自己的用户`user_id`的列表_
    - 响应：
      - > **成功** 新创建的`session信息`
      - > **失败**
        - `未取到用户` 返回自定义的404code
        - `type格式有误` 返回自定义的400code
  
  - **GET** `/chat/session-info/` **获取当前用户的会话信息列表**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - 分页信息：
        - `page_size` 每页数量 _整型_ **可选** _默认值：`10`_
        - `page_num` 页码 _整型_ **可选** _默认值：`1`_
        - `total` 获取所有标记 _不限类型_ **可选** _只要给了东西就不分页_
    - 响应：
      - > **成功** 返回信息：
        - `num_of_sessions` session总数
        - `session_info_list` session信息列表
        - `num_of_pages` 总页数

- ### 聊天记录
  - **GET** `/chat/chat-log-info/` **获取聊天记录**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `session_id` 会话id _字符串_ **非空**
      - 分页信息：
        - `page_size` 每页数量 _整型_ **可选** _默认值：`10`_
        - `page_num` 页码 _整型_ **可选** _默认值：`1`_
        - `total` 获取所有标记 _不限类型_ **可选** _只要给了东西就不分页_
    - 响应：
      - > **成功** 返回信息：
        - `num_of_chat_logs` 此会话的聊天记录总数
        - `chat_log_info_list` 聊天记录信息列表
        - `num_of_pages` 总页数
  - **POST** `/chat/single-chat-mark-as-read/` **单聊标记为已读**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `session_id` 会话id _字符串_ **非空**
    - 响应：
      - > **成功** 返回成功信息以及本次标记已读的信息条数
      - > **失败** 
        - `未取到当前用户` 返回自定义的404code
        - `session不存在或该用户未参与该会话` 返回自定义的404code

- ### 聊天文件
  - **POST** `/file/upload-chat-file/` **上传聊天文件**
  > headers中带 `Authorization`，提前去获取 `user_sig`
  - 请求参数：
    - `file` 上传的文件 _文件_ **非空**
  - 响应：
    - > **成功** 返回文件信息
    - > **失败** 
      - `文件大小超限` 返回自定义的400code，并提示文件大小超限 _限制20M以内_

## WebSocket接口 - 聊天
> **ws** `/ws/chat/[user_id]/[user_sig]/` 方括号中是变量

- ### 认证
  - 响应：
    - > **成功** 返回`SDK_READY`常量
    - > **失败** 
      - `认证失败` 直接关闭连接

- ### 发消息
  > 支持同一用户多端在线同时收发消息，发送消息成功后所有设备将收到同样的成功回应
  - 请求：
    > json格式，需要有:
    - `to_session` 接收消息的会话的session_id *字符串/整型* **非空**
    - `content` 消息内容 *字符串* **可选**
  - 响应：
    - > **成功** 返回`MESSAGE_SEND_SUCCESS`常量，附带`消息内容(content)`、`session信息(session)`和`发送者user_id(sender)`

- ### 收消息
  - 响应：
    - > **成功** 返回`MESSAGE_RECEIVED`常量，附带`消息内容(content)`、`session信息(session)`和`发送者user_id(sender)`

- ### 断开连接
  - 响应：
    - > **成功** 返回`KICKED_OUT`常量

