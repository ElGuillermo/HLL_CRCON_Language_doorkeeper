# HLL_CRCON_Language_doorkeeper

A plugin for HLL CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that filters (kick) players based upon their language.

### Ask a question on a "Punish" screen 
![375491311-95eaf65b-bce5-43d7-9c1b-37e9b4cfff86](https://github.com/user-attachments/assets/5ff37c39-f1e7-4330-b697-5adbb4f69d16)

### Players who do not answer right are kicked
![375491433-36dfe32a-9a93-4c8e-b3a6-c83c34ce9700](https://github.com/user-attachments/assets/335cd921-819d-494f-914e-169cae085337)

### Discord reports
![375491567-05718bb2-23d1-4459-9c8b-4f37177a509d](https://github.com/user-attachments/assets/4208f365-2e74-4052-9af7-d2579710c331)

![375491603-500c01ab-4439-42e4-8699-4250615c019a](https://github.com/user-attachments/assets/7b300e13-4bc5-47a4-a7bb-7d4daa932c38)

## Install
- Create a `custom_tools` folder in CRCON's root (`/root/hll_rcon_tool/`) ;
- Copy `automod_verif_fr.py` in `/root/hll_rcon_tool/custom_tools/` ;
- Copy `custom_common.py` in `/root/hll_rcon_tool/custom_tools/` ;
- Copy `restart.sh` in CRCON's root (`/root/hll_rcon_tool/`) ;
- Edit `/root/hll_rcon_tool/config/supervisord.conf` to add this bot section : 
  ```conf
  [program:automod_verif_fr]
  command=python -m custom_tools.automod_verif_fr
  environment=LOGGING_FILENAME=automod_verif_fr_%(ENV_SERVER_NUMBER)s.log
  startretries=100
  startsecs=120
  autostart=true
  autorestart=true
  ```

## Config :
- Edit `/root/hll_rcon_tool/custom_tools/automod_verif_fr.py` and set the parameters to your needs ;
- Edit `/root/hll_rcon_tool/custom_tools/custom_common.py` and set the parameters to your needs ;
- Restart CRCON :
  ```shell
  cd /root/hll_rcon_tool
  sh ./restart.sh
  ```
Any change to the `/root/hll_rcon_tool/custom_tools/automod_verif_fr.py` or `/root/hll_rcon_tool/custom_tools/custom_common.py` file will need a CRCON restart with the above command to be taken in account.
