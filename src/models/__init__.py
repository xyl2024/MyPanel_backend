# ORM数据模型定义, 即表结构
# 每一个ORM模型对象, 都对应数据库对应表中的某一行(row)记录, 对象中的每个属性(attribute)表示其中的某列(column)

# SQLAlchemy 在底层做了这些事：
# 1. 执行 SQL：SELECT * FROM users WHERE id = 123;
# 2. 数据库返回一行数据（比如 (123, 'Alice', 'alice@example.com')）
# 3. SQLAlchemy 自动将这行数据映射（map）到 User 类的一个实例
# 4. 返回这个实例给你 —— 你就可以用面向对象的方式操作它
