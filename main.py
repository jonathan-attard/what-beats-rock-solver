import os
import random
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from sequence_store import WinningSequence, WinningPathsDir
from word_gen_simple import WordGenerator
from model_training import GPT2Predictor, GPT2PredictorLive

URL = "https://www.whatbeatsrock.com/"


class RPS:
    def __init__(self, winning_sequence: WinningSequence):
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        # service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=options)  # service=service,

        self.word_list = winning_sequence

        self.word_gen = WordGenerator(self.word_list.words_list)

        # self.predictor = GPT2Predictor(
        #     checkpoint_dir='model_training/checkpoints',
        #     checkpoint_filename='best-model-epoch=05-val_loss=0.64.ckpt',  # Replace with actual filename
        #     word_list=self.word_list
        # )

        os.makedirs('model_live/checkpoints', exist_ok=True)
        self.predictor = GPT2PredictorLive(
            # checkpoint_path='./model_training/checkpoints/best-model-epoch=05-val_loss=0.64.ckpt',
            model_save_path='./model_live/checkpoints/live_model.pt',
            # checkpoint_path=None,
            # model_save_path=None,
            log_dir='model_live/live_logs',
            word_list=self.word_list,
            autosave=False
        )

        self.start_words = WinningSequence('start_words.txt')

    def init(self):
        self.driver.get(URL)

    def remove_extra(self):
        while True:
            time.sleep(0.5)

            elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Continue with Recommended Cookies')]")
            if len(elements) == 1:
                element = elements[0]
                element.click()

                break

    def input(self, text):
        elements = self.driver.find_elements(By.XPATH, "//form//input")
        if len(elements) == 1:
            element = elements[0]
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(text + '\n')

    def check_win(self):
        loss = 'does not beat'
        win = 'beats'

        while True:
            time.sleep(0.5)

            elements = self.driver.find_elements(By.XPATH, f"//p[text()='{win}']")
            if len(elements) == 1:
                return True
            elements = self.driver.find_elements(By.XPATH, f"//p[text()='{loss}']")
            if len(elements) == 1:
                return False

    def next(self):
        while True:
            time.sleep(0.5)

            elements = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'next')]")
            if len(elements) == 1:
                element = elements[0]
                element.click()
                break

    def test(self, inputs):
        self.init()
        self.remove_extra()

        for x in inputs:
            self.input(x)
            win = self.check_win()
            if not win:
                break
            self.next()

        time.sleep(10)
        self.close()

    def load_saved_word_list(self):
        for x in self.word_list:
            self.input(x)
            win = self.check_win()

            if not win:
                raise Exception("Should never lose when loading world list!")
                # break

            self.next()

    def load_saved_word_list_start_word(self):
        index, word = self.get_last_start_word()

        for i in range(index, 0, 1):
            word = self.word_list[i]

            self.input(word)
            win = self.check_win()

            if not win:
                raise Exception("Should never lose when loading world list!")
                # break

            self.next()

    def get_last_start_word(self):
        for i, x in enumerate(reversed(self.word_list)):
            if x in self.start_words:
                return -i - 1, x

    def check_start_word(self, text):
        if text in self.start_words:
            return True

        self.init()

        self.input(text)
        win = self.check_win()
        if not win:
            return False
        self.start_words.add_word(text)
        self.next()
        return True

    def start_game(self):
        check_start_words = []

        print("START")

        self.init()

        # self.load_saved_word_list()
        self.load_saved_word_list_start_word()

        while True:
            last_word = self.word_list[-1]

            if random.getrandbits(1):
                word = self.word_gen.get_word()
            else:
                # word = self.predictor.predict_next_word(self.word_list[-1])
                word = self.predictor.predict_next_word_warp(last_word)

            time.sleep(0.5)
            self.input(word)
            win = self.check_win()

            self.predictor.update_model(last_word, word, win)

            if not win:
                break
            self.word_list.add_word(word)
            check_start_words.append(word)
            print(f"{len(self.word_list)}: {word}")
            self.next()

            self.predictor.save_model()

        for x in check_start_words:
            self.check_start_word(x)

        print("LOSS")
        time.sleep(3)

    def start(self):
        self.init()
        self.remove_extra()

        while True:
            self.start_game()
        # self.close()

    def close(self):
        self.driver.quit()

    def winning_run(self):
        self.init()
        self.remove_extra()

        self.load_saved_word_list()


def multiple():
    import threading

    N = 10  # Number of browsers to spawn
    thread_list = list()

    # Start test
    for i in range(N):
        t = threading.Thread(name='Browser {}'.format(i), target=main, args=(i,))
        t.start()
        time.sleep(1)
        print(t.name + ' started!')
        thread_list.append(t)

    # Wait for all threads to complete
    for thread in thread_list:
        thread.join()

    print('Test completed!')


def main(num=0):
    wpd = WinningPathsDir()
    ws = wpd[num]

    rps = RPS(winning_sequence=ws)
    # rps.test(['paper', 'box'])
    rps.start()
    rps.close()


def main_try(num=0, wait=240):
    while True:
        try:
            main()
        except Exception as e:
            print(str(e))
            time.sleep(wait)


def winning_run(num=0):
    wpd = WinningPathsDir()
    ws = wpd[num]

    rps = RPS(winning_sequence=ws)
    # rps.test(['paper', 'box'])
    rps.winning_run()

    time.sleep(60)
    rps.close()


if __name__ == "__main__":
    # multiple()
    # main()
    main_try()
    # winning_run()
