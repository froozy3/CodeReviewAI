def parse_text(text, start_word, end_word=None):
    try:
        start_index = text.index(start_word) + len(start_word)

        if end_word:
            end_index = text.index(end_word)
            return text[start_index:end_index].strip()
        else:
            return text[start_index:-1].strip()
    except ValueError as ve:
        return f"Error: {ve}"
    except Exception as e:
        return f"Error: {e}"