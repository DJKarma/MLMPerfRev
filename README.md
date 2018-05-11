#Setup

## install java-8 (ubuntu 14)

  - sudo apt-add-repository ppa:webupd8team/java
  - sudo apt-get update
  - sudo apt-get update
  - sudo apt-get install oracle-java8-installer
  - java -version

## Install Python
  - sudo apt-get install python-dev  # for python2.x installs
  - sudo apt-get install python3-dev  # for python3.x installs
  - sudo apt-get  update; sudo apt-get install  python-dev -y


## Install Packages using pip
- sudo apt-get install python-numpy
- sudo apt-get install python-pandas
- sudo apt-get install python-tabula
- sudo apt-get install python-pip
- sudo pip install tabula
- sudo pip install tabula-py
- sudo pip install numpy
- sudo pip install pandas
- sudo apt-get install python-pip --upgrade
- sudo pip install tabula --upgrade
- sudo pip install numpy --upgrade
- sudo pip install pandas --upgrade
- sudo pip install pyPdf2
- sudo pip install numexpr --upgrade
- sudo pip install pdfminer
- sudo pip install lxml
- pip install --upgrade pip
- sudo pip install --upgrade pip
- sudo pip install opencv 
- sudo pip install opencv-python
- pip install pytesseract
- sudo apt-get install tesseract-ocr
- pip install scikit-learn
- sudo pip install tensorflow
- sudo pip install pydash

pip install -r requirements.txt --no-index --find-links file:///tmp/packages
http://tabula.technology/ install Tabula using jar file

### UBL docs:
- http://www.datypic.com/sc/ubl21/ss.html
- http://www.datypic.com/sc/ubl21/e-ns39_Invoice.html
- http://www.datypic.com/sc/ubl21/e-cac_AccountingSupplierParty.html
- http://www.datypic.com/sc/ubl21/e-cac_Party.html
- http://www.datypic.com/sc/ubl21/e-cac_AccountingCustomerParty.html


## Estimation Doc
https://docs.google.com/spreadsheets/d/1W2Ebz0EoRfGOQzo-ot6ExHT9EWQsH9K1TzBXU3EaiPw

## Links
https://github.com/tabulapdf/tabula-java/wiki/Using-the-command-line-tabula-extractor-tool#grab-coordinates-of-the-table-you-want

## Running Tablua through shell
- https://github.com/tabulapdf/tabula-java/wiki/Using-the-command-line-tabula-extractor-tool#grab-coordinates-of-the-table-you-want
- http://tabula.technology/
- java -Dfile.encoding=utf-8 -Xms256M -Xmx1024M -Dwarbler.port=9999 -jar tabula/tabula.jar
- http://localhost:8080

## API parameter required to call python API
- fileName (string) and fileContent
- ID - Guid, fileID - Guid
- OrganizationID, - Guid

## Parameters for calling SBQ API URL parameters: 
ID - Guid, fileID - 
Guid Post Object{ OrganizationID, - Guid file {  Name, - string  Content,
    - byte array  ContentType, - string  Extension - string }}

## Parameters for calling SBQ API URL parameters:
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
sudo apt-get install language-pack-NL
