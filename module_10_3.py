# Домашнее задание по теме "Блокировки и обработка ошибок"
# освоить блокировки потоков, используя объекты класса Lock и его методы
import threading
import time
import random
from threading import Thread, Lock


class Bank:

    def __init__(self):
        self.balance = 0
        self.lock = Lock()

    def deposit(self):
        count_iter = 0
        while count_iter <= 99:  # Выполняем цикл 100(от о до 99) раз
            bk = random.randint(50, 500)  # Генерируем случайную сумму от 50 до 500 для пополнения
            # блокировка, чтобы предотвратить одновременный доступ к self.balance из других потоков
            self.lock.acquire()
            # try выполняет код, который может привести к исключениям. Блок finally гарантирует,
            # что блокировка будет освобождена  даже если в блоке try возникнет исключение
            try:
                self.balance += bk  # Пополняем баланс на сгенерированную сумму bk
                print(f'Пополнение: {bk}. Баланс: {self.balance}\n')
            finally:
                self.lock.release()
            time.sleep(0.01)  # задержка на 0,01 сек
            count_iter += 1  # увеличиваем счетчик на 1 итерацию

    def take(self):
        count_iter = 0
        while count_iter <= 99:
            bk = random.randint(50, 500)
            print(f'Запрос на {bk}')
            self.lock.acquire()
            try:
                if bk <= self.balance:  # если баланс больше чем сумма снятия то снимаем
                    self.balance -= bk
                    print(f'Снятие: {bk}. Баланс: {self.balance}\n')
                else:
                    print('Запрос отклонён, недостаточно средств')
            finally:
                self.lock.release()
            time.sleep(0.01)
            count_iter += 1


bk = Bank() # создаем объект класса

# Создаем и запускаем потоки для методов объекта класса
th1 = threading.Thread(target=bk.deposit)
th2 = threading.Thread(target=bk.take)

th1.start()  # стартуем
th2.start()

# Ожидаем завершения потоков
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
