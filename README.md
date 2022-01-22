# N26DataHarv

N26DataHarv is a simple bot that enters in your N26 online banking and harvest all the transaction data.. because the .csv they provides you isn't complete with all the juicy details

## Installation

Create and activate a virtual environment in the cloned directory.
```bash
python3 -m venv venv/
source venv/bin/activate
```
than install the required packages.
```bash
pip install -r requirements.txt
```
For reference on how to use virtual environments check out this [link](https://towardsdatascience.com/virtual-environments-104c62d48c54).

## Usage

```bash
python3 main.py
```
than accept the 2AF request within 30 seconds. It will open a chrome driver browser and start gathering data in a file called N26_Data.csv.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
