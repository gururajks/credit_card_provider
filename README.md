## README

#### An overview of your design decisions
This is a project that implements a credit card provider. 
This provider allows charging/debitting and crediting the account. 


#### Why you picked the programming language you used
Python is a versatile and a dynamic programming language. Python is fast and can run as 
part of a backend like a web application. This makes it very reusable
and there is a abundant supply of pre-existing third party python packages/libraries.   

#### How to install any required dependencies (runtimes, frameworks, etc)
Python version is 3.7.3
- (optional) Create a virtual environment as it keeps the dependencies isolated. Make sure you have virtualenv installed and run `virtualenv venv`

##### Dependencies: `luhn`
Run: `pip install -r requirements.txt`

#### How to build, package or compile your code if applicable
There is a sample input file: `transaction_input` or you can supply your own
`main.py` is the entry point to the code

#### How to run your code and tests
Running the code can be in two ways either through a file or by stdin

`python main.py transaction_input`
or 
` python main.py < transaction_input`

To run the tests:
`python -m unittest discover test_credit_card_provider/`
