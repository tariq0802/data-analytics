# UPPER PRIMARY RECRUITMENT BY WBCSSC ANALYSIS

## 1. PROBLEM STATEMENT

### HISTORY
In 20016 West Bengal Central School Service Commission advertised for recruitment of 14339 Upper Primary level teacher. There was allegation of various malpractice by the Commission, therefore a bunch of cases was filled before High Court of Calcutta. The court orderd to set aside the recruitment process and restart from beginning. In 2023 new panel and waiting list was published. The rule is, if a candidate give interview before commission, the candidate should be in the panel or waiting list. But again same allegation raises against the Commission as several hundred candidates didnt secure their place in panel or waiting list after interview and some candidate moved before the Court.

### STATEMENT
There are 4 types of allegation against the Commission that is cause for rejection of several hundred candidates:
* 1. TET score was changed
* 2. Academic score was changed
* 3. Untrained candidates are present in the panel
* 4. Less meritorius candidates empanelled

Our task is to find out the mismatch and investigate about allegation against WBCSSC in this pannel.

## 2. FORMALIZATION OF THE PROBLEM
We have to find out the answers of these questions:
* 1. How many candidates gave interview?
* 2. How many candidates are present in panel and waiting list?
* 3. How many unique candidates are present in panel and waiting list?
* 4. How many total vacancies are there?
* 5. How many vacancies left unfilled?
* 6. How many candidates TET score was changed?
* 7. How many candidates Academic score was changed?
* 8. Is there any untrained candidate present in the panel or waiting list?
* 9. Is there any miscalculation of some of scores?
* 10. Is there any extreme TET, academic or interview score that is unrealistic?

## 3. DATA COLLECTION AND PROCESSING
For analyzing the panel an waiting list, we collected and processed these data published on the Commissions website:
* Panel data
* Waiting list data
* Interview list data
* Application form data of interviewed candidates
* Total vacancy

## 4. DATA ANALYSIS
After collect, clean and process the datas, we analyze it with mostly pandas librery. All the processes are in 'WBCSSC panel analysis.ipynb" file.

## FINDINGS
* Total interviewed candidate: 16985
* Total empanelled candidate: 8809
* Total waiting candidate: 4525
* Total merit listed candidate: 13334
* Total rejected candidate after interview: 3651
* Total candidate in empanelled or waiting without giving interview: 0
* Total empanelled with academic mismatch: 643
* Total waiting with academic mismatch: 284
* Total TET Score mismatch in panel (difference more than 0.02): 26
* Total TET Score mismatch in waiting list (difference more than 0.02): 8
* Total untrained empanelled: 12
* Total untrained waiting: 4

## 6. RECOMMENDATION
There are clearly some irregualirities practised by the Commission or by the candidates.
* Huge amount of candidates ewere rejected from interview. Cause is not clear as we dont have enough data. But it should'nt be like this
* A great number of candidate have academic mismatch with their filled up form data and panel/waiting data
* There are some mismatch in TET score also
* There are untrained candidates in panel/waiting list

These are very serious irregularities made by the Commission. There is very good opportunity to file case against the Commission to seek their answer.