
# 一直吃香蕉的猴子模拟程序

class Monkey:
    def __init__(self, name):
        self.name = name
        self.bananas_eaten = 0
    
    def eat_banana(self):
        """猴子吃一根香蕉"""
        self.bananas_eaten += 1
        print(f"{self.name} 吃了第 {self.bananas_eaten} 根香蕉 🍌")
    
    def keep_eating(self, count):
        """猴子一直吃香蕉"""
        print(f"{self.name} 开始吃香蕉了！")
        for _ in range(count):
            self.eat_banana()
        print(f"{self.name} 总共吃了 {self.bananas_eaten} 根香蕉！")


# 使用示例
if __name__ == "__main__":
    monkey = Monkey("小猴")
    monkey.keep_eating(10)
