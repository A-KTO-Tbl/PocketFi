from requests import post, get
from typing import Literal
from time import sleep
from threading import Thread, Lock
from colorama import Fore
from datetime import datetime, timedelta
from os import system as sys
from platform import system as s_name
from itertools import cycle
from urllib.parse import unquote
from random import randint

from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Accounts
from Core.Tools.HPV_Proxy import HPV_Proxy_Checker
from Core.Tools.HPV_User_Agent import HPV_User_Agent







class HPV_PocketFi:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Получение ежедневной награды`
    
    [2] - `Выполнение задания с подпиской на Telegram`
    
    [3] - `Выполнение задания с подпиской на Twitter`
    
    [4] - `Сбор монет`
    
    [5] - `Ожидание от 5 до 6 часов`
    
    [6] - `Повторение действий через 5-6 часов`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict) -> None:
        self.Name = Name                   # Ник аккаунта
        self.Token = self.URL_Clean(URL)   # Уникальная ссылка-токен для авторизации в mini app
        self.Proxy = Proxy                 # Прокси (при наличии)
        self.UA = HPV_User_Agent()         # Генерация уникального User Agent



    def URL_Clean(self, URL: str) -> str:
        '''Очистка уникальной ссылки от лишних элементов'''

        try:
            return unquote(URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except:
            return ''



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Name: str, Smile: str, Text: str) -> None:
        '''Логирование'''

        with Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()     # Текущее время
            Name = Fore.MAGENTA + Name     # Ник аккаунта
            Smile = COLOR + str(Smile)     # Смайлик
            Text = COLOR + Text            # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Get_Info(self) -> dict:
        '''Получение информации о балансе и скорости майнинга'''

        URL = 'https://bot.pocketfi.org/mining/getUserMining'
        Headers = {'Connection': 'keep-alive', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'telegramRawData': self.Token, 'sec-ch-ua-mobile': '?1', 'User-Agent': self.UA, 'sec-ch-ua-platform': 'Android', 'Accept': '*/*', 'Origin': 'https://pocketfi.app', 'X-Requested-With': 'org.telegram.plus', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://pocketfi.app/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            HPV = get(URL, headers=Headers, proxies=self.Proxy).json()['userMining']

            Speed = HPV['speed'] # Скорость майнинга в час
            Balance = HPV['gotAmount'] # Баланс
            Mined = HPV['miningAmount'] # Намайнено на данный момент

            return {'Status': True, 'Speed': Speed, 'Balance': f'{Balance:,.2f}', 'Mined': f'{Mined:,.2f}'}
        except:
            return {'Status': False}



    def Daily_Reward(self) -> dict:
        '''Получение ежедневной награды'''

        URL = 'https://rubot.pocketfi.org/boost/activateDailyBoost'
        Headers = {'Connection': 'keep-alive', 'Content-Length': '0', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'telegramRawData': self.Token, 'sec-ch-ua-mobile': '?1', 'User-Agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'Accept': '*/*', 'Origin': 'https://pocketfi.app', 'X-Requested-With': 'org.telegram.plus', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://pocketfi.app/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        Reward = {'1': 1, '2': 1, '3': 2, '4': 3, '5': 5, '6': 8, '7': 13, '8': 21, '9': 34, '10': 55}

        try:
            HPV = post(URL, headers=Headers, proxies=self.Proxy).json()['updatedForDay']

            if HPV == None:
                return {'Status': False}
            else:
                return {'Status': True, 'Reward': Reward[str(HPV + 1)]}
        except:
            return {'Status': False}



    def Run_Tasks(self, Task: Literal['telegram', 'twitter']) -> bool:
        '''Выполнение заданий связанные с подписками'''

        URL = 'https://rubot.pocketfi.org/confirmSubscription'
        Headers = {'Connection': 'keep-alive', 'Content-Length': '30', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'Content-Type': 'text/plain;charset=UTF-8', 'telegramRawData': self.Token, 'sec-ch-ua-mobile': '?1', 'User-Agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'Accept': '*/*', 'Origin': 'https://pocketfi.app', 'X-Requested-With': 'org.telegram.plus', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://pocketfi.app/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
        Data = '{"subscriptionType":"' + Task + '"}'

        try:
            if post(URL, headers=Headers, data=Data, proxies=self.Proxy).json()['ok']:
                return True
            else:
                return False
        except:
            return False



    def Claim(self) -> None:
        '''Сбор монет'''

        URL = 'https://bot.pocketfi.org/mining/claimMining'
        Headers = {'Connection': 'keep-alive', 'Content-Length': '0', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'telegramRawData': self.Token, 'sec-ch-ua-mobile': '?1', 'User-Agent': self.Token, 'sec-ch-ua-platform': 'Android', 'Accept': '*/*', 'Origin': 'https://pocketfi.app', 'X-Requested-With': 'org.telegram.plus', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://pocketfi.app/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            Mined = self.Get_Info()["Mined"]
            post(URL, headers=Headers, proxies=self.Proxy).json()['userMining']['speed']
            self.Logging('Success', self.Name, '🟢', f'Монеты собраны! +{Mined}')
        except:
            self.Logging('Error', self.Name, '🔴', 'Монеты не собраны!')



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Get_Info()['Status']:
                    self.Logging('Success', self.Name, '🟢', 'Инициализация успешна!')
                    INFO = self.Get_Info()


                    Balance = INFO['Balance'] # Баланс
                    Speed = INFO['Speed'] # Скорость майнинга в час


                    self.Logging('Success', self.Name, '💰', f'Текущий баланс: {Balance} /// Скорость майнинга: {Speed}')


                    # Получение ежедневной награды
                    Daily_Reward = self.Daily_Reward()
                    if Daily_Reward['Status']:
                        self.Logging('Success', self.Name, '🎁', f'Ежедневная награда получена! +{Daily_Reward["Reward"]}')
                        sleep(randint(33, 103)) # Промежуточное ожидание


                    # Выполнение задания с подпиской на Telegram
                    if self.Run_Tasks('telegram'):
                        self.Logging('Success', self.Name, '⚡️', 'Задание с Telegram выполнено, скорость майнинга увеличена!')
                        sleep(randint(33, 103)) # Промежуточное ожидание

                    # Выполнение задания с подпиской на Twitter
                    if self.Run_Tasks('twitter'):
                        self.Logging('Success', self.Name, '⚡️', 'Задание с Twitter (Х) выполнено, скорость майнинга увеличена!')
                        sleep(randint(33, 103)) # Промежуточное ожидание


                    self.Claim() # Сбор монет


                    INFO = self.Get_Info()
                    Balance = INFO['Balance'] # Баланс
                    Speed = INFO['Speed'] # Скорость майнинга в час
                    self.Logging('Success', self.Name, '💰', f'Текущий баланс: {Balance} /// Скорость майнинга: {Speed}')


                    Waiting = randint(18_000, 21_000) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                    self.Logging('Warning', self.Name, '⏳', f'Следующий старт сбора монет: {Waiting_STR}!')

                    sleep(Waiting) # Ожидание от 5 до 6 часов

                else: # Если аутентификация не успешна
                    self.Logging('Error', self.Name, '🔴', 'Ошибка инициализации!')
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
            except:
                pass







if __name__ == '__main__':
    sys('cls') if s_name() == 'Windows' else sys('clear')

    Console_Lock = Lock()
    Proxy = HPV_Proxy_Checker()

    def Start_Thread(Account, URL, Proxy = None):
        PocketFi = HPV_PocketFi(Account, URL, Proxy)
        PocketFi.Run()

    if Proxy:
        DIVIDER = Fore.BLACK + ' | '
        Time = Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        Text = Fore.GREEN + f'Проверка прокси окончена! Работоспособные: {len(Proxy)}'
        print(Time + DIVIDER + '🌐' + DIVIDER + Text)
        sleep(5)

    for Account, URL in HPV_Get_Accounts().items():
        if Proxy:
            Proxy = cycle(Proxy)
            Thread(target=Start_Thread, args=(Account, URL, next(Proxy),)).start()
        else:
            Thread(target=Start_Thread, args=(Account, URL,)).start()


