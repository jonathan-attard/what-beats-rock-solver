import os


class WinningPathsDir:
    def __init__(self, path="winning_paths"):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        self.path = path
        self.files = list(os.listdir(self.path))

    def __len__(self):
        return len(self.files)

    def __getitem__(self, item):
        if isinstance(item, int):
            file_name = self.get_filename(item)
            file_path = os.path.join(self.path, file_name)
            ws = WinningSequence(file_path)
            return ws

    def __iter__(self):
        for file_name in self.files:
            file_path = os.path.join(self.path, file_name)
            ws = WinningSequence(file_path)
            yield ws

    @staticmethod
    def get_filename(num: int):
        return f"{num}.txt"

    def add_sequence(self):
        file_name = self.get_filename(len(self.files))
        ws = WinningSequence(file_name)
        return ws


class WinningSequence:
    def __init__(self, txt_path='win_path.txt'):
        self.txt_path = txt_path

        self.words_list = []

        if os.path.exists(self.txt_path):
            # Open the file and read each line
            with open(self.txt_path, 'r') as file:
                # Read each line in the file
                for line in file:
                    # Strip any leading/trailing whitespace characters (including newline characters)
                    word = line.strip()
                    # Add the word to the list if it's not an empty string
                    if word:
                        self.words_list.append(word)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.words_list[item]

    def __iter__(self):
        for word in self.words_list:
            yield word

    def __contains__(self, item):
        return item in self.words_list

    def __reversed__(self):
        return reversed(self.words_list)

    def __len__(self):
        return len(self.words_list)

    def add_word(self, text):
        self.words_list.append(text)

        with open(self.txt_path, 'a') as file:
            file.write(text + '\n')


if __name__ == "__main__":
    ss = WinningSequence()
    print(ss.words_list[:10])
