# HeadlessPool
轻量级无头浏览器连接池

## 简单教程
```
from Headless impor *

# 初始化对象
headless = Headless('无头浏览器路径')
# 将无头object加入到队列
headless.run()
# 从队列获取一个无头对象
driver = headless.queue.get()
# 获取网站cookie
driver, cookies = headless.get_cookie(driver,url)

```