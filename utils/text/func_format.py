def rstrip_and_add_dots(s, max_len):
    return s if len(s) <= max_len else s[:max_len-3] + "..."