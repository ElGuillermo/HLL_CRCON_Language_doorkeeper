# HLL_CRCON_Language_doorkeeper

## Description
A plugin for HLL CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that filters (kick) players based upon their language.

⚠️ This one has been developed for french communities.  
You'll have to do **a lot** of translation work to adapt it to your language.

## Features

### Ask a question on a "Punish" screen 
![375491311-95eaf65b-bce5-43d7-9c1b-37e9b4cfff86](https://github.com/user-attachments/assets/5ff37c39-f1e7-4330-b697-5adbb4f69d16)

### Players who do not answer right are kicked
![375491433-36dfe32a-9a93-4c8e-b3a6-c83c34ce9700](https://github.com/user-attachments/assets/335cd921-819d-494f-914e-169cae085337)

### Discord reports
![375491567-05718bb2-23d1-4459-9c8b-4f37177a509d](https://github.com/user-attachments/assets/4208f365-2e74-4052-9af7-d2579710c331)

![375491603-500c01ab-4439-42e4-8699-4250615c019a](https://github.com/user-attachments/assets/7b300e13-4bc5-47a4-a7bb-7d4daa932c38)

## Install
- Copy `restart.sh` in CRCON's root (`/root/hll_rcon_tool/`)
- Create a `custom_tools` folder in CRCON's root (`/root/hll_rcon_tool/`)
- Copy these files into the newly created `/root/hll_rcon_tool/custom_tools/` folder :
  - `common_functions.py`
  - `language_doorkeeper.py`
  - `language_doorkeeper_config.py`

- Edit `/root/hll_rcon_tool/config/supervisord.conf` to add this bot section : 
  ```conf
  [program:automod_verif_fr]
  command=python -m custom_tools.language_doorkeeper
  environment=LOGGING_FILENAME=language_doorkeeper_%(ENV_SERVER_NUMBER)s.log
  startretries=100
  startsecs=10
  autostart=true
  autorestart=true
  ```

## Config
- Edit `/root/hll_rcon_tool/custom_tools/language_doorkeeper_config.py` and set the parameters to fit your needs ;
- Restart CRCON :
  ```shell
  cd /root/hll_rcon_tool
  sh ./restart.sh
  ```

## Limitations
⚠️ Any change to these files requires a CRCON rebuild and restart (using the `restart.sh` script) to be taken in account :
- `/root/hll_rcon_tool/custom_tools/common_functions.py`
- `/root/hll_rcon_tool/custom_tools/language_doorkeeper.py`
- `/root/hll_rcon_tool/custom_tools/language_doorkeeper_config.py`

⚠️ This plugin requires a modification of the `/root/hll_rcon_tool/config/supervisord.conf` file, which originates from the official CRCON depot.  
If any CRCON upgrade implies updating this file, the usual upgrade procedure, as given in official CRCON instructions, will **FAIL**.  
To successfully upgrade your CRCON, you'll have to revert the changes back, then reinstall this plugin.  
To revert to the original file :  
```shell
cd /root/hll_rcon_tool
git restore config/supervisord.conf
```
