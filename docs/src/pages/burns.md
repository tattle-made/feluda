---
title: Burns
---

# Burns

A catalogue of odd issues that have risen while developing and maintaining this software.
This documentation is intended to help other contributors. If you encounter an issue while
developing this software further, try searching here to see if one of us has walked through the same path as you.

1. TypeError : object of type ndarray is not JSON serializable
   If you try to send a numpy array as a server response via Flask, you get this error.
   `return {"representation": text_vec}`
   This can be resolved by converting the numpy array into a list.
   `return {"representation": text_vec.tolist(), "plain_text": plain_text}`
   I used this SO for reference : https://stackoverflow.com/a/51685601/2767642
   I also read in this (link)[https://github.com/numpy/numpy/issues/10494] that this might not always work but I havent faced any issues yet in our use case.

2. environment variables not being loaded.
   If you are running the app in a way where the environment variables arent set. you might want to import dot_env and run `load_dotenv()` at the outset of your program, this will load the environment variables mentioned in development.env into your environment
