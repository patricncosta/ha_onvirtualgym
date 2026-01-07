# 🏋️ OnVirtualGym - Home Assistant Integration

This is a Custom Component for Home Assistant that allows you to monitor your OnVirtualGym account data, such as your monthly gym attendances.

**Disclaimer**: This integration is a community project and is not officially supported by OnVirtualGym.

## ✨ Features

* Monitors the number of gym attendances during the current month.
* Authentication via Username and Password.
* Automatically retrieves the Access Token and Member ID.
* Automatic data updates (defaulting to every hour).
* Easy configuration via User Interface (UI).

## 🚀 Installation

### Installation via HACS (Recommended)

1. Open **HACS** in your Home Assistant.
2. Go to `Integrations` and click the `three vertical dots` in the top right corner.
3. Select `Custom repositories`.
4. Copy this repository's URL (`https://github.com/patricncosta/ha_onvirtualgym`) and paste it into the `Repository` field.
5. Under `Category`, choose `Integration`.
6. Click `ADD`.
7. Search for the `OnVirtualGym` integration in the HACS list and click `INSTALL`.
8. Restart your Home Assistant.

### Manual Installation

1. Navigate to the `custom_components` folder in your Home Assistant configuration.
2. Create a new folder named `onvirtualgym`.
3. Copy all the integration files from this repository into the `onvirtualgym` folder you just created. The final structure should look like this:
    ```
    config/custom_components/onvirtualgym/
    ├── __init__.py
    ├── config_flow.py
    ├── const.py
    ├── coordinator.py
    ├── manifest.json
    ├── sensor.py
    └── translations/
        ├── en.json
        └── pt.json
    ```
4. Restart your Home Assistant.

## ⚙️ Configuration

After installation (via HACS or manual) and restarting Home Assistant:

1. Go to **Settings > Devices & Services**.
2. Click `+ ADD INTEGRATION` in the bottom right corner.
3. Search for `OnVirtualGym`.
4. Enter your OnVirtualGym `Username` and `Password`.
5. Click `SUBMIT`.

The integration will automatically attempt to log in, retrieve your member ID, and create the `sensor.onvirtualgym_monthly_attendances` entity.

## 📊 Created Entities

* `sensor.onvirtualgym_monthly_attendances`: Displays the number of gym visits in the current month. Includes a `history` attribute with a list of grouped workout sessions (Entry and Exit times).

## 🤝 Contributions

Contributions are welcome! If you find a bug, have an idea for a new feature, or want to help improve the code, please open an `Issue` or a `Pull Request` in this repository.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.