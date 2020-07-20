# Feedly2Instapaper
Feedly2Instapaper is a simple Python script that:connects to your Feedly and Instapaper accounts to add your "Saved for later"-entries as a new bookmark in Instapaper. If the bookmark was created , the corresponding entry in Feedly is removed.

This script is meant to be used with a cron-job to automate the synchronisation.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install feedly2instapaper.

```bash
pip install feedly2instapaper
```

## Usage
1. Prerequisites:
   * for Feedly _(You can request your developer access token [here](https://feedly.com/v3/auth/dev))_
      * client_id
      * access_token 
   * for Instapaper  _(You can request your OAuth token [here](https://www.instapaper.com/main/request_oauth_consumer_token))_ 
      * username
      * password
      * token
      * token secret

2. Fill in those credentials in `settings.yaml`
3. Perform a manual test by executing feedly2instapaper.py`
4. Create a new cron-job that executes `feedly2instapaper.py`
5. Sit back, relax and share a [coffee](https://ko-fi.com/barabas) with me.


## Contributing
You can contribute by code (open a PR) or by generous coffee donations.

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T51XKUJ)

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)