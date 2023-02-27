# Data Extraction from Indian Financial Institutions

Scripts to extract balances from combined statements on email or statements generated from institution's website. Following are supported:
1. HDFC
2. Kotak
3. SBI
4. Zerodha

## Instructions
### Download statements
#### For statements on email
1. Install browser extension [Automa](https://www.automa.site/) to automate browser.
2. Within the extension dashboard, import workflow to download attachments from Gmail using the file `Download Attachments from Gmail.automa.json`.
3. The workflow prompts for 2 inputs on starting:
   1. Gmail inbox url: If you have signed-in multiple Gmail accounts in your browser, provide link to inbox of the account containing statements.
   2. Gmail search query: To search for statement emails. For eg. `from:kotak.com "bank account statement"`. Make sure to test this query first on your inbox so that it returns only the emails that have statements as attachments.
4. You may have to accept a prompt in your browser to allow downloading multiple files together.

#### For statements from institution website
For institutions such as Zerodha, statements on email did not have required data so it was needed to download statements from their website. There is an Automa workflow for that inside the Zerodha folder to automate the process. This workflow can be used as a reference to download from any other website too.

### Extracting data from statements
#### Setup environment
1. Install pyenv and pyenv-virtualenv
   1. brew install pyenv pyenv-virtualenv
2. Create a virtual env and install requirements
   1. pyenv virtualenv finance_data
   2. pyenv activate finance_data
   3. pip3 install -r requirements.txt
3. Open the project in VS Code and select Python environment as `finance_data` whenever prompted.
4. Copy downloaded statements into `data/input` folder inside respective folders for institutions.

#### Running scripts
1. Open the Jupyter notebook for the required institution in VS Code and make sure env for the notebook is `finance_data` on top right.
2. Update password in the first cell if the statement is password protected.
3. Execute cells one-by-one
4. This will create a CSV in output folder with each line denoting date and balances on that date
5. Unencrypted statements are also written to the output folder

#### Sample Output
```
Date,Institution,Account Type,Balance INR,Balance USD,Comments
2022-12-31,HDFC,Savings,10265.19,123.61,
2022-12-31,HDFC,FCNR Deposit,16519.00,200.00,
2022-12-31,HDFC,Deposit,4000.00,48.67,
```