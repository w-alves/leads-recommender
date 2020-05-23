# Leads Recommender

This project is about the development of a product to provide an automated service that recommends leads to a user, given his current list of customers (portfolio).

## Getting Started

### **Prerequisites**

To use this application you must have [Python](https://www.python.org/downloads/) installed in your OS. Also, you must have installed the external packages listed at ```requirements.txt```, if you are running via our executable they will automatically be installed and checked before the start. 

**Portfolio necessary standards**: the portfolio should at least contain a column called 'ID' with the IDs of the companies that are customers of yours and is located at the 'portfolios' folder.

### **Usage**

There is two alternative ways to use this service. Let's check:

#### **Via executable:** 

1. Download the installer

   ```
   https://bit.ly/leadsrecommenderinstaller
   ```

2. Execute it and choose a directory to extract the files

3. Open Leads Recommender.exe

Done that, a page will open in our default browser and you can use the application. In the first run, the model will be trained, but in others sections this will not be necessary. In the application, just upload your portfolio (make sure that it meets the _necessary standards_) and all the results will be at the project directory in a "output" named folder.

#### **Via command prompt:**

1. Clone this repository

   ```
   git clone https://github.com/w-rfrsh/leads-recommender.git
   ```

2. Download market and sample portfolios data and extract it on the project folder.

   ```
   https://bit.ly/leadsrecommender-data
   ```

3. Copy your portfolio file to the 'portfolios' folder.

4. Open the prompt at the project directory.

5. Install requirements.txt

   ```
   $ pip install -r requirements.txt
   ```

6. Run via command prompt 

   ```
   $ python main.py --myportfolio "<insert here your portfolio name>.csv"
   ```

   >  Make sure that the portfolio meets the _necessary standards_.

In the first run, the model will be trained, but in others sections this will not be necessary. All the results will be in "output" folder.

## About the project

### Author

|      Role      | Name                  |
| :------------: | --------------------- |
| Data Scientist | Wesley Alves da Silva |

### **Context**

This project was made as a final project for AceleraDev Data Science course from [Codenation](https://www.codenation.dev/), check below the description of the challenge:

Some companies would like to know who are the other companies in a given market (population) that are most likely to become their next customers. That is, your solution must find in the market who are the most adherent leads given the characteristics of the customers present in the user's portfolio.

In addition, your solution must be user agnostic. Any user with a list of customers who want to explore this market can extract value from the service.

For the challenge, the following bases should be considered:

> Market: Base with information about the companies in the market to be  considered. 

> Portfolio 1: Company customer ids 1

> Portfolio 2: Company customer ids 2

> Portfolio 3: Company customer ids 3

Note: all companies (ids) in the portfolios are contained in the Market (population base).

Link to download the market, portfolio 1, portfolio 2 and portfolio 3 datasets: [bit.ly/leadsrecommender-data](bit.ly/leadsrecommender-data)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/w-rfrsh/leads-recommender/blob/master/LICENSE) file for details.



