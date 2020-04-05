# DataEngineer POS Tagger
A collection of small projects from my internship as a data engineer. All sensitive information and specific links have been removed.

The ARIMA, Regression, and Anomaly detection files: Project that connects the ML Studio Service with blob storage. Allows user to either manually upload a file to blob storage OR name a local file which is then uploaded to blob storage and output the results of the ML analysis to blob storage. The ARIMA file grabs a file from the blob, trains the ARIMA model on the number of tickets per month, and then displays the difference between predicted and actual number of tickets.

The TicketDataVisualFile: Various visualizations created to track trends in the number and category of tickets being submitted.

The POS files: This POS tagging project aimed to prevent accidentally sending information to a company that is not a current client. It parses through the email, tags the proper nouns, checks those proper nouns against the list of current clients, and raises an error if the mentioned company is not a client. An earlier iteration (PythonConnectAPI) uses Azure Text Analytics to tag the organizations rather than the nltk package.
