
def count_words_in_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Split the text into words using whitespace as the delimiter
        words = text.split()

        # Count the number of words
        word_count = len(words)

        return word_count

    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



