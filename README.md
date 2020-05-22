# Leads Recommender

### Getting Started

There is two alternative ways to use this service. Let's check:

**Using a executable:** 

1. Download the installer

   ```
   https://bit.ly/leadsrecommenderinstaller
   ```

2. Execute it and choose a directory to extract the files

3. Open Leads Recommender.exe

Done that, a page will open in our default browser and you can use the application. In the first run, the model will be trained, but in others sections this will not be necessary. Now, just upload your portfolio (make sure that it meets the _necessary standards_) and all the results will be at the project directory in a "output" named folder.

**Via command prompt:**

1. Clone this repository

   ```
   git clone https://github.com/w-rfrsh/leads-recommender.git
   ```

2. Download market and sample portfolios data and extract it on the project folder.

   ```
   https://bit.ly/leadsrecommender-data
   ```

3. Install requirements.txt

   ```
   pip install -r requirements.txt
   ```

4. Run via command prompt 

   ```
   $ python main.py --myportfolio "<insert here your portfolio name>.csv"
   ```

   >  Make sure that the portfolio meets the _necessary standards_ and is on the portfolio folder)

In the first run, the model will be trained, but in others sections this will not be necessary. All the results will be in "output" folder.

> **Portfolio necessary standards**: 
>
> The portfolio should at least contain a column called 'ID' with the IDs of the companies that are customers of yours.

----

### About the project

|      Role      | Responsibility | Name                  |
| :------------: | -------------- | --------------------- |
| Data Scientist | Author         | Wesley Alves da Silva |

This project was made as a final project for AceleraDev Data Science course from [Codenation](https://www.codenation.dev/), check below the description of the challenge:

**Objective**

The purpose of this product is to provide an automated service that recommends leads to a user given their current customer list (portfolio).

**Context**

Some companies would like to know who are the other companies in a given market (population) that are most likely to become their next customers. That is, your solution must find in the market who are the most adherent leads given the characteristics of the customers present in the user's portfolio.

In addition, your solution must be user agnostic. Any user with a list of customers who want to explore this market can extract value from the service.

For the challenge, the following bases should be considered:

> Market: Base with information about the companies in the market to be  considered. 

> Portfolio 1: Company customer ids 1

> Portfolio 2: Company customer ids 2

> Portfolio 3: Company customer ids 3

Note: all companies (ids) in the portfolios are contained in the Market (population base).

Link to download the market, portfolio 1, portfolio 2 and portfolio 3 datasets: [bit.ly/leadsrecommender-data](bit.ly/leadsrecommender-data)


### 



