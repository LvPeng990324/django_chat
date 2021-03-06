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
  
  - **GET** `/chat/unread-count/` **获取用户未读消息数量**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      > 无额外参数
    - 响应：
      - > **成功** 返回当前用户的未读消息总数
  
  - **POST** `/chat/chat-login/` **聊天登录**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `device_id` 设备id *字符串* **非空**
    - 响应：
      - > **成功** 返回登录成功状态标志
      - > **失败** 
        - `未找到该设备` 设备id不存在，返回自定义404code
        - `未找到该用户` user_id不存在，返回自定义404code
  
  - **POST** `/chat/chat-logout/` **聊天登出**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `device_id` 设备id *字符串* **非空**
    - 响应：
      - > **成功** 返回登出成功状态标志
      - > **失败** 
        - `该用户无已登录设备` 该用户无已登录设备或user_id有误，返回自定义404code
        - `该用户下无该设备登录记录` 设备id在该用户记录下不存在，返回自定义404code



- ### 聊天会话
  - **POST** `/chat/create-session/` **创建会话**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `name` 会话名 _字符串_ **非空** **可重复**
      - `type` 会话类型 _字符串/整型_ **非空** _单选：`1`单聊、`2`群聊_
      - `chat_user_id_list` 会话参与者的`user_id`列表 _列表_ **非空** _包含自己的用户`user_id`的列表_
    - 响应：
      - > **成功** http只返回成功响应，通过ws给在线会话参与者发送会话创建生命周期和新创建的session信息
      - > **失败**
        - `未取到用户` 返回自定义的404code
        - `type格式有误` 返回自定义的400code
  
  - **GET** `/chat/session-info/` **获取当前用户的会话信息列表**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - 分页信息：
        - `offset` 偏移量 _整型_ **可选** _默认值：`0`_
        - `length` 获取长度 _整型_ **可选** _默认值：`10`_
        - `total` 获取所有标记 _字符串_ **可选** _只要给了**total**字符串就不分页_
    - 响应：
      - > **成功** 返回信息：
        - `num_of_sessions` session总数
        - `session_info_list` session信息列表
  
  - **GET** `/chat/search-session/` **搜索会话信息**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `search_text` 搜索文本 _字符串_ **必填** _用于包含筛选的字段_
      - `total` 获取所有标记 _字符串_ **可选** _只要给了**total**字符串就给所有，不给就各自给前5个_
    - 响应：
      - > **成功** 返回信息：
        - `single_chat_session_info_list` 单聊session信息列表
        - `group_chat_session_info_list` 群聊session信息列表


- ### 聊天记录
  - **GET** `/chat/chat-log-info/` **获取聊天记录**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `session_id` 会话id _字符串_ **非空**
      - 分页信息：
        - `offset` 偏移量 _整型_ **可选** _默认值：`0`_
        - `length` 获取长度 _整型_ **可选** _默认值：`10`_
        - `total` 获取所有标记 _字符串_ **可选** _只要给了**total**字符串就不分页_
    - 响应：
      - > **成功** 返回信息：
        - `num_of_chat_logs` 此会话的聊天记录总数
        - `chat_log_info_list` 聊天记录信息列表

  - **POST** `/chat/single-chat-mark-as-read/` **单聊标记为已读**
    > headers中带`Authorization`，提前去获取`user_sig`
    - 请求参数：
      - `session_id` 会话id _字符串_ **条件可选，下方total有了就可不填**
      - `total` 标记所有已读 _字符串_ **可选** _只要给了**total**字符串就标记该用户所有未读为已读_
    - 响应：
      - > **成功** 返回成功信息以及本次标记已读的信息条数
      - > **失败** 
        - `未取到当前用户` 返回自定义的404code
        - `session不存在或该用户未参与该会话` 返回自定义的404code

  - **POST** `/chat/mass-massage/` **消息群发**
    - 请求参数：
      - `send_user_id` 发消息的用户user_id _字符串_ **非空**
      - `receive_user_id_list` 收消息的用户user_id列表 _列表_ **非空**
      - `to_send_text` 消息文本内容 _字符串_ **非空**
    - 响应：
      - > **成功** 返回发送成功的自定义200code响应

  - **POST** `/chat/system-massage/` **系统消息**
    - 请求参数：
      - `receive_user_id_list` 收消息的用户user_id列表 _列表_ **条件可选，下方send_all_user给了就可不填**
      - `send_all_user` 是否发送所有用户 _字符串_ **可选** _只要给了**total**字符串就给所有用户发消息_
      - `to_send_context` 消息体 _JSON字符串_ **非空** _符合消息体标准，可以实现卡片等多种样式_
    - 响应：
      - > **成功** 返回发送成功的自定义200code响应


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
> **ws** `/ws/chat/` 不需要认证，访问就建立基础连接，连接建立后会返回设备id：`device_id`用于后续登录登出操作

- ### 登录/登出
  > 使用HTTP接口，详见文档上方

- ### 发消息
  > 需要先登录才可以，未登录会返回未登录的`message`提示。
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

