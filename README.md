# TouchGenshin-MacM

## Description

TouchGenshin-MacM is an assistive tool designed to enhance the gaming experience for Genshin Impact players on macOS. With the M1 chip, macOS users can only download the iOS version of the game, primarily designed for touch-screen interaction. This tool bridges the gap by enabling control using a keyboard and touchpad.

The project also includes an auto-aiming feature, which assists players by automatically moving the cursor to detected in-game entities. This feature is designed to add a new dimension to the gameplay while also respecting the game's balance, ensuring a fair and enjoyable experience for all players.

## Features

- **Keyboard and Touchpad Control:** Play the iOS version of Genshin Impact on macOS with keyboard and touchpad as if you were playing on a traditional gaming platform.

- **Aim-Assistant (Currently Unstable):** Leverages a ML detection model to automatically aim at detected in-game entities, enhancing the user experience. Set True in `functionalities.ini` to enable this feature.

![Aim-Assistant](https://github.com/jiz322/TouchGenshin-MacM/blob/main/accessories/yuanmo_detect.png)

## Getting Started

Follow the instructions below to set up the project on your local machine.

### Prerequisites

- Python 3.9 or above

### Installation

1. Clone the repo:

```bash
git clone https://github.com/jiz322/TouchGenshin-MacM.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

In System Settings, allow the Terminal on Accessibility and Input Monitoring. If aim assistant is on, also allow Screen Recording.

## Configuration

You can adjust the behavior and functionality of this software by modifying the provided configuration files: `position_adjustment.ini`, `functionalities.ini`, and `keyboard_config.ini`. 

### `position_adjustment.ini`

This file is used to adjust the position of the mouse clicks. Modify the values in this file to customize where clicks will occur relative to the current mouse position.

### `functionalities.ini`

You can enable or disable the aim assist feature in this file.

### `keyboard_config.ini`

This file allows you to customize the key bindings. You can modify this file to change the keys used for different actions in the game.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer

This tool is intended to assist players in enjoying Genshin Impact on macOS, not to provide an unfair advantage. Use this tool responsibly and respect the game's balance and other players' experiences.

## License

This project is licensed under the terms of the 3-clause BSD License.

## Contact

Jiageng Zheng - zhengjiageng972@gmail.com

Project Link: https://github.com/jiz322/TouchGenshin-MacM