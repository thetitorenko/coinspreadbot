# coinspreadbot
Another Telegram bot adding coins to Google`s Spreadsheet

## Release notes:

### v0.2
- Spreadsheet template added to repo - `template.xlsx`;
- Added ability to add new expense not only for today. New syntax for message is `[CATEGORY:PRICE/:day/]`, where `day` is optional. Spreadsheet will be sorted basing on _Date_ column in ascending order;
- Price of expense formatted as currency. Predefine format of currency in template.