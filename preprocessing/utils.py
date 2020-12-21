def clean_up_raw_body(raw_text):
    return ' '.join([line.strip() for line in raw_text.strip().splitlines() \
     if line.strip()])
