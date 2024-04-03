Terminal commands:
------------------

To start a project:
scrapy startproject your_project_name

Enter the project:
cd your_project_name

Create a spider:
scrapy genspider spider_name example.com

Run the spider:
scrapy crawl spider_name

Run and save data:
scrapy crawl spider_name -o output.json

Run in shell:
scrapy shell
