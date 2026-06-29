# BitTrans
## translator of bit to man readable


<!--![Diagram Image Link](./puml/architecture.puml)-->

[!image(https://www.plantuml.com/plantuml/png/LO_13OCm34Nldi8Bm00S47I6Bf0IXxXAdSXn9CPlYaIh7lt_yvEzL7DgxPKWalEaU6ExgvEAgswHZJPhIW29Wg5bLDwZeMVj1MS1aEm9rr8G870YF8xnMRDyXzoiD0Fu8ECuN_qKM3nQ9AIZ92VEM31aFQC7MpqNXc7-EIOioc8NWUvVm9QbNxXJpnGM4j-_UWC0)

## TO DO LIST
### 1 json struct -- done
### 2 python app  -- done
### 3 HMI, input and output, use "tkinter" -- done
### 4 add "enum" to convert the value to readable string


### convert the python script to exe
```
python -m PyInstaller -w -F -i icons8-tools-100.ico BitTrans.py

```


### example

```
62 01 23    31 33 35 33 20    31 33 32 39 20    31 33 32 39 01   55 AA   00 04   08   11 06 1A 00   0C   05   00 00 00 00 00 00 00 00 05 00 00 00 00 00 00 E8 03 51 E8 03 00 00 FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF 03 03 03 03 03 03 03 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 00 00 00 00 00 00 00 00 00 FF 0F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```


#### result

```
{
  "mcu_build": "31 33 35 33",
  "mcu_build_0": 1,
  "mcu_build_1": 3,
  "mcu_build_2": 5,
  "mcu_build_3": 3,
  "socR_build": "31 33 32 39",
  "socA_build": "31 33 32 39",
  "socA_build_0": 1,
  "socA_build_1": 3,
  "socA_build_2": 2,
  "socA_build_3": 9,
  "SOC slot": 1,
  "resetReason": "00 04",
  "resetType": "08",
  "resetTimeDay": 17,
  "resetTimeMonth": 6,
  "resetTimeYear": 26,
  "resetTimeHour": 12,
  "resetTimeMinute": 5,
  "wakeupReason": 0,
  "powerStatus": 0,
  "reserved0": 0,
  "restartTask": 0,
  "restartTask_bit0": 0,
  "Odometer": 0,
  "serviceDays": 5,
  "backLightPWM": "00 00 00 00 00 00 e8 03 51 e8 03 00",
  "backLightPWM_powerOffStatus": 0,
  "backLightPWM_funcfaultStatus": 0,
  "backLightPWM_diagMode": 0,
  "backLightPWM_diagLevel": 0,
  "backLightPWM_pwmApp": 0,
  "backLightPWM_pwmDegradeFactor": 1000,
  "backLightPWM_pwmTempIdx": 81,
  "backLightPWM_pwmValue": 1000,
  "backLightPWM_pwmStressTest": 0,
  "resetDateFlag": "00",
  "serviceHoursInThisDay": "ff",
  "resetTypeHistoryPower": "00",
  "resetTypeHistoryPower_bit0": 0,
  "resetTypeHistoryPower_bit1": 0,
  "resetTypeHistoryPower_bit2": 0,
  "resetTypeHistoryPower_bit3": 0,
  "resetTypeHistoryFuncSafe": "00 00",
  "ADCvalue": "00 00",
  "reserved1": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
  "softTT": "00 00 00 00 00 00 00",
  "hardTT": "00 00 00 ff 03 03 03 03 03 03 03 0b 0b 0b",
  "reserved2": "0b 0b 0b 0b 0b 0b 0b 0b 0b 0b 0b 00 00 00 00 00 00 00 00 00"
}


```
