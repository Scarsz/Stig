# Stig
GitHub Gists-inspired, multi-file, anonymous, encrypted pastebin

# Installation
Preferably make a venv & run `pip install -r requirements.txt`. Start with `python app.py`.

# Explanation
*How can the encryption key be transmitted in the URL when the URL is sent to the server? Doesn't that give the server
administrator the ability to just decrypt pastes themselves?*

No. More specifically, no, the encryption key is actually **not** sent to the server, even when it 's in the URL. The
reason behind this is because the key is prefixed by `#`. Browsers **do not** send characters after the hash because
historically this feature of browsers was only to indicate what element on a page needs to be displayed. Thus, there was
no reason for browsers to send that information. Luckily, the hash is still available to JavaScript running on the page.
This is what allows your browser to decrypt the paste data- your browser's JavaScript has access to the key.

# Disclaimer
- I'm a backend developer, not a frontend developer.
  - [Web designing isn't my forte.](https://i.imgur.com/Q3cUg29.gif) If you see areas where the UI can be improved on,
    I'll gladly accept your pull request.
- I'm new to cryptography.
  - If there's a security issue (to the best of my knowledge, there shouldn't be) that would make pastes be readable by
    the server administrator, let me know and maybe give a PR to address it.