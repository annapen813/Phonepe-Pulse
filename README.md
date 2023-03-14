Python-Project-PhonePe-Pulse-Data-Visualization

Steps To Follow
Run the required dependencies given in the requirementALL.txt

Clone your master repository to your local machine. The github repository URL is .

Since the Data is already extracted and stored in my cloud database, you can directly 
start the phonepepulse.py file, using the command "streamlit run phonepepulse.py".

This will initialize the Streamlit form with the cusotm port of http://localhost:8051

If you need to extract and store it on your database. You have to modify the connection settings in the dbConfig.py file.
Once it is done, Run the below DataInsertion.py file, this will call the DataExtraction methods on the below files

AggregatedTransactionData.py
AggregatedUserTransactionData.py
MapHoverTransactionData.py
MapHoverUserTransactionData.py
TopTransactionData.py
TopRegisteredUserData.py

Once the data successfully inserted on your custom database the phonepepulse.py file, using the command "streamlit run phonepepulse.py".

This will initialize the Streamlit form with the cusotm port of http://localhost:8051

It has Menu with Visualization Category list on the Sidebar, Year, State, Quarter fields

   Visualization Category - User option to choose the visualization for Aggregated Data or Map Hover Data
   Year - List of Years
   State - List of States / All India
   Quarter - Qarter of a Year

Once you choose the visualization category, the behid methods will fetch the data from Database and displayed in the Plotly Express Charts





