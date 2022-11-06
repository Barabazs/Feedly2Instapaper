# Feedly2Instapaper
Feedly2Instapaper is a simple Python script that connects to your Feedly and Instapaper accounts to add your "Saved for later"-entries as a new bookmark in Instapaper. If the bookmark was created , the corresponding entry in Feedly is removed.

This script is meant to be used with a cron-job to automate the synchronisation.

## Installation

`python3 -m pip install feedly2instapaper`

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

2. Fill in those credentials in `.env-example`
3. Rename `.env-example` to `.env`
4. Create a new cron-job that executes `python3 -m feedly2instapaper`
5. Sit back, relax and share a [coffee](https://ko-fi.com/barabazs) with me.


## Contributing
You can contribute by code (open a PR) or by generous coffee/crypto donations.


## Donations

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/T6T51XKUJ)

|Ethereum|Bitcoin|
|:-:	|:-:	|
|0x6b78d3deea258914C2f4e44054d22094107407e5|bc1qvvh8s3tt97cwy20mfdttpwqw0vgsrrceq8zkmw|
|![eth](https://raw.githubusercontent.com/Barabazs/Barabazs/master/.github/eth.png)|![btc](https://raw.githubusercontent.com/Barabazs/Barabazs/master/.github/btc.png)|

